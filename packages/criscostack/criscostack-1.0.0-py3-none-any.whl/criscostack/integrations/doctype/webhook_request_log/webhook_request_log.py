# Copyright (c) 2021, Crisco Technologies and contributors
# License: MIT. See LICENSE

import criscostack
from criscostack.model.document import Document


class WebhookRequestLog(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from criscostack.types import DF

		data: DF.Code | None
		error: DF.Text | None
		headers: DF.Code | None
		reference_document: DF.Data | None
		response: DF.Code | None
		url: DF.Data | None
		user: DF.Link | None
		webhook: DF.Link | None
	# end: auto-generated types
	@staticmethod
	def clear_old_logs(days=30):
		from criscostack.query_builder import Interval
		from criscostack.query_builder.functions import Now

		table = criscostack.qb.DocType("Webhook Request Log")
		criscostack.db.delete(table, filters=(table.modified < (Now() - Interval(days=days))))
