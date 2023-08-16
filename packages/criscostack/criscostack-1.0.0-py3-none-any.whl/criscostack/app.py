# Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import gc
import logging
import os
import re

from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.local import LocalManager
from werkzeug.middleware.profiler import ProfilerMiddleware
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.wrappers import Request, Response

import criscostack
import criscostack.api
import criscostack.handler
import criscostack.monitor
import criscostack.rate_limiter
import criscostack.recorder
import criscostack.utils.response
from criscostack import _
from criscostack.auth import SAFE_HTTP_METHODS, UNSAFE_HTTP_METHODS, HTTPRequest
from criscostack.middlewares import StaticDataMiddleware
from criscostack.utils import cint, get_site_name, sanitize_html
from criscostack.utils.error import log_error_snapshot
from criscostack.website.serve import get_response

local_manager = LocalManager(criscostack.local)

_site = None
_sites_path = os.environ.get("SITES_PATH", ".")


# If gc.freeze is done then importing modules before forking allows us to share the memory
if criscostack._tune_gc:
	import bleach
	import pydantic

	import criscostack.boot
	import criscostack.client
	import criscostack.core.doctype.file.file
	import criscostack.core.doctype.user.user
	import criscostack.database.mariadb.database  # Load database related utils
	import criscostack.database.query
	import criscostack.desk.desktop  # workspace
	import criscostack.desk.form.save
	import criscostack.model.db_query
	import criscostack.query_builder
	import criscostack.utils.background_jobs  # Enqueue is very common
	import criscostack.utils.data  # common utils
	import criscostack.utils.jinja  # web page rendering
	import criscostack.utils.jinja_globals
	import criscostack.utils.redis_wrapper  # Exact redis_wrapper
	import criscostack.utils.safe_exec
	import criscostack.utils.typing_validations  # any whitelisted method uses this
	import criscostack.website.path_resolver  # all the page types and resolver
	import criscostack.website.router  # Website router
	import criscostack.website.website_generator  # web page doctypes

# end: module pre-loading


@local_manager.middleware
@Request.application
def application(request: Request):
	response = None

	try:
		rollback = True

		init_request(request)

		criscostack.api.validate_auth()

		if request.method == "OPTIONS":
			response = Response()

		elif criscostack.form_dict.cmd:
			response = criscostack.handler.handle()

		elif request.path.startswith("/api/"):
			response = criscostack.api.handle()

		elif request.path.startswith("/backups"):
			response = criscostack.utils.response.download_backup(request.path)

		elif request.path.startswith("/private/files/"):
			response = criscostack.utils.response.download_private_file(request.path)

		elif request.method in ("GET", "HEAD", "POST"):
			response = get_response()

		else:
			raise NotFound

	except HTTPException as e:
		return e

	except Exception as e:
		response = handle_exception(e)

	else:
		rollback = sync_database(rollback)

	finally:
		# Important note:
		# this function *must* always return a response, hence any exception thrown outside of
		# try..catch block like this finally block needs to be handled appropriately.

		if request.method in UNSAFE_HTTP_METHODS and criscostack.db and rollback:
			criscostack.db.rollback()

		try:
			run_after_request_hooks(request, response)
		except Exception as e:
			# We can not handle exceptions safely here.
			criscostack.logger().error("Failed to run after request hook", exc_info=True)

		log_request(request, response)
		process_response(response)
		if criscostack.db:
			criscostack.db.close()

	return response


def run_after_request_hooks(request, response):
	if not getattr(criscostack.local, "initialised", False):
		return

	for after_request_task in criscostack.get_hooks("after_request"):
		criscostack.call(after_request_task, response=response, request=request)


def init_request(request):
	criscostack.local.request = request
	criscostack.local.is_ajax = criscostack.get_request_header("X-Requested-With") == "XMLHttpRequest"

	site = _site or request.headers.get("X-Crisco-Site-Name") or get_site_name(request.host)
	criscostack.init(site=site, sites_path=_sites_path, force=True)

	if not (criscostack.local.conf and criscostack.local.conf.db_name):
		# site does not exist
		raise NotFound

	if criscostack.local.conf.maintenance_mode:
		criscostack.connect()
		if criscostack.local.conf.allow_reads_during_maintenance:
			setup_read_only_mode()
		else:
			raise criscostack.SessionStopped("Session Stopped")
	else:
		criscostack.connect(set_admin_as_user=False)

	request.max_content_length = cint(criscostack.local.conf.get("max_file_size")) or 10 * 1024 * 1024

	make_form_dict(request)

	if request.method != "OPTIONS":
		criscostack.local.http_request = HTTPRequest()

	for before_request_task in criscostack.get_hooks("before_request"):
		criscostack.call(before_request_task)


