# Copyright (c) 2015, Crisco Technologies and Contributors
# License: MIT. See LICENSE
import criscostack
from criscostack.contacts.doctype.address_template.address_template import get_default_address_template
from criscostack.tests.utils import CriscoTestCase
from criscostack.utils.jinja import validate_template


class TestAddressTemplate(CriscoTestCase):
	def setUp(self) -> None:
		criscostack.db.delete("Address Template", {"country": "India"})
		criscostack.db.delete("Address Template", {"country": "Brazil"})

	def test_default_address_template(self):
		validate_template(get_default_address_template())

	def test_default_is_unset(self):
		criscostack.get_doc({"doctype": "Address Template", "country": "India", "is_default": 1}).insert()

		self.assertEqual(criscostack.db.get_value("Address Template", "India", "is_default"), 1)

		criscostack.get_doc({"doctype": "Address Template", "country": "Brazil", "is_default": 1}).insert()

		self.assertEqual(criscostack.db.get_value("Address Template", "India", "is_default"), 0)
		self.assertEqual(criscostack.db.get_value("Address Template", "Brazil", "is_default"), 1)

	def test_delete_address_template(self):
		india = criscostack.get_doc(
			{"doctype": "Address Template", "country": "India", "is_default": 0}
		).insert()

		brazil = criscostack.get_doc(
			{"doctype": "Address Template", "country": "Brazil", "is_default": 1}
		).insert()

		india.reload()  # might have been modified by the second template
		india.delete()  # should not raise an error

		self.assertRaises(criscostack.ValidationError, brazil.delete)
