# Copyright (c) 2020, Crisco Technologies and contributors
# License: MIT. See LICENSE

import json

import criscostack

# import criscostack
from criscostack.model.document import Document


class DashboardSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from criscostack.types import DF

		chart_config: DF.Code | None
		user: DF.Link | None
	# end: auto-generated types
	pass


@criscostack.whitelist()
def create_dashboard_settings(user):
	if not criscostack.db.exists("Dashboard Settings", user):
		doc = criscostack.new_doc("Dashboard Settings")
		doc.name = user
		doc.insert(ignore_permissions=True)
		criscostack.db.commit()
		return doc


def get_permission_query_conditions(user):
	if not user:
		user = criscostack.session.user

	return f"""(`tabDashboard Settings`.name = {criscostack.db.escape(user)})"""


@criscostack.whitelist()
def save_chart_config(reset, config, chart_name):
	reset = criscostack.parse_json(reset)
	doc = criscostack.get_doc("Dashboard Settings", criscostack.session.user)
	chart_config = criscostack.parse_json(doc.chart_config) or {}

	if reset:
		chart_config[chart_name] = {}
	else:
		config = criscostack.parse_json(config)
		if not chart_name in chart_config:
			chart_config[chart_name] = {}
		chart_config[chart_name].update(config)

	criscostack.db.set_value(
		"Dashboard Settings", criscostack.session.user, "chart_config", json.dumps(chart_config)
	)
