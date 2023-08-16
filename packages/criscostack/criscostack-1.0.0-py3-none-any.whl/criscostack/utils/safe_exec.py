import copy
import inspect
import json
import mimetypes
import types
from contextlib import contextmanager
from functools import lru_cache

import RestrictedPython.Guards
from RestrictedPython import compile_restricted, safe_globals
from RestrictedPython.transformer import RestrictingNodeTransformer

import criscostack
import criscostack.exceptions
import criscostack.integrations.utils
import criscostack.utils
import criscostack.utils.data
from criscostack import _
from criscostack.core.utils import html2text
from criscostack.criscostackclient import CriscoClient
from criscostack.handler import execute_cmd
from criscostack.model.delete_doc import delete_doc
from criscostack.model.mapper import get_mapped_doc
from criscostack.model.rename_doc import rename_doc
from criscostack.modules import scrub
from criscostack.utils.background_jobs import enqueue, get_jobs
from criscostack.website.utils import get_next_link, get_toc
from criscostack.www.printview import get_visible_columns


class ServerScriptNotEnabled(criscostack.PermissionError):
	pass


class NamespaceDict(criscostack._dict):
	"""Raise AttributeError if function not found in namespace"""

	def __getattr__(self, key):
		ret = self.get(key)
		if (not ret and key.startswith("__")) or (key not in self):

			def default_function(*args, **kwargs):
				raise AttributeError(f"module has no attribute '{key}'")

			return default_function
		return ret


class CriscoTransformer(RestrictingNodeTransformer):
	def check_name(self, node, name, *args, **kwargs):
		if name == "_dict":
			return

		return super().check_name(node, name, *args, **kwargs)


def safe_exec(script, _globals=None, _locals=None, restrict_commit_rollback=False):
	# server scripts can be disabled via site_config.json
	# they are enabled by default
	if "server_script_enabled" in criscostack.conf:
		enabled = criscostack.conf.server_script_enabled
	else:
		enabled = True

	if not enabled:
		criscostack.throw(_("Please Enable Server Scripts"), ServerScriptNotEnabled)

	# build globals
	exec_globals = get_safe_globals()
	if _globals:
		exec_globals.update(_globals)

	if restrict_commit_rollback:
		# prevent user from using these in docevents
		exec_globals.criscostack.db.pop("commit", None)
		exec_globals.criscostack.db.pop("rollback", None)
		exec_globals.criscostack.db.pop("add_index", None)

	with safe_exec_flags(), patched_qb():
		# execute script compiled by RestrictedPython
		exec(
			compile_restricted(script, filename="<serverscript>", policy=CriscoTransformer),
			exec_globals,
			_locals,
		)

	return exec_globals, _locals


@contextmanager
def safe_exec_flags():
	criscostack.flags.in_safe_exec = True
	yield
	criscostack.flags.in_safe_exec = False


