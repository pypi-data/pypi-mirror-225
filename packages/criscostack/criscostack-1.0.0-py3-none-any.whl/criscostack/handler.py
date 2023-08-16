# Copyright (c) 2022, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import os
from mimetypes import guess_type
from typing import TYPE_CHECKING

from werkzeug.wrappers import Response

import criscostack
import criscostack.sessions
import criscostack.utils
from criscostack import _, is_whitelisted
from criscostack.core.doctype.server_script.server_script_utils import get_server_script_map
from criscostack.monitor import add_data_to_monitor
from criscostack.utils import cint
from criscostack.utils.csvutils import build_csv_response
from criscostack.utils.image import optimize_image
from criscostack.utils.response import build_response

if TYPE_CHECKING:
	from criscostack.core.doctype.file.file import File
	from criscostack.core.doctype.user.user import User

ALLOWED_MIMETYPES = (
	"image/png",
	"image/jpeg",
	"application/pdf",
	"application/msword",
	"application/vnd.openxmlformats-officedocument.wordprocessingml.document",
	"application/vnd.ms-excel",
	"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
	"application/vnd.oasis.opendocument.text",
	"application/vnd.oasis.opendocument.spreadsheet",
	"text/plain",
	"video/quicktime",
	"video/mp4",
)


def handle():
	"""handle request"""

	cmd = criscostack.local.form_dict.cmd
	data = None

	if cmd != "login":
		data = execute_cmd(cmd)

	# data can be an empty string or list which are valid responses
	if data is not None:
		if isinstance(data, Response):
			# method returns a response object, pass it on
			return data

		# add the response to `message` label
		criscostack.response["message"] = data

	return build_response("json")


def execute_cmd(cmd, from_async=False):
	"""execute a request as python module"""
	for hook in criscostack.get_hooks("override_whitelisted_methods", {}).get(cmd, []):
		# override using the first hook
		cmd = hook
		break

	# via server script
	server_script = get_server_script_map().get("_api", {}).get(cmd)
	if server_script:
		return run_server_script(server_script)

	try:
		method = get_attr(cmd)
	except Exception as e:
		criscostack.throw(_("Failed to get method for command {0} with {1}").format(cmd, e))

	if from_async:
		method = method.queue

	if method != run_doc_method:
		is_whitelisted(method)
		is_valid_http_method(method)

	return criscostack.call(method, **criscostack.form_dict)


def run_server_script(server_script):
	response = criscostack.get_doc("Server Script", server_script).execute_method()

	# some server scripts return output using flags (empty dict by default),
	# while others directly modify criscostack.response
	# return flags if not empty dict (this overwrites criscostack.response.message)
	if response != {}:
		return response


def is_valid_http_method(method):
	if criscostack.flags.in_safe_exec:
		return

	http_method = criscostack.local.request.method

	if http_method not in criscostack.allowed_http_methods_for_whitelisted_func[method]:
		throw_permission_error()


def throw_permission_error():
	criscostack.throw(_("Not permitted"), criscostack.PermissionError)


@criscostack.whitelist(allow_guest=True)
def logout():
	criscostack.local.login_manager.logout()
	criscostack.db.commit()


@criscostack.whitelist(allow_guest=True)
def web_logout():
	criscostack.local.login_manager.logout()
	criscostack.db.commit()
	criscostack.respond_as_web_page(
		_("Logged Out"), _("You have been successfully logged out"), indicator_color="green"
	)


@criscostack.whitelist()
def uploadfile():
	ret = None

	try:
		if criscostack.form_dict.get("from_form"):
			try:
				ret = criscostack.get_doc(
					{
						"doctype": "File",
						"attached_to_name": criscostack.form_dict.docname,
						"attached_to_doctype": criscostack.form_dict.doctype,
						"attached_to_field": criscostack.form_dict.docfield,
						"file_url": criscostack.form_dict.file_url,
						"file_name": criscostack.form_dict.filename,
						"is_private": criscostack.utils.cint(criscostack.form_dict.is_private),
						"content": criscostack.form_dict.filedata,
						"decode": True,
					}
				)
				ret.save()
			except criscostack.DuplicateEntryError:
				# ignore pass
				ret = None
				criscostack.db.rollback()
		else:
			if criscostack.form_dict.get("method"):
				method = criscostack.get_attr(criscostack.form_dict.method)
				is_whitelisted(method)
				ret = method()
	except Exception:
		criscostack.errprint(criscostack.utils.get_traceback())
		criscostack.response["http_status_code"] = 500
		ret = None

	return ret


