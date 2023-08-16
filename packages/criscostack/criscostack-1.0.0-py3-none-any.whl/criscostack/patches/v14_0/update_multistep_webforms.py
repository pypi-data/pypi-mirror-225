import criscostack


def execute():
	if not criscostack.db.has_column("Web Form", "is_multi_step_form"):
		return

	for web_form in criscostack.get_all("Web Form", filters={"is_multi_step_form": 1}):
		web_form_fields = criscostack.get_doc("Web Form", web_form.name).web_form_fields
		for web_form_field in web_form_fields:
			if web_form_field.fieldtype == "Section Break" and web_form_field.idx != 1:
				criscostack.db.set_value("Web Form Field", web_form_field.name, "fieldtype", "Page Break")
