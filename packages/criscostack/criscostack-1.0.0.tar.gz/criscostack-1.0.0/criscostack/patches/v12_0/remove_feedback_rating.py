import criscostack


def execute():
	"""
	Deprecate Feedback Trigger and Rating. This feature was not customizable.
	Now can be achieved via custom Web Forms
	"""
	criscostack.delete_doc("DocType", "Feedback Trigger")
	criscostack.delete_doc("DocType", "Feedback Rating")
