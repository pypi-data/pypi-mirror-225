# Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import criscostack

sitemap = 1


def get_context(context):
	context.doc = criscostack.get_cached_doc("About Us Settings")

	return context
