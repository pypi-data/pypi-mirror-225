# Copyright (c) 2020, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import criscostack


def execute():
	criscostack.reload_doc("website", "doctype", "web_page_block")
	# remove unused templates
	criscostack.delete_doc("Web Template", "Navbar with Links on Right", force=1)
	criscostack.delete_doc("Web Template", "Footer Horizontal", force=1)
