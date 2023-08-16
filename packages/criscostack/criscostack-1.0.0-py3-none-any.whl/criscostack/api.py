# Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE
import base64
import binascii
import json
from typing import Literal
from urllib.parse import urlencode, urlparse

import criscostack
import criscostack.client
import criscostack.handler
from criscostack import _
from criscostack.utils.data import sbool
from criscostack.utils.response import build_response


def handle():
	"""
	Handler for `/api` methods

	### Examples:

	`/api/method/{methodname}` will call a whitelisted method

	`/api/resource/{doctype}` will query a table
	        examples:
	        - `?fields=["name", "owner"]`
	        - `?filters=[["Task", "name", "like", "%005"]]`
	        - `?limit_start=0`
	        - `?limit_page_length=20`

	`/api/resource/{doctype}/{name}` will point to a resource
	        `GET` will return doclist
	        `POST` will insert
	        `PUT` will update
	        `DELETE` will delete

	`/api/resource/{doctype}/{name}?run_method={method}` will run a whitelisted controller method
	"""

	parts = criscostack.request.path[1:].split("/", 3)
	call = doctype = name = None

	if len(parts) > 1:
		call = parts[1]

	if len(parts) > 2:
		doctype = parts[2]

	if len(parts) > 3:
		name = parts[3]

	return _RESTAPIHandler(call, doctype, name).get_response()


class _RESTAPIHandler:
	def __init__(self, call: Literal["method", "resource"], doctype: str | None, name: str | None):
		self.call = call
		self.doctype = doctype
		self.name = name

	def get_response(self):
		"""Prepare and get response based on URL and form body.

		Note: most methods of this class directly operate on the response local.
		"""
		match self.call:
			case "method":
				return self.handle_method()
			case "resource":
				self.handle_resource()
			case _:
				raise criscostack.DoesNotExistError

		return build_response("json")

	def handle_method(self):
		criscostack.local.form_dict.cmd = self.doctype
		return criscostack.handler.handle()

	def handle_resource(self):
		if self.doctype and self.name:
			self.handle_document_resource()
		elif self.doctype:
			self.handle_doctype_resource()
		else:
			raise criscostack.DoesNotExistError

	def handle_document_resource(self):
		if "run_method" in criscostack.local.form_dict:
			self.execute_doc_method()
			return

		match criscostack.local.request.method:
			case "GET":
				self.get_doc()
			case "PUT":
				self.update_doc()
			case "DELETE":
				self.delete_doc()
			case _:
				raise criscostack.DoesNotExistError

	def handle_doctype_resource(self):
		match criscostack.local.request.method:
			case "GET":
				self.get_doc_list()
			case "POST":
				self.create_doc()
			case _:
				raise criscostack.DoesNotExistError

	def execute_doc_method(self):
		method = criscostack.local.form_dict.pop("run_method")
		doc = criscostack.get_doc(self.doctype, self.name)
		doc.is_whitelisted(method)

		if criscostack.local.request.method == "GET":
			if not doc.has_permission("read"):
				criscostack.throw(_("Not permitted"), criscostack.PermissionError)
			criscostack.local.response.update({"data": doc.run_method(method, **criscostack.local.form_dict)})

		elif criscostack.local.request.method == "POST":
			if not doc.has_permission("write"):
				criscostack.throw(_("Not permitted"), criscostack.PermissionError)

			criscostack.local.response.update({"data": doc.run_method(method, **criscostack.local.form_dict)})
			criscostack.db.commit()

	def get_doc(self):
		doc = criscostack.get_doc(self.doctype, self.name)
		if not doc.has_permission("read"):
			raise criscostack.PermissionError
		doc.apply_fieldlevel_read_permissions()
		criscostack.local.response.update({"data": doc})

	def update_doc(self):
		data = get_request_form_data()

		doc = criscostack.get_doc(self.doctype, self.name, for_update=True)

		if "flags" in data:
			del data["flags"]

		# Not checking permissions here because it's checked in doc.save
		doc.update(data)

		criscostack.local.response.update({"data": doc.save().as_dict()})

		# check for child table doctype
		if doc.get("parenttype"):
			criscostack.get_doc(doc.parenttype, doc.parent).save()
		criscostack.db.commit()

	def delete_doc(self):
		# Not checking permissions here because it's checked in delete_doc
		criscostack.delete_doc(self.doctype, self.name, ignore_missing=False)
		criscostack.local.response.http_status_code = 202
		criscostack.local.response.message = "ok"
		criscostack.db.commit()

	def get_doc_list(self):
		if criscostack.local.form_dict.get("fields"):
			criscostack.local.form_dict["fields"] = json.loads(criscostack.local.form_dict["fields"])

		# set limit of records for criscostack.get_list
		criscostack.local.form_dict.setdefault(
			"limit_page_length",
			criscostack.local.form_dict.limit or criscostack.local.form_dict.limit_page_length or 20,
		)

		# convert strings to native types - only as_dict and debug accept bool
		for param in ["as_dict", "debug"]:
			param_val = criscostack.local.form_dict.get(param)
			if param_val is not None:
				criscostack.local.form_dict[param] = sbool(param_val)

		# evaluate criscostack.get_list
		data = criscostack.call(criscostack.client.get_list, self.doctype, **criscostack.local.form_dict)

		# set criscostack.get_list result to response
		criscostack.local.response.update({"data": data})

	def create_doc(self):
		data = get_request_form_data()
		data.update({"doctype": self.doctype})

		# insert document from request data
		doc = criscostack.get_doc(data).insert()

		# set response data
		criscostack.local.response.update({"data": doc.as_dict()})

		# commit for POST requests
		criscostack.db.commit()


