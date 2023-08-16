# Copyright (c) 2020, Crisco Technologies and contributors
# License: MIT. See LICENSE

# import criscostack
from criscostack.model.document import Document


class DocumentNamingRuleCondition(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from criscostack.types import DF

		condition: DF.Literal["=", "!=", ">", "<", ">=", "<="]
		field: DF.Literal
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		value: DF.Data
	# end: auto-generated types
	pass
