# Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE
import criscostack
from criscostack.tests.utils import CriscoTestCase


class TestDocumentLocks(CriscoTestCase):
	def test_locking(self):
		todo = criscostack.get_doc(dict(doctype="ToDo", description="test")).insert()
		todo_1 = criscostack.get_doc("ToDo", todo.name)

		todo.lock()
		self.assertRaises(criscostack.DocumentLockedError, todo_1.lock)
		todo.unlock()

		todo_1.lock()
		self.assertRaises(criscostack.DocumentLockedError, todo.lock)
		todo_1.unlock()

	def test_operations_on_locked_documents(self):
		todo = criscostack.get_doc(dict(doctype="ToDo", description="testing operations")).insert()
		todo.lock()

		with self.assertRaises(criscostack.DocumentLockedError):
			todo.description = "Random"
			todo.save()

		# Checking for persistant locks across all instances.
		doc = criscostack.get_doc("ToDo", todo.name)
		self.assertEqual(doc.is_locked, True)

		with self.assertRaises(criscostack.DocumentLockedError):
			doc.description = "Random"
			doc.save()

		doc.unlock()
		self.assertEqual(doc.is_locked, False)
		self.assertEqual(todo.is_locked, False)
