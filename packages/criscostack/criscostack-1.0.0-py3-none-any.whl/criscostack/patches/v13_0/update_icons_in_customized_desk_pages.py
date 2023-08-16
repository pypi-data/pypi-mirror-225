import criscostack


def execute():
	if not criscostack.db.exists("Desk Page"):
		return

	pages = criscostack.get_all(
		"Desk Page", filters={"is_standard": False}, fields=["name", "extends", "for_user"]
	)
	default_icon = {}
	for page in pages:
		if page.extends and page.for_user:
			if not default_icon.get(page.extends):
				default_icon[page.extends] = criscostack.db.get_value("Desk Page", page.extends, "icon")

			icon = default_icon.get(page.extends)
			criscostack.db.set_value("Desk Page", page.name, "icon", icon)
