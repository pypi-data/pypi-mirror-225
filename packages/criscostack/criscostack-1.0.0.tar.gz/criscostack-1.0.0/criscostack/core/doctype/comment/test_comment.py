# Copyright (c) 2019, Crisco Technologies and Contributors
# License: MIT. See LICENSE
import json

import criscostack
from criscostack.templates.includes.comments.comments import add_comment
from criscostack.tests.test_model_utils import set_user
from criscostack.tests.utils import CriscoTestCase, change_settings
from criscostack.website.doctype.blog_post.test_blog_post import make_test_blog


class TestComment(CriscoTestCase):
	def tearDown(self):
		criscostack.form_dict.comment = None
		criscostack.form_dict.comment_email = None
		criscostack.form_dict.comment_by = None
		criscostack.form_dict.reference_doctype = None
		criscostack.form_dict.reference_name = None
		criscostack.form_dict.route = None
		criscostack.local.request_ip = None

	def test_comment_creation(self):
		test_doc = criscostack.get_doc(dict(doctype="ToDo", description="test"))
		test_doc.insert()
		comment = test_doc.add_comment("Comment", "test comment")

		test_doc.reload()

		# check if updated in _comments cache
		comments = json.loads(test_doc.get("_comments"))
		self.assertEqual(comments[0].get("name"), comment.name)
		self.assertEqual(comments[0].get("comment"), comment.content)

		# check document creation
		comment_1 = criscostack.get_all(
			"Comment",
			fields=["*"],
			filters=dict(reference_doctype=test_doc.doctype, reference_name=test_doc.name),
		)[0]

		self.assertEqual(comment_1.content, "test comment")

	# test via blog
	def test_public_comment(self):
		test_blog = make_test_blog()

		criscostack.db.delete("Comment", {"reference_doctype": "Blog Post"})

		criscostack.form_dict.comment = "Good comment with 10 chars"
		criscostack.form_dict.comment_email = "test@test.com"
		criscostack.form_dict.comment_by = "Good Tester"
		criscostack.form_dict.reference_doctype = "Blog Post"
		criscostack.form_dict.reference_name = test_blog.name
		criscostack.form_dict.route = test_blog.route
		criscostack.local.request_ip = "127.0.0.1"

		add_comment()

		self.assertEqual(
			criscostack.get_all(
				"Comment",
				fields=["*"],
				filters=dict(reference_doctype=test_blog.doctype, reference_name=test_blog.name),
			)[0].published,
			1,
		)

		criscostack.db.delete("Comment", {"reference_doctype": "Blog Post"})

		criscostack.form_dict.comment = "pleez vizits my site http://mysite.com"
		criscostack.form_dict.comment_by = "bad commentor"

		add_comment()

		self.assertEqual(
			len(
				criscostack.get_all(
					"Comment",
					fields=["*"],
					filters=dict(reference_doctype=test_blog.doctype, reference_name=test_blog.name),
				)
			),
			0,
		)

		# test for filtering html and css injection elements
		criscostack.db.delete("Comment", {"reference_doctype": "Blog Post"})

		criscostack.form_dict.comment = "<script>alert(1)</script>Comment"
		criscostack.form_dict.comment_by = "hacker"

		add_comment()

		self.assertEqual(
			criscostack.get_all(
				"Comment",
				fields=["content"],
				filters=dict(reference_doctype=test_blog.doctype, reference_name=test_blog.name),
			)[0]["content"],
			"Comment",
		)

		test_blog.delete()

	@change_settings("Blog Settings", {"allow_guest_to_comment": 0})
	def test_guest_cannot_comment(self):
		test_blog = make_test_blog()
		with set_user("Guest"):
			criscostack.form_dict.comment = "Good comment with 10 chars"
			criscostack.form_dict.comment_email = "mail@example.org"
			criscostack.form_dict.comment_by = "Good Tester"
			criscostack.form_dict.reference_doctype = "Blog Post"
			criscostack.form_dict.reference_name = test_blog.name
			criscostack.form_dict.route = test_blog.route
			criscostack.local.request_ip = "127.0.0.1"

			self.assertEqual(add_comment(), None)

	def test_user_not_logged_in(self):
		some_system_user = criscostack.db.get_value("User", {})

		test_blog = make_test_blog()
		with set_user("Guest"):
			criscostack.form_dict.comment = "Good comment with 10 chars"
			criscostack.form_dict.comment_email = some_system_user
			criscostack.form_dict.comment_by = "Good Tester"
			criscostack.form_dict.reference_doctype = "Blog Post"
			criscostack.form_dict.reference_name = test_blog.name
			criscostack.form_dict.route = test_blog.route
			criscostack.local.request_ip = "127.0.0.1"

			self.assertRaises(criscostack.ValidationError, add_comment)
