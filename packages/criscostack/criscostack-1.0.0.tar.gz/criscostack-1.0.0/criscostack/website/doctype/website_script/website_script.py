# Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

# License: MIT. See LICENSE

import criscostack
from criscostack.model.document import Document


class WebsiteScript(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from criscostack.types import DF

		javascript: DF.Code | None
	# end: auto-generated types
	def on_update(self):
		"""clear cache"""
		criscostack.clear_cache(user="Guest")

		from criscostack.website.utils import clear_cache

		clear_cache()
