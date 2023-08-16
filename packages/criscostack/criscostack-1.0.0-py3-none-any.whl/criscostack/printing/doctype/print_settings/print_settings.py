# Copyright (c) 2018, Crisco Technologies and contributors
# License: MIT. See LICENSE

import criscostack
from criscostack import _
from criscostack.model.document import Document
from criscostack.utils import cint


class PrintSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from criscostack.types import DF

		add_draft_heading: DF.Check
		allow_page_break_inside_tables: DF.Check
		allow_print_for_cancelled: DF.Check
		allow_print_for_draft: DF.Check
		enable_print_server: DF.Check
		enable_raw_printing: DF.Check
		font: DF.Literal[
			"Default", "Helvetica Neue", "Arial", "Helvetica", "Inter", "Verdana", "Monospace"
		]
		font_size: DF.Float
		pdf_page_height: DF.Float
		pdf_page_size: DF.Literal[
			"A0",
			"A1",
			"A2",
			"A3",
			"A4",
			"A5",
			"A6",
			"A7",
			"A8",
			"A9",
			"B0",
			"B1",
			"B2",
			"B3",
			"B4",
			"B5",
			"B6",
			"B7",
			"B8",
			"B9",
			"B10",
			"C5E",
			"Comm10E",
			"DLE",
			"Executive",
			"Folio",
			"Ledger",
			"Legal",
			"Letter",
			"Tabloid",
			"Custom",
		]
		pdf_page_width: DF.Float
		print_style: DF.Link | None
		repeat_header_footer: DF.Check
		send_print_as_pdf: DF.Check
		with_letterhead: DF.Check
	# end: auto-generated types
	def validate(self):
		if self.pdf_page_size == "Custom" and not (self.pdf_page_height and self.pdf_page_width):
			criscostack.throw(_("Page height and width cannot be zero"))

	def on_update(self):
		criscostack.clear_cache()


@criscostack.whitelist()
def is_print_server_enabled():
	if not hasattr(criscostack.local, "enable_print_server"):
		criscostack.local.enable_print_server = cint(
			criscostack.db.get_single_value("Print Settings", "enable_print_server")
		)

	return criscostack.local.enable_print_server
