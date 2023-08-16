# Copyright (c) 2020, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import criscostack


def execute():
	criscostack.delete_doc("DocType", "Package Publish Tool", ignore_missing=True)
	criscostack.delete_doc("DocType", "Package Document Type", ignore_missing=True)
	criscostack.delete_doc("DocType", "Package Publish Target", ignore_missing=True)
