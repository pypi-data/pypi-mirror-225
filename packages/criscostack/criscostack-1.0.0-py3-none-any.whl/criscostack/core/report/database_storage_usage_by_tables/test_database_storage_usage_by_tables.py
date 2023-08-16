# Copyright (c) 2022, Crisco Technologies and contributors
# For license information, please see license.txt


from criscostack.core.report.database_storage_usage_by_tables.database_storage_usage_by_tables import (
	execute,
)
from criscostack.tests.utils import CriscoTestCase


class TestDBUsageReport(CriscoTestCase):
	def test_basic_query(self):
		_, data = execute()
		tables = [d.table for d in data]
		self.assertFalse({"tabUser", "tabDocField"}.difference(tables))
