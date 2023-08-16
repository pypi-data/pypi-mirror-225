from . import __version__ as app_version

app_name = "criscostack"
app_title = "Crisco Framework"
app_publisher = "Crisco Technologies"
app_description = "Full stack web framework with Python, Javascript, MariaDB, Redis, Node"
source_link = "https://github.com/criscostack/criscostack"
app_license = "MIT"
app_logo_url = "/assets/criscostack/images/criscostack-framework-logo.svg"

develop_version = "15.x.x-develop"

app_email = "developers@criscostack.io"

docs_app = "criscostack_docs"

translator_url = "https://translate.criscoerp.com"

before_install = "criscostack.utils.install.before_install"
after_install = "criscostack.utils.install.after_install"

page_js = {"setup-wizard": "public/js/criscostack/setup_wizard.js"}

# website
app_include_js = [
	"libs.bundle.js",
	"desk.bundle.js",
	"list.bundle.js",
	"form.bundle.js",
	"controls.bundle.js",
	"report.bundle.js",
	"telemetry.bundle.js",
]
app_include_css = [
	"desk.bundle.css",
	"report.bundle.css",
]

doctype_js = {
	"Web Page": "public/js/criscostack/utils/web_template.js",
	"Website Settings": "public/js/criscostack/utils/web_template.js",
}

web_include_js = ["website_script.js"]

web_include_css = []

email_css = ["email.bundle.css"]

website_route_rules = [
	{"from_route": "/blog/<category>", "to_route": "Blog Post"},
	{"from_route": "/kb/<category>", "to_route": "Help Article"},
	{"from_route": "/newsletters", "to_route": "Newsletter"},
	{"from_route": "/profile", "to_route": "me"},
	{"from_route": "/app/<path:app_path>", "to_route": "app"},
]

website_redirects = [
	{"source": r"/desk(.*)", "target": r"/app\1"},
]

base_template = "templates/base.html"

write_file_keys = ["file_url", "file_name"]

notification_config = "criscostack.core.notifications.get_notification_config"

before_tests = "criscostack.utils.install.before_tests"

email_append_to = ["Event", "ToDo", "Communication"]

calendars = ["Event"]

leaderboards = "criscostack.desk.leaderboard.get_leaderboards"

# login

on_session_creation = [
	"criscostack.core.doctype.activity_log.feed.login_feed",
	"criscostack.core.doctype.user.user.notify_admin_access_to_system_manager",
]

on_logout = (
	"criscostack.core.doctype.session_default_settings.session_default_settings.clear_session_defaults"
)

# PDF
pdf_header_html = "criscostack.utils.pdf.pdf_header_html"
pdf_body_html = "criscostack.utils.pdf.pdf_body_html"
pdf_footer_html = "criscostack.utils.pdf.pdf_footer_html"

# permissions

permission_query_conditions = {
	"Event": "criscostack.desk.doctype.event.event.get_permission_query_conditions",
	"ToDo": "criscostack.desk.doctype.todo.todo.get_permission_query_conditions",
	"User": "criscostack.core.doctype.user.user.get_permission_query_conditions",
	"Dashboard Settings": "criscostack.desk.doctype.dashboard_settings.dashboard_settings.get_permission_query_conditions",
	"Notification Log": "criscostack.desk.doctype.notification_log.notification_log.get_permission_query_conditions",
	"Dashboard": "criscostack.desk.doctype.dashboard.dashboard.get_permission_query_conditions",
	"Dashboard Chart": "criscostack.desk.doctype.dashboard_chart.dashboard_chart.get_permission_query_conditions",
	"Number Card": "criscostack.desk.doctype.number_card.number_card.get_permission_query_conditions",
	"Notification Settings": "criscostack.desk.doctype.notification_settings.notification_settings.get_permission_query_conditions",
	"Note": "criscostack.desk.doctype.note.note.get_permission_query_conditions",
	"Kanban Board": "criscostack.desk.doctype.kanban_board.kanban_board.get_permission_query_conditions",
	"Contact": "criscostack.contacts.address_and_contact.get_permission_query_conditions_for_contact",
	"Address": "criscostack.contacts.address_and_contact.get_permission_query_conditions_for_address",
	"Communication": "criscostack.core.doctype.communication.communication.get_permission_query_conditions_for_communication",
	"Workflow Action": "criscostack.workflow.doctype.workflow_action.workflow_action.get_permission_query_conditions",
	"Prepared Report": "criscostack.core.doctype.prepared_report.prepared_report.get_permission_query_condition",
	"File": "criscostack.core.doctype.file.file.get_permission_query_conditions",
}

