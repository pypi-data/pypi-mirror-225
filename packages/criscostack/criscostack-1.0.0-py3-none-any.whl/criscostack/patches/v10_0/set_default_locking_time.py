# Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import criscostack


def execute():
	criscostack.reload_doc("core", "doctype", "system_settings")
	criscostack.db.set_single_value("System Settings", "allow_login_after_fail", 60)
