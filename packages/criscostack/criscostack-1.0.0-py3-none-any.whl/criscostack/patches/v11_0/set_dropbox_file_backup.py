import criscostack
from criscostack.utils import cint


def execute():
	criscostack.reload_doctype("Dropbox Settings")
	check_dropbox_enabled = cint(criscostack.db.get_single_value("Dropbox Settings", "enabled"))
	if check_dropbox_enabled == 1:
		criscostack.db.set_single_value("Dropbox Settings", "file_backup", 1)
