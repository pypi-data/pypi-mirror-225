# Copyright (c) 2022, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import criscostack
from criscostack import _, msgprint
from criscostack.utils import cint, cstr, get_url, now_datetime
from criscostack.utils.data import getdate
from criscostack.utils.verified_command import get_signed_params, verify_request


def get_emails_sent_this_month(email_account=None):
	"""Get count of emails sent from a specific email account.

	:param email_account: name of the email account used to send mail

	if email_account=None, email account filter is not applied while counting
	"""
	today = getdate()
	month_start = today.replace(day=1)

	filters = {
		"status": "Sent",
		"creation": [">=", str(month_start)],
	}
	if email_account:
		filters["email_account"] = email_account

	return criscostack.db.count("Email Queue", filters=filters)


def get_emails_sent_today(email_account=None):
	"""Get count of emails sent from a specific email account.

	:param email_account: name of the email account used to send mail

	if email_account=None, email account filter is not applied while counting
	"""
	q = """
		SELECT
			COUNT(`name`)
		FROM
			`tabEmail Queue`
		WHERE
			`status` in ('Sent', 'Not Sent', 'Sending')
			AND
			`creation` > (NOW() - INTERVAL '24' HOUR)
	"""

	q_args = {}
	if email_account is not None:
		if email_account:
			q += " AND email_account = %(email_account)s"
			q_args["email_account"] = email_account
		else:
			q += " AND (email_account is null OR email_account='')"

	return criscostack.db.sql(q, q_args)[0][0]


def get_unsubscribe_message(
	unsubscribe_message: str, expose_recipients: str
) -> "criscostack._dict[str, str]":
	unsubscribe_message = unsubscribe_message or _("Unsubscribe")
	unsubscribe_link = f'<a href="<!--unsubscribe_url-->" target="_blank">{unsubscribe_message}</a>'
	unsubscribe_html = _("{0} to stop receiving emails of this type").format(unsubscribe_link)
	html = f"""<div class="email-unsubscribe">
			<!--cc_message-->
			<div>
				{unsubscribe_html}
			</div>
		</div>"""

	text = f"\n\n{unsubscribe_message}: <!--unsubscribe_url-->\n"
	if expose_recipients == "footer":
		text = f"\n<!--cc_message-->{text}"

	return criscostack._dict(html=html, text=text)


def get_unsubcribed_url(
	reference_doctype, reference_name, email, unsubscribe_method, unsubscribe_params
):
	params = {
		"email": cstr(email),
		"doctype": cstr(reference_doctype),
		"name": cstr(reference_name),
	}
	if unsubscribe_params:
		params.update(unsubscribe_params)

	query_string = get_signed_params(params)

	# for test
	criscostack.local.flags.signed_query_string = query_string

	return get_url(unsubscribe_method + "?" + get_signed_params(params))


@criscostack.whitelist(allow_guest=True)
def unsubscribe(doctype, name, email):
	# unsubsribe from comments and communications
	if not criscostack.flags.in_test and not verify_request():
		return

	try:
		criscostack.get_doc(
			{
				"doctype": "Email Unsubscribe",
				"email": email,
				"reference_doctype": doctype,
				"reference_name": name,
			}
		).insert(ignore_permissions=True)

	except criscostack.DuplicateEntryError:
		criscostack.db.rollback()

	else:
		criscostack.db.commit()

	return_unsubscribed_page(email, doctype, name)


def return_unsubscribed_page(email, doctype, name):
	criscostack.respond_as_web_page(
		_("Unsubscribed"),
		_("{0} has left the conversation in {1} {2}").format(email, _(doctype), name),
		indicator_color="green",
	)


def flush(from_test=False):
	"""flush email queue, every time: called from scheduler"""
	from criscostack.email.doctype.email_queue.email_queue import send_mail

	# To avoid running jobs inside unit tests
	if criscostack.are_emails_muted():
		msgprint(_("Emails are muted"))
		from_test = True

	if cint(criscostack.db.get_default("suspend_email_queue")) == 1:
		return

	for row in get_queue():
		try:
			criscostack.enqueue(
				method=send_mail,
				email_queue_name=row.name,
				now=from_test,
				job_id=f"email_queue_sendmail_{row.name}",
				queue="short",
				deduplicate=True,
			)
		except Exception:
			criscostack.get_doc("Email Queue", row.name).log_error()


def get_queue():
	return criscostack.db.sql(
		"""select
			name, sender
		from
			`tabEmail Queue`
		where
			(status='Not Sent' or status='Partially Sent') and
			(send_after is null or send_after < %(now)s)
		order
			by priority desc, creation asc
		limit 500""",
		{"now": now_datetime()},
		as_dict=True,
	)
