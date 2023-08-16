import criscostack


def execute():
	criscostack.db.delete("DocType", {"name": "Feedback Request"})
