# Copyright (c) 2020, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import criscostack


def execute():
	if not criscostack.db.table_exists("Data Import"):
		return

	meta = criscostack.get_meta("Data Import")
	# if Data Import is the new one, return early
	if meta.fields[1].fieldname == "import_type":
		return

	criscostack.db.sql("DROP TABLE IF EXISTS `tabData Import Legacy`")
	criscostack.rename_doc("DocType", "Data Import", "Data Import Legacy")
	criscostack.db.commit()
	criscostack.db.sql("DROP TABLE IF EXISTS `tabData Import`")
	criscostack.rename_doc("DocType", "Data Import Beta", "Data Import")
