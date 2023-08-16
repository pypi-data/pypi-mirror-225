import json

import criscostack


def execute():
	"""Handle introduction of UI tours"""
	completed = {}
	for tour in criscostack.get_all("Form Tour", {"ui_tour": 1}, pluck="name"):
		completed[tour] = {"is_complete": True}

	User = criscostack.qb.DocType("User")
	criscostack.qb.update(User).set("onboarding_status", json.dumps(completed)).run()
