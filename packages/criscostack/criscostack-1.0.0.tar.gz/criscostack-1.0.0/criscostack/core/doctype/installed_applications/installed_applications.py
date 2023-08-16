# Copyright (c) 2020, Crisco Technologies and contributors
# License: MIT. See LICENSE

import json

import criscostack
from criscostack import _
from criscostack.model.document import Document


class InvalidAppOrder(criscostack.ValidationError):
	pass


class InstalledApplications(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from criscostack.core.doctype.installed_application.installed_application import InstalledApplication
		from criscostack.types import DF

		installed_applications: DF.Table[InstalledApplication]
	# end: auto-generated types
	def update_versions(self):
		self.delete_key("installed_applications")
		for app in criscostack.utils.get_installed_apps_info():
			self.append(
				"installed_applications",
				{
					"app_name": app.get("app_name"),
					"app_version": app.get("version") or "UNVERSIONED",
					"git_branch": app.get("branch") or "UNVERSIONED",
				},
			)
		self.save()


@criscostack.whitelist()
def update_installed_apps_order(new_order: list[str] | str):
	"""Change the ordering of `installed_apps` global

	This list is used to resolve hooks and by default it's order of installation on site.

	Sometimes it might not be the ordering you want, so thie function is provided to override it.
	"""
	criscostack.only_for("System Manager")

	if isinstance(new_order, str):
		new_order = json.loads(new_order)

	criscostack.local.request_cache and criscostack.local.request_cache.clear()
	existing_order = criscostack.get_installed_apps(_ensure_on_bench=True)

	if set(existing_order) != set(new_order) or not isinstance(new_order, list):
		criscostack.throw(
			_("You are only allowed to update order, do not remove or add apps."), exc=InvalidAppOrder
		)

	# Ensure criscostack is always first regardless of user's preference.
	if "criscostack" in new_order:
		new_order.remove("criscostack")
	new_order.insert(0, "criscostack")

	criscostack.db.set_global("installed_apps", json.dumps(new_order))

	_create_version_log_for_change(existing_order, new_order)


def _create_version_log_for_change(old, new):
	version = criscostack.new_doc("Version")
	version.ref_doctype = "DefaultValue"
	version.docname = "installed_apps"
	version.data = criscostack.as_json({"changed": [["current", json.dumps(old), json.dumps(new)]]})
	version.flags.ignore_links = True  # This is a fake doctype
	version.flags.ignore_permissions = True
	version.insert()


@criscostack.whitelist()
def get_installed_app_order() -> list[str]:
	criscostack.only_for("System Manager")

	return criscostack.get_installed_apps(_ensure_on_bench=True)
