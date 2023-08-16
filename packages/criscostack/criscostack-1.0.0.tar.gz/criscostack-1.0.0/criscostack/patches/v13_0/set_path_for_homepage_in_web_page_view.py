import criscostack


def execute():
	criscostack.reload_doc("website", "doctype", "web_page_view", force=True)
	criscostack.db.sql("""UPDATE `tabWeb Page View` set path='/' where path=''""")
