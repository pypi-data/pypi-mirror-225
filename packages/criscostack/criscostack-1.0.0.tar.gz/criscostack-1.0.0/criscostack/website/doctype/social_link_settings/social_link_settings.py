# Copyright (c) 2020, Crisco Technologies and contributors
# License: MIT. See LICENSE

# import criscostack
from criscostack.model.document import Document


class SocialLinkSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from criscostack.types import DF

		background_color: DF.Color | None
		color: DF.Color | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		social_link_type: DF.Literal["", "facebook", "linkedin", "twitter", "email"]
	# end: auto-generated types
	pass
