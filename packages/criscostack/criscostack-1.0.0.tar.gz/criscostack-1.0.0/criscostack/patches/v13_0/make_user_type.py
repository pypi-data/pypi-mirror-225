import criscostack
from criscostack.utils.install import create_user_type


def execute():
	criscostack.reload_doc("core", "doctype", "role")
	criscostack.reload_doc("core", "doctype", "user_document_type")
	criscostack.reload_doc("core", "doctype", "user_type_module")
	criscostack.reload_doc("core", "doctype", "user_select_document_type")
	criscostack.reload_doc("core", "doctype", "user_type")

	create_user_type()
