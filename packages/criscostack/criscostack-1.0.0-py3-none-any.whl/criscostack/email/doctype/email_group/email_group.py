# Copyright (c) 2015, Crisco Technologies and contributors
# License: MIT. See LICENSE

import criscostack
from criscostack import _
from criscostack.model.document import Document
from criscostack.utils import parse_addr, validate_email_address


class EmailGroup(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from criscostack.types import DF

		confirmation_email_template: DF.Link | None
		title: DF.Data
		total_subscribers: DF.Int
		welcome_email_template: DF.Link | None
	# end: auto-generated types
	def onload(self):
		singles = [d.name for d in criscostack.get_all("DocType", "name", {"issingle": 1})]
		self.get("__onload").import_types = [
			{"value": d.parent, "label": f"{d.parent} ({d.label})"}
			for d in criscostack.get_all("DocField", ("parent", "label"), {"options": "Email"})
			if d.parent not in singles
		]

	def import_from(self, doctype):
		"""Extract Email Addresses from given doctype and add them to the current list"""
		meta = criscostack.get_meta(doctype)
		email_field = [
			d.fieldname
			for d in meta.fields
			if d.fieldtype in ("Data", "Small Text", "Text", "Code") and d.options == "Email"
		][0]
		unsubscribed_field = "unsubscribed" if meta.get_field("unsubscribed") else None
		added = 0

		for user in criscostack.get_all(doctype, [email_field, unsubscribed_field or "name"]):
			try:
				email = parse_addr(user.get(email_field))[1] if user.get(email_field) else None
				if email:
					criscostack.get_doc(
						{
							"doctype": "Email Group Member",
							"email_group": self.name,
							"email": email,
							"unsubscribed": user.get(unsubscribed_field) if unsubscribed_field else 0,
						}
					).insert(ignore_permissions=True)

					added += 1
			except criscostack.UniqueValidationError:
				pass

		criscostack.msgprint(_("{0} subscribers added").format(added))

		return self.update_total_subscribers()

	def update_total_subscribers(self):
		self.total_subscribers = self.get_total_subscribers()
		self.db_update()
		return self.total_subscribers

	def get_total_subscribers(self):
		return criscostack.db.sql(
			"""select count(*) from `tabEmail Group Member`
			where email_group=%s""",
			self.name,
		)[0][0]

	def on_trash(self):
		for d in criscostack.get_all("Email Group Member", "name", {"email_group": self.name}):
			criscostack.delete_doc("Email Group Member", d.name)


@criscostack.whitelist()
def import_from(name, doctype):
	nlist = criscostack.get_doc("Email Group", name)
	if nlist.has_permission("write"):
		return nlist.import_from(doctype)


@criscostack.whitelist()
def add_subscribers(name, email_list):
	if not isinstance(email_list, (list, tuple)):
		email_list = email_list.replace(",", "\n").split("\n")

	template = criscostack.db.get_value("Email Group", name, "welcome_email_template")
	welcome_email = criscostack.get_doc("Email Template", template) if template else None

	count = 0
	for email in email_list:
		email = email.strip()
		parsed_email = validate_email_address(email, False)

		if parsed_email:
			if not criscostack.db.get_value("Email Group Member", {"email_group": name, "email": parsed_email}):
				criscostack.get_doc(
					{"doctype": "Email Group Member", "email_group": name, "email": parsed_email}
				).insert(ignore_permissions=criscostack.flags.ignore_permissions)

				send_welcome_email(welcome_email, parsed_email, name)

				count += 1
			else:
				pass
		else:
			criscostack.msgprint(_("{0} is not a valid Email Address").format(email))

	criscostack.msgprint(_("{0} subscribers added").format(count))

	return criscostack.get_doc("Email Group", name).update_total_subscribers()


def send_welcome_email(welcome_email, email, email_group):
	"""Send welcome email for the subscribers of a given email group."""
	if not welcome_email:
		return

	args = dict(email=email, email_group=email_group)
	email_message = welcome_email.response or welcome_email.response_html
	message = criscostack.render_template(email_message, args)
	criscostack.sendmail(email, subject=welcome_email.subject, message=message)
