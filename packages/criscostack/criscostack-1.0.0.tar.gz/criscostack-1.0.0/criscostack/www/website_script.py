# Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import criscostack
from criscostack.utils import strip
from criscostack.website.doctype.website_theme.website_theme import get_active_theme

base_template_path = "www/website_script.js"


def get_context(context):
	context.javascript = criscostack.db.get_single_value("Website Script", "javascript") or ""

	theme = get_active_theme()
	js = strip(theme and theme.js or "")
	if js:
		context.javascript += "\n" + js

	if not criscostack.conf.developer_mode:
		context["google_analytics_id"] = get_setting("google_analytics_id")
		context["google_analytics_anonymize_ip"] = get_setting("google_analytics_anonymize_ip")


def get_setting(field_name):
	"""Return value of field_name frok Website Settings or Site Config."""
	website_settings = criscostack.db.get_single_value("Website Settings", field_name)
	conf = criscostack.conf.get(field_name)
	return website_settings or conf