has_permission = {
	"Event": "criscostack.desk.doctype.event.event.has_permission",
	"ToDo": "criscostack.desk.doctype.todo.todo.has_permission",
	"User": "criscostack.core.doctype.user.user.has_permission",
	"Dashboard Chart": "criscostack.desk.doctype.dashboard_chart.dashboard_chart.has_permission",
	"Number Card": "criscostack.desk.doctype.number_card.number_card.has_permission",
	"Kanban Board": "criscostack.desk.doctype.kanban_board.kanban_board.has_permission",
	"Contact": "criscostack.contacts.address_and_contact.has_permission",
	"Address": "criscostack.contacts.address_and_contact.has_permission",
	"Communication": "criscostack.core.doctype.communication.communication.has_permission",
	"Workflow Action": "criscostack.workflow.doctype.workflow_action.workflow_action.has_permission",
	"File": "criscostack.core.doctype.file.file.has_permission",
	"Prepared Report": "criscostack.core.doctype.prepared_report.prepared_report.has_permission",
}

has_website_permission = {
	"Address": "criscostack.contacts.doctype.address.address.has_website_permission"
}

jinja = {
	"methods": "criscostack.utils.jinja_globals",
	"filters": [
		"criscostack.utils.data.global_date_format",
		"criscostack.utils.markdown",
		"criscostack.website.utils.abs_url",
	],
}

standard_queries = {"User": "criscostack.core.doctype.user.user.user_query"}

doc_events = {
	"*": {
		"on_update": [
			"criscostack.desk.notifications.clear_doctype_notifications",
			"criscostack.workflow.doctype.workflow_action.workflow_action.process_workflow_actions",
			"criscostack.automation.doctype.assignment_rule.assignment_rule.apply",
			"criscostack.core.doctype.file.utils.attach_files_to_document",
			"criscostack.automation.doctype.assignment_rule.assignment_rule.update_due_date",
			"criscostack.core.doctype.user_type.user_type.apply_permissions_for_non_standard_user_type",
		],
		"after_rename": "criscostack.desk.notifications.clear_doctype_notifications",
		"on_cancel": [
			"criscostack.desk.notifications.clear_doctype_notifications",
			"criscostack.workflow.doctype.workflow_action.workflow_action.process_workflow_actions",
		],
		"on_trash": [
			"criscostack.desk.notifications.clear_doctype_notifications",
			"criscostack.workflow.doctype.workflow_action.workflow_action.process_workflow_actions",
		],
		"on_update_after_submit": [
			"criscostack.workflow.doctype.workflow_action.workflow_action.process_workflow_actions"
		],
		"on_change": [
			"criscostack.social.doctype.energy_point_rule.energy_point_rule.process_energy_points",
			"criscostack.automation.doctype.milestone_tracker.milestone_tracker.evaluate_milestone",
		],
	},
	"Event": {
		"after_insert": "criscostack.integrations.doctype.google_calendar.google_calendar.insert_event_in_google_calendar",
		"on_update": "criscostack.integrations.doctype.google_calendar.google_calendar.update_event_in_google_calendar",
		"on_trash": "criscostack.integrations.doctype.google_calendar.google_calendar.delete_event_from_google_calendar",
	},
	"Contact": {
		"after_insert": "criscostack.integrations.doctype.google_contacts.google_contacts.insert_contacts_to_google_contacts",
		"on_update": "criscostack.integrations.doctype.google_contacts.google_contacts.update_contacts_to_google_contacts",
	},
	"DocType": {
		"on_update": "criscostack.cache_manager.build_domain_restriced_doctype_cache",
	},
	"Page": {
		"on_update": "criscostack.cache_manager.build_domain_restriced_page_cache",
	},
}

