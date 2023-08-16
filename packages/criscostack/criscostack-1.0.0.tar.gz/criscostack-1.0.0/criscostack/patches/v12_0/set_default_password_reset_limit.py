# Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import criscostack


def execute():
	criscostack.reload_doc("core", "doctype", "system_settings", force=1)
	criscostack.db.set_single_value("System Settings", "password_reset_limit", 3)
