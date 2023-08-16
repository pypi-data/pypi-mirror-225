import json
from urllib.parse import quote, urlencode

from oauthlib.oauth2 import FatalClientError, OAuth2Error
from oauthlib.openid.connect.core.endpoints.pre_configured import Server as WebApplicationServer

import criscostack
from criscostack.integrations.doctype.oauth_provider_settings.oauth_provider_settings import (
	get_oauth_settings,
)
from criscostack.oauth import (
	OAuthWebRequestValidator,
	generate_json_error_response,
	get_server_url,
	get_userinfo,
)


def get_oauth_server():
	if not getattr(criscostack.local, "oauth_server", None):
		oauth_validator = OAuthWebRequestValidator()
		criscostack.local.oauth_server = WebApplicationServer(oauth_validator)

	return criscostack.local.oauth_server


def sanitize_kwargs(param_kwargs):
	"""Remove 'data' and 'cmd' keys, if present."""
	arguments = param_kwargs
	arguments.pop("data", None)
	arguments.pop("cmd", None)

	return arguments


def encode_params(params):
	"""
	Encode a dict of params into a query string.

	Use `quote_via=urllib.parse.quote` so that whitespaces will be encoded as
	`%20` instead of as `+`. This is needed because oauthlib cannot handle `+`
	as a whitespace.
	"""
	return urlencode(params, quote_via=quote)


@criscostack.whitelist()
def approve(*args, **kwargs):
	r = criscostack.request

	try:
		(scopes, criscostack.flags.oauth_credentials,) = get_oauth_server().validate_authorization_request(
			r.url, r.method, r.get_data(), r.headers
		)

		headers, body, status = get_oauth_server().create_authorization_response(
			uri=criscostack.flags.oauth_credentials["redirect_uri"],
			body=r.get_data(),
			headers=r.headers,
			scopes=scopes,
			credentials=criscostack.flags.oauth_credentials,
		)
		uri = headers.get("Location", None)

		criscostack.local.response["type"] = "redirect"
		criscostack.local.response["location"] = uri
		return

	except (FatalClientError, OAuth2Error) as e:
		return generate_json_error_response(e)


@criscostack.whitelist(allow_guest=True)
def authorize(**kwargs):
	success_url = "/api/method/criscostack.integrations.oauth2.approve?" + encode_params(
		sanitize_kwargs(kwargs)
	)
	failure_url = criscostack.form_dict["redirect_uri"] + "?error=access_denied"

	if criscostack.session.user == "Guest":
		# Force login, redirect to preauth again.
		criscostack.local.response["type"] = "redirect"
		criscostack.local.response["location"] = "/login?" + encode_params(
			{"redirect-to": criscostack.request.url}
		)
	else:
		try:
			r = criscostack.request
			(scopes, criscostack.flags.oauth_credentials,) = get_oauth_server().validate_authorization_request(
				r.url, r.method, r.get_data(), r.headers
			)

			skip_auth = criscostack.db.get_value(
				"OAuth Client",
				criscostack.flags.oauth_credentials["client_id"],
				"skip_authorization",
			)
			unrevoked_tokens = criscostack.get_all("OAuth Bearer Token", filters={"status": "Active"})

			if skip_auth or (get_oauth_settings().skip_authorization == "Auto" and unrevoked_tokens):
				criscostack.local.response["type"] = "redirect"
				criscostack.local.response["location"] = success_url
			else:
				if "openid" in scopes:
					scopes.remove("openid")
					scopes.extend(["Full Name", "Email", "User Image", "Roles"])

				# Show Allow/Deny screen.
				response_html_params = criscostack._dict(
					{
						"client_id": criscostack.db.get_value("OAuth Client", kwargs["client_id"], "app_name"),
						"success_url": success_url,
						"failure_url": failure_url,
						"details": scopes,
					}
				)
				resp_html = criscostack.render_template(
					"templates/includes/oauth_confirmation.html", response_html_params
				)
				criscostack.respond_as_web_page("Confirm Access", resp_html, primary_action=None)
		except (FatalClientError, OAuth2Error) as e:
			return generate_json_error_response(e)


