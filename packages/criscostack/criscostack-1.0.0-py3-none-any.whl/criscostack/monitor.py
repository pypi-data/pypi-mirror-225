# Copyright (c) 2020, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import json
import os
import traceback
import uuid
from datetime import datetime

import rq

import criscostack

MONITOR_REDIS_KEY = "monitor-transactions"
MONITOR_MAX_ENTRIES = 1000000


def start(transaction_type="request", method=None, kwargs=None):
	if criscostack.conf.monitor:
		criscostack.local.monitor = Monitor(transaction_type, method, kwargs)


def stop(response=None):
	if hasattr(criscostack.local, "monitor"):
		criscostack.local.monitor.dump(response)


def add_data_to_monitor(**kwargs) -> None:
	"""Add additional custom key-value pairs along with monitor log.
	Note: Key-value pairs should be simple JSON exportable types."""
	if hasattr(criscostack.local, "monitor"):
		criscostack.local.monitor.add_custom_data(**kwargs)


def log_file():
	return os.path.join(criscostack.utils.get_bench_path(), "logs", "monitor.json.log")


class Monitor:
	__slots__ = ("data",)

	def __init__(self, transaction_type, method, kwargs):
		try:
			self.data = criscostack._dict(
				{
					"site": criscostack.local.site,
					"timestamp": datetime.utcnow(),
					"transaction_type": transaction_type,
					"uuid": str(uuid.uuid4()),
				}
			)

			if transaction_type == "request":
				self.collect_request_meta()
			else:
				self.collect_job_meta(method, kwargs)
		except Exception:
			traceback.print_exc()

	def collect_request_meta(self):
		self.data.request = criscostack._dict(
			{
				"ip": criscostack.local.request_ip,
				"method": criscostack.request.method,
				"path": criscostack.request.path,
			}
		)

	def collect_job_meta(self, method, kwargs):
		self.data.job = criscostack._dict({"method": method, "scheduled": False, "wait": 0})
		if "run_scheduled_job" in method:
			self.data.job.method = kwargs["job_type"]
			self.data.job.scheduled = True

		job = rq.get_current_job()
		if job:
			self.data.uuid = job.id
			waitdiff = self.data.timestamp - job.enqueued_at
			self.data.job.wait = int(waitdiff.total_seconds() * 1000000)

	def add_custom_data(self, **kwargs):
		if self.data:
			self.data.update(kwargs)

	def dump(self, response=None):
		try:
			timediff = datetime.utcnow() - self.data.timestamp
			# Obtain duration in microseconds
			self.data.duration = int(timediff.total_seconds() * 1000000)

			if self.data.transaction_type == "request":
				if response:
					self.data.request.status_code = response.status_code
					self.data.request.response_length = int(response.headers.get("Content-Length", 0))
				else:
					self.data.request.status_code = 500

				if hasattr(criscostack.local, "rate_limiter"):
					limiter = criscostack.local.rate_limiter
					self.data.request.counter = limiter.counter
					if limiter.rejected:
						self.data.request.reset = limiter.reset

			self.store()
		except Exception:
			traceback.print_exc()

	def store(self):
		if criscostack.cache.llen(MONITOR_REDIS_KEY) > MONITOR_MAX_ENTRIES:
			criscostack.cache.ltrim(MONITOR_REDIS_KEY, 1, -1)
		serialized = json.dumps(self.data, sort_keys=True, default=str, separators=(",", ":"))
		criscostack.cache.rpush(MONITOR_REDIS_KEY, serialized)


def flush():
	try:
		# Fetch all the logs without removing from cache
		logs = criscostack.cache.lrange(MONITOR_REDIS_KEY, 0, -1)
		if logs:
			logs = list(map(criscostack.safe_decode, logs))
			with open(log_file(), "a", os.O_NONBLOCK) as f:
				f.write("\n".join(logs))
				f.write("\n")
			# Remove fetched entries from cache
			criscostack.cache.ltrim(MONITOR_REDIS_KEY, len(logs) - 1, -1)
	except Exception:
		traceback.print_exc()
