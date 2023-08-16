# Copyright (c) 2021, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE
"""
Boot session from cache or build

Session bootstraps info needed by common client side activities including
permission, homepage, default variables, system defaults etc
"""
import json
from urllib.parse import unquote

import redis

import criscostack
import criscostack.defaults
import criscostack.model.meta
import criscostack.translate
import criscostack.utils
from criscostack import _
from criscostack.cache_manager import clear_user_cache
from criscostack.query_builder import Order
from criscostack.utils import cint, cstr, get_assets_json
from criscostack.utils.data import add_to_date


@criscostack.whitelist()
def clear():
	criscostack.local.session_obj.update(force=True)
	criscostack.local.db.commit()
	clear_user_cache(criscostack.session.user)
	criscostack.response["message"] = _("Cache Cleared")


def clear_sessions(user=None, keep_current=False, force=False):
	"""Clear other sessions of the current user. Called at login / logout

	:param user: user name (default: current user)
	:param keep_current: keep current session (default: false)
	:param force: triggered by the user (default false)
	"""

	reason = "Logged In From Another Session"
	if force:
		reason = "Force Logged out by the user"

	for sid in get_sessions_to_clear(user, keep_current):
		delete_session(sid, reason=reason)


def get_sessions_to_clear(user=None, keep_current=False):
	"""Returns sessions of the current user. Called at login / logout

	:param user: user name (default: current user)
	:param keep_current: keep current session (default: false)
	"""
	if not user:
		user = criscostack.session.user

	offset = 0
	if user == criscostack.session.user:
		simultaneous_sessions = criscostack.db.get_value("User", user, "simultaneous_sessions") or 1
		offset = simultaneous_sessions - 1

	session = criscostack.qb.DocType("Sessions")
	session_id = criscostack.qb.from_(session).where(session.user == user)
	if keep_current:
		session_id = session_id.where(session.sid != criscostack.session.sid)

	query = (
		session_id.select(session.sid)
		.offset(offset)
		.limit(100)
		.orderby(session.lastupdate, order=Order.desc)
	)

	return query.run(pluck=True)


def delete_session(sid=None, user=None, reason="Session Expired"):
	from criscostack.core.doctype.activity_log.feed import logout_feed

	if criscostack.flags.read_only:
		# This isn't manually initated logout, most likely user's cookies were expired in such case
		# we should just ignore it till database is back up again.
		return

	criscostack.cache.hdel("session", sid)
	criscostack.cache.hdel("last_db_session_update", sid)
	if sid and not user:
		table = criscostack.qb.DocType("Sessions")
		user_details = (
			criscostack.qb.from_(table).where(table.sid == sid).select(table.user).run(as_dict=True)
		)
		if user_details:
			user = user_details[0].get("user")

	logout_feed(user, reason)
	criscostack.db.delete("Sessions", {"sid": sid})
	criscostack.db.commit()


def clear_all_sessions(reason=None):
	"""This effectively logs out all users"""
	criscostack.only_for("Administrator")
	if not reason:
		reason = "Deleted All Active Session"
	for sid in criscostack.qb.from_("Sessions").select("sid").run(pluck=True):
		delete_session(sid, reason=reason)


def get_expired_sessions():
	"""Returns list of expired sessions"""

	sessions = criscostack.qb.DocType("Sessions")
	return (
		criscostack.qb.from_(sessions)
		.select(sessions.sid)
		.where(sessions.lastupdate < get_expired_threshold())
	).run(pluck=True)


def clear_expired_sessions():
	"""This function is meant to be called from scheduler"""
	for sid in get_expired_sessions():
		delete_session(sid, reason="Session Expired")