@criscostack.whitelist(allow_guest=True)
def get_token(*args, **kwargs):
	try:
		r = criscostack.request
		headers, body, status = get_oauth_server().create_token_response(
			r.url, r.method, r.form, r.headers, criscostack.flags.oauth_credentials
		)
		body = criscostack._dict(json.loads(body))

		if body.error:
			criscostack.local.response = body
			criscostack.local.response["http_status_code"] = 400
			return

		criscostack.local.response = body
		return

	except (FatalClientError, OAuth2Error) as e:
		return generate_json_error_response(e)


@criscostack.whitelist(allow_guest=True)
def revoke_token(*args, **kwargs):
	try:
		r = criscostack.request
		headers, body, status = get_oauth_server().create_revocation_response(
			r.url,
			headers=r.headers,
			body=r.form,
			http_method=r.method,
		)
	except (FatalClientError, OAuth2Error):
		pass

	# status_code must be 200
	criscostack.local.response = criscostack._dict({})
	criscostack.local.response["http_status_code"] = status or 200
	return


@criscostack.whitelist()
def openid_profile(*args, **kwargs):
	try:
		r = criscostack.request
		headers, body, status = get_oauth_server().create_userinfo_response(
			r.url,
			headers=r.headers,
			body=r.form,
		)
		body = criscostack._dict(json.loads(body))
		criscostack.local.response = body
		return

	except (FatalClientError, OAuth2Error) as e:
		return generate_json_error_response(e)


@criscostack.whitelist(allow_guest=True)
def openid_configuration():
	criscostack_server_url = get_server_url()
	criscostack.local.response = criscostack._dict(
		{
			"issuer": criscostack_server_url,
			"authorization_endpoint": f"{criscostack_server_url}/api/method/criscostack.integrations.oauth2.authorize",
			"token_endpoint": f"{criscostack_server_url}/api/method/criscostack.integrations.oauth2.get_token",
			"userinfo_endpoint": f"{criscostack_server_url}/api/method/criscostack.integrations.oauth2.openid_profile",
			"revocation_endpoint": f"{criscostack_server_url}/api/method/criscostack.integrations.oauth2.revoke_token",
			"introspection_endpoint": f"{criscostack_server_url}/api/method/criscostack.integrations.oauth2.introspect_token",
			"response_types_supported": [
				"code",
				"token",
				"code id_token",
				"code token id_token",
				"id_token",
				"id_token token",
			],
			"subject_types_supported": ["public"],
			"id_token_signing_alg_values_supported": ["HS256"],
		}
	)


@criscostack.whitelist(allow_guest=True)
def introspect_token(token=None, token_type_hint=None):
	if token_type_hint not in ["access_token", "refresh_token"]:
		token_type_hint = "access_token"
	try:
		bearer_token = None
		if token_type_hint == "access_token":
			bearer_token = criscostack.get_doc("OAuth Bearer Token", {"access_token": token})
		elif token_type_hint == "refresh_token":
			bearer_token = criscostack.get_doc("OAuth Bearer Token", {"refresh_token": token})

		client = criscostack.get_doc("OAuth Client", bearer_token.client)

		token_response = criscostack._dict(
			{
				"client_id": client.client_id,
				"trusted_client": client.skip_authorization,
				"active": bearer_token.status == "Active",
				"exp": round(bearer_token.expiration_time.timestamp()),
				"scope": bearer_token.scopes,
			}
		)

		if "openid" in bearer_token.scopes:
			sub = criscostack.get_value(
				"User Social Login",
				{"provider": "criscostack", "parent": bearer_token.user},
				"userid",
			)

			if sub:
				token_response.update({"sub": sub})
				user = criscostack.get_doc("User", bearer_token.user)
				userinfo = get_userinfo(user)
				token_response.update(userinfo)

		criscostack.local.response = token_response

	except Exception:
		criscostack.local.response = criscostack._dict({"active": False})
