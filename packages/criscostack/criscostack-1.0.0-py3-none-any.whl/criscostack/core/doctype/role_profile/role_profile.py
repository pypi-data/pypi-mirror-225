# Copyright (c) 2017, Crisco Technologies and contributors
# License: MIT. See LICENSE

import criscostack
from criscostack.model.document import Document


class RoleProfile(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from criscostack.core.doctype.has_role.has_role import HasRole
		from criscostack.types import DF

		role_profile: DF.Data
		roles: DF.Table[HasRole]
	# end: auto-generated types
	def autoname(self):
		"""set name as Role Profile name"""
		self.name = self.role_profile

	def on_update(self):
		"""Changes in role_profile reflected across all its user"""
		users = criscostack.get_all("User", filters={"role_profile_name": self.name})
		roles = [role.role for role in self.roles]
		for d in users:
			user = criscostack.get_doc("User", d)
			user.set("roles", [])
			user.add_roles(*roles)
