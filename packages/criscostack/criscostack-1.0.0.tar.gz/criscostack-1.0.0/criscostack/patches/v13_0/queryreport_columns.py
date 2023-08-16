# Copyright (c) 2021, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import json

import criscostack


def execute():
	"""Convert Query Report json to support other content"""
	records = criscostack.get_all("Report", filters={"json": ["!=", ""]}, fields=["name", "json"])
	for record in records:
		jstr = record["json"]
		data = json.loads(jstr)
		if isinstance(data, list):
			# double escape braces
			jstr = f'{{"columns":{jstr}}}'
			criscostack.db.set_value("Report", record["name"], "json", jstr)
