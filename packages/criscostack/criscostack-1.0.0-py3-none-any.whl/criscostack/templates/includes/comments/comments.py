# Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE
import re

import criscostack
from criscostack import _, scrub
from criscostack.rate_limiter import rate_limit
from criscostack.utils.html_utils import clean_html
from criscostack.website.doctype.blog_settings.blog_settings import get_comment_limit
from criscostack.website.utils import clear_cache

URLS_COMMENT_PATTERN = re.compile(
	r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", re.IGNORECASE
)
EMAIL_PATTERN = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", re.IGNORECASE)


@criscostack.whitelist(allow_guest=True)
@rate_limit(key="reference_name", limit=get_comment_limit, seconds=60 * 60)
def add_comment(comment, comment_email, comment_by, reference_doctype, reference_name, route):
	if criscostack.session.user == "Guest":
		if reference_doctype not in ("Blog Post", "Web Page"):
			return

		if reference_doctype == "Blog Post" and not criscostack.db.get_single_value(
			"Blog Settings", "allow_guest_to_comment"
		):
			return

		if criscostack.db.exists("User", comment_email):
			criscostack.throw(_("Please login to post a comment."))

	if not comment.strip():
		criscostack.msgprint(_("The comment cannot be empty"))
		return False

	if URLS_COMMENT_PATTERN.search(comment) or EMAIL_PATTERN.search(comment):
		criscostack.msgprint(_("Comments cannot have links or email addresses"))
		return False

	doc = criscostack.get_doc(reference_doctype, reference_name)
	comment = doc.add_comment(
		text=clean_html(comment), comment_email=comment_email, comment_by=comment_by
	)

	comment.db_set("published", 1)

	# since comments are embedded in the page, clear the web cache
	if route:
		clear_cache(route)

	if doc.get("route"):
		url = f"{criscostack.utils.get_request_site_address()}/{doc.route}#{comment.name}"
	else:
		url = f"{criscostack.utils.get_request_site_address()}/app/{scrub(doc.doctype)}/{doc.name}#comment-{comment.name}"

	content = comment.content + "<p><a href='{}' style='font-size: 80%'>{}</a></p>".format(
		url, _("View Comment")
	)

	if doc.doctype != "Blog Post" or doc.enable_email_notification:
		# notify creator
		creator_email = criscostack.db.get_value("User", doc.owner, "email") or doc.owner
		subject = _("New Comment on {0}: {1}").format(doc.doctype, doc.get_title())

		criscostack.sendmail(
			recipients=creator_email,
			subject=subject,
			message=content,
			reference_doctype=doc.doctype,
			reference_name=doc.name,
		)

	# revert with template if all clear (no backlinks)
	template = criscostack.get_template("templates/includes/comments/comment.html")
	return template.render({"comment": comment.as_dict()})
