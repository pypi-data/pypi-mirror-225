# Copyright (c) 2017, Crisco Technologies and Contributors
# License: MIT. See LICENSE
import criscostack
from criscostack.tests.utils import CriscoTestCase


class TestLetterHead(CriscoTestCase):
	def test_auto_image(self):
		letter_head = criscostack.get_doc(
			dict(doctype="Letter Head", letter_head_name="Test", source="Image", image="/public/test.png")
		).insert()

		# test if image is automatically set
		self.assertTrue(letter_head.image in letter_head.content)
