# Copyright (c) 2020, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import criscostack


def validate_route_conflict(doctype, name):
	"""
	Raises exception if name clashes with routes from other documents for /app routing
	"""

	if criscostack.flags.in_migrate:
		return

	all_names = []
	for _doctype in ["Page", "Workspace", "DocType"]:
		all_names.extend(
			[slug(d) for d in criscostack.get_all(_doctype, pluck="name") if (doctype != _doctype and d != name)]
		)

	if slug(name) in all_names:
		criscostack.msgprint(criscostack._("Name already taken, please set a new name"))
		raise criscostack.NameError


def slug(name):
	return name.lower().replace(" ", "-")


def pop_csv_params(form_dict):
	"""Pop csv params from form_dict and return them as a dict."""
	from csv import QUOTE_NONNUMERIC

	from criscostack.utils.data import cint, cstr

	return {
		"delimiter": cstr(form_dict.pop("csv_delimiter", ","))[0],
		"quoting": cint(form_dict.pop("csv_quoting", QUOTE_NONNUMERIC)),
	}


def get_csv_bytes(data: list[list], csv_params: dict) -> bytes:
	"""Convert data to csv bytes."""
	from csv import writer
	from io import StringIO

	file = StringIO()
	csv_writer = writer(file, **csv_params)
	csv_writer.writerows(data)

	return file.getvalue().encode("utf-8")


def provide_binary_file(filename: str, extension: str, content: bytes) -> None:
	"""Provide a binary file to the client."""
	from criscostack import _

	criscostack.response["type"] = "binary"
	criscostack.response["filecontent"] = content
	criscostack.response["filename"] = f"{_(filename)}.{extension}"
