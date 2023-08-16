import os

import criscostack


def setup_database(force, source_sql=None, verbose=False):
	root_conn = get_root_connection(criscostack.flags.root_login, criscostack.flags.root_password)
	root_conn.commit()
	root_conn.sql("end")
	root_conn.sql(f"DROP DATABASE IF EXISTS `{criscostack.conf.db_name}`")
	root_conn.sql(f"DROP USER IF EXISTS {criscostack.conf.db_name}")
	root_conn.sql(f"CREATE DATABASE `{criscostack.conf.db_name}`")
	root_conn.sql(f"CREATE user {criscostack.conf.db_name} password '{criscostack.conf.db_password}'")
	root_conn.sql("GRANT ALL PRIVILEGES ON DATABASE `{0}` TO {0}".format(criscostack.conf.db_name))
	root_conn.close()

	bootstrap_database(criscostack.conf.db_name, verbose, source_sql=source_sql)
	criscostack.connect()


def bootstrap_database(db_name, verbose, source_sql=None):
	criscostack.connect(db_name=db_name)
	import_db_from_sql(source_sql, verbose)
	criscostack.connect(db_name=db_name)

	if "tabDefaultValue" not in criscostack.db.get_tables():
		import sys

		from click import secho

		secho(
			"Table 'tabDefaultValue' missing in the restored site. "
			"This may be due to incorrect permissions or the result of a restore from a bad backup file. "
			"Database not installed correctly.",
			fg="red",
		)
		sys.exit(1)


def import_db_from_sql(source_sql=None, verbose=False):
	from shutil import which
	from subprocess import PIPE, run

	# we can't pass psql password in arguments in postgresql as mysql. So
	# set password connection parameter in environment variable
	subprocess_env = os.environ.copy()
	subprocess_env["PGPASSWORD"] = str(criscostack.conf.db_password)

	# bootstrap db
	if not source_sql:
		source_sql = os.path.join(os.path.dirname(__file__), "framework_postgres.sql")

	pv = which("pv")

	_command = (
		f"psql {criscostack.conf.db_name} "
		f"-h {criscostack.conf.db_host} -p {str(criscostack.conf.db_port)} "
		f"-U {criscostack.conf.db_name}"
	)

	if pv:
		command = f"{pv} {source_sql} | " + _command
	else:
		command = _command + f" -f {source_sql}"

	print("Restoring Database file...")
	if verbose:
		print(command)

	restore_proc = run(command, env=subprocess_env, shell=True, stdout=PIPE)

	if verbose:
		print(
			f"\nSTDOUT by psql:\n{restore_proc.stdout.decode()}\nImported from Database File: {source_sql}"
		)


def get_root_connection(root_login=None, root_password=None):
	if not criscostack.local.flags.root_connection:
		if not root_login:
			root_login = criscostack.conf.get("root_login") or None

		if not root_login:
			root_login = input("Enter postgres super user: ")

		if not root_password:
			root_password = criscostack.conf.get("root_password") or None

		if not root_password:
			from getpass import getpass

			root_password = getpass("Postgres super user password: ")

		criscostack.local.flags.root_connection = criscostack.database.get_db(
			host=criscostack.conf.db_host,
			port=criscostack.conf.db_port,
			user=root_login,
			password=root_password,
		)

	return criscostack.local.flags.root_connection


def drop_user_and_database(db_name, root_login, root_password):
	root_conn = get_root_connection(
		criscostack.flags.root_login or root_login, criscostack.flags.root_password or root_password
	)
	root_conn.commit()
	root_conn.sql(
		"SELECT pg_terminate_backend (pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = %s",
		(db_name,),
	)
	root_conn.sql("end")
	root_conn.sql(f"DROP DATABASE IF EXISTS {db_name}")
	root_conn.sql(f"DROP USER IF EXISTS {db_name}")
