# Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import criscostack
from criscostack import _
from criscostack.rate_limiter import rate_limit
from criscostack.website.doctype.blog_settings.blog_settings import get_like_limit
from criscostack.website.utils import clear_cache


@criscostack.whitelist(allow_guest=True)
@rate_limit(key="reference_name", limit=get_like_limit, seconds=60 * 60)
def like(reference_doctype, reference_name, like, route=""):
	like = criscostack.parse_json(like)
	ref_doc = criscostack.get_doc(reference_doctype, reference_name)
	if ref_doc.disable_likes == 1:
		return

	if like:
		liked = add_like(reference_doctype, reference_name)
	else:
		liked = delete_like(reference_doctype, reference_name)

	# since likes are embedded in the page, clear the web cache
	if route:
		clear_cache(route)

	if like and ref_doc.enable_email_notification:
		ref_doc_title = ref_doc.get_title()
		subject = _("Like on {0}: {1}").format(reference_doctype, ref_doc_title)
		content = _("You have received a ❤️ like on your blog post")
		message = f"<p>{content} <b>{ref_doc_title}</b></p>"
		message = message + "<p><a href='{}/{}#likes' style='font-size: 80%'>{}</a></p>".format(
			criscostack.utils.get_request_site_address(), ref_doc.route, _("View Blog Post")
		)

		# notify creator
		criscostack.sendmail(
			recipients=criscostack.db.get_value("User", ref_doc.owner, "email") or ref_doc.owner,
			subject=subject,
			message=message,
			reference_doctype=ref_doc.doctype,
			reference_name=ref_doc.name,
		)

	return liked


def add_like(reference_doctype, reference_name):
	user = criscostack.session.user

	like = criscostack.new_doc("Comment")
	like.comment_type = "Like"
	like.comment_email = user
	like.reference_doctype = reference_doctype
	like.reference_name = reference_name
	like.content = "Liked by: " + user
	if user == "Guest":
		like.ip_address = criscostack.local.request_ip
	like.save(ignore_permissions=True)
	return True


def delete_like(reference_doctype, reference_name):
	user = criscostack.session.user

	filters = {
		"comment_type": "Like",
		"comment_email": user,
		"reference_doctype": reference_doctype,
		"reference_name": reference_name,
	}

	if user == "Guest":
		filters["ip_address"] = criscostack.local.request_ip

	criscostack.db.delete("Comment", filters)
	return False
