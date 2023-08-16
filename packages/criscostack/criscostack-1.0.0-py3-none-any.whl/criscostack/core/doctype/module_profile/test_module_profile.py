# Copyright (c) 2020, Crisco Technologies and Contributors
# License: MIT. See LICENSE
import criscostack
from criscostack.tests.utils import CriscoTestCase


class TestModuleProfile(CriscoTestCase):
	def test_make_new_module_profile(self):
		if not criscostack.db.get_value("Module Profile", "_Test Module Profile"):
			criscostack.get_doc(
				{
					"doctype": "Module Profile",
					"module_profile_name": "_Test Module Profile",
					"block_modules": [{"module": "Accounts"}],
				}
			).insert()

		# add to user and check
		if not criscostack.db.get_value("User", "test-for-module_profile@example.com"):
			new_user = criscostack.get_doc(
				{"doctype": "User", "email": "test-for-module_profile@example.com", "first_name": "Test User"}
			).insert()
		else:
			new_user = criscostack.get_doc("User", "test-for-module_profile@example.com")

		new_user.module_profile = "_Test Module Profile"
		new_user.save()

		self.assertEqual(new_user.block_modules[0].module, "Accounts")
