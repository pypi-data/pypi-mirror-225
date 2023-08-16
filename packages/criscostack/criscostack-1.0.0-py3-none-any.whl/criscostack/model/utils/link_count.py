# Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

from collections import defaultdict

import criscostack

ignore_doctypes = ("DocType", "Print Format", "Role", "Module Def", "Communication", "ToDo")


def notify_link_count(doctype, name):
	"""updates link count for given document"""
	if not hasattr(criscostack.local, "_link_count"):
		criscostack.local._link_count = defaultdict(int)
		criscostack.db.after_commit.add(flush_local_link_count)

	criscostack.local._link_count[(doctype, name)] += 1


def flush_local_link_count():
	"""flush from local before ending request"""
	new_links = getattr(criscostack.local, "_link_count", None)
	if not new_links:
		return

	link_count = criscostack.cache.get_value("_link_count") or {}

	for key, value in new_links.items():
		if key in link_count:
			link_count[key] += value
		else:
			link_count[key] = value

	criscostack.cache.set_value("_link_count", link_count)
	new_links.clear()


def update_link_count():
	"""increment link count in the `idx` column for the given document"""
	link_count = criscostack.cache.get_value("_link_count")

	if link_count:
		for (doctype, name), count in link_count.items():
			if doctype not in ignore_doctypes:
				try:
					table = criscostack.qb.DocType(doctype)
					criscostack.qb.update(table).set(table.idx, table.idx + count).where(table.name == name).run()
					criscostack.db.commit()
				except Exception as e:
					if not criscostack.db.is_table_missing(e):  # table not found, single
						raise e
	# reset the count
	criscostack.cache.delete_value("_link_count")
