# Copyright (c) 2023, Crisco Technologies and Contributors
# See license.txt

import criscostack
from criscostack.automation.doctype.reminder.reminder import create_new_reminder, send_reminders
from criscostack.desk.doctype.notification_log.notification_log import get_notification_logs
from criscostack.tests.utils import CriscoTestCase
from criscostack.utils import add_to_date, now_datetime


class TestReminder(CriscoTestCase):
	def test_reminder(self):

		description = "TEST_REMINDER"

		create_new_reminder(
			remind_at=add_to_date(now_datetime(), minutes=1, as_datetime=True, as_string=True),
			description=description,
		)

		send_reminders()

		notifications = get_notification_logs()["notification_logs"]
		self.assertIn(
			description,
			[n.subject for n in notifications],
			msg=f"Failed to find reminder notification \n{notifications}",
		)
