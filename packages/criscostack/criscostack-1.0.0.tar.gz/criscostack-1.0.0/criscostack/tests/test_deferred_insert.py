import criscostack
from criscostack.deferred_insert import deferred_insert, save_to_db
from criscostack.tests.utils import CriscoTestCase


class TestDeferredInsert(CriscoTestCase):
	def test_deferred_insert(self):
		route_history = {"route": criscostack.generate_hash(), "user": "Administrator"}
		deferred_insert("Route History", [route_history])

		save_to_db()
		self.assertTrue(criscostack.db.exists("Route History", route_history))
