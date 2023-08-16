import criscostack


def execute():
	doctype = "Top Bar Item"
	if not criscostack.db.table_exists(doctype) or not criscostack.db.has_column(doctype, "target"):
		return

	criscostack.reload_doc("website", "doctype", "top_bar_item")
	criscostack.db.set_value(doctype, {"target": 'target = "_blank"'}, "open_in_new_tab", 1)
