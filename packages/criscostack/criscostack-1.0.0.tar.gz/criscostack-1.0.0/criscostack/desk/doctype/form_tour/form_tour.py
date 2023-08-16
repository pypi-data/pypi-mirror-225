# Copyright (c) 2021, Crisco Technologies and contributors
# License: MIT. See LICENSE

import json

import criscostack
from criscostack import _
from criscostack.model.document import Document
from criscostack.modules.export_file import export_to_files


class FormTour(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from criscostack.desk.doctype.form_tour_step.form_tour_step import FormTourStep
		from criscostack.types import DF

		dashboard_name: DF.Link | None
		first_document: DF.Check
		include_name_field: DF.Check
		is_standard: DF.Check
		list_name: DF.Literal[
			"List", "Report", "Dashboard", "Kanban", "Gantt", "Calendar", "File", "Image", "Inbox", "Map"
		]
		module: DF.Link | None
		new_document_form: DF.Check
		page_name: DF.Link | None
		page_route: DF.SmallText | None
		reference_doctype: DF.Link | None
		report_name: DF.Link | None
		save_on_complete: DF.Check
		steps: DF.Table[FormTourStep]
		title: DF.Data
		track_steps: DF.Check
		ui_tour: DF.Check
		view_name: DF.Literal["Workspaces", "List", "Form", "Tree", "Page"]
		workspace_name: DF.Link | None
	# end: auto-generated types
	def before_save(self):
		if self.is_standard and not self.module:
			if self.workspace_name:
				self.module = criscostack.db.get_value("Workspace", self.workspace_name, "module")
			elif self.dashboard_name:
				dashboard_doctype = criscostack.db.get_value("Dashboard", self.dashboard_name, "module")
				self.module = criscostack.db.get_value("DocType", dashboard_doctype, "module")
			else:
				self.module = "Desk"
		if not self.ui_tour:
			meta = criscostack.get_meta(self.reference_doctype)
			for step in self.steps:
				if step.is_table_field and step.parent_fieldname:
					parent_field_df = meta.get_field(step.parent_fieldname)
					step.child_doctype = parent_field_df.options
					field_df = criscostack.get_meta(step.child_doctype).get_field(step.fieldname)
					step.label = field_df.label
					step.fieldtype = field_df.fieldtype
				else:
					field_df = meta.get_field(step.fieldname)
					step.label = field_df.label
					step.fieldtype = field_df.fieldtype

	def on_update(self):
		criscostack.cache.delete_key("bootinfo")

		if criscostack.conf.developer_mode and self.is_standard:
			export_to_files([["Form Tour", self.name]], self.module)

	def on_trash(self):
		criscostack.cache.delete_key("bootinfo")


@criscostack.whitelist()
def reset_tour(tour_name):
	for user in criscostack.get_all("User", pluck="name"):
		onboarding_status = criscostack.parse_json(criscostack.db.get_value("User", user, "onboarding_status"))
		onboarding_status.pop(tour_name, None)
		criscostack.db.set_value(
			"User", user, "onboarding_status", criscostack.as_json(onboarding_status), update_modified=False
		)
		criscostack.cache.hdel("bootinfo", user)

	criscostack.msgprint(_("Successfully reset onboarding status for all users."), alert=True)


@criscostack.whitelist()
def update_user_status(value, step):
	from criscostack.utils.telemetry import capture

	step = criscostack.parse_json(step)
	tour = criscostack.parse_json(value)

	capture(
		criscostack.scrub(f"{step.parent}_{step.title}"),
		app="criscostack_ui_tours",
		properties={"is_completed": tour.is_completed},
	)
	criscostack.db.set_value(
		"User", criscostack.session.user, "onboarding_status", value, update_modified=False
	)

	criscostack.cache.hdel("bootinfo", criscostack.session.user)


def get_onboarding_ui_tours():
	if not criscostack.get_system_settings("enable_onboarding"):
		return []

	ui_tours = criscostack.get_all("Form Tour", filters={"ui_tour": 1}, fields=["page_route", "name"])

	return [[tour.name, json.loads(tour.page_route)] for tour in ui_tours]
