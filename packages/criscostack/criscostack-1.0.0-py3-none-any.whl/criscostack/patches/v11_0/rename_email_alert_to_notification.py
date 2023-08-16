import criscostack
from criscostack.model.rename_doc import rename_doc


def execute():
	if criscostack.db.table_exists("Email Alert Recipient") and not criscostack.db.table_exists(
		"Notification Recipient"
	):
		rename_doc("DocType", "Email Alert Recipient", "Notification Recipient")
		criscostack.reload_doc("email", "doctype", "notification_recipient")

	if criscostack.db.table_exists("Email Alert") and not criscostack.db.table_exists("Notification"):
		rename_doc("DocType", "Email Alert", "Notification")
		criscostack.reload_doc("email", "doctype", "notification")
