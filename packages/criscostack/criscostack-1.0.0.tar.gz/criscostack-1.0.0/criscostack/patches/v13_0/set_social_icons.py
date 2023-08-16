import criscostack


def execute():
	providers = criscostack.get_all("Social Login Key")

	for provider in providers:
		doc = criscostack.get_doc("Social Login Key", provider)
		doc.set_icon()
		doc.save()
