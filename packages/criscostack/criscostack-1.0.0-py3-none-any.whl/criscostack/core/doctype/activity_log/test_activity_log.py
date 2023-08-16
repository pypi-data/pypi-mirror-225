# Copyright (c) 2015, Crisco Technologies and Contributors
# License: MIT. See LICENSE
import time

import criscostack
from criscostack.auth import CookieManager, LoginManager
from criscostack.tests.utils import CriscoTestCase


class TestActivityLog(CriscoTestCase):
	def test_activity_log(self):

		# test user login log
		criscostack.local.form_dict = criscostack._dict(
			{
				"cmd": "login",
				"sid": "Guest",
				"pwd": criscostack.conf.admin_password or "admin",
				"usr": "Administrator",
			}
		)

		criscostack.local.cookie_manager = CookieManager()
		criscostack.local.login_manager = LoginManager()

		auth_log = self.get_auth_log()
		self.assertFalse(criscostack.form_dict.pwd)
		self.assertEqual(auth_log.status, "Success")

		# test user logout log
		criscostack.local.login_manager.logout()
		auth_log = self.get_auth_log(operation="Logout")
		self.assertEqual(auth_log.status, "Success")

		# test invalid login
		criscostack.form_dict.update({"pwd": "password"})
		self.assertRaises(criscostack.AuthenticationError, LoginManager)
		auth_log = self.get_auth_log()
		self.assertEqual(auth_log.status, "Failed")

		criscostack.local.form_dict = criscostack._dict()

	def get_auth_log(self, operation="Login"):
		names = criscostack.get_all(
			"Activity Log",
			filters={
				"user": "Administrator",
				"operation": operation,
			},
			order_by="`creation` DESC",
		)

		name = names[0]
		auth_log = criscostack.get_doc("Activity Log", name)
		return auth_log

	def test_brute_security(self):
		update_system_settings({"allow_consecutive_login_attempts": 3, "allow_login_after_fail": 5})

		criscostack.local.form_dict = criscostack._dict(
			{"cmd": "login", "sid": "Guest", "pwd": "admin", "usr": "Administrator"}
		)

		criscostack.local.cookie_manager = CookieManager()
		criscostack.local.login_manager = LoginManager()

		auth_log = self.get_auth_log()
		self.assertEqual(auth_log.status, "Success")

		# test user logout log
		criscostack.local.login_manager.logout()
		auth_log = self.get_auth_log(operation="Logout")
		self.assertEqual(auth_log.status, "Success")

		# test invalid login
		criscostack.form_dict.update({"pwd": "password"})
		self.assertRaises(criscostack.AuthenticationError, LoginManager)
		self.assertRaises(criscostack.AuthenticationError, LoginManager)
		self.assertRaises(criscostack.AuthenticationError, LoginManager)

		# REMOVE ME: current logic allows allow_consecutive_login_attempts+1 attempts
		# before raising security exception, remove below line when that is fixed.
		self.assertRaises(criscostack.AuthenticationError, LoginManager)
		self.assertRaises(criscostack.SecurityException, LoginManager)
		time.sleep(5)
		self.assertRaises(criscostack.AuthenticationError, LoginManager)

		criscostack.local.form_dict = criscostack._dict()


def update_system_settings(args):
	doc = criscostack.get_doc("System Settings")
	doc.update(args)
	doc.flags.ignore_mandatory = 1
	doc.save()
