# Copyright (c) 2015, Crisco Technologies and contributors
# License: MIT. See LICENSE

import criscostack
from criscostack import _
from criscostack.model.document import Document


class OAuthProviderSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from criscostack.types import DF

		skip_authorization: DF.Literal["Force", "Auto"]
	# end: auto-generated types
	pass


def get_oauth_settings():
	"""Returns oauth settings"""
	out = criscostack._dict(
		{
			"skip_authorization": criscostack.db.get_single_value(
				"OAuth Provider Settings", "skip_authorization"
			)
		}
	)

	return out