@criscostack.whitelist(allow_guest=True)
def upload_file():
	user = None
	if criscostack.session.user == "Guest":
		if criscostack.get_system_settings("allow_guests_to_upload_files"):
			ignore_permissions = True
		else:
			raise criscostack.PermissionError
	else:
		user: "User" = criscostack.get_doc("User", criscostack.session.user)
		ignore_permissions = False

	files = criscostack.request.files
	is_private = criscostack.form_dict.is_private
	doctype = criscostack.form_dict.doctype
	docname = criscostack.form_dict.docname
	fieldname = criscostack.form_dict.fieldname
	file_url = criscostack.form_dict.file_url
	folder = criscostack.form_dict.folder or "Home"
	method = criscostack.form_dict.method
	filename = criscostack.form_dict.file_name
	optimize = criscostack.form_dict.optimize
	content = None

	if "file" in files:
		file = files["file"]
		content = file.stream.read()
		filename = file.filename

		content_type = guess_type(filename)[0]
		if optimize and content_type and content_type.startswith("image/"):
			args = {"content": content, "content_type": content_type}
			if criscostack.form_dict.max_width:
				args["max_width"] = int(criscostack.form_dict.max_width)
			if criscostack.form_dict.max_height:
				args["max_height"] = int(criscostack.form_dict.max_height)
			content = optimize_image(**args)

	criscostack.local.uploaded_file = content
	criscostack.local.uploaded_filename = filename

	if content is not None and (
		criscostack.session.user == "Guest" or (user and not user.has_desk_access())
	):
		filetype = guess_type(filename)[0]
		if filetype not in ALLOWED_MIMETYPES:
			criscostack.throw(_("You can only upload JPG, PNG, PDF, TXT or Microsoft documents."))

	if method:
		method = criscostack.get_attr(method)
		is_whitelisted(method)
		return method()
	else:
		return criscostack.get_doc(
			{
				"doctype": "File",
				"attached_to_doctype": doctype,
				"attached_to_name": docname,
				"attached_to_field": fieldname,
				"folder": folder,
				"file_name": filename,
				"file_url": file_url,
				"is_private": cint(is_private),
				"content": content,
			}
		).save(ignore_permissions=ignore_permissions)


@criscostack.whitelist(allow_guest=True)
def download_file(file_url: str):
	"""
	Download file using token and REST API. Valid session or
	token is required to download private files.

	Method : GET
	Endpoints : download_file, criscostack.core.doctype.file.file.download_file
	URL Params : file_name = /path/to/file relative to site path
	"""
	file: "File" = criscostack.get_doc("File", {"file_url": file_url})
	if not file.is_downloadable():
		raise criscostack.PermissionError

	criscostack.local.response.filename = os.path.basename(file_url)
	criscostack.local.response.filecontent = file.get_content()
	criscostack.local.response.type = "download"


def get_attr(cmd):
	"""get method object from cmd"""
	if "." in cmd:
		method = criscostack.get_attr(cmd)
	else:
		method = globals()[cmd]
	criscostack.log("method:" + cmd)
	return method


@criscostack.whitelist(allow_guest=True)
def ping():
	return "pong"


def run_doc_method(method, docs=None, dt=None, dn=None, arg=None, args=None):
	"""run a whitelisted controller method"""
	from inspect import signature

	if not args and arg:
		args = arg

	if dt:  # not called from a doctype (from a page)
		if not dn:
			dn = dt  # single
		doc = criscostack.get_doc(dt, dn)

	else:
		docs = criscostack.parse_json(docs)
		doc = criscostack.get_doc(docs)
		doc._original_modified = doc.modified
		doc.check_if_latest()

	if not doc or not doc.has_permission("read"):
		throw_permission_error()

	try:
		args = criscostack.parse_json(args)
	except ValueError:
		pass

	method_obj = getattr(doc, method)
	fn = getattr(method_obj, "__func__", method_obj)
	is_whitelisted(fn)
	is_valid_http_method(fn)

	fnargs = list(signature(method_obj).parameters)

	if not fnargs or (len(fnargs) == 1 and fnargs[0] == "self"):
		response = doc.run_method(method)

	elif "args" in fnargs or not isinstance(args, dict):
		response = doc.run_method(method, args)

	else:
		response = doc.run_method(method, **args)

	criscostack.response.docs.append(doc)
	if response is None:
		return

	# build output as csv
	if cint(criscostack.form_dict.get("as_csv")):
		build_csv_response(response, _(doc.doctype).replace(" ", ""))
		return

	criscostack.response["message"] = response

	add_data_to_monitor(methodname=method)


# for backwards compatibility
runserverobj = run_doc_method
