import criscostack
from criscostack.model.rename_doc import rename_doc


def execute():
	if criscostack.db.exists("DocType", "Desk Page"):
		if criscostack.db.exists("DocType", "Workspace"):
			# this patch was not added initially, so this page might still exist
			criscostack.delete_doc("DocType", "Desk Page")
		else:
			criscostack.flags.ignore_route_conflict_validation = True
			rename_doc("DocType", "Desk Page", "Workspace")
			criscostack.flags.ignore_route_conflict_validation = False

	rename_doc("DocType", "Desk Chart", "Workspace Chart", ignore_if_exists=True)
	rename_doc("DocType", "Desk Shortcut", "Workspace Shortcut", ignore_if_exists=True)
	rename_doc("DocType", "Desk Link", "Workspace Link", ignore_if_exists=True)

	criscostack.reload_doc("desk", "doctype", "workspace", force=True)
	criscostack.reload_doc("desk", "doctype", "workspace_link", force=True)
	criscostack.reload_doc("desk", "doctype", "workspace_chart", force=True)
	criscostack.reload_doc("desk", "doctype", "workspace_shortcut", force=True)
