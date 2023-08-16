# Copyright (c) 2015, Crisco Technologies and contributors
# License: MIT. See LICENSE

import criscostack
from criscostack.core.doctype.report.report import is_prepared_report_enabled
from criscostack.model.document import Document
from criscostack.utils import cint


class RolePermissionforPageandReport(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from criscostack.core.doctype.has_role.has_role import HasRole
		from criscostack.types import DF

		enable_prepared_report: DF.Check
		page: DF.Link | None
		report: DF.Link | None
		roles: DF.Table[HasRole]
		set_role_for: DF.Literal["", "Page", "Report"]
	# end: auto-generated types
	@criscostack.whitelist()
	def set_report_page_data(self):
		self.set_custom_roles()
		self.check_prepared_report_disabled()

	def set_custom_roles(self):
		args = self.get_args()
		self.set("roles", [])

		name = criscostack.db.get_value("Custom Role", args, "name")
		if name:
			doc = criscostack.get_doc("Custom Role", name)
			roles = doc.roles
		else:
			roles = self.get_standard_roles()

		self.set("roles", roles)

	def check_prepared_report_disabled(self):
		if self.report:
			self.enable_prepared_report = is_prepared_report_enabled(self.report)

	def get_standard_roles(self):
		doctype = self.set_role_for
		docname = self.page if self.set_role_for == "Page" else self.report
		doc = criscostack.get_doc(doctype, docname)
		return doc.roles

	@criscostack.whitelist()
	def reset_roles(self):
		roles = self.get_standard_roles()
		self.set("roles", roles)
		self.update_custom_roles()
		self.update_disable_prepared_report()

	@criscostack.whitelist()
	def update_report_page_data(self):
		self.update_custom_roles()
		self.update_disable_prepared_report()

	def update_custom_roles(self):
		args = self.get_args()
		name = criscostack.db.get_value("Custom Role", args, "name")

		args.update({"doctype": "Custom Role", "roles": self.get_roles()})

		if self.report:
			args.update({"ref_doctype": criscostack.db.get_value("Report", self.report, "ref_doctype")})

		if name:
			custom_role = criscostack.get_doc("Custom Role", name)
			custom_role.set("roles", self.get_roles())
			custom_role.save()
		else:
			criscostack.get_doc(args).insert()

	def update_disable_prepared_report(self):
		if self.report:
			# intentionally written update query in criscostack.db.sql instead of criscostack.db.set_value
			criscostack.db.sql(
				"""update `tabReport` set prepared_report = %s
				where name = %s""",
				(self.enable_prepared_report, self.report),
			)

	def get_args(self, row=None):
		name = self.page if self.set_role_for == "Page" else self.report
		check_for_field = self.set_role_for.replace(" ", "_").lower()

		return {check_for_field: name}

	def get_roles(self):
		roles = []
		for data in self.roles:
			if data.role != "All":
				roles.append({"role": data.role, "parenttype": "Custom Role"})
		return roles

	def update_status(self):
		return criscostack.render_template
