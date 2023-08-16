import criscostack


def execute():
	Event = criscostack.qb.DocType("Event")
	query = (
		criscostack.qb.update(Event)
		.set(Event.event_type, "Private")
		.set(Event.status, "Cancelled")
		.where(Event.event_type == "Cancelled")
	)
	query.run()
