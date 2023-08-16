import criscostack


def execute():
	for name in ("desktop", "space"):
		criscostack.delete_doc("Page", name)
