import criscostack
from criscostack.desk.doctype.notification_settings.notification_settings import (
	create_notification_settings,
)


def execute():
	criscostack.reload_doc("desk", "doctype", "notification_settings")
	criscostack.reload_doc("desk", "doctype", "notification_subscribed_document")

	users = criscostack.get_all("User", fields=["name"])
	for user in users:
		create_notification_settings(user.name)
