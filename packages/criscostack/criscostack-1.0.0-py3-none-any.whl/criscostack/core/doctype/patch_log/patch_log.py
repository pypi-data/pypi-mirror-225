# Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

# License: MIT. See LICENSE

import criscostack
from criscostack import _
from criscostack.model.document import Document


class PatchLog(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from criscostack.types import DF

		patch: DF.Code | None
		skipped: DF.Check
		traceback: DF.Code | None
	# end: auto-generated types
	@criscostack.whitelist()
	def rerun_patch(self):
		from criscostack.modules.patch_handler import run_single

		if not criscostack.conf.developer_mode:
			criscostack.throw(_("Re-running patch is only allowed in developer mode."))

		run_single(self.patch, force=True)
		criscostack.msgprint(_("Successfully re-ran patch: {0}").format(self.patch), alert=True)


def before_migrate():
	criscostack.reload_doc("core", "doctype", "patch_log")
