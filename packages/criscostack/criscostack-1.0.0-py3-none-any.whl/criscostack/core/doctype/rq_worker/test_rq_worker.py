# Copyright (c) 2022, Crisco Technologies and Contributors
# See license.txt

import criscostack
from criscostack.core.doctype.rq_worker.rq_worker import RQWorker
from criscostack.tests.utils import CriscoTestCase


class TestRQWorker(CriscoTestCase):
	def test_get_worker_list(self):
		workers = RQWorker.get_list({})
		self.assertGreaterEqual(len(workers), 1)
		self.assertTrue(any("short" in w.queue_type for w in workers))

	def test_worker_serialization(self):
		workers = RQWorker.get_list({})
		criscostack.get_doc("RQ Worker", workers[0].pid)
