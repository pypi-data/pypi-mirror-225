# Copyright (c) 2023, Crisco Technologies and contributors
# For license information, please see license.txt

# import criscostack
from criscostack.model.document import Document


class MarketingCampaign(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from criscostack.types import DF

		campaign_description: DF.SmallText | None
	# end: auto-generated types
	pass
