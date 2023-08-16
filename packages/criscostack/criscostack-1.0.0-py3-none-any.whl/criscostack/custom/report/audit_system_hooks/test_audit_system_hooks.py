# Copyright (c) 2022, Crisco Technologies and contributors
# For license information, please see license.txt


from criscostack.custom.report.audit_system_hooks.audit_system_hooks import execute
from criscostack.tests.utils import CriscoTestCase


class TestAuditSystemHooksReport(CriscoTestCase):
	def test_basic_query(self):
		_, data = execute()
		for row in data:
			if row.get("hook_name") == "app_name":
				self.assertEqual(row.get("hook_values"), "criscostack")
				break
		else:
			self.fail("Failed to generate hooks report")
