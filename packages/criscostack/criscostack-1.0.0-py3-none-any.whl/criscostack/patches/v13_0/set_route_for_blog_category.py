import criscostack


def execute():
	categories = criscostack.get_list("Blog Category")
	for category in categories:
		doc = criscostack.get_doc("Blog Category", category["name"])
		doc.set_route()
		doc.save()
