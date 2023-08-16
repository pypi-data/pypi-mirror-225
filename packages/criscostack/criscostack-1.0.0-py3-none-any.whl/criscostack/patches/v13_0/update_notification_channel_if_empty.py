# Copyright (c) 2020, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import criscostack


def execute():

	criscostack.reload_doc("Email", "doctype", "Notification")

	notifications = criscostack.get_all("Notification", {"is_standard": 1}, {"name", "channel"})
	for notification in notifications:
		if not notification.channel:
			criscostack.db.set_value(
				"Notification", notification.name, "channel", "Email", update_modified=False
			)
			criscostack.db.commit()