def get():
	"""get session boot info"""
	from criscostack.boot import get_bootinfo, get_unseen_notes
	from criscostack.utils.change_log import get_change_log

	bootinfo = None
	if not getattr(criscostack.conf, "disable_session_cache", None):
		# check if cache exists
		bootinfo = criscostack.cache.hget("bootinfo", criscostack.session.user)
		if bootinfo:
			bootinfo["from_cache"] = 1
			bootinfo["user"]["recent"] = json.dumps(criscostack.cache.hget("user_recent", criscostack.session.user))

	if not bootinfo:
		# if not create it
		bootinfo = get_bootinfo()
		criscostack.cache.hset("bootinfo", criscostack.session.user, bootinfo)
		try:
			criscostack.cache.ping()
		except redis.exceptions.ConnectionError:
			message = _("Redis cache server not running. Please contact Administrator / Tech support")
			if "messages" in bootinfo:
				bootinfo["messages"].append(message)
			else:
				bootinfo["messages"] = [message]

		# check only when clear cache is done, and don't cache this
		if criscostack.local.request:
			bootinfo["change_log"] = get_change_log()

	bootinfo["metadata_version"] = criscostack.cache.get_value("metadata_version")
	if not bootinfo["metadata_version"]:
		bootinfo["metadata_version"] = criscostack.reset_metadata_version()

	bootinfo.notes = get_unseen_notes()
	bootinfo.assets_json = get_assets_json()
	bootinfo.read_only = bool(criscostack.flags.read_only)

	for hook in criscostack.get_hooks("extend_bootinfo"):
		criscostack.get_attr(hook)(bootinfo=bootinfo)

	bootinfo["lang"] = criscostack.translate.get_user_lang()
	bootinfo["disable_async"] = criscostack.conf.disable_async

	bootinfo["setup_complete"] = cint(criscostack.get_system_settings("setup_complete"))

	bootinfo["desk_theme"] = criscostack.db.get_value("User", criscostack.session.user, "desk_theme") or "Light"

	return bootinfo


@criscostack.whitelist()
def get_boot_assets_json():
	return get_assets_json()


def get_csrf_token():
	if not criscostack.local.session.data.csrf_token:
		generate_csrf_token()

	return criscostack.local.session.data.csrf_token


def generate_csrf_token():
	criscostack.local.session.data.csrf_token = criscostack.generate_hash()
	if not criscostack.flags.in_test:
		criscostack.local.session_obj.update(force=True)


