import criscostack
from criscostack.model.rename_doc import rename_doc


def execute():
	if criscostack.db.table_exists("Standard Reply") and not criscostack.db.table_exists("Email Template"):
		rename_doc("DocType", "Standard Reply", "Email Template")
		criscostack.reload_doc("email", "doctype", "email_template")