def get_safe_globals():
	datautils = criscostack._dict()

	if criscostack.db:
		date_format = criscostack.db.get_default("date_format") or "yyyy-mm-dd"
		time_format = criscostack.db.get_default("time_format") or "HH:mm:ss"
	else:
		date_format = "yyyy-mm-dd"
		time_format = "HH:mm:ss"

	add_data_utils(datautils)

	form_dict = getattr(criscostack.local, "form_dict", criscostack._dict())

	if "_" in form_dict:
		del criscostack.local.form_dict["_"]

	user = getattr(criscostack.local, "session", None) and criscostack.local.session.user or "Guest"

	out = NamespaceDict(
		# make available limited methods of criscostack
		json=NamespaceDict(loads=json.loads, dumps=json.dumps),
		as_json=criscostack.as_json,
		dict=dict,
		log=criscostack.log,
		_dict=criscostack._dict,
		args=form_dict,
		criscostack=NamespaceDict(
			call=call_whitelisted_function,
			flags=criscostack._dict(),
			format=criscostack.format_value,
			format_value=criscostack.format_value,
			date_format=date_format,
			time_format=time_format,
			format_date=criscostack.utils.data.global_date_format,
			form_dict=form_dict,
			bold=criscostack.bold,
			copy_doc=criscostack.copy_doc,
			errprint=criscostack.errprint,
			qb=criscostack.qb,
			get_meta=criscostack.get_meta,
			new_doc=criscostack.new_doc,
			get_doc=criscostack.get_doc,
			get_mapped_doc=get_mapped_doc,
			get_last_doc=criscostack.get_last_doc,
			get_cached_doc=criscostack.get_cached_doc,
			get_list=criscostack.get_list,
			get_all=criscostack.get_all,
			get_system_settings=criscostack.get_system_settings,
			rename_doc=rename_doc,
			delete_doc=delete_doc,
			utils=datautils,
			get_url=criscostack.utils.get_url,
			render_template=criscostack.render_template,
			msgprint=criscostack.msgprint,
			throw=criscostack.throw,
			sendmail=criscostack.sendmail,
			get_print=criscostack.get_print,
			attach_print=criscostack.attach_print,
			user=user,
			get_fullname=criscostack.utils.get_fullname,
			get_gravatar=criscostack.utils.get_gravatar_url,
			full_name=criscostack.local.session.data.full_name
			if getattr(criscostack.local, "session", None)
			else "Guest",
			request=getattr(criscostack.local, "request", {}),
			session=criscostack._dict(
				user=user,
				csrf_token=criscostack.local.session.data.csrf_token
				if getattr(criscostack.local, "session", None)
				else "",
			),
			make_get_request=criscostack.integrations.utils.make_get_request,
			make_post_request=criscostack.integrations.utils.make_post_request,
			make_put_request=criscostack.integrations.utils.make_put_request,
			socketio_port=criscostack.conf.socketio_port,
			get_hooks=get_hooks,
			enqueue=safe_enqueue,
			sanitize_html=criscostack.utils.sanitize_html,
			log_error=criscostack.log_error,
			log=criscostack.log,
			db=NamespaceDict(
				get_list=criscostack.get_list,
				get_all=criscostack.get_all,
				get_value=criscostack.db.get_value,
				set_value=criscostack.db.set_value,
				get_single_value=criscostack.db.get_single_value,
				get_default=criscostack.db.get_default,
				exists=criscostack.db.exists,
				count=criscostack.db.count,
				escape=criscostack.db.escape,
				sql=read_sql,
				commit=criscostack.db.commit,
				rollback=criscostack.db.rollback,
				add_index=criscostack.db.add_index,
			),
			lang=getattr(criscostack.local, "lang", "en"),
		),
		CriscoClient=CriscoClient,
		style=criscostack._dict(border_color="#d1d8dd"),
		get_toc=get_toc,
		get_next_link=get_next_link,
		_=criscostack._,
		scrub=scrub,
		guess_mimetype=mimetypes.guess_type,
		html2text=html2text,
		dev_server=criscostack.local.dev_server,
		run_script=run_script,
		is_job_queued=is_job_queued,
		get_visible_columns=get_visible_columns,
	)

	add_module_properties(
		criscostack.exceptions, out.criscostack, lambda obj: inspect.isclass(obj) and issubclass(obj, Exception)
	)

	if criscostack.response:
		out.criscostack.response = criscostack.response

	out.update(safe_globals)

	# default writer allows write access
	out._write_ = _write
	out._getitem_ = _getitem
	out._getattr_ = _getattr

	# allow iterators and list comprehension
	out._getiter_ = iter
	out._iter_unpack_sequence_ = RestrictedPython.Guards.guarded_iter_unpack_sequence

	# add common python builtins
	out.update(get_python_builtins())

	return out


