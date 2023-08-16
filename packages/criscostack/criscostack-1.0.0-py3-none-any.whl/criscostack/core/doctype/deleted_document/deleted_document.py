# Copyright (c) 2015, Crisco Technologies and contributors
# License: MIT. See LICENSE

import json

import criscostack
from criscostack import _
from criscostack.desk.doctype.bulk_update.bulk_update import show_progress
from criscostack.model.document import Document
from criscostack.model.workflow import get_workflow_name


class DeletedDocument(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from criscostack.types import DF

		data: DF.Code | None
		deleted_doctype: DF.Data | None
		deleted_name: DF.Data | None
		new_name: DF.ReadOnly | None
		restored: DF.Check
	# end: auto-generated types
	pass


@criscostack.whitelist()
def restore(name, alert=True):
	deleted = criscostack.get_doc("Deleted Document", name)

	if deleted.restored:
		criscostack.throw(_("Document {0} Already Restored").format(name), exc=criscostack.DocumentAlreadyRestored)

	doc = criscostack.get_doc(json.loads(deleted.data))

	try:
		doc.insert()
	except criscostack.DocstatusTransitionError:
		criscostack.msgprint(_("Cancelled Document restored as Draft"))
		doc.docstatus = 0
		active_workflow = get_workflow_name(doc.doctype)
		if active_workflow:
			workflow_state_fieldname = criscostack.get_value("Workflow", active_workflow, "workflow_state_field")
			if doc.get(workflow_state_fieldname):
				doc.set(workflow_state_fieldname, None)
		doc.insert()

	doc.add_comment("Edit", _("restored {0} as {1}").format(deleted.deleted_name, doc.name))

	deleted.new_name = doc.name
	deleted.restored = 1
	deleted.db_update()

	if alert:
		criscostack.msgprint(_("Document Restored"))


@criscostack.whitelist()
def bulk_restore(docnames):
	docnames = criscostack.parse_json(docnames)
	message = _("Restoring Deleted Document")
	restored, invalid, failed = [], [], []

	for i, d in enumerate(docnames):
		try:
			show_progress(docnames, message, i + 1, d)
			restore(d, alert=False)
			criscostack.db.commit()
			restored.append(d)

		except criscostack.DocumentAlreadyRestored:
			criscostack.message_log.pop()
			invalid.append(d)

		except Exception:
			criscostack.message_log.pop()
			failed.append(d)
			criscostack.db.rollback()

	return {"restored": restored, "invalid": invalid, "failed": failed}
