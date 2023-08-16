# Copyright (c) 2021, Crisco Technologies and contributors
# License: MIT. See LICENSE
from tenacity import retry, retry_if_exception_type, stop_after_attempt

import criscostack
from criscostack.model.document import Document
from criscostack.utils import cstr


class AccessLog(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from criscostack.types import DF

		columns: DF.HTMLEditor | None
		export_from: DF.Data | None
		file_type: DF.Data | None
		filters: DF.Code | None
		method: DF.Data | None
		page: DF.HTMLEditor | None
		reference_document: DF.Data | None
		report_name: DF.Data | None
		timestamp: DF.Datetime | None
		user: DF.Link | None
	# end: auto-generated types
	@staticmethod
	def clear_old_logs(days=30):
		from criscostack.query_builder import Interval
		from criscostack.query_builder.functions import Now

		table = criscostack.qb.DocType("Access Log")
		criscostack.db.delete(table, filters=(table.modified < (Now() - Interval(days=days))))


@criscostack.whitelist()
def make_access_log(
	doctype=None,
	document=None,
	method=None,
	file_type=None,
	report_name=None,
	filters=None,
	page=None,
	columns=None,
):
	_make_access_log(
		doctype,
		document,
		method,
		file_type,
		report_name,
		filters,
		page,
		columns,
	)


@criscostack.write_only()
@retry(
	stop=stop_after_attempt(3),
	retry=retry_if_exception_type(criscostack.DuplicateEntryError),
	reraise=True,
)
def _make_access_log(
	doctype=None,
	document=None,
	method=None,
	file_type=None,
	report_name=None,
	filters=None,
	page=None,
	columns=None,
):
	user = criscostack.session.user
	in_request = criscostack.request and criscostack.request.method == "GET"

	access_log = criscostack.get_doc(
		{
			"doctype": "Access Log",
			"user": user,
			"export_from": doctype,
			"reference_document": document,
			"file_type": file_type,
			"report_name": report_name,
			"page": page,
			"method": method,
			"filters": cstr(filters) or None,
			"columns": columns,
		}
	)

	if criscostack.flags.read_only:
		access_log.deferred_insert()
		return
	else:
		access_log.db_insert()

	# `criscostack.db.commit` added because insert doesnt `commit` when called in GET requests like `printview`
	# dont commit in test mode. It must be tempting to put this block along with the in_request in the
	# whitelisted method...yeah, don't do it. That part would be executed possibly on a read only DB conn
	if not criscostack.flags.in_test or in_request:
		criscostack.db.commit()
