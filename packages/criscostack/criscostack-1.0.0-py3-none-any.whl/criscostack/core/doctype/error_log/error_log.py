# Copyright (c) 2015, Crisco Technologies and contributors
# License: MIT. See LICENSE

import criscostack
from criscostack.model.document import Document
from criscostack.query_builder import Interval
from criscostack.query_builder.functions import Now


class ErrorLog(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from criscostack.types import DF

		error: DF.Code | None
		method: DF.Data | None
		reference_doctype: DF.Link | None
		reference_name: DF.Data | None
		seen: DF.Check
	# end: auto-generated types
	def onload(self):
		if not self.seen and not criscostack.flags.read_only:
			self.db_set("seen", 1, update_modified=0)
			criscostack.db.commit()

	@staticmethod
	def clear_old_logs(days=30):
		table = criscostack.qb.DocType("Error Log")
		criscostack.db.delete(table, filters=(table.modified < (Now() - Interval(days=days))))


@criscostack.whitelist()
def clear_error_logs():
	"""Flush all Error Logs"""
	criscostack.only_for("System Manager")
	criscostack.db.truncate("Error Log")
