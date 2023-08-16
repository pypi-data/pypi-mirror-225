import criscostack


def execute():
	# if current = 0, simply delete the key as it'll be recreated on first entry
	criscostack.db.delete("Series", {"current": 0})

	duplicate_keys = criscostack.db.sql(
		"""
		SELECT name, max(current) as current
		from
			`tabSeries`
		group by
			name
		having count(name) > 1
	""",
		as_dict=True,
	)

	for row in duplicate_keys:
		criscostack.db.delete("Series", {"name": row.name})
		if row.current:
			criscostack.db.sql("insert into `tabSeries`(`name`, `current`) values (%(name)s, %(current)s)", row)
	criscostack.db.commit()

	criscostack.db.sql("ALTER table `tabSeries` ADD PRIMARY KEY IF NOT EXISTS (name)")
