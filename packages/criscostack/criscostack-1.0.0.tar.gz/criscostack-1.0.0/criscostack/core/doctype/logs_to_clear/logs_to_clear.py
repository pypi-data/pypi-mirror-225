# Copyright (c) 2022, Crisco Technologies and contributors
# For license information, please see license.txt

# import criscostack
from criscostack.model.document import Document


class LogsToClear(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from criscostack.types import DF

		days: DF.Int
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		ref_doctype: DF.Link
	# end: auto-generated types
	pass
