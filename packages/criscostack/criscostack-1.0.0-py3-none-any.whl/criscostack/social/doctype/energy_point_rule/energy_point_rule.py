# Copyright (c) 2018, Crisco Technologies and contributors
# License: MIT. See LICENSE

import criscostack
import criscostack.cache_manager
from criscostack import _
from criscostack.core.doctype.user.user import get_enabled_users
from criscostack.model import log_types
from criscostack.model.document import Document
from criscostack.social.doctype.energy_point_log.energy_point_log import create_energy_points_log
from criscostack.social.doctype.energy_point_settings.energy_point_settings import (
	is_energy_point_enabled,
)


class EnergyPointRule(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from criscostack.types import DF

		apply_only_once: DF.Check
		condition: DF.Code | None
		enabled: DF.Check
		field_to_check: DF.Literal
		for_assigned_users: DF.Check
		for_doc_event: DF.Literal["New", "Submit", "Cancel", "Value Change", "Custom"]
		max_points: DF.Int
		multiplier_field: DF.Literal
		points: DF.Int
		reference_doctype: DF.Link
		rule_name: DF.Data
		user_field: DF.Literal
	# end: auto-generated types
	def on_update(self):
		criscostack.cache_manager.clear_doctype_map("Energy Point Rule", self.reference_doctype)

	def on_trash(self):
		criscostack.cache_manager.clear_doctype_map("Energy Point Rule", self.reference_doctype)

	def apply(self, doc):
		if self.rule_condition_satisfied(doc):
			multiplier = 1

			points = self.points
			if self.multiplier_field:
				multiplier = doc.get(self.multiplier_field) or 1
				points = round(points * multiplier)
				max_points = self.max_points
				if max_points and points > max_points:
					points = max_points

			reference_doctype = doc.doctype
			reference_name = doc.name
			users = []
			if self.for_assigned_users:
				users = doc.get_assigned_users()
			else:
				users = [doc.get(self.user_field)]
			rule = self.name

			# incase of zero as result after roundoff
			if not points:
				return

			try:
				for user in users:
					if not is_eligible_user(user):
						continue
					create_energy_points_log(
						reference_doctype,
						reference_name,
						{"points": points, "user": user, "rule": rule},
						self.apply_only_once,
					)
			except Exception as e:
				self.log_error("Energy points failed")

	def rule_condition_satisfied(self, doc):
		if self.for_doc_event == "New":
			# indicates that this was a new doc
			return doc.get_doc_before_save() is None
		if self.for_doc_event == "Submit":
			return doc.docstatus.is_submitted()
		if self.for_doc_event == "Cancel":
			return doc.docstatus.is_cancelled()
		if self.for_doc_event == "Value Change":
			field_to_check = self.field_to_check
			if not field_to_check:
				return False
			doc_before_save = doc.get_doc_before_save()
			# check if the field has been changed
			# if condition is set check if it is satisfied
			return (
				doc_before_save
				and doc_before_save.get(field_to_check) != doc.get(field_to_check)
				and (not self.condition or self.eval_condition(doc))
			)

		if self.for_doc_event == "Custom" and self.condition:
			return self.eval_condition(doc)
		return False

	def eval_condition(self, doc):
		return self.condition and criscostack.safe_eval(self.condition, None, {"doc": doc.as_dict()})


def process_energy_points(doc, state):
	if (
		criscostack.flags.in_patch
		or criscostack.flags.in_install
		or criscostack.flags.in_migrate
		or criscostack.flags.in_import
		or criscostack.flags.in_setup_wizard
		or doc.doctype in log_types
	):
		return

	if not is_energy_point_enabled():
		return

	old_doc = doc.get_doc_before_save()

	# check if doc has been cancelled
	if old_doc and old_doc.docstatus.is_submitted() and doc.docstatus.is_cancelled():
		return revert_points_for_cancelled_doc(doc)

	for d in criscostack.cache_manager.get_doctype_map(
		"Energy Point Rule", doc.doctype, dict(reference_doctype=doc.doctype, enabled=1)
	):
		criscostack.get_doc("Energy Point Rule", d.get("name")).apply(doc)


def revert_points_for_cancelled_doc(doc):
	energy_point_logs = criscostack.get_all(
		"Energy Point Log",
		{"reference_doctype": doc.doctype, "reference_name": doc.name, "type": "Auto"},
	)
	for log in energy_point_logs:
		reference_log = criscostack.get_doc("Energy Point Log", log.name)
		reference_log.revert(_("Reference document has been cancelled"), ignore_permissions=True)


def get_energy_point_doctypes():
	return [
		d.reference_doctype
		for d in criscostack.get_all("Energy Point Rule", ["reference_doctype"], {"enabled": 1})
	]


def is_eligible_user(user):
	"""Checks if user is eligible to get energy points"""
	enabled_users = get_enabled_users()
	return user and user in enabled_users and user != "Administrator"
