import criscostack
from criscostack.desk.utils import slug


def execute():
	for doctype in criscostack.get_all("DocType", ["name", "route"], dict(istable=0)):
		if not doctype.route:
			criscostack.db.set_value("DocType", doctype.name, "route", slug(doctype.name), update_modified=False)
