# Copyright (c) 2017, Crisco Technologies and contributors
# License: MIT. See LICENSE

import json

import criscostack
import criscostack.utils
from criscostack import _
from criscostack.model.document import Document
from criscostack.utils.jinja import validate_template
from criscostack.utils.weasyprint import download_pdf, get_html


class PrintFormat(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from criscostack.types import DF

		absolute_value: DF.Check
		align_labels_right: DF.Check
		css: DF.Code | None
		custom_format: DF.Check
		default_print_language: DF.Link | None
		disabled: DF.Check
		doc_type: DF.Link
		font: DF.Data | None
		font_size: DF.Int
		format_data: DF.Code | None
		html: DF.Code | None
		line_breaks: DF.Check
		margin_bottom: DF.Float
		margin_left: DF.Float
		margin_right: DF.Float
		margin_top: DF.Float
		module: DF.Link | None
		page_number: DF.Literal[
			"Hide", "Top Left", "Top Center", "Top Right", "Bottom Left", "Bottom Center", "Bottom Right"
		]
		print_format_builder: DF.Check
		print_format_builder_beta: DF.Check
		print_format_type: DF.Literal["Jinja", "JS"]
		raw_commands: DF.Code | None
		raw_printing: DF.Check
		show_section_headings: DF.Check
		standard: DF.Literal["No", "Yes"]
	# end: auto-generated types
	def onload(self):
		templates = criscostack.get_all(
			"Print Format Field Template",
			fields=["template", "field", "name"],
			filters={"document_type": self.doc_type},
		)
		self.set_onload("print_templates", templates)

	def get_html(self, docname, letterhead=None):
		return get_html(self.doc_type, docname, self.name, letterhead)

	def download_pdf(self, docname, letterhead=None):
		return download_pdf(self.doc_type, docname, self.name, letterhead)

	def validate(self):
		if (
			self.standard == "Yes"
			and not criscostack.local.conf.get("developer_mode")
			and not (criscostack.flags.in_import or criscostack.flags.in_test)
		):

			criscostack.throw(criscostack._("Standard Print Format cannot be updated"))

		# old_doc_type is required for clearing item cache
		self.old_doc_type = criscostack.db.get_value("Print Format", self.name, "doc_type")

		self.extract_images()

		if not self.module:
			self.module = criscostack.db.get_value("DocType", self.doc_type, "module")

		if self.html and self.print_format_type != "JS":
			validate_template(self.html)

		if self.custom_format and self.raw_printing and not self.raw_commands:
			criscostack.throw(
				_("{0} are required").format(criscostack.bold(_("Raw Commands"))), criscostack.MandatoryError
			)

		if self.custom_format and not self.html and not self.raw_printing:
			criscostack.throw(_("{0} is required").format(criscostack.bold(_("HTML"))), criscostack.MandatoryError)

	def extract_images(self):
		from criscostack.core.doctype.file.utils import extract_images_from_html

		if self.print_format_builder_beta:
			return

		if self.format_data:
			data = json.loads(self.format_data)
			for df in data:
				if df.get("fieldtype") and df["fieldtype"] in ("HTML", "Custom HTML") and df.get("options"):
					df["options"] = extract_images_from_html(self, df["options"])
			self.format_data = json.dumps(data)

	def on_update(self):
		if hasattr(self, "old_doc_type") and self.old_doc_type:
			criscostack.clear_cache(doctype=self.old_doc_type)
		if self.doc_type:
			criscostack.clear_cache(doctype=self.doc_type)

		self.export_doc()

	def after_rename(self, old: str, new: str, *args, **kwargs):
		if self.doc_type:
			criscostack.clear_cache(doctype=self.doc_type)

		# update property setter default_print_format if set
		criscostack.db.set_value(
			"Property Setter",
			{
				"doctype_or_field": "DocType",
				"doc_type": self.doc_type,
				"property": "default_print_format",
				"value": old,
			},
			"value",
			new,
		)

	def export_doc(self):
		from criscostack.modules.utils import export_module_json

		return export_module_json(self, self.standard == "Yes", self.module)

	def on_trash(self):
		if self.doc_type:
			criscostack.clear_cache(doctype=self.doc_type)


@criscostack.whitelist()
def make_default(name):
	"""Set print format as default"""
	criscostack.has_permission("Print Format", "write")

	print_format = criscostack.get_doc("Print Format", name)

	doctype = criscostack.get_doc("DocType", print_format.doc_type)
	if doctype.custom:
		doctype.default_print_format = name
		doctype.save()
	else:
		# "Customize form"
		criscostack.make_property_setter(
			{
				"doctype_or_field": "DocType",
				"doctype": print_format.doc_type,
				"property": "default_print_format",
				"value": name,
			}
		)

	criscostack.msgprint(
		criscostack._("{0} is now default print format for {1} doctype").format(
			criscostack.bold(name), criscostack.bold(print_format.doc_type)
		)
	)
