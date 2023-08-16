import criscostack


def execute():
	criscostack.reload_doctype("Letter Head")

	# source of all existing letter heads must be HTML
	criscostack.db.sql("update `tabLetter Head` set source = 'HTML'")
