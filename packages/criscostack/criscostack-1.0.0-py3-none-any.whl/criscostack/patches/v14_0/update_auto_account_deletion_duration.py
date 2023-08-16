import criscostack


def execute():
	days = criscostack.db.get_single_value("Website Settings", "auto_account_deletion")
	criscostack.db.set_single_value("Website Settings", "auto_account_deletion", days * 24)
