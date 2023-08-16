import criscostack
from criscostack import format
from criscostack.tests.utils import CriscoTestCase


class TestFormatter(CriscoTestCase):
	def test_currency_formatting(self):
		df = criscostack._dict({"fieldname": "amount", "fieldtype": "Currency", "options": "currency"})

		doc = criscostack._dict({"amount": 5})
		criscostack.db.set_default("currency", "INR")

		# if currency field is not passed then default currency should be used.
		self.assertEqual(format(100000, df, doc, format="#,###.##"), "₹ 100,000.00")

		doc.currency = "USD"
		self.assertEqual(format(100000, df, doc, format="#,###.##"), "$ 100,000.00")

		criscostack.db.set_default("currency", None)
