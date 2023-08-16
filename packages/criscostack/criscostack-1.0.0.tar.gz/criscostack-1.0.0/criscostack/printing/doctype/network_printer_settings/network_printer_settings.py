# Copyright (c) 2021, Crisco Technologies and contributors
# For license information, please see license.txt

import criscostack
from criscostack import _
from criscostack.model.document import Document


class NetworkPrinterSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from criscostack.types import DF

		port: DF.Int
		printer_name: DF.Literal
		server_ip: DF.Data
	# end: auto-generated types
	@criscostack.whitelist()
	def get_printers_list(self, ip="localhost", port=631):
		printer_list = []
		try:
			import cups
		except ImportError:
			criscostack.throw(
				_(
					"""This feature can not be used as dependencies are missing.
				Please contact your system manager to enable this by installing pycups!"""
				)
			)
			return
		try:
			cups.setServer(self.server_ip)
			cups.setPort(self.port)
			conn = cups.Connection()
			printers = conn.getPrinters()
			for printer_id, printer in printers.items():
				printer_list.append({"value": printer_id, "label": printer["printer-make-and-model"]})

		except RuntimeError:
			criscostack.throw(_("Failed to connect to server"))
		except criscostack.ValidationError:
			criscostack.throw(_("Failed to connect to server"))
		return printer_list


@criscostack.whitelist()
def get_network_printer_settings():
	return criscostack.db.get_list("Network Printer Settings", pluck="name")
