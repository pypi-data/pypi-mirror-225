import criscostack


def execute():
	communications = criscostack.db.sql(
		"""
		SELECT
			`tabCommunication`.name, `tabCommunication`.creation, `tabCommunication`.modified,
			`tabCommunication`.modified_by,`tabCommunication`.timeline_doctype, `tabCommunication`.timeline_name,
			`tabCommunication`.link_doctype, `tabCommunication`.link_name
		FROM `tabCommunication`
		WHERE `tabCommunication`.communication_medium='Email'
	""",
		as_dict=True,
	)

	name = 1000000000
	values = []

	for count, communication in enumerate(communications):
		counter = 1
		if communication.timeline_doctype and communication.timeline_name:
			name += 1
			values.append(
				"""({}, "{}", "timeline_links", "Communication", "{}", "{}", "{}", "{}", "{}", "{}")""".format(
					counter,
					str(name),
					criscostack.db.escape(communication.name),
					criscostack.db.escape(communication.timeline_doctype),
					criscostack.db.escape(communication.timeline_name),
					communication.creation,
					communication.modified,
					communication.modified_by,
				)
			)
			counter += 1
		if communication.link_doctype and communication.link_name:
			name += 1
			values.append(
				"""({}, "{}", "timeline_links", "Communication", "{}", "{}", "{}", "{}", "{}", "{}")""".format(
					counter,
					str(name),
					criscostack.db.escape(communication.name),
					criscostack.db.escape(communication.link_doctype),
					criscostack.db.escape(communication.link_name),
					communication.creation,
					communication.modified,
					communication.modified_by,
				)
			)

		if values and (count % 10000 == 0 or count == len(communications) - 1):
			criscostack.db.sql(
				"""
				INSERT INTO `tabCommunication Link`
					(`idx`, `name`, `parentfield`, `parenttype`, `parent`, `link_doctype`, `link_name`, `creation`,
					`modified`, `modified_by`)
				VALUES {}
			""".format(
					", ".join([d for d in values])
				)
			)

			values = []

	criscostack.db.add_index("Communication Link", ["link_doctype", "link_name"])
