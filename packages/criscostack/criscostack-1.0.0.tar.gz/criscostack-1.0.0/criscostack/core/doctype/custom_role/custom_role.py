# Copyright (c) 2015, Crisco Technologies and contributors
# License: MIT. See LICENSE

import criscostack
from criscostack.model.document import Document


class CustomRole(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from criscostack.core.doctype.has_role.has_role import HasRole
		from criscostack.types import DF

		page: DF.Link | None
		ref_doctype: DF.Data | None
		report: DF.Link | None
		roles: DF.Table[HasRole]
	# end: auto-generated types
	def validate(self):
		if self.report and not self.ref_doctype:
			self.ref_doctype = criscostack.db.get_value("Report", self.report, "ref_doctype")


def get_custom_allowed_roles(field, name):
	allowed_roles = []
	custom_role = criscostack.db.get_value("Custom Role", {field: name}, "name")
	if custom_role:
		custom_role_doc = criscostack.get_doc("Custom Role", custom_role)
		allowed_roles = [d.role for d in custom_role_doc.roles]

	return allowed_roles
