import criscostack
from criscostack.boot import get_unseen_notes, get_user_pages_or_reports
from criscostack.desk.doctype.note.note import mark_as_seen
from criscostack.tests.utils import CriscoTestCase


class TestBootData(CriscoTestCase):
	def test_get_unseen_notes(self):
		criscostack.db.delete("Note")
		criscostack.db.delete("Note Seen By")
		note = criscostack.get_doc(
			{
				"doctype": "Note",
				"title": "Test Note",
				"notify_on_login": 1,
				"content": "Test Note 1",
				"public": 1,
			}
		)
		note.insert()

		criscostack.set_user("test@example.com")
		unseen_notes = [d.title for d in get_unseen_notes()]
		self.assertListEqual(unseen_notes, ["Test Note"])

		mark_as_seen(note.name)
		unseen_notes = [d.title for d in get_unseen_notes()]
		self.assertListEqual(unseen_notes, [])

	def test_get_user_pages_or_reports_with_permission_query(self):
		# Create a ToDo custom report with admin user
		criscostack.set_user("Administrator")
		criscostack.get_doc(
			{
				"doctype": "Report",
				"ref_doctype": "ToDo",
				"report_name": "Test Admin Report",
				"report_type": "Report Builder",
				"is_standard": "No",
			}
		).insert()

		# Add permission query such that each user can only see their own custom reports
		criscostack.get_doc(
			dict(
				doctype="Server Script",
				name="test_report_permission_query",
				script_type="Permission Query",
				reference_doctype="Report",
				script="""conditions = f"(`tabReport`.is_standard = 'Yes' or `tabReport`.owner = '{criscostack.session.user}')"
				""",
			)
		).insert()

		# Create a ToDo custom report with test user
		criscostack.set_user("test@example.com")
		criscostack.get_doc(
			{
				"doctype": "Report",
				"ref_doctype": "ToDo",
				"report_name": "Test User Report",
				"report_type": "Report Builder",
				"is_standard": "No",
			}
		).insert(ignore_permissions=True)

		get_user_pages_or_reports("Report")
		allowed_reports = criscostack.cache.get_value("has_role:Report", user=criscostack.session.user)

		# Test user must not see admin user's report
		self.assertNotIn("Test Admin Report", allowed_reports)
		self.assertIn("Test User Report", allowed_reports)
