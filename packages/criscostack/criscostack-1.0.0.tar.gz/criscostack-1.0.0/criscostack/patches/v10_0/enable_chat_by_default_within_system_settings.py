import criscostack


def execute():
	criscostack.reload_doctype("System Settings")
	doc = criscostack.get_single("System Settings")
	doc.enable_chat = 1

	# Changes prescribed by Nabin Hait (nabin@criscostack.io)
	doc.flags.ignore_mandatory = True
	doc.flags.ignore_permissions = True

	doc.save()
