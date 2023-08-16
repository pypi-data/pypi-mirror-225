# Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

from contextlib import suppress

import criscostack
from criscostack import _
from criscostack.rate_limiter import rate_limit
from criscostack.utils import validate_email_address

sitemap = 1


def get_context(context):
	doc = criscostack.get_doc("Contact Us Settings", "Contact Us Settings")

	if doc.query_options:
		query_options = [opt.strip() for opt in doc.query_options.replace(",", "\n").split("\n") if opt]
	else:
		query_options = ["Sales", "Support", "General"]

	out = {"query_options": query_options, "parents": [{"name": _("Home"), "route": "/"}]}
	out.update(doc.as_dict())

	return out


@criscostack.whitelist(allow_guest=True)
@rate_limit(limit=1000, seconds=60 * 60)
def send_message(sender, message, subject="Website Query"):
	sender = validate_email_address(sender, throw=True)

	with suppress(criscostack.OutgoingEmailError):
		if forward_to_email := criscostack.db.get_single_value("Contact Us Settings", "forward_to_email"):
			criscostack.sendmail(recipients=forward_to_email, reply_to=sender, content=message, subject=subject)

		criscostack.sendmail(
			recipients=sender,
			content=f"<div style='white-space: pre-wrap'>Thank you for reaching out to us. We will get back to you at the earliest.\n\n\nYour query:\n\n{message}</div>",
			subject="We've received your query!",
		)

	# for clearing outgoing email error message
	criscostack.clear_last_message()

	# add to to-do ?
	criscostack.get_doc(
		dict(
			doctype="Communication",
			sender=sender,
			subject=_("New Message from Website Contact Page"),
			sent_or_received="Received",
			content=message,
			status="Open",
		)
	).insert(ignore_permissions=True)