def is_job_queued(job_name, queue="default"):
	"""
	:param job_name: used to identify a queued job, usually dotted path to function
	:param queue: should be either long, default or short
	"""

	site = criscostack.local.site
	queued_jobs = get_jobs(site=site, queue=queue, key="job_name").get(site)
	return queued_jobs and job_name in queued_jobs


def safe_enqueue(function, **kwargs):
	"""
	Enqueue function to be executed using a background worker
	Accepts criscostack.enqueue params like job_name, queue, timeout, etc.
	in addition to params to be passed to function

	:param function: whitelised function or API Method set in Server Script
	"""

	return enqueue("criscostack.utils.safe_exec.call_whitelisted_function", function=function, **kwargs)


def call_whitelisted_function(function, **kwargs):
	"""Executes a whitelisted function or Server Script of type API"""

	return call_with_form_dict(lambda: execute_cmd(function), kwargs)


def run_script(script, **kwargs):
	"""run another server script"""

	return call_with_form_dict(
		lambda: criscostack.get_doc("Server Script", script).execute_method(), kwargs
	)


def call_with_form_dict(function, kwargs):
	# temporarily update form_dict, to use inside below call
	form_dict = getattr(criscostack.local, "form_dict", criscostack._dict())
	if kwargs:
		criscostack.local.form_dict = form_dict.copy().update(kwargs)

	try:
		return function()
	finally:
		criscostack.local.form_dict = form_dict


@contextmanager
def patched_qb():
	require_patching = isinstance(criscostack.qb.terms, types.ModuleType)
	try:
		if require_patching:
			_terms = criscostack.qb.terms
			criscostack.qb.terms = _flatten(criscostack.qb.terms)
		yield
	finally:
		if require_patching:
			criscostack.qb.terms = _terms


@lru_cache
def _flatten(module):
	new_mod = NamespaceDict()
	for name, obj in inspect.getmembers(module, lambda x: not inspect.ismodule(x)):
		if not name.startswith("_"):
			new_mod[name] = obj
	return new_mod


def get_python_builtins():
	return {
		"abs": abs,
		"all": all,
		"any": any,
		"bool": bool,
		"dict": dict,
		"enumerate": enumerate,
		"isinstance": isinstance,
		"issubclass": issubclass,
		"list": list,
		"max": max,
		"min": min,
		"range": range,
		"set": set,
		"sorted": sorted,
		"sum": sum,
		"tuple": tuple,
	}


def get_hooks(hook=None, default=None, app_name=None):
	hooks = criscostack.get_hooks(hook=hook, default=default, app_name=app_name)
	return copy.deepcopy(hooks)


def read_sql(query, *args, **kwargs):
	"""a wrapper for criscostack.db.sql to allow reads"""
	query = str(query)
	check_safe_sql_query(query)
	return criscostack.db.sql(query, *args, **kwargs)


def check_safe_sql_query(query: str, throw: bool = True) -> bool:
	"""Check if SQL query is safe for running in restricted context.

	Safe queries:
	        1. Read only 'select' or 'explain' queries
	        2. CTE on mariadb where writes are not allowed.
	"""

	query = query.strip().lower()
	whitelisted_statements = ("select", "explain")

	if query.startswith(whitelisted_statements) or (
		query.startswith("with") and criscostack.db.db_type == "mariadb"
	):
		return True

	if throw:
		criscostack.throw(
			_("Query must be of SELECT or read-only WITH type."),
			title=_("Unsafe SQL query"),
			exc=criscostack.PermissionError,
		)

	return False


def _getitem(obj, key):
	# guard function for RestrictedPython
	# allow any key to be accessed as long as it does not start with underscore
	if isinstance(key, str) and key.startswith("_"):
		raise SyntaxError("Key starts with _")
	return obj[key]


