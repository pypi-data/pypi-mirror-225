# Copyright (c) 2020, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import criscostack
import criscostack.monitor
from criscostack.monitor import MONITOR_REDIS_KEY
from criscostack.tests.utils import CriscoTestCase
from criscostack.utils import set_request
from criscostack.utils.response import build_response


class TestMonitor(CriscoTestCase):
	def setUp(self):
		criscostack.conf.monitor = 1
		criscostack.cache.delete_value(MONITOR_REDIS_KEY)

	def test_enable_monitor(self):
		set_request(method="GET", path="/api/method/criscostack.ping")
		response = build_response("json")

		criscostack.monitor.start()
		criscostack.monitor.stop(response)

		logs = criscostack.cache.lrange(MONITOR_REDIS_KEY, 0, -1)
		self.assertEqual(len(logs), 1)

		log = criscostack.parse_json(logs[0].decode())
		self.assertTrue(log.duration)
		self.assertTrue(log.site)
		self.assertTrue(log.timestamp)
		self.assertTrue(log.uuid)
		self.assertTrue(log.request)
		self.assertEqual(log.transaction_type, "request")
		self.assertEqual(log.request["method"], "GET")

	def test_no_response(self):
		set_request(method="GET", path="/api/method/criscostack.ping")

		criscostack.monitor.start()
		criscostack.monitor.stop(response=None)

		logs = criscostack.cache.lrange(MONITOR_REDIS_KEY, 0, -1)
		self.assertEqual(len(logs), 1)

		log = criscostack.parse_json(logs[0].decode())
		self.assertEqual(log.request["status_code"], 500)
		self.assertEqual(log.transaction_type, "request")
		self.assertEqual(log.request["method"], "GET")

	def test_job(self):
		criscostack.utils.background_jobs.execute_job(
			criscostack.local.site, "criscostack.ping", None, None, {}, is_async=False
		)

		logs = criscostack.cache.lrange(MONITOR_REDIS_KEY, 0, -1)
		self.assertEqual(len(logs), 1)
		log = criscostack.parse_json(logs[0].decode())
		self.assertEqual(log.transaction_type, "job")
		self.assertTrue(log.job)
		self.assertEqual(log.job["method"], "criscostack.ping")
		self.assertEqual(log.job["scheduled"], False)
		self.assertEqual(log.job["wait"], 0)

	def test_flush(self):
		set_request(method="GET", path="/api/method/criscostack.ping")
		response = build_response("json")
		criscostack.monitor.start()
		criscostack.monitor.stop(response)

		open(criscostack.monitor.log_file(), "w").close()
		criscostack.monitor.flush()

		with open(criscostack.monitor.log_file()) as f:
			logs = f.readlines()

		self.assertEqual(len(logs), 1)
		log = criscostack.parse_json(logs[0])
		self.assertEqual(log.transaction_type, "request")

	def tearDown(self):
		criscostack.conf.monitor = 0
		criscostack.cache.delete_value(MONITOR_REDIS_KEY)
