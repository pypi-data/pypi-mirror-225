import criscostack


def execute():
	table = criscostack.qb.DocType("Report")
	criscostack.qb.update(table).set(table.prepared_report, 0).where(table.disable_prepared_report == 1)
