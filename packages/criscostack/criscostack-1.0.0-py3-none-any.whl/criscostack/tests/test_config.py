# Copyright (c) 2022, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE
import criscostack
from criscostack.config import get_modules_from_all_apps_for_user
from criscostack.tests.utils import CriscoTestCase


class TestConfig(CriscoTestCase):
	def test_get_modules(self):
		criscostack_modules = criscostack.get_all("Module Def", filters={"app_name": "criscostack"}, pluck="name")
		all_modules_data = get_modules_from_all_apps_for_user()
		all_modules = [x["module_name"] for x in all_modules_data]
		self.assertIsInstance(all_modules_data, list)
		self.assertFalse([x for x in criscostack_modules if x not in all_modules])
