# Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import criscostack
from criscostack.utils import strip_html_tags
from criscostack.utils.html_utils import clean_html

no_cache = 1


def get_context(context):
	message_context = criscostack._dict()
	if hasattr(criscostack.local, "message"):
		message_context["header"] = criscostack.local.message_title
		message_context["title"] = strip_html_tags(criscostack.local.message_title)
		message_context["message"] = criscostack.local.message
		if hasattr(criscostack.local, "message_success"):
			message_context["success"] = criscostack.local.message_success

	elif criscostack.local.form_dict.id:
		message_id = criscostack.local.form_dict.id
		key = f"message_id:{message_id}"
		message = criscostack.cache.get_value(key, expires=True)
		if message:
			message_context.update(message.get("context", {}))
			if message.get("http_status_code"):
				criscostack.local.response["http_status_code"] = message["http_status_code"]

	if not message_context.title:
		message_context.title = clean_html(criscostack.form_dict.title)

	if not message_context.message:
		message_context.message = clean_html(criscostack.form_dict.message)

	return message_context