def setup_read_only_mode():
	"""During maintenance_mode reads to DB can still be performed to reduce downtime. This
	function sets up read only mode

	- Setting global flag so other pages, desk and database can know that we are in read only mode.
	- Setup read only database access either by:
	    - Connecting to read replica if one exists
	    - Or setting up read only SQL transactions.
	"""
	criscostack.flags.read_only = True

	# If replica is available then just connect replica, else setup read only transaction.
	if criscostack.conf.read_from_replica:
		criscostack.connect_replica()
	else:
		criscostack.db.begin(read_only=True)


def log_request(request, response):
	if hasattr(criscostack.local, "conf") and criscostack.local.conf.enable_criscostack_logger:
		criscostack.logger("criscostack.web", allow_site=criscostack.local.site).info(
			{
				"site": get_site_name(request.host),
				"remote_addr": getattr(request, "remote_addr", "NOTFOUND"),
				"pid": os.getpid(),
				"user": getattr(criscostack.local.session, "user", "NOTFOUND"),
				"base_url": getattr(request, "base_url", "NOTFOUND"),
				"full_path": getattr(request, "full_path", "NOTFOUND"),
				"method": getattr(request, "method", "NOTFOUND"),
				"scheme": getattr(request, "scheme", "NOTFOUND"),
				"http_status_code": getattr(response, "status_code", "NOTFOUND"),
			}
		)


def process_response(response):
	if not response:
		return

	# set cookies
	if hasattr(criscostack.local, "cookie_manager"):
		criscostack.local.cookie_manager.flush_cookies(response=response)

	# rate limiter headers
	if hasattr(criscostack.local, "rate_limiter"):
		response.headers.extend(criscostack.local.rate_limiter.headers())

	# CORS headers
	if hasattr(criscostack.local, "conf"):
		set_cors_headers(response)


def set_cors_headers(response):
	if not (
		(allowed_origins := criscostack.conf.allow_cors)
		and (request := criscostack.local.request)
		and (origin := request.headers.get("Origin"))
	):
		return

	if allowed_origins != "*":
		if not isinstance(allowed_origins, list):
			allowed_origins = [allowed_origins]

		if origin not in allowed_origins:
			return

	cors_headers = {
		"Access-Control-Allow-Credentials": "true",
		"Access-Control-Allow-Origin": origin,
		"Vary": "Origin",
	}

	# only required for preflight requests
	if request.method == "OPTIONS":
		cors_headers["Access-Control-Allow-Methods"] = request.headers.get(
			"Access-Control-Request-Method"
		)

		if allowed_headers := request.headers.get("Access-Control-Request-Headers"):
			cors_headers["Access-Control-Allow-Headers"] = allowed_headers

		# allow browsers to cache preflight requests for upto a day
		if not criscostack.conf.developer_mode:
			cors_headers["Access-Control-Max-Age"] = "86400"

	response.headers.extend(cors_headers)


def make_form_dict(request):
	import json

	request_data = request.get_data(as_text=True)
	if "application/json" in (request.content_type or "") and request_data:
		args = json.loads(request_data)
	else:
		args = {}
		args.update(request.args or {})
		args.update(request.form or {})

	if not isinstance(args, dict):
		criscostack.throw(_("Invalid request arguments"))

	criscostack.local.form_dict = criscostack._dict(args)

	if "_" in criscostack.local.form_dict:
		# _ is passed by $.ajax so that the request is not cached by the browser. So, remove _ from form_dict
		criscostack.local.form_dict.pop("_")


