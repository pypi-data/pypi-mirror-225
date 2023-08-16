# Copyright (c) 2018, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import criscostack


def execute():
	criscostack.db.set_value("Currency", "USD", "smallest_currency_fraction_value", "0.01")
