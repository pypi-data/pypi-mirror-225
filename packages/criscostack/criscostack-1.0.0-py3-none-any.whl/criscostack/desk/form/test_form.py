# Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import criscostack
from criscostack.desk.form.linked_with import get_linked_docs, get_linked_doctypes
from criscostack.tests.utils import CriscoTestCase


class TestForm(CriscoTestCase):
	def test_linked_with(self):
		results = get_linked_docs("Role", "System Manager", linkinfo=get_linked_doctypes("Role"))
		self.assertTrue("User" in results)
		self.assertTrue("DocType" in results)


if __name__ == "__main__":
	import unittest

	criscostack.connect()
	unittest.main()
