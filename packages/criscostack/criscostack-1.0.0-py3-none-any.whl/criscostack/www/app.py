# Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE
no_cache = 1

import json
import os
import re

import criscostack
import criscostack.sessions
from criscostack import _
from criscostack.utils.jinja_globals import is_rtl

SCRIPT_TAG_PATTERN = re.compile(r"\<script[^<]*\</script\>")
CLOSING_SCRIPT_TAG_PATTERN = re.compile(r"</script\>")


def get_context(context):
	if criscostack.session.user == "Guest":
		criscostack.throw(_("Log in to access this page."), criscostack.PermissionError)
	elif (
		criscostack.db.get_value("User", criscostack.session.user, "user_type", order_by=None) == "Website User"
	):
		criscostack.throw(_("You are not permitted to access this page."), criscostack.PermissionError)

	hooks = criscostack.get_hooks()
	try:
		boot = criscostack.sessions.get()
	except Exception as e:
		raise criscostack.SessionBootFailed from e

	# this needs commit
	csrf_token = criscostack.sessions.get_csrf_token()

	criscostack.db.commit()

	boot_json = criscostack.as_json(boot, indent=None, separators=(",", ":"))

	# remove script tags from boot
	boot_json = SCRIPT_TAG_PATTERN.sub("", boot_json)

	# TODO: Find better fix
	boot_json = CLOSING_SCRIPT_TAG_PATTERN.sub("", boot_json)
	boot_json = json.dumps(boot_json)

	include_js = hooks.get("app_include_js", []) + criscostack.conf.get("app_include_js", [])
	include_css = hooks.get("app_include_css", []) + criscostack.conf.get("app_include_css", [])

	context.update(
		{
			"no_cache": 1,
			"build_version": criscostack.utils.get_build_version(),
			"include_js": include_js,
			"include_css": include_css,
			"layout_direction": "rtl" if is_rtl() else "ltr",
			"lang": criscostack.local.lang,
			"sounds": hooks["sounds"],
			"boot": boot if context.get("for_mobile") else boot_json,
			"desk_theme": boot.get("desk_theme") or "Light",
			"csrf_token": csrf_token,
			"google_analytics_id": criscostack.conf.get("google_analytics_id"),
			"google_analytics_anonymize_ip": criscostack.conf.get("google_analytics_anonymize_ip"),
			"app_name": (
				criscostack.get_website_settings("app_name") or criscostack.get_system_settings("app_name") or "Crisco"
			),
		}
	)

	return context