class Session:
	__slots__ = ("user", "user_type", "full_name", "data", "time_diff", "sid")

	def __init__(self, user, resume=False, full_name=None, user_type=None):
		self.sid = cstr(
			criscostack.form_dict.get("sid") or unquote(criscostack.request.cookies.get("sid", "Guest"))
		)
		self.user = user
		self.user_type = user_type
		self.full_name = full_name
		self.data = criscostack._dict({"data": criscostack._dict({})})
		self.time_diff = None

		# set local session
		criscostack.local.session = self.data

		if resume:
			self.resume()

		else:
			if self.user:
				self.start()

	def start(self):
		"""start a new session"""
		# generate sid
		if self.user == "Guest":
			sid = "Guest"
		else:
			sid = criscostack.generate_hash()

		self.data.user = self.user
		self.sid = self.data.sid = sid
		self.data.data.user = self.user
		self.data.data.session_ip = criscostack.local.request_ip
		if self.user != "Guest":
			self.data.data.update(
				{
					"last_updated": criscostack.utils.now(),
					"session_expiry": get_expiry_period(),
					"full_name": self.full_name,
					"user_type": self.user_type,
				}
			)

		# insert session
		if self.user != "Guest":
			self.insert_session_record()

			# update user
			user = criscostack.get_doc("User", self.data["user"])
			user_doctype = criscostack.qb.DocType("User")
			(
				criscostack.qb.update(user_doctype)
				.set(user_doctype.last_login, criscostack.utils.now())
				.set(user_doctype.last_ip, criscostack.local.request_ip)
				.set(user_doctype.last_active, criscostack.utils.now())
				.where(user_doctype.name == self.data["user"])
			).run()

			user.run_notifications("before_change")
			user.run_notifications("on_update")
			criscostack.db.commit()

	def insert_session_record(self):

		Sessions = criscostack.qb.DocType("Sessions")
		now = criscostack.utils.now()

		(
			criscostack.qb.into(Sessions)
			.columns(
				Sessions.sessiondata, Sessions.user, Sessions.lastupdate, Sessions.sid, Sessions.status
			)
			.insert((str(self.data["data"]), self.data["user"], now, self.data["sid"], "Active"))
		).run()
		criscostack.cache.hset("session", self.data.sid, self.data)

	def resume(self):
		"""non-login request: load a session"""
		import criscostack
		from criscostack.auth import validate_ip_address

		data = self.get_session_record()

		if data:
			self.data.update({"data": data, "user": data.user, "sid": self.sid})
			self.user = data.user
			validate_ip_address(self.user)
		else:
			self.start_as_guest()

		if self.sid != "Guest":
			criscostack.local.user_lang = criscostack.translate.get_user_lang(self.data.user)
			criscostack.local.lang = criscostack.local.user_lang

	def get_session_record(self):
		"""get session record, or return the standard Guest Record"""
		from criscostack.auth import clear_cookies

		r = self.get_session_data()

		if not r:
			criscostack.response["session_expired"] = 1
			clear_cookies()
			self.sid = "Guest"
			r = self.get_session_data()

		return r

	def get_session_data(self):
		if self.sid == "Guest":
			return criscostack._dict({"user": "Guest"})

		data = self.get_session_data_from_cache()
		if not data:
			data = self.get_session_data_from_db()
		return data

	def get_session_data_from_cache(self):
		data = criscostack.cache.hget("session", self.sid)
		if data:
			data = criscostack._dict(data)
			session_data = data.get("data", {})

			# set user for correct timezone
			self.time_diff = criscostack.utils.time_diff_in_seconds(
				criscostack.utils.now(), session_data.get("last_updated")
			)
			expiry = get_expiry_in_seconds(session_data.get("session_expiry"))

			if self.time_diff > expiry:
				self._delete_session()
				data = None

		return data and data.data

	def get_session_data_from_db(self):
		sessions = criscostack.qb.DocType("Sessions")

		record = (
			criscostack.qb.from_(sessions)
			.select(sessions.user, sessions.sessiondata)
			.where(sessions.sid == self.sid)
			.where(sessions.lastupdate > get_expired_threshold())
		).run()

		if record:
			data = criscostack._dict(criscostack.safe_eval(record and record[0][1] or "{}"))
			data.user = record[0][0]
		else:
			self._delete_session()
			data = None

		return data

	def _delete_session(self):
		delete_session(self.sid, reason="Session Expired")

	def start_as_guest(self):
		"""all guests share the same 'Guest' session"""
		self.user = "Guest"
		self.start()

	def update(self, force=False):
		"""extend session expiry"""
		if criscostack.session["user"] == "Guest" or criscostack.form_dict.cmd == "logout":
			return

		now = criscostack.utils.now()

		Sessions = criscostack.qb.DocType("Sessions")

		self.data["data"]["last_updated"] = now
		self.data["data"]["lang"] = str(criscostack.lang)

		# update session in db
		last_updated = criscostack.cache.hget("last_db_session_update", self.sid)
		time_diff = criscostack.utils.time_diff_in_seconds(now, last_updated) if last_updated else None

		# database persistence is secondary, don't update it too often
		updated_in_db = False
		if (force or (time_diff is None) or (time_diff > 600)) and not criscostack.flags.read_only:
			# update sessions table
			(
				criscostack.qb.update(Sessions)
				.where(Sessions.sid == self.data["sid"])
				.set(Sessions.sessiondata, str(self.data["data"]))
				.set(Sessions.lastupdate, now)
			).run()

			criscostack.db.set_value("User", criscostack.session.user, "last_active", now, update_modified=False)

			criscostack.db.commit()
			criscostack.cache.hset("last_db_session_update", self.sid, now)

			updated_in_db = True

		criscostack.cache.hset("session", self.sid, self.data)

		return updated_in_db


def get_expiry_period_for_query():
	if criscostack.db.db_type == "postgres":
		return get_expiry_period()
	else:
		return get_expiry_in_seconds()


def get_expiry_in_seconds(expiry=None):
	if not expiry:
		expiry = get_expiry_period()

	parts = expiry.split(":")
	return (cint(parts[0]) * 3600) + (cint(parts[1]) * 60) + cint(parts[2])


def get_expired_threshold():
	"""Get cutoff time before which all sessions are considered expired."""

	now = criscostack.utils.now()
	expiry_in_seconds = get_expiry_in_seconds()

	return add_to_date(now, seconds=-expiry_in_seconds, as_string=True)


def get_expiry_period():
	exp_sec = criscostack.defaults.get_global_default("session_expiry") or "06:00:00"

	# incase seconds is missing
	if len(exp_sec.split(":")) == 2:
		exp_sec = exp_sec + ":00"

	return exp_sec


def get_geo_from_ip(ip_addr):
	try:
		from geolite2 import geolite2

		with geolite2 as f:
			reader = f.reader()
			data = reader.get(ip_addr)

			return criscostack._dict(data)
	except ImportError:
		return
	except ValueError:
		return
	except TypeError:
		return


def get_geo_ip_country(ip_addr):
	match = get_geo_from_ip(ip_addr)
	if match:
		return match.country
