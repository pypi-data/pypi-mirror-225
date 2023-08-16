# Copyright (c) 2020, Crisco Technologies and Contributors
# License: MIT. See LICENSE

import criscostack
from criscostack.core.doctype.installed_applications.installed_applications import (
	InvalidAppOrder,
	update_installed_apps_order,
)
from criscostack.tests.utils import CriscoTestCase


class TestInstalledApplications(CriscoTestCase):
	def test_order_change(self):
		update_installed_apps_order(["criscostack"])
		self.assertRaises(InvalidAppOrder, update_installed_apps_order, [])
		self.assertRaises(InvalidAppOrder, update_installed_apps_order, ["criscostack", "deepmind"])
