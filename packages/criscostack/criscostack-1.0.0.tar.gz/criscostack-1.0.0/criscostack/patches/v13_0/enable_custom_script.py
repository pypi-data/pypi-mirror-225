# Copyright (c) 2020, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import criscostack


def execute():
	"""Enable all the existing Client script"""

	criscostack.db.sql(
		"""
		UPDATE `tabClient Script` SET enabled=1
	"""
	)
