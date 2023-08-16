# Copyright (c) 2022, Crisco and Contributors
# License: MIT. See LICENSE


import criscostack
from criscostack.model import data_field_options


def execute():
	custom_field = criscostack.qb.DocType("Custom Field")
	(
		criscostack.qb.update(custom_field)
		.set(custom_field.options, None)
		.where((custom_field.fieldtype == "Data") & (custom_field.options.notin(data_field_options)))
	).run()
