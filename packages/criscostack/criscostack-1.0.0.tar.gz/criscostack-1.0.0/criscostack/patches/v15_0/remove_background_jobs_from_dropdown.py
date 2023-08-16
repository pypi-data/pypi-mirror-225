import criscostack


def execute():
	item = criscostack.db.exists("Navbar Item", {"item_label": "Background Jobs"})
	if not item:
		return

	criscostack.delete_doc("Navbar Item", item)
