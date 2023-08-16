# Copyright (c) 2020, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import criscostack


def execute():
	"""Set default module for standard Web Template, if none."""
	criscostack.reload_doc("website", "doctype", "Web Template Field")
	criscostack.reload_doc("website", "doctype", "web_template")

	standard_templates = criscostack.get_list("Web Template", {"standard": 1})
	for template in standard_templates:
		doc = criscostack.get_doc("Web Template", template.name)
		if not doc.module:
			doc.module = "Website"
			doc.save()
