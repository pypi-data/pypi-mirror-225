# Copyright (c) 2019, Crisco Technologies and contributors
# License: MIT. See LICENSE

import os
from urllib.parse import urlencode, urljoin

from requests_oauthlib import OAuth2Session

import criscostack
from criscostack import _
from criscostack.model.document import Document

if any((os.getenv("CI"), criscostack.conf.developer_mode, criscostack.conf.allow_tests)):
	# Disable mandatory TLS in developer mode and tests
	os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"


class ConnectedApp(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from criscostack.integrations.doctype.oauth_scope.oauth_scope import OAuthScope
		from criscostack.integrations.doctype.query_parameters.query_parameters import QueryParameters
		from criscostack.types import DF

		authorization_uri: DF.SmallText | None
		client_id: DF.Data | None
		client_secret: DF.Password | None
		introspection_uri: DF.Data | None
		openid_configuration: DF.Data | None
		provider_name: DF.Data
		query_parameters: DF.Table[QueryParameters]
		redirect_uri: DF.Data | None
		revocation_uri: DF.Data | None
		scopes: DF.Table[OAuthScope]
		token_uri: DF.Data | None
		userinfo_uri: DF.Data | None
	# end: auto-generated types
	"""Connect to a remote oAuth Server. Retrieve and store user's access token
	in a Token Cache.
	"""

	def validate(self):
		base_url = criscostack.utils.get_url()
		callback_path = (
			"/api/method/criscostack.integrations.doctype.connected_app.connected_app.callback/" + self.name
		)
		self.redirect_uri = urljoin(base_url, callback_path)

	def get_oauth2_session(self, user=None, init=False):
		"""Return an auto-refreshing OAuth2 session which is an extension of a requests.Session()"""
		token = None
		token_updater = None
		auto_refresh_kwargs = None

		if not init:
			user = user or criscostack.session.user
			token_cache = self.get_user_token(user)
			token = token_cache.get_json()
			token_updater = token_cache.update_data
			auto_refresh_kwargs = {"client_id": self.client_id}
			client_secret = self.get_password("client_secret")
			if client_secret:
				auto_refresh_kwargs["client_secret"] = client_secret

		return OAuth2Session(
			client_id=self.client_id,
			token=token,
			token_updater=token_updater,
			auto_refresh_url=self.token_uri,
			auto_refresh_kwargs=auto_refresh_kwargs,
			redirect_uri=self.redirect_uri,
			scope=self.get_scopes(),
		)

	@criscostack.whitelist()
	def initiate_web_application_flow(self, user=None, success_uri=None):
		"""Return an authorization URL for the user. Save state in Token Cache."""
		user = user or criscostack.session.user
		oauth = self.get_oauth2_session(user, init=True)
		query_params = self.get_query_params()
		authorization_url, state = oauth.authorization_url(self.authorization_uri, **query_params)
		token_cache = self.get_token_cache(user)

		if not token_cache:
			token_cache = criscostack.new_doc("Token Cache")
			token_cache.user = user
			token_cache.connected_app = self.name

		token_cache.success_uri = success_uri
		token_cache.state = state
		token_cache.save(ignore_permissions=True)
		criscostack.db.commit()

		return authorization_url

	def get_user_token(self, user=None, success_uri=None):
		"""Return an existing user token or initiate a Web Application Flow."""
		user = user or criscostack.session.user
		token_cache = self.get_token_cache(user)

		if token_cache:
			return token_cache

		redirect = self.initiate_web_application_flow(user, success_uri)
		criscostack.local.response["type"] = "redirect"
		criscostack.local.response["location"] = redirect
		return redirect

	def get_token_cache(self, user):
		token_cache = None
		token_cache_name = self.name + "-" + user

		if criscostack.db.exists("Token Cache", token_cache_name):
			token_cache = criscostack.get_doc("Token Cache", token_cache_name)

		return token_cache

	def get_scopes(self):
		return [row.scope for row in self.scopes]

	def get_query_params(self):
		return {param.key: param.value for param in self.query_parameters}

	def get_active_token(self, user=None):
		user = user or criscostack.session.user
		token_cache = self.get_token_cache(user)
		if token_cache and token_cache.is_expired():
			oauth_session = self.get_oauth2_session(user)

			try:
				token = oauth_session.refresh_token(
					body=f"redirect_uri={self.redirect_uri}",
					token_url=self.token_uri,
				)
			except Exception:
				self.log_error("Token Refresh Error")
				return None

			token_cache.update_data(token)

		return token_cache


@criscostack.whitelist(methods=["GET"], allow_guest=True)
def callback(code=None, state=None):
	"""Handle client's code.

	Called during the oauthorization flow by the remote oAuth2 server to
	transmit a code that can be used by the local server to obtain an access
	token.
	"""

	if criscostack.session.user == "Guest":
		criscostack.local.response["type"] = "redirect"
		criscostack.local.response["location"] = "/login?" + urlencode({"redirect-to": criscostack.request.url})
		return

	path = criscostack.request.path[1:].split("/")
	if len(path) != 4 or not path[3]:
		criscostack.throw(_("Invalid Parameters."))

	connected_app = criscostack.get_doc("Connected App", path[3])
	token_cache = criscostack.get_doc("Token Cache", connected_app.name + "-" + criscostack.session.user)

	if state != token_cache.state:
		criscostack.throw(_("Invalid state."))

	oauth_session = connected_app.get_oauth2_session(init=True)
	query_params = connected_app.get_query_params()
	token = oauth_session.fetch_token(
		connected_app.token_uri,
		code=code,
		client_secret=connected_app.get_password("client_secret"),
		include_client_id=True,
		**query_params,
	)
	token_cache.update_data(token)

	criscostack.local.response["type"] = "redirect"
	criscostack.local.response["location"] = token_cache.get("success_uri") or connected_app.get_url()


@criscostack.whitelist()
def has_token(connected_app, connected_user=None):
	app = criscostack.get_doc("Connected App", connected_app)
	token_cache = app.get_token_cache(connected_user or criscostack.session.user)
	return bool(token_cache and token_cache.get_password("access_token", False))
