import criscostack


def execute():
	criscostack.delete_doc_if_exists("DocType", "Web View")
	criscostack.delete_doc_if_exists("DocType", "Web View Component")
	criscostack.delete_doc_if_exists("DocType", "CSS Class")
