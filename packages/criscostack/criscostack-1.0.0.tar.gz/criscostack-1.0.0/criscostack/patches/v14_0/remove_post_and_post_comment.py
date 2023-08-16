import criscostack


def execute():
	criscostack.delete_doc_if_exists("DocType", "Post")
	criscostack.delete_doc_if_exists("DocType", "Post Comment")
