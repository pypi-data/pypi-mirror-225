# Copyright (c) 2021, Crisco Technologies and Contributors
# License: MIT. See LICENSE
import criscostack
from criscostack.installer import update_site_config
from criscostack.tests.utils import CriscoTestCase


class TestUserType(CriscoTestCase):
	def setUp(self):
		create_role()

	def test_add_select_perm_doctypes(self):
		user_type = create_user_type("Test User Type")

		# select perms added for all link fields
		doc = criscostack.get_meta("Contact")
		link_fields = doc.get_link_fields()
		select_doctypes = criscostack.get_all(
			"User Select Document Type", {"parent": user_type.name}, pluck="document_type"
		)

		for entry in link_fields:
			self.assertTrue(entry.options in select_doctypes)

		# select perms added for all child table link fields
		link_fields = []
		for child_table in doc.get_table_fields():
			child_doc = criscostack.get_meta(child_table.options)
			link_fields.extend(child_doc.get_link_fields())

		for entry in link_fields:
			self.assertTrue(entry.options in select_doctypes)

	def tearDown(self):
		criscostack.db.rollback()


def create_user_type(user_type):
	if criscostack.db.exists("User Type", user_type):
		criscostack.delete_doc("User Type", user_type)

	user_type_limit = {criscostack.scrub(user_type): 1}
	update_site_config("user_type_doctype_limit", user_type_limit)

	doc = criscostack.get_doc(
		{
			"doctype": "User Type",
			"name": user_type,
			"role": "_Test User Type",
			"user_id_field": "user",
			"apply_user_permission_on": "User",
		}
	)

	doc.append("user_doctypes", {"document_type": "Contact", "read": 1, "write": 1})

	return doc.insert()


def create_role():
	if not criscostack.db.exists("Role", "_Test User Type"):
		criscostack.get_doc(
			{"doctype": "Role", "role_name": "_Test User Type", "desk_access": 1, "is_custom": 1}
		).insert()
