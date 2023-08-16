# Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

# pre loaded

import criscostack
from criscostack.tests.utils import CriscoTestCase


class TestUser(CriscoTestCase):
	def test_default_currency_on_setup(self):
		usd = criscostack.get_doc("Currency", "USD")
		self.assertDocumentEqual({"enabled": 1, "fraction": "Cent"}, usd)