def _getattr(object, name, default=None):
	# guard function for RestrictedPython
	# allow any key to be accessed as long as
	# 1. it does not start with an underscore (safer_getattr)
	# 2. it is not an UNSAFE_ATTRIBUTES

	UNSAFE_ATTRIBUTES = {
		# Generator Attributes
		"gi_frame",
		"gi_code",
		# Coroutine Attributes
		"cr_frame",
		"cr_code",
		"cr_origin",
		# Async Generator Attributes
		"ag_code",
		"ag_frame",
		# Traceback Attributes
		"tb_frame",
		"tb_next",
	}

	if isinstance(name, str) and (name in UNSAFE_ATTRIBUTES):
		raise SyntaxError(f"{name} is an unsafe attribute")

	if isinstance(object, (types.ModuleType, types.CodeType, types.TracebackType, types.FrameType)):
		raise SyntaxError(f"Reading {object} attributes is not allowed")

	return RestrictedPython.Guards.safer_getattr(object, name, default=default)


def _write(obj):
	# guard function for RestrictedPython
	# allow writing to any object
	return obj


def add_data_utils(data):
	for key, obj in criscostack.utils.data.__dict__.items():
		if key in VALID_UTILS:
			data[key] = obj


def add_module_properties(module, data, filter_method):
	for key, obj in module.__dict__.items():
		if key.startswith("_"):
			# ignore
			continue

		if filter_method(obj):
			# only allow functions
			data[key] = obj


VALID_UTILS = (
	"DATE_FORMAT",
	"TIME_FORMAT",
	"DATETIME_FORMAT",
	"is_invalid_date_string",
	"getdate",
	"get_datetime",
	"to_timedelta",
	"get_timedelta",
	"add_to_date",
	"add_days",
	"add_months",
	"add_years",
	"date_diff",
	"month_diff",
	"time_diff",
	"time_diff_in_seconds",
	"time_diff_in_hours",
	"now_datetime",
	"get_timestamp",
	"get_eta",
	"get_system_timezone",
	"convert_utc_to_system_timezone",
	"now",
	"nowdate",
	"today",
	"nowtime",
	"get_first_day",
	"get_quarter_start",
	"get_quarter_ending",
	"get_first_day_of_week",
	"get_year_start",
	"get_last_day_of_week",
	"get_last_day",
	"get_time",
	"get_datetime_in_timezone",
	"get_datetime_str",
	"get_date_str",
	"get_time_str",
	"get_user_date_format",
	"get_user_time_format",
	"format_date",
	"format_time",
	"format_datetime",
	"format_duration",
	"get_weekdays",
	"get_weekday",
	"get_timespan_date_range",
	"global_date_format",
	"has_common",
	"flt",
	"cint",
	"floor",
	"ceil",
	"cstr",
	"rounded",
	"remainder",
	"safe_div",
	"round_based_on_smallest_currency_fraction",
	"encode",
	"parse_val",
	"fmt_money",
	"get_number_format_info",
	"money_in_words",
	"in_words",
	"is_html",
	"is_image",
	"get_thumbnail_base64_for_image",
	"image_to_base64",
	"pdf_to_base64",
	"strip_html",
	"escape_html",
	"pretty_date",
	"comma_or",
	"comma_and",
	"comma_sep",
	"new_line_sep",
	"filter_strip_join",
	"get_url",
	"get_host_name_from_request",
	"url_contains_port",
	"get_host_name",
	"get_link_to_form",
	"get_link_to_report",
	"get_absolute_url",
	"get_url_to_form",
	"get_url_to_list",
	"get_url_to_report",
	"get_url_to_report_with_filters",
	"evaluate_filters",
	"compare",
	"get_filter",
	"make_filter_tuple",
	"make_filter_dict",
	"sanitize_column",
	"scrub_urls",
	"expand_relative_urls",
	"quoted",
	"quote_urls",
	"unique",
	"strip",
	"to_markdown",
	"md_to_html",
	"markdown",
	"is_subset",
	"generate_hash",
	"formatdate",
	"get_user_info_for_avatar",
	"get_abbr",
)
