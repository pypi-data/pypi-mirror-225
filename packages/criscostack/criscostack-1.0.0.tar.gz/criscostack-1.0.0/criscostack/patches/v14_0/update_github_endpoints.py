import json

import criscostack


def execute():
	if criscostack.db.exists("Social Login Key", "github"):
		criscostack.db.set_value(
			"Social Login Key", "github", "auth_url_data", json.dumps({"scope": "user:email"})
		)
