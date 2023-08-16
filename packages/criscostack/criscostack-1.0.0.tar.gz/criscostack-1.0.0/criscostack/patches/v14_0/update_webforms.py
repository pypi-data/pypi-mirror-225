# Copyright (c) 2021, Crisco Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt


import criscostack


def execute():
	criscostack.reload_doc("website", "doctype", "web_form_list_column")
	criscostack.reload_doctype("Web Form")

	for web_form in criscostack.get_all("Web Form", fields=["*"]):
		if web_form.allow_multiple and not web_form.show_list:
			criscostack.db.set_value("Web Form", web_form.name, "show_list", True)
