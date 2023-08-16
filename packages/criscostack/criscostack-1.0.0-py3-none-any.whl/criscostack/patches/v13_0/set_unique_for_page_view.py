import criscostack


def execute():
	criscostack.reload_doc("website", "doctype", "web_page_view", force=True)
	site_url = criscostack.utils.get_site_url(criscostack.local.site)
	criscostack.db.sql(f"""UPDATE `tabWeb Page View` set is_unique=1 where referrer LIKE '%{site_url}%'""")
