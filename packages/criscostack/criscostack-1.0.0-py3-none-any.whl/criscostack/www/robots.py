import criscostack

base_template_path = "www/robots.txt"


def get_context(context):
	robots_txt = (
		criscostack.db.get_single_value("Website Settings", "robots_txt")
		or (criscostack.local.conf.robots_txt and criscostack.read_file(criscostack.local.conf.robots_txt))
		or ""
	)

	return {"robots_txt": robots_txt}
