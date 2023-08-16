import criscostack
from criscostack.model.utils.rename_field import rename_field


def execute():
	if not criscostack.db.table_exists("Dashboard Chart"):
		return

	criscostack.reload_doc("desk", "doctype", "dashboard_chart")

	if criscostack.db.has_column("Dashboard Chart", "is_custom"):
		rename_field("Dashboard Chart", "is_custom", "use_report_chart")
