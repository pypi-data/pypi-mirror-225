import criscostack


def execute():
	if criscostack.db.table_exists("Prepared Report"):
		criscostack.reload_doc("core", "doctype", "prepared_report")
		prepared_reports = criscostack.get_all("Prepared Report")
		for report in prepared_reports:
			criscostack.delete_doc("Prepared Report", report.name)
