# Copyright (c) 2022, Crisco Technologies and contributors
# License: MIT. See LICENSE

import criscostack
from criscostack.deferred_insert import deferred_insert as _deferred_insert
from criscostack.model.document import Document


class RouteHistory(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from criscostack.types import DF

		route: DF.Data | None
		user: DF.Link | None
	# end: auto-generated types
	@staticmethod
	def clear_old_logs(days=30):
		from criscostack.query_builder import Interval
		from criscostack.query_builder.functions import Now

		table = criscostack.qb.DocType("Route History")
		criscostack.db.delete(table, filters=(table.modified < (Now() - Interval(days=days))))


@criscostack.whitelist()
def deferred_insert(routes):
	routes = [
		{
			"user": criscostack.session.user,
			"route": route.get("route"),
			"creation": route.get("creation"),
		}
		for route in criscostack.parse_json(routes)
	]

	_deferred_insert("Route History", routes)


@criscostack.whitelist()
def frequently_visited_links():
	return criscostack.get_all(
		"Route History",
		fields=["route", "count(name) as count"],
		filters={"user": criscostack.session.user},
		group_by="route",
		order_by="count desc",
		limit=5,
	)
