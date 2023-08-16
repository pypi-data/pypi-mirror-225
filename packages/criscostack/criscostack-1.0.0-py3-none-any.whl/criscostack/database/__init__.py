# Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

# Database Module
# --------------------

from criscostack.database.database import savepoint


def setup_database(force, source_sql=None, verbose=None, no_mariadb_socket=False):
	import criscostack

	if criscostack.conf.db_type == "postgres":
		import criscostack.database.postgres.setup_db

		return criscostack.database.postgres.setup_db.setup_database(force, source_sql, verbose)
	else:
		import criscostack.database.mariadb.setup_db

		return criscostack.database.mariadb.setup_db.setup_database(
			force, source_sql, verbose, no_mariadb_socket=no_mariadb_socket
		)


def drop_user_and_database(db_name, root_login=None, root_password=None):
	import criscostack

	if criscostack.conf.db_type == "postgres":
		import criscostack.database.postgres.setup_db

		return criscostack.database.postgres.setup_db.drop_user_and_database(
			db_name, root_login, root_password
		)
	else:
		import criscostack.database.mariadb.setup_db

		return criscostack.database.mariadb.setup_db.drop_user_and_database(
			db_name, root_login, root_password
		)


def get_db(host=None, user=None, password=None, port=None):
	import criscostack

	if criscostack.conf.db_type == "postgres":
		import criscostack.database.postgres.database

		return criscostack.database.postgres.database.PostgresDatabase(host, user, password, port=port)
	else:
		import criscostack.database.mariadb.database

		return criscostack.database.mariadb.database.MariaDBDatabase(host, user, password, port=port)
