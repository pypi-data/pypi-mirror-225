import criscostack
from criscostack.model.rename_doc import rename_doc


def execute():
	if criscostack.db.table_exists("Workflow Action") and not criscostack.db.table_exists(
		"Workflow Action Master"
	):
		rename_doc("DocType", "Workflow Action", "Workflow Action Master")
		criscostack.reload_doc("workflow", "doctype", "workflow_action_master")
