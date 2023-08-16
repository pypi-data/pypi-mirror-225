# Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

from urllib.parse import parse_qsl

import criscostack
from criscostack import _
from criscostack.twofactor import get_qr_svg_code


def get_context(context):
	context.no_cache = 1
	context.qr_code_user, context.qrcode_svg = get_user_svg_from_cache()


def get_query_key():
	"""Return query string arg."""
	query_string = criscostack.local.request.query_string
	query = dict(parse_qsl(query_string))
	query = {key.decode(): val.decode() for key, val in query.items()}
	if not "k" in list(query):
		criscostack.throw(_("Not Permitted"), criscostack.PermissionError)
	query = (query["k"]).strip()
	if False in [i.isalpha() or i.isdigit() for i in query]:
		criscostack.throw(_("Not Permitted"), criscostack.PermissionError)
	return query


def get_user_svg_from_cache():
	"""Get User and SVG code from cache."""
	key = get_query_key()
	totp_uri = criscostack.cache.get_value(f"{key}_uri")
	user = criscostack.cache.get_value(f"{key}_user")
	if not totp_uri or not user:
		criscostack.throw(_("Page has expired!"), criscostack.PermissionError)
	if not criscostack.db.exists("User", user):
		criscostack.throw(_("Not Permitted"), criscostack.PermissionError)
	user = criscostack.get_doc("User", user)
	svg = get_qr_svg_code(totp_uri)
	return (user, svg.decode())