def handle_exception(e):
	response = None
	http_status_code = getattr(e, "http_status_code", 500)
	return_as_message = False
	accept_header = criscostack.get_request_header("Accept") or ""
	respond_as_json = (
		criscostack.get_request_header("Accept")
		and (criscostack.local.is_ajax or "application/json" in accept_header)
		or (criscostack.local.request.path.startswith("/api/") and not accept_header.startswith("text"))
	)

	allow_traceback = criscostack.get_system_settings("allow_error_traceback") if criscostack.db else False

	if not criscostack.session.user:
		# If session creation fails then user won't be unset. This causes a lot of code that
		# assumes presence of this to fail. Session creation fails => guest or expired login
		# usually.
		criscostack.session.user = "Guest"

	if respond_as_json:
		# handle ajax responses first
		# if the request is ajax, send back the trace or error message
		response = criscostack.utils.response.report_error(http_status_code)

	elif isinstance(e, criscostack.SessionStopped):
		response = criscostack.utils.response.handle_session_stopped()

	elif (
		http_status_code == 500
		and (criscostack.db and isinstance(e, criscostack.db.InternalError))
		and (criscostack.db and (criscostack.db.is_deadlocked(e) or criscostack.db.is_timedout(e)))
	):
		http_status_code = 508

	elif http_status_code == 401:
		criscostack.respond_as_web_page(
			_("Session Expired"),
			_("Your session has expired, please login again to continue."),
			http_status_code=http_status_code,
			indicator_color="red",
		)
		return_as_message = True

	elif http_status_code == 403:
		criscostack.respond_as_web_page(
			_("Not Permitted"),
			_("You do not have enough permissions to complete the action"),
			http_status_code=http_status_code,
			indicator_color="red",
		)
		return_as_message = True

	elif http_status_code == 404:
		criscostack.respond_as_web_page(
			_("Not Found"),
			_("The resource you are looking for is not available"),
			http_status_code=http_status_code,
			indicator_color="red",
		)
		return_as_message = True

	elif http_status_code == 429:
		response = criscostack.rate_limiter.respond()

	else:
		traceback = "<pre>" + sanitize_html(criscostack.get_traceback()) + "</pre>"
		# disable traceback in production if flag is set
		if criscostack.local.flags.disable_traceback or not allow_traceback and not criscostack.local.dev_server:
			traceback = ""

		criscostack.respond_as_web_page(
			"Server Error", traceback, http_status_code=http_status_code, indicator_color="red", width=640
		)
		return_as_message = True

	if e.__class__ == criscostack.AuthenticationError:
		if hasattr(criscostack.local, "login_manager"):
			criscostack.local.login_manager.clear_cookies()

	if http_status_code >= 500:
		log_error_snapshot(e)

	if return_as_message:
		response = get_response("message", http_status_code=http_status_code)

	if criscostack.conf.get("developer_mode") and not respond_as_json:
		# don't fail silently for non-json response errors
		print(criscostack.get_traceback())

	return response


def sync_database(rollback: bool) -> bool:
	# if HTTP method would change server state, commit if necessary
	if (
		criscostack.db
		and (criscostack.local.flags.commit or criscostack.local.request.method in UNSAFE_HTTP_METHODS)
		and criscostack.db.transaction_writes
	):
		criscostack.db.commit()
		rollback = False
	elif criscostack.db:
		criscostack.db.rollback()
		rollback = False

	# update session
	if session := getattr(criscostack.local, "session_obj", None):
		if session.update():
			criscostack.db.commit()
			rollback = False

	return rollback


def serve(
	port=8000, profile=False, no_reload=False, no_threading=False, site=None, sites_path="."
):
	global application, _site, _sites_path
	_site = site
	_sites_path = sites_path

	from werkzeug.serving import run_simple

	if profile or os.environ.get("USE_PROFILER"):
		application = ProfilerMiddleware(application, sort_by=("cumtime", "calls"))

	if not os.environ.get("NO_STATICS"):
		application = SharedDataMiddleware(
			application, {"/assets": str(os.path.join(sites_path, "assets"))}
		)

		application = StaticDataMiddleware(application, {"/files": str(os.path.abspath(sites_path))})

	application.debug = True
	application.config = {"SERVER_NAME": "localhost:8000"}

	log = logging.getLogger("werkzeug")
	log.propagate = False

	in_test_env = os.environ.get("CI")
	if in_test_env:
		log.setLevel(logging.ERROR)

	run_simple(
		"0.0.0.0",
		int(port),
		application,
		exclude_patterns=["test_*"],
		use_reloader=False if in_test_env else not no_reload,
		use_debugger=not in_test_env,
		use_evalex=not in_test_env,
		threaded=not no_threading,
	)


# Remove references to pattern that are pre-compiled and loaded to global scopes.
re.purge()

# Both Gunicorn and RQ use forking to spawn workers. In an ideal world, the fork should be sharing
# most of the memory if there are no writes made to data because of Copy on Write, however,
# python's GC is not CoW friendly and writes to data even if user-code doesn't. Specifically, the
# generational GC which stores and mutates every python object: `PyGC_Head`
#
# Calling gc.freeze() moves all the objects imported so far into permanant generation and hence
# doesn't mutate `PyGC_Head`
#
# Refer to issue for more info: https://github.com/criscostack/criscostack/issues/18927
if criscostack._tune_gc:
	gc.collect()  # clean up any garbage created so far before freeze
	gc.freeze()
