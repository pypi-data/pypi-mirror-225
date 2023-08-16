# Copyright (c) 2022, Crisco Technologies and contributors
# For license information, please see license.txt

# import criscostack
from criscostack.model.document import Document


class WebFormListColumn(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from criscostack.types import DF

		fieldname: DF.Literal
		fieldtype: DF.Data | None
		label: DF.Data | None
		name: DF.Int | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
	# end: auto-generated types
	pass
