import criscostack
from criscostack.model.naming import append_number_if_name_exists
from criscostack.utils.dashboard import get_dashboards_with_link


def execute():
	if (
		not criscostack.db.table_exists("Dashboard Chart")
		or not criscostack.db.table_exists("Number Card")
		or not criscostack.db.table_exists("Dashboard")
	):
		return

	criscostack.reload_doc("desk", "doctype", "dashboard_chart")
	criscostack.reload_doc("desk", "doctype", "number_card")
	criscostack.reload_doc("desk", "doctype", "dashboard")

	modified_charts = get_modified_docs("Dashboard Chart")
	modified_cards = get_modified_docs("Number Card")
	modified_dashboards = [doc.name for doc in get_modified_docs("Dashboard")]

	for chart in modified_charts:
		modified_dashboards += get_dashboards_with_link(chart.name, "Dashboard Chart")
		rename_modified_doc(chart.name, "Dashboard Chart")

	for card in modified_cards:
		modified_dashboards += get_dashboards_with_link(card.name, "Number Card")
		rename_modified_doc(card.name, "Number Card")

	modified_dashboards = list(set(modified_dashboards))

	for dashboard in modified_dashboards:
		rename_modified_doc(dashboard, "Dashboard")


def get_modified_docs(doctype):
	return criscostack.get_all(
		doctype, filters={"owner": "Administrator", "modified_by": ["!=", "Administrator"]}
	)


def rename_modified_doc(docname, doctype):
	new_name = docname + " Custom"
	try:
		criscostack.rename_doc(doctype, docname, new_name)
	except criscostack.ValidationError:
		new_name = append_number_if_name_exists(doctype, new_name)
		criscostack.rename_doc(doctype, docname, new_name)
