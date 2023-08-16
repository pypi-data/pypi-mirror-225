# Copyright (c) 2020, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import criscostack


def execute():
	criscostack.reload_doc("core", "doctype", "DocField")

	if criscostack.db.has_column("DocField", "show_days"):
		criscostack.db.sql(
			"""
			UPDATE
				tabDocField
			SET
				hide_days = 1 WHERE show_days = 0
		"""
		)
		criscostack.db.sql_ddl("alter table tabDocField drop column show_days")

	if criscostack.db.has_column("DocField", "show_seconds"):
		criscostack.db.sql(
			"""
			UPDATE
				tabDocField
			SET
				hide_seconds = 1 WHERE show_seconds = 0
		"""
		)
		criscostack.db.sql_ddl("alter table tabDocField drop column show_seconds")

	criscostack.clear_cache(doctype="DocField")
