# Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import criscostack


def sendmail_to_system_managers(subject, content):
	criscostack.sendmail(recipients=get_system_managers(), subject=subject, content=content)


@criscostack.whitelist()
def get_contact_list(txt, page_length=20) -> list[dict]:
	"""Return email ids for a multiselect field."""
	from criscostack.contacts.doctype.contact.contact import get_full_name

	if cached_contacts := get_cached_contacts(txt):
		return cached_contacts[:page_length]

	fields = ["first_name", "middle_name", "last_name", "company_name"]
	contacts = criscostack.get_list(
		"Contact",
		fields=fields + ["`tabContact Email`.email_id"],
		filters=[
			["Contact Email", "email_id", "is", "set"],
		],
		or_filters=[[field, "like", f"%{txt}%"] for field in fields]
		+ [["Contact Email", "email_id", "like", f"%{txt}%"]],
		limit_page_length=page_length,
	)

	# The multiselect field will store the `label` as the selected value.
	# The `value` is just used as a unique key to distinguish between the options.
	# https://github.com/criscostack/criscostack/blob/6c6a89bcdd9454060a1333e23b855d0505c9ebc2/criscostack/public/js/criscostack/form/controls/autocomplete.js#L29-L35
	result = [
		criscostack._dict(
			value=d.email_id,
			label=d.email_id,
			description=get_full_name(d.first_name, d.middle_name, d.last_name, d.company_name),
		)
		for d in contacts
	]

	update_contact_cache(result)

	return result


def get_system_managers():
	return criscostack.db.sql_list(
		"""select parent FROM `tabHas Role`
		WHERE role='System Manager'
		AND parent!='Administrator'
		AND parent IN (SELECT email FROM tabUser WHERE enabled=1)"""
	)


@criscostack.whitelist()
def relink(name, reference_doctype=None, reference_name=None):
	criscostack.db.sql(
		"""update
			`tabCommunication`
		set
			reference_doctype = %s,
			reference_name = %s,
			status = "Linked"
		where
			communication_type = "Communication" and
			name = %s""",
		(reference_doctype, reference_name, name),
	)


@criscostack.whitelist()
@criscostack.validate_and_sanitize_search_inputs
def get_communication_doctype(doctype, txt, searchfield, start, page_len, filters):
	user_perms = criscostack.utils.user.UserPermissions(criscostack.session.user)
	user_perms.build_permissions()
	can_read = user_perms.can_read
	from criscostack.modules import load_doctype_module

	com_doctypes = []
	if len(txt) < 2:

		for name in criscostack.get_hooks("communication_doctypes"):
			try:
				module = load_doctype_module(name, suffix="_dashboard")
				if hasattr(module, "get_data"):
					for i in module.get_data()["transactions"]:
						com_doctypes += i["items"]
			except ImportError:
				pass
	else:
		com_doctypes = [
			d[0] for d in criscostack.db.get_values("DocType", {"issingle": 0, "istable": 0, "hide_toolbar": 0})
		]

	out = []
	for dt in com_doctypes:
		if txt.lower().replace("%", "") in dt.lower() and dt in can_read:
			out.append([dt])
	return out


def get_cached_contacts(txt):
	contacts = criscostack.cache.hget("contacts", criscostack.session.user) or []

	if not contacts:
		return

	if not txt:
		return contacts

	match = [
		d
		for d in contacts
		if (d.value and ((d.value and txt in d.value) or (d.description and txt in d.description)))
	]
	return match


def update_contact_cache(contacts):
	cached_contacts = criscostack.cache.hget("contacts", criscostack.session.user) or []

	uncached_contacts = [d for d in contacts if d not in cached_contacts]
	cached_contacts.extend(uncached_contacts)

	criscostack.cache.hset("contacts", criscostack.session.user, cached_contacts)
