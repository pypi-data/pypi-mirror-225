import re

import criscostack
from criscostack.query_builder import DocType


def execute():
	"""Replace temporarily available Database Aggregate APIs on criscostack (develop)

	APIs changed:
	        * criscostack.db.max => criscostack.qb.max
	        * criscostack.db.min => criscostack.qb.min
	        * criscostack.db.sum => criscostack.qb.sum
	        * criscostack.db.avg => criscostack.qb.avg
	"""
	ServerScript = DocType("Server Script")
	server_scripts = (
		criscostack.qb.from_(ServerScript)
		.where(
			ServerScript.script.like("%criscostack.db.max(%")
			| ServerScript.script.like("%criscostack.db.min(%")
			| ServerScript.script.like("%criscostack.db.sum(%")
			| ServerScript.script.like("%criscostack.db.avg(%")
		)
		.select("name", "script")
		.run(as_dict=True)
	)

	for server_script in server_scripts:
		name, script = server_script["name"], server_script["script"]

		for agg in ["avg", "max", "min", "sum"]:
			script = re.sub(f"criscostack.db.{agg}\\(", f"criscostack.qb.{agg}(", script)

		criscostack.db.set_value("Server Script", name, "script", script)
