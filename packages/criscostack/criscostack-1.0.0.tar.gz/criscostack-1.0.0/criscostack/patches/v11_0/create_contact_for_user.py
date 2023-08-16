import re

import criscostack
from criscostack.core.doctype.user.user import create_contact


def execute():
	"""Create Contact for each User if not present"""
	criscostack.reload_doc("integrations", "doctype", "google_contacts")
	criscostack.reload_doc("contacts", "doctype", "contact")
	criscostack.reload_doc("core", "doctype", "dynamic_link")

	contact_meta = criscostack.get_meta("Contact")
	if contact_meta.has_field("phone_nos") and contact_meta.has_field("email_ids"):
		criscostack.reload_doc("contacts", "doctype", "contact_phone")
		criscostack.reload_doc("contacts", "doctype", "contact_email")

	users = criscostack.get_all("User", filters={"name": ("not in", "Administrator, Guest")}, fields=["*"])
	for user in users:
		if criscostack.db.exists("Contact", {"email_id": user.email}) or criscostack.db.exists(
			"Contact Email", {"email_id": user.email}
		):
			continue
		if user.first_name:
			user.first_name = re.sub("[<>]+", "", criscostack.safe_decode(user.first_name))
		if user.last_name:
			user.last_name = re.sub("[<>]+", "", criscostack.safe_decode(user.last_name))
		create_contact(user, ignore_links=True, ignore_mandatory=True)
