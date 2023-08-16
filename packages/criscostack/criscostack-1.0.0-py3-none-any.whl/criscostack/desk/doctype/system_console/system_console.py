# Copyright (c) 2020, Crisco Technologies and contributors
# License: MIT. See LICENSE

import json

import criscostack
from criscostack.model.document import Document
from criscostack.utils.safe_exec import read_sql, safe_exec


class SystemConsole(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from criscostack.types import DF

		commit: DF.Check
		console: DF.Code | None
		output: DF.Code | None
		show_processlist: DF.Check
		type: DF.Literal["Python", "SQL"]
	# end: auto-generated types
	def run(self):
		criscostack.only_for("System Manager")
		try:
			criscostack.local.debug_log = []
			if self.type == "Python":
				safe_exec(self.console)
				self.output = "\n".join(criscostack.debug_log)
			elif self.type == "SQL":
				self.output = criscostack.as_json(read_sql(self.console, as_dict=1))
		except Exception:
			self.commit = False
			self.output = criscostack.get_traceback()

		if self.commit:
			criscostack.db.commit()
		else:
			criscostack.db.rollback()

		criscostack.get_doc(dict(doctype="Console Log", script=self.console)).insert()
		criscostack.db.commit()


@criscostack.whitelist()
def execute_code(doc):
	console = criscostack.get_doc(json.loads(doc))
	console.run()
	return console.as_dict()


@criscostack.whitelist()
def show_processlist():
	criscostack.only_for("System Manager")

	return criscostack.db.multisql(
		{
			"postgres": """
			SELECT pid AS "Id",
				query_start AS "Time",
				state AS "State",
				query AS "Info",
				wait_event AS "Progress"
			FROM pg_stat_activity""",
			"mariadb": "show full processlist",
		},
		as_dict=True,
	)
