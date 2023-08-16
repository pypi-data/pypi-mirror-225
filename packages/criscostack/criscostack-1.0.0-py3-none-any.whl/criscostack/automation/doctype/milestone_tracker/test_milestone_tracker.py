# Copyright (c) 2019, Crisco Technologies and Contributors
# License: MIT. See LICENSE
import criscostack
import criscostack.cache_manager
from criscostack.tests.utils import CriscoTestCase


class TestMilestoneTracker(CriscoTestCase):
	def test_milestone(self):
		criscostack.db.delete("Milestone Tracker")

		criscostack.cache.delete_key("milestone_tracker_map")

		milestone_tracker = criscostack.get_doc(
			dict(doctype="Milestone Tracker", document_type="ToDo", track_field="status")
		).insert()

		todo = criscostack.get_doc(dict(doctype="ToDo", description="test milestone", status="Open")).insert()

		milestones = criscostack.get_all(
			"Milestone",
			fields=["track_field", "value", "milestone_tracker"],
			filters=dict(reference_type=todo.doctype, reference_name=todo.name),
		)

		self.assertEqual(len(milestones), 1)
		self.assertEqual(milestones[0].track_field, "status")
		self.assertEqual(milestones[0].value, "Open")

		todo.status = "Closed"
		todo.save()

		milestones = criscostack.get_all(
			"Milestone",
			fields=["track_field", "value", "milestone_tracker"],
			filters=dict(reference_type=todo.doctype, reference_name=todo.name),
			order_by="modified desc",
		)

		self.assertEqual(len(milestones), 2)
		self.assertEqual(milestones[0].track_field, "status")
		self.assertEqual(milestones[0].value, "Closed")

		# cleanup
		criscostack.db.delete("Milestone")
		milestone_tracker.delete()
