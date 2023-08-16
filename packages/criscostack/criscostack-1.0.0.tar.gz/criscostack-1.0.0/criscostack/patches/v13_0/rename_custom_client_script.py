import criscostack
from criscostack.model.rename_doc import rename_doc


def execute():
	if criscostack.db.exists("DocType", "Client Script"):
		return

	criscostack.flags.ignore_route_conflict_validation = True
	rename_doc("DocType", "Custom Script", "Client Script")
	criscostack.flags.ignore_route_conflict_validation = False

	criscostack.reload_doctype("Client Script", force=True)
