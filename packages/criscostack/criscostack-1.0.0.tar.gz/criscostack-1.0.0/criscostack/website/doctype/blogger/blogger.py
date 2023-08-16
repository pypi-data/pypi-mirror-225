# Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

# License: MIT. See LICENSE

import criscostack
from criscostack import _
from criscostack.model.document import Document


class Blogger(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from criscostack.types import DF

		avatar: DF.AttachImage | None
		bio: DF.SmallText | None
		disabled: DF.Check
		full_name: DF.Data
		short_name: DF.Data
		user: DF.Link | None
	# end: auto-generated types
	def validate(self):
		if self.user and not criscostack.db.exists("User", self.user):
			# for data import
			criscostack.get_doc(
				{"doctype": "User", "email": self.user, "first_name": self.user.split("@", 1)[0]}
			).insert()

	def on_update(self):
		"if user is set, then update all older blogs"

		from criscostack.website.doctype.blog_post.blog_post import clear_blog_cache

		clear_blog_cache()

		if self.user:
			for blog in criscostack.db.sql_list(
				"""select name from `tabBlog Post` where owner=%s
				and ifnull(blogger,'')=''""",
				self.user,
			):
				b = criscostack.get_doc("Blog Post", blog)
				b.blogger = self.name
				b.save()

			criscostack.permissions.add_user_permission("Blogger", self.name, self.user)
