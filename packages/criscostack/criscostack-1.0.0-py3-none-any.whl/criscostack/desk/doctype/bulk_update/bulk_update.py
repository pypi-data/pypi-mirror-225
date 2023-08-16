# Copyright (c) 2015, Crisco Technologies and contributors
# License: MIT. See LICENSE

import criscostack
from criscostack import _
from criscostack.core.doctype.submission_queue.submission_queue import queue_submission
from criscostack.model.document import Document
from criscostack.utils import cint
from criscostack.utils.scheduler import is_scheduler_inactive


class BulkUpdate(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from criscostack.types import DF

		condition: DF.SmallText | None
		document_type: DF.Link
		field: DF.Literal
		limit: DF.Int
		update_value: DF.SmallText
	# end: auto-generated types
	@criscostack.whitelist()
	def bulk_update(self):
		self.check_permission("write")
		limit = self.limit if self.limit and cint(self.limit) < 500 else 500

		condition = ""
		if self.condition:
			if ";" in self.condition:
				criscostack.throw(_("; not allowed in condition"))

			condition = f" where {self.condition}"

		docnames = criscostack.db.sql_list(
			f"""select name from `tab{self.document_type}`{condition} limit {limit} offset 0"""
		)
		return submit_cancel_or_update_docs(
			self.document_type, docnames, "update", {self.field: self.update_value}
		)


@criscostack.whitelist()
def submit_cancel_or_update_docs(doctype, docnames, action="submit", data=None):
	docnames = criscostack.parse_json(docnames)

	if data:
		data = criscostack.parse_json(data)

	failed = []

	for i, d in enumerate(docnames, 1):
		doc = criscostack.get_doc(doctype, d)
		try:
			message = ""
			if action == "submit" and doc.docstatus.is_draft():
				if doc.meta.queue_in_background and not is_scheduler_inactive():
					queue_submission(doc, action)
					message = _("Queuing {0} for Submission").format(doctype)
				else:
					doc.submit()
					message = _("Submitting {0}").format(doctype)
			elif action == "cancel" and doc.docstatus.is_submitted():
				doc.cancel()
				message = _("Cancelling {0}").format(doctype)
			elif action == "update" and not doc.docstatus.is_cancelled():
				doc.update(data)
				doc.save()
				message = _("Updating {0}").format(doctype)
			else:
				failed.append(d)
			criscostack.db.commit()
			show_progress(docnames, message, i, d)

		except Exception:
			failed.append(d)
			criscostack.db.rollback()

	return failed


def show_progress(docnames, message, i, description):
	n = len(docnames)
	if n >= 10:
		criscostack.publish_progress(float(i) * 100 / n, title=message, description=description)
