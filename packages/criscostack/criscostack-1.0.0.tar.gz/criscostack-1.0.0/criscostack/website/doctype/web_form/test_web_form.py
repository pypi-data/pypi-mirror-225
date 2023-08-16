# Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE
import json

import criscostack
from criscostack.tests.utils import CriscoTestCase
from criscostack.utils import set_request
from criscostack.website.doctype.web_form.web_form import accept
from criscostack.website.serve import get_response_content

test_dependencies = ["Web Form"]


class TestWebForm(CriscoTestCase):
	def setUp(self):
		criscostack.conf.disable_website_cache = True
		criscostack.local.path = None

	def tearDown(self):
		criscostack.conf.disable_website_cache = False
		criscostack.local.path = None
		criscostack.local.request_ip = None
		criscostack.form_dict.web_form = None
		criscostack.form_dict.data = None
		criscostack.form_dict.docname = None

	def test_accept(self):
		criscostack.set_user("Administrator")

		doc = {
			"doctype": "Event",
			"subject": "_Test Event Web Form",
			"description": "_Test Event Description",
			"starts_on": "2014-09-09",
		}

		criscostack.form_dict.web_form = "manage-events"
		criscostack.form_dict.data = json.dumps(doc)
		criscostack.local.request_ip = "127.0.0.1"

		accept(web_form="manage-events", data=json.dumps(doc))

		self.event_name = criscostack.db.get_value("Event", {"subject": "_Test Event Web Form"})
		self.assertTrue(self.event_name)

	def test_edit(self):
		self.test_accept()

		doc = {
			"doctype": "Event",
			"subject": "_Test Event Web Form",
			"description": "_Test Event Description 1",
			"starts_on": "2014-09-09",
			"name": self.event_name,
		}

		self.assertNotEqual(
			criscostack.db.get_value("Event", self.event_name, "description"), doc.get("description")
		)

		criscostack.form_dict.web_form = "manage-events"
		criscostack.form_dict.docname = self.event_name
		criscostack.form_dict.data = json.dumps(doc)

		accept(web_form="manage-events", docname=self.event_name, data=json.dumps(doc))

		self.assertEqual(
			criscostack.db.get_value("Event", self.event_name, "description"), doc.get("description")
		)

	def test_webform_render(self):
		set_request(method="GET", path="manage-events/new")
		content = get_response_content("manage-events/new")
		self.assertIn('<h1 class="ellipsis">New Manage Events</h1>', content)
		self.assertIn('data-doctype="Web Form"', content)
		self.assertIn('data-path="manage-events/new"', content)
		self.assertIn('source-type="Generator"', content)

	def test_webform_html_meta_is_added(self):
		set_request(method="GET", path="manage-events/new")
		content = get_response_content("manage-events/new")

		self.assertIn('<meta name="name" content="Test Meta Form Title">', content)
		self.assertIn('<meta property="og:description" content="Test Meta Form Description">', content)
		self.assertIn('<meta property="og:image" content="https://criscostack.io/files/criscostack.png">', content)
