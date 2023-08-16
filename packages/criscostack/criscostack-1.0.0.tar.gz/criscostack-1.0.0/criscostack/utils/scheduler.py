# Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE
"""
Events:
	always
	daily
	monthly
	weekly
"""

# imports - standard imports
import os
import time
from typing import NoReturn

# imports - module imports
import criscostack
from criscostack.utils import cint, get_datetime, get_sites, now_datetime
from criscostack.utils.background_jobs import set_niceness

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def cprint(*args, **kwargs):
	"""Prints only if called from STDOUT"""
	try:
		os.get_terminal_size()
		print(*args, **kwargs)
	except Exception:
		pass


def start_scheduler() -> NoReturn:
	"""Run enqueue_events_for_all_sites based on scheduler tick.
	Specify scheduler_interval in seconds in common_site_config.json"""

	tick = cint(criscostack.get_conf().scheduler_tick_interval) or 60
	set_niceness()

	while True:
		time.sleep(tick)
		enqueue_events_for_all_sites()


def enqueue_events_for_all_sites() -> None:
	"""Loop through sites and enqueue events that are not already queued"""

	if os.path.exists(os.path.join(".", ".restarting")):
		# Don't add task to queue if webserver is in restart mode
		return

	with criscostack.init_site():
		sites = get_sites()

	for site in sites:
		try:
			enqueue_events_for_site(site=site)
		except Exception:
			criscostack.logger("scheduler").debug(f"Failed to enqueue events for site: {site}", exc_info=True)


def enqueue_events_for_site(site: str) -> None:
	def log_exc():
		criscostack.logger("scheduler").error(f"Exception in Enqueue Events for Site {site}", exc_info=True)

	try:
		criscostack.init(site=site)
		criscostack.connect()
		if is_scheduler_inactive():
			return

		enqueue_events(site=site)

		criscostack.logger("scheduler").debug(f"Queued events for site {site}")
	except Exception as e:
		if criscostack.db.is_access_denied(e):
			criscostack.logger("scheduler").debug(f"Access denied for site {site}")
		log_exc()

	finally:
		criscostack.destroy()


def enqueue_events(site: str) -> list[str] | None:
	if schedule_jobs_based_on_activity():
		enqueued_jobs = []
		for job_type in criscostack.get_all("Scheduled Job Type", filters={"stopped": 0}, fields="*"):
			job_type = criscostack.get_doc(doctype="Scheduled Job Type", **job_type)
			if job_type.enqueue():
				enqueued_jobs.append(job_type.method)

		return enqueued_jobs


def is_scheduler_inactive(verbose=True) -> bool:
	if criscostack.local.conf.maintenance_mode:
		if verbose:
			cprint(f"{criscostack.local.site}: Maintenance mode is ON")
		return True

	if criscostack.local.conf.pause_scheduler:
		if verbose:
			cprint(f"{criscostack.local.site}: criscostack.conf.pause_scheduler is SET")
		return True

	if is_scheduler_disabled(verbose=verbose):
		return True

	return False


def is_scheduler_disabled(verbose=True) -> bool:
	if criscostack.conf.disable_scheduler:
		if verbose:
			cprint(f"{criscostack.local.site}: criscostack.conf.disable_scheduler is SET")
		return True

	scheduler_disabled = not criscostack.utils.cint(
		criscostack.db.get_single_value("System Settings", "enable_scheduler")
	)
	if scheduler_disabled:
		if verbose:
			cprint(f"{criscostack.local.site}: SystemSettings.enable_scheduler is UNSET")
	return scheduler_disabled


def toggle_scheduler(enable):
	criscostack.db.set_single_value("System Settings", "enable_scheduler", int(enable))


def enable_scheduler():
	toggle_scheduler(True)


def disable_scheduler():
	toggle_scheduler(False)


def schedule_jobs_based_on_activity(check_time=None):
	"""Returns True for active sites defined by Activity Log
	Returns True for inactive sites once in 24 hours"""
	if is_dormant(check_time=check_time):
		# ensure last job is one day old
		last_job_timestamp = _get_last_modified_timestamp("Scheduled Job Log")
		if not last_job_timestamp:
			return True
		else:
			if ((check_time or now_datetime()) - last_job_timestamp).total_seconds() >= 86400:
				# one day is passed since jobs are run, so lets do this
				return True
			else:
				# schedulers run in the last 24 hours, do nothing
				return False
	else:
		# site active, lets run the jobs
		return True


def is_dormant(check_time=None):
	last_activity_log_timestamp = _get_last_modified_timestamp("Activity Log")
	since = (criscostack.get_system_settings("dormant_days") or 4) * 86400
	if not last_activity_log_timestamp:
		return True
	if ((check_time or now_datetime()) - last_activity_log_timestamp).total_seconds() >= since:
		return True
	return False


def _get_last_modified_timestamp(doctype):
	timestamp = criscostack.db.get_value(
		doctype, filters={}, fieldname="modified", order_by="modified desc"
	)
	if timestamp:
		return get_datetime(timestamp)


@criscostack.whitelist()
def activate_scheduler():
	from criscostack.installer import update_site_config

	criscostack.only_for("Administrator")

	if criscostack.local.conf.maintenance_mode:
		criscostack.throw(criscostack._("Scheduler can not be re-enabled when maintenance mode is active."))

	if is_scheduler_disabled():
		enable_scheduler()
	if criscostack.conf.pause_scheduler:
		update_site_config("pause_scheduler", 0)


@criscostack.whitelist()
def get_scheduler_status():
	if is_scheduler_inactive():
		return {"status": "inactive"}
	return {"status": "active"}