scheduler_events = {
	"cron": {
		"0/15 * * * *": [
			"criscostack.oauth.delete_oauth2_data",
			"criscostack.website.doctype.web_page.web_page.check_publish_status",
			"criscostack.twofactor.delete_all_barcodes_for_users",
		],
		"0/10 * * * *": [
			"criscostack.email.doctype.email_account.email_account.pull",
		],
		# Hourly but offset by 30 minutes
		"30 * * * *": [
			"criscostack.core.doctype.prepared_report.prepared_report.expire_stalled_report",
		],
		# Daily but offset by 45 minutes
		"45 0 * * *": [
			"criscostack.core.doctype.log_settings.log_settings.run_log_clean_up",
		],
	},
	"all": [
		"criscostack.email.queue.flush",
		"criscostack.email.doctype.email_account.email_account.notify_unreplied",
		"criscostack.utils.global_search.sync_global_search",
		"criscostack.monitor.flush",
		"criscostack.automation.doctype.reminder.reminder.send_reminders",
	],
	"hourly": [
		"criscostack.model.utils.link_count.update_link_count",
		"criscostack.model.utils.user_settings.sync_user_settings",
		"criscostack.desk.page.backups.backups.delete_downloadable_backups",
		"criscostack.deferred_insert.save_to_db",
		"criscostack.desk.form.document_follow.send_hourly_updates",
		"criscostack.integrations.doctype.google_calendar.google_calendar.sync",
		"criscostack.email.doctype.newsletter.newsletter.send_scheduled_email",
		"criscostack.website.doctype.personal_data_deletion_request.personal_data_deletion_request.process_data_deletion_request",
	],
	"daily": [
		"criscostack.desk.notifications.clear_notifications",
		"criscostack.desk.doctype.event.event.send_event_digest",
		"criscostack.sessions.clear_expired_sessions",
		"criscostack.email.doctype.notification.notification.trigger_daily_alerts",
		"criscostack.website.doctype.personal_data_deletion_request.personal_data_deletion_request.remove_unverified_record",
		"criscostack.desk.form.document_follow.send_daily_updates",
		"criscostack.social.doctype.energy_point_settings.energy_point_settings.allocate_review_points",
		"criscostack.integrations.doctype.google_contacts.google_contacts.sync",
		"criscostack.automation.doctype.auto_repeat.auto_repeat.make_auto_repeat_entry",
		"criscostack.automation.doctype.auto_repeat.auto_repeat.set_auto_repeat_as_completed",
		"criscostack.email.doctype.unhandled_email.unhandled_email.remove_old_unhandled_emails",
	],
	"daily_long": [
		"criscostack.integrations.doctype.dropbox_settings.dropbox_settings.take_backups_daily",
		"criscostack.utils.change_log.check_for_update",
		"criscostack.integrations.doctype.s3_backup_settings.s3_backup_settings.take_backups_daily",
		"criscostack.email.doctype.auto_email_report.auto_email_report.send_daily",
		"criscostack.integrations.doctype.google_drive.google_drive.daily_backup",
	],
	"weekly_long": [
		"criscostack.integrations.doctype.dropbox_settings.dropbox_settings.take_backups_weekly",
		"criscostack.integrations.doctype.s3_backup_settings.s3_backup_settings.take_backups_weekly",
		"criscostack.desk.form.document_follow.send_weekly_updates",
		"criscostack.social.doctype.energy_point_log.energy_point_log.send_weekly_summary",
		"criscostack.integrations.doctype.google_drive.google_drive.weekly_backup",
	],
	"monthly": [
		"criscostack.email.doctype.auto_email_report.auto_email_report.send_monthly",
		"criscostack.social.doctype.energy_point_log.energy_point_log.send_monthly_summary",
	],
	"monthly_long": [
		"criscostack.integrations.doctype.s3_backup_settings.s3_backup_settings.take_backups_monthly"
	],
}

get_translated_dict = {
	("doctype", "System Settings"): "criscostack.geo.country_info.get_translated_dict",
	("page", "setup-wizard"): "criscostack.geo.country_info.get_translated_dict",
}

sounds = [
	{"name": "email", "src": "/assets/criscostack/sounds/email.mp3", "volume": 0.1},
	{"name": "submit", "src": "/assets/criscostack/sounds/submit.mp3", "volume": 0.1},
	{"name": "cancel", "src": "/assets/criscostack/sounds/cancel.mp3", "volume": 0.1},
	{"name": "delete", "src": "/assets/criscostack/sounds/delete.mp3", "volume": 0.05},
	{"name": "click", "src": "/assets/criscostack/sounds/click.mp3", "volume": 0.05},
	{"name": "error", "src": "/assets/criscostack/sounds/error.mp3", "volume": 0.1},
	{"name": "alert", "src": "/assets/criscostack/sounds/alert.mp3", "volume": 0.2},
	# {"name": "chime", "src": "/assets/criscostack/sounds/chime.mp3"},
]

setup_wizard_exception = [
	"criscostack.desk.page.setup_wizard.setup_wizard.email_setup_wizard_exception",
	"criscostack.desk.page.setup_wizard.setup_wizard.log_setup_wizard_exception",
]

before_migrate = ["criscostack.core.doctype.patch_log.patch_log.before_migrate"]
after_migrate = ["criscostack.website.doctype.website_theme.website_theme.after_migrate"]

otp_methods = ["OTP App", "Email", "SMS"]

