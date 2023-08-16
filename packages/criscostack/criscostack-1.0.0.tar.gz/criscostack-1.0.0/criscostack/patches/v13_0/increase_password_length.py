import criscostack


def execute():
	criscostack.db.change_column_type("__Auth", column="password", type="TEXT")
