# Copyright (c) 2019, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import sqlparse

import criscostack
import criscostack.recorder
from criscostack.recorder import normalize_query
from criscostack.tests.utils import CriscoTestCase
from criscostack.utils import set_request
from criscostack.website.serve import get_response_content


class TestRecorder(CriscoTestCase):
	def setUp(self):
		criscostack.recorder.stop()
		criscostack.recorder.delete()
		set_request()
		criscostack.recorder.start()
		criscostack.recorder.record()

	def test_start(self):
		criscostack.recorder.dump()
		requests = criscostack.recorder.get()
		self.assertEqual(len(requests), 1)

	def test_do_not_record(self):
		criscostack.recorder.do_not_record(criscostack.get_all)("DocType")
		criscostack.recorder.dump()
		requests = criscostack.recorder.get()
		self.assertEqual(len(requests), 0)

	def test_get(self):
		criscostack.recorder.dump()

		requests = criscostack.recorder.get()
		self.assertEqual(len(requests), 1)

		request = criscostack.recorder.get(requests[0]["uuid"])
		self.assertTrue(request)

	def test_delete(self):
		criscostack.recorder.dump()

		requests = criscostack.recorder.get()
		self.assertEqual(len(requests), 1)

		criscostack.recorder.delete()

		requests = criscostack.recorder.get()
		self.assertEqual(len(requests), 0)

	def test_record_without_sql_queries(self):
		criscostack.recorder.dump()

		requests = criscostack.recorder.get()
		request = criscostack.recorder.get(requests[0]["uuid"])

		self.assertEqual(len(request["calls"]), 0)

	def test_record_with_sql_queries(self):
		criscostack.get_all("DocType")
		criscostack.recorder.dump()

		requests = criscostack.recorder.get()
		request = criscostack.recorder.get(requests[0]["uuid"])

		self.assertNotEqual(len(request["calls"]), 0)

	def test_explain(self):
		criscostack.db.sql("SELECT * FROM tabDocType")
		criscostack.db.sql("COMMIT")
		criscostack.recorder.dump()
		criscostack.recorder.post_process()

		requests = criscostack.recorder.get()
		request = criscostack.recorder.get(requests[0]["uuid"])

		self.assertEqual(len(request["calls"][0]["explain_result"]), 1)
		self.assertEqual(len(request["calls"][1]["explain_result"]), 0)

	def test_multiple_queries(self):
		queries = [
			{"mariadb": "SELECT * FROM tabDocType", "postgres": 'SELECT * FROM "tabDocType"'},
			{"mariadb": "SELECT COUNT(*) FROM tabDocType", "postgres": 'SELECT COUNT(*) FROM "tabDocType"'},
			{"mariadb": "COMMIT", "postgres": "COMMIT"},
		]

		sql_dialect = criscostack.db.db_type or "mariadb"
		for query in queries:
			criscostack.db.sql(query[sql_dialect])

		criscostack.recorder.dump()
		criscostack.recorder.post_process()

		requests = criscostack.recorder.get()
		request = criscostack.recorder.get(requests[0]["uuid"])

		self.assertEqual(len(request["calls"]), len(queries))

		for query, call in zip(queries, request["calls"]):
			self.assertEqual(
				call["query"], sqlparse.format(query[sql_dialect].strip(), keyword_case="upper", reindent=True)
			)

	def test_duplicate_queries(self):
		queries = [
			("SELECT * FROM tabDocType", 2),
			("SELECT COUNT(*) FROM tabDocType", 1),
			("select * from tabDocType", 2),
			("COMMIT", 3),
			("COMMIT", 3),
			("COMMIT", 3),
		]
		for query in queries:
			criscostack.db.sql(query[0])

		criscostack.recorder.dump()
		criscostack.recorder.post_process()

		requests = criscostack.recorder.get()
		request = criscostack.recorder.get(requests[0]["uuid"])

		for query, call in zip(queries, request["calls"]):
			self.assertEqual(call["exact_copies"], query[1])

	def test_error_page_rendering(self):
		content = get_response_content("error")
		self.assertIn("Error", content)


class TestRecorderDeco(CriscoTestCase):
	def test_recorder_flag(self):
		criscostack.recorder.delete()

		@criscostack.recorder.record_queries
		def test():
			criscostack.get_all("User")

		test()
		self.assertTrue(criscostack.recorder.get())


class TestQueryNormalization(CriscoTestCase):
	def test_query_normalization(self):
		test_cases = {
			"select * from user where name = 'x'": "select * from user where name = ?",
			"select * from user where a > 5": "select * from user where a > ?",
			"select * from `user` where a > 5": "select * from `user` where a > ?",
			"select `name` from `user`": "select `name` from `user`",
			"select `name` from `user` limit 10": "select `name` from `user` limit ?",
		}

		for query, normalized in test_cases.items():
			self.assertEqual(normalize_query(query), normalized)
