# Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE
import criscostack
from criscostack.tests.utils import CriscoTestCase

test_records = criscostack.get_test_records("Page")


class TestPage(CriscoTestCase):
	def test_naming(self):
		self.assertRaises(
			criscostack.NameError,
			criscostack.get_doc(dict(doctype="Page", page_name="DocType", module="Core")).insert,
		)
		self.assertRaises(
			criscostack.NameError,
			criscostack.get_doc(dict(doctype="Page", page_name="Settings", module="Core")).insert,
		)
