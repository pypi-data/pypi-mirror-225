import criscostack
from criscostack.desk.page.setup_wizard.install_fixtures import update_global_search_doctypes


def execute():
	criscostack.reload_doc("desk", "doctype", "global_search_doctype")
	criscostack.reload_doc("desk", "doctype", "global_search_settings")
	update_global_search_doctypes()
