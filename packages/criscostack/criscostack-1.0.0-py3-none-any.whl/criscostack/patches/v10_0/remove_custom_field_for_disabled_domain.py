import criscostack


def execute():
	criscostack.reload_doc("core", "doctype", "domain")
	criscostack.reload_doc("core", "doctype", "has_domain")
	active_domains = criscostack.get_active_domains()
	all_domains = criscostack.get_all("Domain")

	for d in all_domains:
		if d.name not in active_domains:
			inactive_domain = criscostack.get_doc("Domain", d.name)
			inactive_domain.setup_data()
			inactive_domain.remove_custom_field()
