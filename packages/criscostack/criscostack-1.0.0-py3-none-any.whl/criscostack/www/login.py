# Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import criscostack
import criscostack.utils
from criscostack import _
from criscostack.auth import LoginManager
from criscostack.rate_limiter import rate_limit
from criscostack.utils import cint, get_url
from criscostack.utils.data import escape_html
from criscostack.utils.html_utils import get_icon_html
from criscostack.utils.jinja import guess_is_path
from criscostack.utils.oauth import get_oauth2_authorize_url, get_oauth_keys, redirect_post_login
from criscostack.utils.password import get_decrypted_password
from criscostack.website.utils import get_home_page

no_cache = True


def get_context(context):
	redirect_to = criscostack.local.request.args.get("redirect-to")

	if criscostack.session.user != "Guest":
		if not redirect_to:
			if criscostack.session.data.user_type == "Website User":
				redirect_to = get_home_page()
			else:
				redirect_to = "/app"

		if redirect_to != "login":
			criscostack.local.flags.redirect_location = redirect_to
			raise criscostack.Redirect

	context.no_header = True
	context.for_test = "login.html"
	context["title"] = "Login"
	context["hide_login"] = True  # dont show login link on login page again.
	context["provider_logins"] = []
	context["disable_signup"] = cint(criscostack.get_website_settings("disable_signup"))
	context["disable_user_pass_login"] = cint(criscostack.get_system_settings("disable_user_pass_login"))
	context["logo"] = criscostack.get_website_settings("app_logo") or criscostack.get_hooks("app_logo_url")[-1]
	context["app_name"] = (
		criscostack.get_website_settings("app_name") or criscostack.get_system_settings("app_name") or _("Crisco")
	)

	signup_form_template = criscostack.get_hooks("signup_form_template")
	if signup_form_template and len(signup_form_template):
		path = signup_form_template[-1]
		if not guess_is_path(path):
			path = criscostack.get_attr(signup_form_template[-1])()
	else:
		path = "criscostack/templates/signup.html"

	if path:
		context["signup_form_template"] = criscostack.get_template(path).render()

	providers = criscostack.get_all(
		"Social Login Key",
		filters={"enable_social_login": 1},
		fields=["name", "client_id", "base_url", "provider_name", "icon"],
		order_by="name",
	)

	for provider in providers:
		client_secret = get_decrypted_password("Social Login Key", provider.name, "client_secret")
		if not client_secret:
			continue

		icon = None
		if provider.icon:
			if provider.provider_name == "Custom":
				icon = get_icon_html(provider.icon, small=True)
			else:
				icon = f"<img src={escape_html(provider.icon)!r} alt={escape_html(provider.provider_name)!r}>"

		if provider.client_id and provider.base_url and get_oauth_keys(provider.name):
			context.provider_logins.append(
				{
					"name": provider.name,
					"provider_name": provider.provider_name,
					"auth_url": get_oauth2_authorize_url(provider.name, redirect_to),
					"icon": icon,
				}
			)
			context["social_login"] = True

	if cint(criscostack.db.get_value("LDAP Settings", "LDAP Settings", "enabled")):
		from criscostack.integrations.doctype.ldap_settings.ldap_settings import LDAPSettings

		context["ldap_settings"] = LDAPSettings.get_ldap_client_settings()

	login_label = [_("Email")]

	if criscostack.utils.cint(criscostack.get_system_settings("allow_login_using_mobile_number")):
		login_label.append(_("Mobile"))

	if criscostack.utils.cint(criscostack.get_system_settings("allow_login_using_user_name")):
		login_label.append(_("Username"))

	context["login_label"] = f" {_('or')} ".join(login_label)

	context["login_with_email_link"] = criscostack.get_system_settings("login_with_email_link")

	return context


@criscostack.whitelist(allow_guest=True)
def login_via_token(login_token: str):
	sid = criscostack.cache.get_value(f"login_token:{login_token}", expires=True)
	if not sid:
		criscostack.respond_as_web_page(_("Invalid Request"), _("Invalid Login Token"), http_status_code=417)
		return

	criscostack.local.form_dict.sid = sid
	criscostack.local.login_manager = LoginManager()

	redirect_post_login(
		desk_user=criscostack.db.get_value("User", criscostack.session.user, "user_type") == "System User"
	)


@criscostack.whitelist(allow_guest=True)
@rate_limit(limit=5, seconds=60 * 60)
def send_login_link(email: str):

	if not criscostack.get_system_settings("login_with_email_link"):
		return

	expiry = criscostack.get_system_settings("login_with_email_link_expiry") or 10
	link = _generate_temporary_login_link(email, expiry)

	app_name = (
		criscostack.get_website_settings("app_name") or criscostack.get_system_settings("app_name") or _("Crisco")
	)

	subject = _("Login To {0}").format(app_name)

	criscostack.sendmail(
		subject=subject,
		recipients=email,
		template="login_with_email_link",
		args={"link": link, "minutes": expiry, "app_name": app_name},
		now=True,
	)


def _generate_temporary_login_link(email: str, expiry: int):
	assert isinstance(email, str)

	if not criscostack.db.exists("User", email):
		criscostack.throw(
			_("User with email address {0} does not exist").format(email), criscostack.DoesNotExistError
		)
	key = criscostack.generate_hash()
	criscostack.cache.set_value(f"one_time_login_key:{key}", email, expires_in_sec=expiry * 60)

	return get_url(f"/api/method/criscostack.www.login.login_via_key?key={key}")


@criscostack.whitelist(allow_guest=True, methods=["GET"])
@rate_limit(limit=5, seconds=60 * 60)
def login_via_key(key: str):
	cache_key = f"one_time_login_key:{key}"
	email = criscostack.cache.get_value(cache_key)

	if email:
		criscostack.cache.delete_value(cache_key)

		criscostack.local.login_manager.login_as(email)

		redirect_post_login(
			desk_user=criscostack.db.get_value("User", criscostack.session.user, "user_type") == "System User"
		)
	else:
		criscostack.respond_as_web_page(
			_("Not Permitted"),
			_("The link you trying to login is invalid or expired."),
			http_status_code=403,
			indicator_color="red",
		)
