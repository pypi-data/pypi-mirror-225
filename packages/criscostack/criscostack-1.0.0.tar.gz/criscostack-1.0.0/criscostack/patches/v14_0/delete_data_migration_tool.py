# Copyright (c) 2022, Crisco Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

import criscostack


def execute():
	doctypes = criscostack.get_all("DocType", {"module": "Data Migration", "custom": 0}, pluck="name")
	for doctype in doctypes:
		criscostack.delete_doc("DocType", doctype, ignore_missing=True)

	criscostack.delete_doc("Module Def", "Data Migration", ignore_missing=True, force=True)
