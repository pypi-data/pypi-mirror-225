# Copyright (c) 2018, Crisco Technologies and Contributors
# License: MIT. See LICENSE
import hashlib

import criscostack
from criscostack.tests.utils import CriscoTestCase

test_records = []


class TestTransactionLog(CriscoTestCase):
	def test_validate_chaining(self):
		criscostack.get_doc(
			{
				"doctype": "Transaction Log",
				"reference_doctype": "Test Doctype",
				"document_name": "Test Document 1",
				"data": "first_data",
			}
		).insert(ignore_permissions=True)

		second_log = criscostack.get_doc(
			{
				"doctype": "Transaction Log",
				"reference_doctype": "Test Doctype",
				"document_name": "Test Document 2",
				"data": "second_data",
			}
		).insert(ignore_permissions=True)

		third_log = criscostack.get_doc(
			{
				"doctype": "Transaction Log",
				"reference_doctype": "Test Doctype",
				"document_name": "Test Document 3",
				"data": "third_data",
			}
		).insert(ignore_permissions=True)

		sha = hashlib.sha256()
		sha.update(
			criscostack.safe_encode(str(third_log.transaction_hash))
			+ criscostack.safe_encode(str(second_log.chaining_hash))
		)

		self.assertEqual(sha.hexdigest(), third_log.chaining_hash)
