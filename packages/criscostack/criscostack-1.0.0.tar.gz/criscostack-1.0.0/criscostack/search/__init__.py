# Copyright (c) 2020, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import criscostack
from criscostack.search.full_text_search import FullTextSearch
from criscostack.search.website_search import WebsiteSearch
from criscostack.utils import cint


@criscostack.whitelist(allow_guest=True)
def web_search(query, scope=None, limit=20):
	limit = cint(limit)
	ws = WebsiteSearch(index_name="web_routes")
	return ws.search(query, scope, limit)
