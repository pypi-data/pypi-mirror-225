import criscostack
import criscostack.www.list
from criscostack import _

no_cache = 1


def get_context(context):
	if criscostack.session.user == "Guest":
		criscostack.throw(_("You need to be logged in to access this page"), criscostack.PermissionError)

	active_tokens = criscostack.get_all(
		"OAuth Bearer Token",
		filters=[["user", "=", criscostack.session.user]],
		fields=["client"],
		distinct=True,
		order_by="creation",
	)

	client_apps = []

	for token in active_tokens:
		creation = get_first_login(token.client)
		app = {
			"name": token.get("client"),
			"app_name": criscostack.db.get_value("OAuth Client", token.get("client"), "app_name"),
			"creation": creation,
		}
		client_apps.append(app)

	app = None
	if "app" in criscostack.form_dict:
		app = criscostack.get_doc("OAuth Client", criscostack.form_dict.app)
		app = app.__dict__
		app["client_secret"] = None

	if app:
		context.app = app

	context.apps = client_apps


def get_first_login(client):
	login_date = criscostack.get_all(
		"OAuth Bearer Token",
		filters=[["user", "=", criscostack.session.user], ["client", "=", client]],
		fields=["creation"],
		order_by="creation",
		limit=1,
	)

	login_date = login_date[0].get("creation") if login_date and len(login_date) > 0 else None

	return login_date


@criscostack.whitelist()
def delete_client(client_id: str):
	active_client_id_tokens = criscostack.get_all(
		"OAuth Bearer Token", filters=[["user", "=", criscostack.session.user], ["client", "=", client_id]]
	)
	for token in active_client_id_tokens:
		criscostack.delete_doc("OAuth Bearer Token", token.get("name"), ignore_permissions=True)
