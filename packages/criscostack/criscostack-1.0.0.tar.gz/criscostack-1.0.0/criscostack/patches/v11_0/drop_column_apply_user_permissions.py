import criscostack


def execute():
	column = "apply_user_permissions"
	to_remove = ["DocPerm", "Custom DocPerm"]

	for doctype in to_remove:
		if criscostack.db.table_exists(doctype):
			if column in criscostack.db.get_table_columns(doctype):
				criscostack.db.sql(f"alter table `tab{doctype}` drop column {column}")

	criscostack.reload_doc("core", "doctype", "docperm", force=True)
	criscostack.reload_doc("core", "doctype", "custom_docperm", force=True)
