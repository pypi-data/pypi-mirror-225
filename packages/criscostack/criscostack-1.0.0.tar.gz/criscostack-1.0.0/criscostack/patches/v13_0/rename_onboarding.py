# Copyright (c) 2020, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import criscostack


def execute():
	if criscostack.db.exists("DocType", "Onboarding"):
		criscostack.rename_doc("DocType", "Onboarding", "Module Onboarding", ignore_if_exists=True)
