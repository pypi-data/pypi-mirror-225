# Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import criscostack
import criscostack.www.list
from criscostack import _

no_cache = 1


def get_context(context):
	if criscostack.session.user == "Guest":
		criscostack.throw(_("You need to be logged in to access this page"), criscostack.PermissionError)

	context.current_user = criscostack.get_doc("User", criscostack.session.user)
	context.show_sidebar = True
