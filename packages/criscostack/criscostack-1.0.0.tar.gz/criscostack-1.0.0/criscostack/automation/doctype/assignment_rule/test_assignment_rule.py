# Copyright (c) 2021, Crisco Technologies and Contributors
# License: MIT. See LICENSE

import criscostack
from criscostack.test_runner import make_test_records
from criscostack.tests.utils import CriscoTestCase

TEST_DOCTYPE = "Assignment Test"


class TestAutoAssign(CriscoTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		criscostack.db.delete("Assignment Rule")
		create_test_doctype(TEST_DOCTYPE)

	@classmethod
	def tearDownClass(cls):
		criscostack.db.rollback()

	def setUp(self):
		criscostack.set_user("Administrator")
		make_test_records("User")
		days = [
			dict(day="Sunday"),
			dict(day="Monday"),
			dict(day="Tuesday"),
			dict(day="Wednesday"),
			dict(day="Thursday"),
			dict(day="Friday"),
			dict(day="Saturday"),
		]
		self.days = days
		self.assignment_rule = get_assignment_rule([days, days])
		clear_assignments()

	def test_round_robin(self):
		# check if auto assigned to first user
		record = _make_test_record(public=1)
		self.assertEqual(
			criscostack.db.get_value(
				"ToDo",
				dict(reference_type=TEST_DOCTYPE, reference_name=record.name, status="Open"),
				"allocated_to",
			),
			"test@example.com",
		)

		# check if auto assigned to second user
		record = _make_test_record(public=1)
		self.assertEqual(
			criscostack.db.get_value(
				"ToDo",
				dict(reference_type=TEST_DOCTYPE, reference_name=record.name, status="Open"),
				"allocated_to",
			),
			"test1@example.com",
		)

		clear_assignments()

		# check if auto assigned to third user, even if
		# previous assignments where closed
		record = _make_test_record(public=1)
		self.assertEqual(
			criscostack.db.get_value(
				"ToDo",
				dict(reference_type=TEST_DOCTYPE, reference_name=record.name, status="Open"),
				"allocated_to",
			),
			"test2@example.com",
		)

		# check loop back to first user
		record = _make_test_record(public=1)
		self.assertEqual(
			criscostack.db.get_value(
				"ToDo",
				dict(reference_type=TEST_DOCTYPE, reference_name=record.name, status="Open"),
				"allocated_to",
			),
			"test@example.com",
		)

	def test_load_balancing(self):
		self.assignment_rule.rule = "Load Balancing"
		self.assignment_rule.save()

		for _ in range(30):
			_make_test_record(public=1)

		# check if each user has 10 assignments (?)
		for user in ("test@example.com", "test1@example.com", "test2@example.com"):
			self.assertEqual(
				len(criscostack.get_all("ToDo", dict(allocated_to=user, reference_type=TEST_DOCTYPE))), 10
			)

		# clear 5 assignments for first user
		# can't do a limit in "delete" since postgres does not support it
		for d in criscostack.get_all(
			"ToDo", dict(reference_type=TEST_DOCTYPE, allocated_to="test@example.com"), limit=5
		):
			criscostack.db.delete("ToDo", {"name": d.name})

		# add 5 more assignments
		for i in range(5):
			_make_test_record(public=1)

		# check if each user still has 10 assignments
		for user in ("test@example.com", "test1@example.com", "test2@example.com"):
			self.assertEqual(
				len(criscostack.get_all("ToDo", dict(allocated_to=user, reference_type=TEST_DOCTYPE))), 10
			)

	def test_based_on_field(self):
		self.assignment_rule.rule = "Based on Field"
		self.assignment_rule.field = "owner"
		self.assignment_rule.save()

		for test_user in ("test1@example.com", "test2@example.com"):
			criscostack.set_user(test_user)
			note = _make_test_record(public=1)
			# check if auto assigned to doc owner, test1@example.com
			self.assertEqual(
				criscostack.db.get_value(
					"ToDo", dict(reference_type=TEST_DOCTYPE, reference_name=note.name, status="Open"), "owner"
				),
				test_user,
			)

	def test_assign_condition(self):
		# check condition
		note = _make_test_record(public=0)

		self.assertEqual(
			criscostack.db.get_value(
				"ToDo",
				dict(reference_type=TEST_DOCTYPE, reference_name=note.name, status="Open"),
				"allocated_to",
			),
			None,
		)

	def test_clear_assignment(self):
		note = _make_test_record(public=1)

		# check if auto assigned to first user
		todo = criscostack.get_list(
			"ToDo", dict(reference_type=TEST_DOCTYPE, reference_name=note.name, status="Open"), limit=1
		)[0]

		todo = criscostack.get_doc("ToDo", todo["name"])
		self.assertEqual(todo.allocated_to, "test@example.com")

		# test auto unassign
		note.public = 0
		note.save()

		todo.load_from_db()

		# check if todo is cancelled
		self.assertEqual(todo.status, "Cancelled")

	def test_close_assignment(self):
		note = _make_test_record(public=1, content="valid")

		# check if auto assigned
		todo = criscostack.get_list(
			"ToDo", dict(reference_type=TEST_DOCTYPE, reference_name=note.name, status="Open"), limit=1
		)[0]

		todo = criscostack.get_doc("ToDo", todo["name"])
		self.assertEqual(todo.allocated_to, "test@example.com")

		note.content = "Closed"
		note.save()

		todo.load_from_db()

		# check if todo is closed
		self.assertEqual(todo.status, "Closed")
		# check if closed todo retained assignment
		self.assertEqual(todo.allocated_to, "test@example.com")

	def check_multiple_rules(self):
		note = _make_test_record(public=1, notify_on_login=1)

		# check if auto assigned to test3 (2nd rule is applied, as it has higher priority)
		self.assertEqual(
			criscostack.db.get_value(
				"ToDo",
				dict(reference_type=TEST_DOCTYPE, reference_name=note.name, status="Open"),
				"allocated_to",
			),
			"test@example.com",
		)

	def check_assignment_rule_scheduling(self):
		criscostack.db.delete("Assignment Rule")

		days_1 = [dict(day="Sunday"), dict(day="Monday"), dict(day="Tuesday")]

		days_2 = [dict(day="Wednesday"), dict(day="Thursday"), dict(day="Friday"), dict(day="Saturday")]

		get_assignment_rule([days_1, days_2], ["public == 1", "public == 1"])

		criscostack.flags.assignment_day = "Monday"
		note = _make_test_record(public=1)

		self.assertIn(
			criscostack.db.get_value(
				"ToDo",
				dict(reference_type=TEST_DOCTYPE, reference_name=note.name, status="Open"),
				"allocated_to",
			),
			["test@example.com", "test1@example.com", "test2@example.com"],
		)

		criscostack.flags.assignment_day = "Friday"
		note = _make_test_record(public=1)

		self.assertIn(
			criscostack.db.get_value(
				"ToDo",
				dict(reference_type=TEST_DOCTYPE, reference_name=note.name, status="Open"),
				"allocated_to",
			),
			["test3@example.com"],
		)

	def test_assignment_rule_condition(self):
		criscostack.db.delete("Assignment Rule")

		assignment_rule = criscostack.get_doc(
			dict(
				name="Assignment with Due Date",
				doctype="Assignment Rule",
				document_type=TEST_DOCTYPE,
				assign_condition="public == 0",
				due_date_based_on="expiry_date",
				assignment_days=self.days,
				users=[
					dict(user="test@example.com"),
				],
			)
		).insert()

		expiry_date = criscostack.utils.add_days(criscostack.utils.nowdate(), 2)
		note1 = _make_test_record(expiry_date=expiry_date)
		note2 = _make_test_record(expiry_date=expiry_date)

		note1_todo = criscostack.get_all(
			"ToDo", filters=dict(reference_type=TEST_DOCTYPE, reference_name=note1.name, status="Open")
		)[0]

		note1_todo_doc = criscostack.get_doc("ToDo", note1_todo.name)
		self.assertEqual(criscostack.utils.get_date_str(note1_todo_doc.date), expiry_date)

		# due date should be updated if the reference doc's date is updated.
		note1.expiry_date = criscostack.utils.add_days(expiry_date, 2)
		note1.save()
		note1_todo_doc.reload()
		self.assertEqual(criscostack.utils.get_date_str(note1_todo_doc.date), note1.expiry_date)

		# saving one note's expiry should not update other note todo's due date
		note2_todo = criscostack.get_all(
			"ToDo",
			filters=dict(reference_type=TEST_DOCTYPE, reference_name=note2.name, status="Open"),
			fields=["name", "date"],
		)[0]
		self.assertNotEqual(criscostack.utils.get_date_str(note2_todo.date), note1.expiry_date)
		self.assertEqual(criscostack.utils.get_date_str(note2_todo.date), expiry_date)
		assignment_rule.delete()
		criscostack.db.commit()  # undo changes commited by DDL


def clear_assignments():
	criscostack.db.delete("ToDo", {"reference_type": TEST_DOCTYPE})


def get_assignment_rule(days, assign=None):
	criscostack.delete_doc_if_exists("Assignment Rule", f"For {TEST_DOCTYPE} 1")

	if not assign:
		assign = ["public == 1", "notify_on_login == 1"]

	assignment_rule = criscostack.get_doc(
		dict(
			name=f"For {TEST_DOCTYPE} 1",
			doctype="Assignment Rule",
			priority=0,
			document_type=TEST_DOCTYPE,
			assign_condition=assign[0],
			unassign_condition="public == 0 or notify_on_login == 1",
			close_condition='"Closed" in content',
			rule="Round Robin",
			assignment_days=days[0],
			users=[
				dict(user="test@example.com"),
				dict(user="test1@example.com"),
				dict(user="test2@example.com"),
			],
		)
	).insert()

	criscostack.delete_doc_if_exists("Assignment Rule", f"For {TEST_DOCTYPE} 2")

	# 2nd rule
	criscostack.get_doc(
		dict(
			name=f"For {TEST_DOCTYPE} 2",
			doctype="Assignment Rule",
			priority=1,
			document_type=TEST_DOCTYPE,
			assign_condition=assign[1],
			unassign_condition="notify_on_login == 0",
			rule="Round Robin",
			assignment_days=days[1],
			users=[dict(user="test3@example.com")],
		)
	).insert()

	return assignment_rule


def _make_test_record(**kwargs):
	doc = criscostack.new_doc(TEST_DOCTYPE)

	if kwargs:
		doc.update(kwargs)

	return doc.insert()


def create_test_doctype(doctype: str):
	"""Create custom doctype."""
	criscostack.db.delete("DocType", doctype)

	criscostack.get_doc(
		{
			"doctype": "DocType",
			"name": doctype,
			"module": "Custom",
			"custom": 1,
			"fields": [
				{
					"fieldname": "expiry_date",
					"label": "Expiry Date",
					"fieldtype": "Date",
				},
				{
					"fieldname": "notify_on_login",
					"label": "Notify on Login",
					"fieldtype": "Check",
				},
				{
					"fieldname": "public",
					"label": "Public",
					"fieldtype": "Check",
				},
				{
					"fieldname": "content",
					"label": "Content",
					"fieldtype": "Text",
				},
			],
			"permissions": [
				{
					"create": 1,
					"delete": 1,
					"email": 1,
					"export": 1,
					"print": 1,
					"read": 1,
					"report": 1,
					"role": "All",
					"share": 1,
					"write": 1,
				},
			],
		}
	).insert()
