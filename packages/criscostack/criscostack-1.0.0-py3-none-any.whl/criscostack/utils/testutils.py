# Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE
import criscostack


def add_custom_field(doctype, fieldname, fieldtype="Data", options=None):
	criscostack.get_doc(
		{
			"doctype": "Custom Field",
			"dt": doctype,
			"fieldname": fieldname,
			"fieldtype": fieldtype,
			"options": options,
		}
	).insert()


def clear_custom_fields(doctype):
	criscostack.db.delete("Custom Field", {"dt": doctype})
	criscostack.clear_cache(doctype=doctype)
