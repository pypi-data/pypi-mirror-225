# Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import json

import criscostack
from criscostack import _
from criscostack.model import core_doctypes_list
from criscostack.model.docfield import supports_translation
from criscostack.model.document import Document
from criscostack.query_builder.functions import IfNull
from criscostack.utils import cstr, random_string


class CustomField(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from criscostack.types import DF

		allow_in_quick_entry: DF.Check
		allow_on_submit: DF.Check
		bold: DF.Check
		collapsible: DF.Check
		collapsible_depends_on: DF.Code | None
		columns: DF.Int
		default: DF.Text | None
		depends_on: DF.Code | None
		description: DF.Text | None
		dt: DF.Link
		fetch_from: DF.SmallText | None
		fetch_if_empty: DF.Check
		fieldname: DF.Data | None
		fieldtype: DF.Literal[
			"Autocomplete",
			"Attach",
			"Attach Image",
			"Barcode",
			"Button",
			"Check",
			"Code",
			"Color",
			"Column Break",
			"Currency",
			"Data",
			"Date",
			"Datetime",
			"Duration",
			"Dynamic Link",
			"Float",
			"Fold",
			"Geolocation",
			"Heading",
			"HTML",
			"HTML Editor",
			"Icon",
			"Image",
			"Int",
			"JSON",
			"Link",
			"Long Text",
			"Markdown Editor",
			"Password",
			"Percent",
			"Phone",
			"Read Only",
			"Rating",
			"Section Break",
			"Select",
			"Signature",
			"Small Text",
			"Tab Break",
			"Table",
			"Table MultiSelect",
			"Text",
			"Text Editor",
			"Time",
		]
		hidden: DF.Check
		hide_border: DF.Check
		hide_days: DF.Check
		hide_seconds: DF.Check
		ignore_user_permissions: DF.Check
		ignore_xss_filter: DF.Check
		in_global_search: DF.Check
		in_list_view: DF.Check
		in_preview: DF.Check
		in_standard_filter: DF.Check
		insert_after: DF.Literal
		is_system_generated: DF.Check
		is_virtual: DF.Check
		label: DF.Data | None
		length: DF.Int
		mandatory_depends_on: DF.Code | None
		module: DF.Link | None
		no_copy: DF.Check
		non_negative: DF.Check
		options: DF.SmallText | None
		permlevel: DF.Int
		precision: DF.Literal["", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
		print_hide: DF.Check
		print_hide_if_no_value: DF.Check
		print_width: DF.Data | None
		read_only: DF.Check
		read_only_depends_on: DF.Code | None
		report_hide: DF.Check
		reqd: DF.Check
		search_index: DF.Check
		sort_options: DF.Check
		translatable: DF.Check
		unique: DF.Check
		width: DF.Data | None
	# end: auto-generated types
	def autoname(self):
		self.set_fieldname()
		self.name = self.dt + "-" + self.fieldname

	def set_fieldname(self):
		restricted = (
			"name",
			"parent",
			"creation",
			"modified",
			"modified_by",
			"parentfield",
			"parenttype",
			"file_list",
			"flags",
			"docstatus",
		)
		if not self.fieldname:
			label = self.label
			if not label:
				if self.fieldtype in ["Section Break", "Column Break", "Tab Break"]:
					label = self.fieldtype + "_" + str(random_string(5))
				else:
					criscostack.throw(_("Label is mandatory"))

			# remove special characters from fieldname
			self.fieldname = "".join(
				[c for c in cstr(label).replace(" ", "_") if c.isdigit() or c.isalpha() or c == "_"]
			)
			self.fieldname = f"custom_{self.fieldname}"

		# fieldnames should be lowercase
		self.fieldname = self.fieldname.lower()

		if self.fieldname in restricted:
			self.fieldname = self.fieldname + "1"

	def before_insert(self):
		self.set_fieldname()

	def validate(self):
		# these imports have been added to avoid cyclical import, should fix in future
		from criscostack.core.doctype.doctype.doctype import check_fieldname_conflicts
		from criscostack.custom.doctype.customize_form.customize_form import CustomizeForm

		# don't always get meta to improve performance
		# setting idx is just an improvement, not a requirement
		if self.is_new() or self.insert_after == "append":
			meta = criscostack.get_meta(self.dt, cached=False)
			fieldnames = [df.fieldname for df in meta.get("fields")]

			if self.is_new() and self.fieldname in fieldnames:
				criscostack.throw(
					_("A field with the name {0} already exists in {1}").format(
						criscostack.bold(self.fieldname), self.dt
					)
				)

			if self.insert_after == "append":
				self.insert_after = fieldnames[-1]

			if self.insert_after and self.insert_after in fieldnames:
				self.idx = fieldnames.index(self.insert_after) + 1

		if (
			not self.is_virtual
			and (doc_before_save := self.get_doc_before_save())
			and (old_fieldtype := doc_before_save.fieldtype) != self.fieldtype
			and not CustomizeForm.allow_fieldtype_change(old_fieldtype, self.fieldtype)
		):
			criscostack.throw(
				_("Fieldtype cannot be changed from {0} to {1}").format(old_fieldtype, self.fieldtype)
			)

		if not self.fieldname:
			criscostack.throw(_("Fieldname not set for Custom Field"))

		if self.get("translatable", 0) and not supports_translation(self.fieldtype):
			self.translatable = 0

		check_fieldname_conflicts(self)

	def on_update(self):
		# validate field
		if not self.flags.ignore_validate:
			from criscostack.core.doctype.doctype.doctype import validate_fields_for_doctype

			validate_fields_for_doctype(self.dt)

		# clear cache and update the schema
		if not criscostack.flags.in_create_custom_fields:
			criscostack.clear_cache(doctype=self.dt)
			criscostack.db.updatedb(self.dt)

	def on_trash(self):
		# check if Admin owned field
		if self.owner == "Administrator" and criscostack.session.user != "Administrator":
			criscostack.throw(
				_(
					"Custom Field {0} is created by the Administrator and can only be deleted through the Administrator account."
				).format(criscostack.bold(self.label))
			)

		# delete property setter entries
		criscostack.db.delete("Property Setter", {"doc_type": self.dt, "field_name": self.fieldname})

		# update doctype layouts
		doctype_layouts = criscostack.get_all(
			"DocType Layout", filters={"document_type": self.dt}, pluck="name"
		)

		for layout in doctype_layouts:
			layout_doc = criscostack.get_doc("DocType Layout", layout)
			for field in layout_doc.fields:
				if field.fieldname == self.fieldname:
					layout_doc.remove(field)
					layout_doc.save()
					break

		criscostack.clear_cache(doctype=self.dt)

	def validate_insert_after(self, meta):
		if not meta.get_field(self.insert_after):
			criscostack.throw(
				_(
					"Insert After field '{0}' mentioned in Custom Field '{1}', with label '{2}', does not exist"
				).format(self.insert_after, self.name, self.label),
				criscostack.DoesNotExistError,
			)

		if self.fieldname == self.insert_after:
			criscostack.throw(_("Insert After cannot be set as {0}").format(meta.get_label(self.insert_after)))


@criscostack.whitelist()
def get_fields_label(doctype=None):
	meta = criscostack.get_meta(doctype)

	if doctype in core_doctypes_list:
		return criscostack.msgprint(_("Custom Fields cannot be added to core DocTypes."))

	if meta.custom:
		return criscostack.msgprint(_("Custom Fields can only be added to a standard DocType."))

	return [
		{"value": df.fieldname or "", "label": _(df.label) if df.label else ""}
		for df in criscostack.get_meta(doctype).get("fields")
	]


def create_custom_field_if_values_exist(doctype, df):
	df = criscostack._dict(df)
	if df.fieldname in criscostack.db.get_table_columns(doctype) and criscostack.db.count(
		dt=doctype, filters=IfNull(df.fieldname, "") != ""
	):
		create_custom_field(doctype, df)


def create_custom_field(doctype, df, ignore_validate=False, is_system_generated=True):
	df = criscostack._dict(df)
	if not df.fieldname and df.label:
		df.fieldname = criscostack.scrub(df.label)
	if not criscostack.db.get_value("Custom Field", {"dt": doctype, "fieldname": df.fieldname}):
		custom_field = criscostack.get_doc(
			{
				"doctype": "Custom Field",
				"dt": doctype,
				"permlevel": 0,
				"fieldtype": "Data",
				"hidden": 0,
				"is_system_generated": is_system_generated,
			}
		)
		custom_field.update(df)
		custom_field.flags.ignore_validate = ignore_validate
		custom_field.insert()
		return custom_field


def create_custom_fields(custom_fields, ignore_validate=False, update=True):
	"""Add / update multiple custom fields

	:param custom_fields: example `{'Sales Invoice': [dict(fieldname='test')]}`"""

	try:
		criscostack.flags.in_create_custom_fields = True
		doctypes_to_update = set()

		if criscostack.flags.in_setup_wizard:
			ignore_validate = True

		for doctypes, fields in custom_fields.items():
			if isinstance(fields, dict):
				# only one field
				fields = [fields]

			if isinstance(doctypes, str):
				# only one doctype
				doctypes = (doctypes,)

			for doctype in doctypes:
				doctypes_to_update.add(doctype)

				for df in fields:
					field = criscostack.db.get_value("Custom Field", {"dt": doctype, "fieldname": df["fieldname"]})
					if not field:
						try:
							df = df.copy()
							df["owner"] = "Administrator"
							create_custom_field(doctype, df, ignore_validate=ignore_validate)

						except criscostack.exceptions.DuplicateEntryError:
							pass

					elif update:
						custom_field = criscostack.get_doc("Custom Field", field)
						custom_field.flags.ignore_validate = ignore_validate
						custom_field.update(df)
						custom_field.save()

		for doctype in doctypes_to_update:
			criscostack.clear_cache(doctype=doctype)
			criscostack.db.updatedb(doctype)

	finally:
		criscostack.flags.in_create_custom_fields = False
