import criscostack


def execute():
	criscostack.reload_doc("core", "doctype", "user")
	criscostack.db.sql(
		"""
		UPDATE `tabUser`
		SET `home_settings` = ''
		WHERE `user_type` = 'System User'
	"""
	)
