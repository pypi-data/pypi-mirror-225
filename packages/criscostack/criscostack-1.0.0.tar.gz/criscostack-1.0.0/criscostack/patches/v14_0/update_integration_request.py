import criscostack


def execute():
	doctype = "Integration Request"

	if not criscostack.db.has_column(doctype, "integration_type"):
		return

	criscostack.db.set_value(
		doctype,
		{"integration_type": "Remote", "integration_request_service": ("!=", "PayPal")},
		"is_remote_request",
		1,
	)
	criscostack.db.set_value(
		doctype,
		{"integration_type": "Subscription Notification"},
		"request_description",
		"Subscription Notification",
	)
