# Copyright (c) 2019, Crisco Technologies and contributors
# License: MIT. See LICENSE

import criscostack
from criscostack.model.document import Document
from criscostack.query_builder import Interval
from criscostack.query_builder.functions import Now


class ScheduledJobLog(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from criscostack.types import DF

		details: DF.Code | None
		scheduled_job_type: DF.Link
		status: DF.Literal["Scheduled", "Complete", "Failed"]
	# end: auto-generated types
	@staticmethod
	def clear_old_logs(days=90):
		table = criscostack.qb.DocType("Scheduled Job Log")
		criscostack.db.delete(table, filters=(table.modified < (Now() - Interval(days=days))))
