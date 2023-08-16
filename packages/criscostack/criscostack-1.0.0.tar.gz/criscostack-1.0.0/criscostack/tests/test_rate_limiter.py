# Copyright (c) 2020, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import time

from werkzeug.wrappers import Response

import criscostack
import criscostack.rate_limiter
from criscostack.rate_limiter import RateLimiter
from criscostack.tests.utils import CriscoTestCase
from criscostack.utils import cint


class TestRateLimiter(CriscoTestCase):
	def test_apply_with_limit(self):
		criscostack.conf.rate_limit = {"window": 86400, "limit": 1}
		criscostack.rate_limiter.apply()

		self.assertTrue(hasattr(criscostack.local, "rate_limiter"))
		self.assertIsInstance(criscostack.local.rate_limiter, RateLimiter)

		criscostack.cache.delete(criscostack.local.rate_limiter.key)
		delattr(criscostack.local, "rate_limiter")

	def test_apply_without_limit(self):
		criscostack.conf.rate_limit = None
		criscostack.rate_limiter.apply()

		self.assertFalse(hasattr(criscostack.local, "rate_limiter"))

	def test_respond_over_limit(self):
		limiter = RateLimiter(0.01, 86400)
		time.sleep(0.01)
		limiter.update()

		criscostack.conf.rate_limit = {"window": 86400, "limit": 0.01}
		self.assertRaises(criscostack.TooManyRequestsError, criscostack.rate_limiter.apply)
		criscostack.rate_limiter.update()

		response = criscostack.rate_limiter.respond()

		self.assertIsInstance(response, Response)
		self.assertEqual(response.status_code, 429)

		headers = criscostack.local.rate_limiter.headers()
		self.assertIn("Retry-After", headers)
		self.assertNotIn("X-RateLimit-Used", headers)
		self.assertIn("X-RateLimit-Reset", headers)
		self.assertIn("X-RateLimit-Limit", headers)
		self.assertIn("X-RateLimit-Remaining", headers)
		self.assertTrue(int(headers["X-RateLimit-Reset"]) <= 86400)
		self.assertEqual(int(headers["X-RateLimit-Limit"]), 10000)
		self.assertEqual(int(headers["X-RateLimit-Remaining"]), 0)

		criscostack.cache.delete(limiter.key)
		criscostack.cache.delete(criscostack.local.rate_limiter.key)
		delattr(criscostack.local, "rate_limiter")

	def test_respond_under_limit(self):
		criscostack.conf.rate_limit = {"window": 86400, "limit": 0.01}
		criscostack.rate_limiter.apply()
		criscostack.rate_limiter.update()
		response = criscostack.rate_limiter.respond()
		self.assertEqual(response, None)

		criscostack.cache.delete(criscostack.local.rate_limiter.key)
		delattr(criscostack.local, "rate_limiter")

	def test_headers_under_limit(self):
		criscostack.conf.rate_limit = {"window": 86400, "limit": 0.01}
		criscostack.rate_limiter.apply()
		criscostack.rate_limiter.update()
		headers = criscostack.local.rate_limiter.headers()
		self.assertNotIn("Retry-After", headers)
		self.assertIn("X-RateLimit-Reset", headers)
		self.assertTrue(int(headers["X-RateLimit-Reset"] < 86400))
		self.assertEqual(int(headers["X-RateLimit-Used"]), criscostack.local.rate_limiter.duration)
		self.assertEqual(int(headers["X-RateLimit-Limit"]), 10000)
		self.assertEqual(int(headers["X-RateLimit-Remaining"]), 10000)

		criscostack.cache.delete(criscostack.local.rate_limiter.key)
		delattr(criscostack.local, "rate_limiter")

	def test_reject_over_limit(self):
		limiter = RateLimiter(0.01, 86400)
		time.sleep(0.01)
		limiter.update()

		limiter = RateLimiter(0.01, 86400)
		self.assertRaises(criscostack.TooManyRequestsError, limiter.apply)

		criscostack.cache.delete(limiter.key)

	def test_do_not_reject_under_limit(self):
		limiter = RateLimiter(0.01, 86400)
		time.sleep(0.01)
		limiter.update()

		limiter = RateLimiter(0.02, 86400)
		self.assertEqual(limiter.apply(), None)

		criscostack.cache.delete(limiter.key)

	def test_update_method(self):
		limiter = RateLimiter(0.01, 86400)
		time.sleep(0.01)
		limiter.update()

		self.assertEqual(limiter.duration, cint(criscostack.cache.get(limiter.key)))

		criscostack.cache.delete(limiter.key)
