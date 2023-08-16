import criscostack
from criscostack.utils.install import add_standard_navbar_items


def execute():
	# Add standard navbar items for Criscoerp in Navbar Settings
	criscostack.reload_doc("core", "doctype", "navbar_settings")
	criscostack.reload_doc("core", "doctype", "navbar_item")
	add_standard_navbar_items()
