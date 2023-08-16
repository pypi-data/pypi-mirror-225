"""
This file contains multiple primitive tests for avoiding performance regressions.

- Time bound tests: Benchmarks are done on GHA before adding numbers
- Query count tests: More than expected # of queries for any action is frequent source of
  performance issues. This guards against such problems.


E.g. We know get_controller is supposed to be cached and hence shouldn't make query post first
query. This test can be written like this.

>>> def test_controller_caching(self):
>>>
>>> 	get_controller("User")  # <- "warm up code"
>>> 	with self.assertQueryCount(0):
>>> 		get_controller("User")

"""
import time

from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

import criscostack
from criscostack.criscostackclient import CriscoClient
from criscostack.model.base_document import get_controller
from criscostack.query_builder.utils import db_type_is
from criscostack.tests.test_query_builder import run_only_if
from criscostack.tests.utils import CriscoTestCase
from criscostack.utils import cint
from criscostack.website.path_resolver import PathResolver

TEST_USER = "test@example.com"


@run_only_if(db_type_is.MARIADB)
class TestPerformance(CriscoTestCase):
	def reset_request_specific_caches(self):
		# To simulate close to request level of handling
		criscostack.destroy()  # releases everything on criscostack.local
		criscostack.init(site=self.TEST_SITE)
		criscostack.connect()
		criscostack.clear_cache()

	def setUp(self) -> None:
		self.HOST = criscostack.utils.get_site_url(criscostack.local.site)

		self.reset_request_specific_caches()

	def test_meta_caching(self):
		criscostack.clear_cache()
		criscostack.get_meta("User")
		criscostack.clear_cache(doctype="ToDo")

		with self.assertQueryCount(0):
			criscostack.get_meta("User")

	def test_set_value_query_count(self):
		criscostack.db.set_value("User", "Administrator", "interest", "Nothing")

		with self.assertQueryCount(1):
			criscostack.db.set_value("User", "Administrator", "interest", "Nothing")

		with self.assertQueryCount(1):
			criscostack.db.set_value("User", {"user_type": "System User"}, "interest", "Nothing")

		with self.assertQueryCount(1):
			criscostack.db.set_value(
				"User", {"user_type": "System User"}, {"interest": "Nothing", "bio": "boring person"}
			)

	def test_controller_caching(self):

		get_controller("User")
		with self.assertQueryCount(0):
			get_controller("User")

	def test_get_value_limits(self):
		# check both dict and list style filters
		filters = [{"enabled": 1}, [["enabled", "=", 1]]]

		# Warm up code
		criscostack.db.get_values("User", filters=filters[0], limit=1)
		for filter in filters:
			with self.assertRowsRead(1):
				self.assertEqual(1, len(criscostack.db.get_values("User", filters=filter, limit=1)))
			with self.assertRowsRead(2):
				self.assertEqual(2, len(criscostack.db.get_values("User", filters=filter, limit=2)))

			self.assertEqual(
				len(criscostack.db.get_values("User", filters=filter)), criscostack.db.count("User", filter)
			)

			with self.assertRowsRead(1):
				criscostack.db.get_value("User", filters=filter)

			with self.assertRowsRead(1):
				criscostack.db.exists("User", filter)

	def test_db_value_cache(self):
		"""Link validation if repeated should just use db.value_cache, hence no extra queries"""
		doc = criscostack.get_last_doc("User")
		doc.get_invalid_links()

		with self.assertQueryCount(0):
			doc.get_invalid_links()

	@retry(
		retry=retry_if_exception_type(AssertionError),
		stop=stop_after_attempt(3),
		wait=wait_fixed(0.5),
		reraise=True,
	)
	def test_req_per_seconds_basic(self):
		"""Ideally should be ran against gunicorn worker, though I have not seen any difference
		when using werkzeug's run_simple for synchronous requests."""

		EXPECTED_RPS = 50  # measured on GHA
		FAILURE_THREASHOLD = 0.1

		req_count = 1000
		client = CriscoClient(self.HOST, "Administrator", self.ADMIN_PASSWORD)

		start = time.perf_counter()
		for _ in range(req_count):
			client.get_list("ToDo", limit_page_length=1)
		end = time.perf_counter()

		rps = req_count / (end - start)

		print(f"Completed {req_count} in {end - start} @ {rps} requests per seconds")
		self.assertGreaterEqual(
			rps,
			EXPECTED_RPS * (1 - FAILURE_THREASHOLD),
			f"Possible performance regression in basic /api/Resource list  requests",
		)

	def test_homepage_resolver(self):
		paths = ["/", "/app"]
		for path in paths:
			PathResolver(path).resolve()
			with self.assertQueryCount(1):
				PathResolver(path).resolve()

	def test_consistent_build_version(self):
		from criscostack.utils import get_build_version

		self.assertEqual(get_build_version(), get_build_version())

	def test_get_list_single_query(self):
		"""get_list should only perform single query."""

		user = criscostack.get_doc("User", TEST_USER)

		criscostack.set_user(TEST_USER)
		# Give full read access, no share/user perm check should be done.
		user.add_roles("System Manager")

		criscostack.get_list("User")
		with self.assertQueryCount(1):
			criscostack.get_list("User")

	def test_no_ifnull_checks(self):
		query = criscostack.get_all("DocType", {"autoname": ("is", "set")}, run=0).lower()
		self.assertNotIn("coalesce", query)
		self.assertNotIn("ifnull", query)