user_data_fields = [
	{"doctype": "Access Log", "strict": True},
	{"doctype": "Activity Log", "strict": True},
	{"doctype": "Comment", "strict": True},
	{
		"doctype": "Contact",
		"filter_by": "email_id",
		"redact_fields": ["first_name", "last_name", "phone", "mobile_no"],
		"rename": True,
	},
	{"doctype": "Contact Email", "filter_by": "email_id"},
	{
		"doctype": "Address",
		"filter_by": "email_id",
		"redact_fields": [
			"address_title",
			"address_line1",
			"address_line2",
			"city",
			"county",
			"state",
			"pincode",
			"phone",
			"fax",
		],
	},
	{
		"doctype": "Communication",
		"filter_by": "sender",
		"redact_fields": ["sender_full_name", "phone_no", "content"],
	},
	{"doctype": "Communication", "filter_by": "recipients"},
	{"doctype": "Email Group Member", "filter_by": "email"},
	{"doctype": "Email Unsubscribe", "filter_by": "email", "partial": True},
	{"doctype": "Email Queue", "filter_by": "sender"},
	{"doctype": "Email Queue Recipient", "filter_by": "recipient"},
	{
		"doctype": "File",
		"filter_by": "attached_to_name",
		"redact_fields": ["file_name", "file_url"],
	},
	{
		"doctype": "User",
		"filter_by": "name",
		"redact_fields": [
			"email",
			"username",
			"first_name",
			"middle_name",
			"last_name",
			"full_name",
			"birth_date",
			"user_image",
			"phone",
			"mobile_no",
			"location",
			"banner_image",
			"interest",
			"bio",
			"email_signature",
		],
	},
	{"doctype": "Version", "strict": True},
]

global_search_doctypes = {
	"Default": [
		{"doctype": "Contact"},
		{"doctype": "Address"},
		{"doctype": "ToDo"},
		{"doctype": "Note"},
		{"doctype": "Event"},
		{"doctype": "Blog Post"},
		{"doctype": "Dashboard"},
		{"doctype": "Country"},
		{"doctype": "Currency"},
		{"doctype": "Newsletter"},
		{"doctype": "Letter Head"},
		{"doctype": "Workflow"},
		{"doctype": "Web Page"},
		{"doctype": "Web Form"},
	]
}

override_whitelisted_methods = {
	# Legacy File APIs
	"criscostack.core.doctype.file.file.download_file": "download_file",
	"criscostack.core.doctype.file.file.unzip_file": "criscostack.core.api.file.unzip_file",
	"criscostack.core.doctype.file.file.get_attached_images": "criscostack.core.api.file.get_attached_images",
	"criscostack.core.doctype.file.file.get_files_in_folder": "criscostack.core.api.file.get_files_in_folder",
	"criscostack.core.doctype.file.file.get_files_by_search_text": "criscostack.core.api.file.get_files_by_search_text",
	"criscostack.core.doctype.file.file.get_max_file_size": "criscostack.core.api.file.get_max_file_size",
	"criscostack.core.doctype.file.file.create_new_folder": "criscostack.core.api.file.create_new_folder",
	"criscostack.core.doctype.file.file.move_file": "criscostack.core.api.file.move_file",
	"criscostack.core.doctype.file.file.zip_files": "criscostack.core.api.file.zip_files",
	# Legacy (& Consistency) OAuth2 APIs
	"criscostack.www.login.login_via_google": "criscostack.integrations.oauth2_logins.login_via_google",
	"criscostack.www.login.login_via_github": "criscostack.integrations.oauth2_logins.login_via_github",
	"criscostack.www.login.login_via_facebook": "criscostack.integrations.oauth2_logins.login_via_facebook",
	"criscostack.www.login.login_via_criscostack": "criscostack.integrations.oauth2_logins.login_via_criscostack",
	"criscostack.www.login.login_via_office365": "criscostack.integrations.oauth2_logins.login_via_office365",
	"criscostack.www.login.login_via_salesforce": "criscostack.integrations.oauth2_logins.login_via_salesforce",
	"criscostack.www.login.login_via_fairlogin": "criscostack.integrations.oauth2_logins.login_via_fairlogin",
}

ignore_links_on_delete = [
	"Communication",
	"ToDo",
	"DocShare",
	"Email Unsubscribe",
	"Activity Log",
	"File",
	"Version",
	"Document Follow",
	"Comment",
	"View Log",
	"Tag Link",
	"Notification Log",
	"Email Queue",
	"Document Share Key",
	"Integration Request",
	"Unhandled Email",
	"Webhook Request Log",
]

# Request Hooks
before_request = [
	"criscostack.recorder.record",
	"criscostack.monitor.start",
	"criscostack.rate_limiter.apply",
]
after_request = ["criscostack.rate_limiter.update", "criscostack.monitor.stop", "criscostack.recorder.dump"]

# Background Job Hooks
before_job = [
	"criscostack.monitor.start",
]
after_job = [
	"criscostack.monitor.stop",
	"criscostack.utils.file_lock.release_document_locks",
]

extend_bootinfo = [
	"criscostack.utils.telemetry.add_bootinfo",
	"criscostack.core.doctype.user_permission.user_permission.send_user_permissions",
]

export_python_type_annotations = True
