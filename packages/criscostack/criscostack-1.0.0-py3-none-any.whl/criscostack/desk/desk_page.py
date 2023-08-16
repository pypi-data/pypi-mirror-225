# Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import criscostack


@criscostack.whitelist()
def get(name):
	"""
	Return the :term:`doclist` of the `Page` specified by `name`
	"""
	page = criscostack.get_doc("Page", name)
	if page.is_permitted():
		page.load_assets()
		docs = criscostack._dict(page.as_dict())
		if getattr(page, "_dynamic_page", None):
			docs["_dynamic_page"] = 1

		return docs
	else:
		criscostack.response["403"] = 1
		raise criscostack.PermissionError("No read permission for Page %s" % (page.title or name))


@criscostack.whitelist(allow_guest=True)
def getpage():
	"""
	Load the page from `criscostack.form` and send it via `criscostack.response`
	"""
	page = criscostack.form_dict.get("name")
	doc = get(page)

	criscostack.response.docs.append(doc)
