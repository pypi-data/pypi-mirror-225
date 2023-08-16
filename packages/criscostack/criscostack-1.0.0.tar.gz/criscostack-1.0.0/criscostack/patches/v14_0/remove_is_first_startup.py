import criscostack


def execute():
	singles = criscostack.qb.Table("tabSingles")
	criscostack.qb.from_(singles).delete().where(
		(singles.doctype == "System Settings") & (singles.field == "is_first_startup")
	).run()