def get_request_form_data():
	if criscostack.local.form_dict.data is None:
		data = criscostack.safe_decode(criscostack.local.request.get_data())
	else:
		data = criscostack.local.form_dict.data

	try:
		return criscostack.parse_json(data)
	except ValueError:
		return criscostack.local.form_dict


def validate_auth():
	"""
	Authenticate and sets user for the request.
	"""
	authorization_header = criscostack.get_request_header("Authorization", "").split(" ")

	if len(authorization_header) == 2:
		validate_oauth(authorization_header)
		validate_auth_via_api_keys(authorization_header)

	validate_auth_via_hooks()


def validate_oauth(authorization_header):
	"""
	Authenticate request using OAuth and set session user

	Args:
	        authorization_header (list of str): The 'Authorization' header containing the prefix and token
	"""

	from criscostack.integrations.oauth2 import get_oauth_server
	from criscostack.oauth import get_url_delimiter

	form_dict = criscostack.local.form_dict
	token = authorization_header[1]
	req = criscostack.request
	parsed_url = urlparse(req.url)
	access_token = {"access_token": token}
	uri = (
		parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path + "?" + urlencode(access_token)
	)
	http_method = req.method
	headers = req.headers
	body = req.get_data()
	if req.content_type and "multipart/form-data" in req.content_type:
		body = None

	try:
		required_scopes = criscostack.db.get_value("OAuth Bearer Token", token, "scopes").split(
			get_url_delimiter()
		)
		valid, oauthlib_request = get_oauth_server().verify_request(
			uri, http_method, body, headers, required_scopes
		)
		if valid:
			criscostack.set_user(criscostack.db.get_value("OAuth Bearer Token", token, "user"))
			criscostack.local.form_dict = form_dict
	except AttributeError:
		pass


def validate_auth_via_api_keys(authorization_header):
	"""
	Authenticate request using API keys and set session user

	Args:
	        authorization_header (list of str): The 'Authorization' header containing the prefix and token
	"""

	try:
		auth_type, auth_token = authorization_header
		authorization_source = criscostack.get_request_header("Crisco-Authorization-Source")
		if auth_type.lower() == "basic":
			api_key, api_secret = criscostack.safe_decode(base64.b64decode(auth_token)).split(":")
			validate_api_key_secret(api_key, api_secret, authorization_source)
		elif auth_type.lower() == "token":
			api_key, api_secret = auth_token.split(":")
			validate_api_key_secret(api_key, api_secret, authorization_source)
	except binascii.Error:
		criscostack.throw(
			_("Failed to decode token, please provide a valid base64-encoded token."),
			criscostack.InvalidAuthorizationToken,
		)
	except (AttributeError, TypeError, ValueError):
		pass


def validate_api_key_secret(api_key, api_secret, criscostack_authorization_source=None):
	"""criscostack_authorization_source to provide api key and secret for a doctype apart from User"""
	doctype = criscostack_authorization_source or "User"
	doc = criscostack.db.get_value(doctype=doctype, filters={"api_key": api_key}, fieldname=["name"])
	form_dict = criscostack.local.form_dict
	doc_secret = criscostack.utils.password.get_decrypted_password(doctype, doc, fieldname="api_secret")
	if api_secret == doc_secret:
		if doctype == "User":
			user = criscostack.db.get_value(doctype="User", filters={"api_key": api_key}, fieldname=["name"])
		else:
			user = criscostack.db.get_value(doctype, doc, "user")
		if criscostack.local.login_manager.user in ("", "Guest"):
			criscostack.set_user(user)
		criscostack.local.form_dict = form_dict


def validate_auth_via_hooks():
	for auth_hook in criscostack.get_hooks("auth_hooks", []):
		criscostack.get_attr(auth_hook)()
