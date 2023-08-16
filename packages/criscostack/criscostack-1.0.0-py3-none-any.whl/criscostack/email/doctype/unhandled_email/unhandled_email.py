# Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and contributors
# License: MIT. See LICENSE

import criscostack
from criscostack.model.document import Document


class UnhandledEmail(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from criscostack.types import DF

		email_account: DF.Link | None
		message_id: DF.Code | None
		raw: DF.Code | None
		reason: DF.LongText | None
		uid: DF.Data | None
	# end: auto-generated types
	pass


def remove_old_unhandled_emails():
	criscostack.db.delete(
		"Unhandled Email", {"creation": ("<", criscostack.utils.add_days(criscostack.utils.nowdate(), -30))}
	)
