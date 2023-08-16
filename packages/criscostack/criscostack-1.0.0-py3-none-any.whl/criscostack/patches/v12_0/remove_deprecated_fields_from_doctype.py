import criscostack


def execute():
	criscostack.reload_doc("core", "doctype", "doctype_link")
	criscostack.reload_doc("core", "doctype", "doctype_action")
	criscostack.reload_doc("core", "doctype", "doctype")
	criscostack.model.delete_fields(
		{"DocType": ["hide_heading", "image_view", "read_only_onload"]}, delete=1
	)

	criscostack.db.delete("Property Setter", {"property": "read_only_onload"})
