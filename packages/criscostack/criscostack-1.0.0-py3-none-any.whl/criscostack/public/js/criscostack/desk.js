// Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
// MIT License. See license.txt
/* eslint-disable no-console */

// __('Modules') __('Domains') __('Places') __('Administration') # for translation, don't remove

criscostack.start_app = function () {
	if (!criscostack.Application) return;
	criscostack.assets.check();
	criscostack.provide("criscostack.app");
	criscostack.provide("criscostack.desk");
	criscostack.app = new criscostack.Application();
};

$(document).ready(function () {
	if (!criscostack.utils.supportsES6) {
		criscostack.msgprint({
			indicator: "red",
			title: __("Browser not supported"),
			message: __(
				"Some of the features might not work in your browser. Please update your browser to the latest version."
			),
		});
	}
	criscostack.start_app();
});

criscostack.Application = class Application {
	constructor() {
		this.startup();
	}

	startup() {
		criscostack.realtime.init();
		criscostack.model.init();

		this.load_bootinfo();
		this.load_user_permissions();
		this.make_nav_bar();
		this.set_favicon();
		this.set_fullwidth_if_enabled();
		this.add_browser_class();
		this.setup_energy_point_listeners();
		this.setup_copy_doc_listener();

		criscostack.ui.keys.setup();

		criscostack.ui.keys.add_shortcut({
			shortcut: "shift+ctrl+g",
			description: __("Switch Theme"),
			action: () => {
				if (criscostack.theme_switcher && criscostack.theme_switcher.dialog.is_visible) {
					criscostack.theme_switcher.hide();
				} else {
					criscostack.theme_switcher = new criscostack.ui.ThemeSwitcher();
					criscostack.theme_switcher.show();
				}
			},
		});

		criscostack.ui.add_system_theme_switch_listener();
		const root = document.documentElement;

		const observer = new MutationObserver(() => {
			criscostack.ui.set_theme();
		});
		observer.observe(root, {
			attributes: true,
			attributeFilter: ["data-theme-mode"],
		});

		criscostack.ui.set_theme();

		// page container
		this.make_page_container();
		if (
			!window.Cypress &&
			criscostack.boot.onboarding_tours &&
			criscostack.boot.user.onboarding_status != null
		) {
			let pending_tours =
				criscostack.boot.onboarding_tours.findIndex((tour) => {
					criscostack.boot.user.onboarding_status[tour[0]]?.is_complete == true;
				}) == -1;
			if (pending_tours && criscostack.boot.onboarding_tours.length > 0) {
				criscostack.require("onboarding_tours.bundle.js", () => {
					criscostack.utils.sleep(1000).then(() => {
						criscostack.ui.init_onboarding_tour();
					});
				});
			}
		}
		this.set_route();

		// trigger app startup
		$(document).trigger("startup");

		$(document).trigger("app_ready");

		if (criscostack.boot.messages) {
			criscostack.msgprint(criscostack.boot.messages);
		}

		if (criscostack.user_roles.includes("System Manager")) {
			// delayed following requests to make boot faster
			setTimeout(() => {
				this.show_change_log();
				this.show_update_available();
			}, 1000);
		}

		if (!criscostack.boot.developer_mode) {
			let console_security_message = __(
				"Using this console may allow attackers to impersonate you and steal your information. Do not enter or paste code that you do not understand."
			);
			console.log(`%c${console_security_message}`, "font-size: large");
		}

		this.show_notes();

		if (criscostack.ui.startup_setup_dialog && !criscostack.boot.setup_complete) {
			criscostack.ui.startup_setup_dialog.pre_show();
			criscostack.ui.startup_setup_dialog.show();
		}

		criscostack.realtime.on("version-update", function () {
			var dialog = criscostack.msgprint({
				message: __(
					"The application has been updated to a new version, please refresh this page"
				),
				indicator: "green",
				title: __("Version Updated"),
			});
			dialog.set_primary_action(__("Refresh"), function () {
				location.reload(true);
			});
			dialog.get_close_btn().toggle(false);
		});

		// listen to build errors
		this.setup_build_events();

		if (criscostack.sys_defaults.email_user_password) {
			var email_list = criscostack.sys_defaults.email_user_password.split(",");
			for (var u in email_list) {
				if (email_list[u] === criscostack.user.name) {
					this.set_password(email_list[u]);
				}
			}
		}

		// REDESIGN-TODO: Fix preview popovers
		this.link_preview = new criscostack.ui.LinkPreview();
	}

	set_route() {
		if (criscostack.boot && localStorage.getItem("session_last_route")) {
			criscostack.set_route(localStorage.getItem("session_last_route"));
			localStorage.removeItem("session_last_route");
		} else {
			// route to home page
			criscostack.router.route();
		}
		criscostack.router.on("change", () => {
			$(".tooltip").hide();
		});
	}

	set_password(user) {
		var me = this;
		criscostack.call({
			method: "criscostack.core.doctype.user.user.get_email_awaiting",
			args: {
				user: user,
			},
			callback: function (email_account) {
				email_account = email_account["message"];
				if (email_account) {
					var i = 0;
					if (i < email_account.length) {
						me.email_password_prompt(email_account, user, i);
					}
				}
			},
		});
	}

	email_password_prompt(email_account, user, i) {
		var me = this;
		const email_id = email_account[i]["email_id"];
		let d = new criscostack.ui.Dialog({
			title: __("Password missing in Email Account"),
			fields: [
				{
					fieldname: "password",
					fieldtype: "Password",
					label: __(
						"Please enter the password for: <b>{0}</b>",
						[email_id],
						"Email Account"
					),
					reqd: 1,
				},
				{
					fieldname: "submit",
					fieldtype: "Button",
					label: __("Submit", null, "Submit password for Email Account"),
				},
			],
		});
		d.get_input("submit").on("click", function () {
			//setup spinner
			d.hide();
			var s = new criscostack.ui.Dialog({
				title: __("Checking one moment"),
				fields: [
					{
						fieldtype: "HTML",
						fieldname: "checking",
					},
				],
			});
			s.fields_dict.checking.$wrapper.html('<i class="fa fa-spinner fa-spin fa-4x"></i>');
			s.show();
			criscostack.call({
				method: "criscostack.email.doctype.email_account.email_account.set_email_password",
				args: {
					email_account: email_account[i]["email_account"],
					password: d.get_value("password"),
				},
				callback: function (passed) {
					s.hide();
					d.hide(); //hide waiting indication
					if (!passed["message"]) {
						criscostack.show_alert(
							{ message: __("Login Failed please try again"), indicator: "error" },
							5
						);
						me.email_password_prompt(email_account, user, i);
					} else {
						if (i + 1 < email_account.length) {
							i = i + 1;
							me.email_password_prompt(email_account, user, i);
						}
					}
				},
			});
		});
		d.show();
	}
	load_bootinfo() {
		if (criscostack.boot) {
			this.setup_workspaces();
			criscostack.model.sync(criscostack.boot.docs);
			this.check_metadata_cache_status();
			this.set_globals();
			this.sync_pages();
			criscostack.router.setup();
			this.setup_moment();
			if (criscostack.boot.print_css) {
				criscostack.dom.set_style(criscostack.boot.print_css, "print-style");
			}
			criscostack.user.name = criscostack.boot.user.name;
			criscostack.router.setup();
		} else {
			this.set_as_guest();
		}
	}

	setup_workspaces() {
		criscostack.modules = {};
		criscostack.workspaces = {};
		for (let page of criscostack.boot.allowed_workspaces || []) {
			criscostack.modules[page.module] = page;
			criscostack.workspaces[criscostack.router.slug(page.name)] = page;
		}
	}

	load_user_permissions() {
		criscostack.defaults.load_user_permission_from_boot();

		criscostack.realtime.on(
			"update_user_permissions",
			criscostack.utils.debounce(() => {
				criscostack.defaults.update_user_permissions();
			}, 500)
		);
	}

	check_metadata_cache_status() {
		if (criscostack.boot.metadata_version != localStorage.metadata_version) {
			criscostack.assets.clear_local_storage();
			criscostack.assets.init_local_storage();
		}
	}

	set_globals() {
		criscostack.session.user = criscostack.boot.user.name;
		criscostack.session.logged_in_user = criscostack.boot.user.name;
		criscostack.session.user_email = criscostack.boot.user.email;
		criscostack.session.user_fullname = criscostack.user_info().fullname;

		criscostack.user_defaults = criscostack.boot.user.defaults;
		criscostack.user_roles = criscostack.boot.user.roles;
		criscostack.sys_defaults = criscostack.boot.sysdefaults;

		criscostack.ui.py_date_format = criscostack.boot.sysdefaults.date_format
			.replace("dd", "%d")
			.replace("mm", "%m")
			.replace("yyyy", "%Y");
		criscostack.boot.user.last_selected_values = {};
	}
	sync_pages() {
		// clear cached pages if timestamp is not found
		if (localStorage["page_info"]) {
			criscostack.boot.allowed_pages = [];
			var page_info = JSON.parse(localStorage["page_info"]);
			$.each(criscostack.boot.page_info, function (name, p) {
				if (!page_info[name] || page_info[name].modified != p.modified) {
					delete localStorage["_page:" + name];
				}
				criscostack.boot.allowed_pages.push(name);
			});
		} else {
			criscostack.boot.allowed_pages = Object.keys(criscostack.boot.page_info);
		}
		localStorage["page_info"] = JSON.stringify(criscostack.boot.page_info);
	}
	set_as_guest() {
		criscostack.session.user = "Guest";
		criscostack.session.user_email = "";
		criscostack.session.user_fullname = "Guest";

		criscostack.user_defaults = {};
		criscostack.user_roles = ["Guest"];
		criscostack.sys_defaults = {};
	}
	make_page_container() {
		if ($("#body").length) {
			$(".splash").remove();
			criscostack.temp_container = $("<div id='temp-container' style='display: none;'>").appendTo(
				"body"
			);
			criscostack.container = new criscostack.views.Container();
		}
	}
	make_nav_bar() {
		// toolbar
		if (criscostack.boot && criscostack.boot.home_page !== "setup-wizard") {
			criscostack.criscostack_toolbar = new criscostack.ui.toolbar.Toolbar();
		}
	}
	logout() {
		var me = this;
		me.logged_out = true;
		return criscostack.call({
			method: "logout",
			callback: function (r) {
				if (r.exc) {
					return;
				}
				me.redirect_to_login();
			},
		});
	}
	handle_session_expired() {
		criscostack.app.redirect_to_login();
	}
	redirect_to_login() {
		window.location.href = `/login?redirect-to=${encodeURIComponent(
			window.location.pathname + window.location.search
		)}`;
	}
	set_favicon() {
		var link = $('link[type="image/x-icon"]').remove().attr("href");
		$('<link rel="shortcut icon" href="' + link + '" type="image/x-icon">').appendTo("head");
		$('<link rel="icon" href="' + link + '" type="image/x-icon">').appendTo("head");
	}
	trigger_primary_action() {
		// to trigger change event on active input before triggering primary action
		$(document.activeElement).blur();
		// wait for possible JS validations triggered after blur (it might change primary button)
		setTimeout(() => {
			if (window.cur_dialog && cur_dialog.display) {
				// trigger primary
				cur_dialog.get_primary_btn().trigger("click");
			} else if (cur_frm && cur_frm.page.btn_primary.is(":visible")) {
				cur_frm.page.btn_primary.trigger("click");
			} else if (criscostack.container.page.save_action) {
				criscostack.container.page.save_action();
			}
		}, 100);
	}

	show_change_log() {
		var me = this;
		let change_log = criscostack.boot.change_log;

		// criscostack.boot.change_log = [{
		// 	"change_log": [
		// 		[<version>, <change_log in markdown>],
		// 		[<version>, <change_log in markdown>],
		// 	],
		// 	"description": "ERP made simple",
		// 	"title": "Criscoerp",
		// 	"version": "12.2.0"
		// }];

		if (
			!Array.isArray(change_log) ||
			!change_log.length ||
			window.Cypress ||
			cint(criscostack.boot.sysdefaults.disable_change_log_notification)
		) {
			return;
		}

		// Iterate over changelog
		var change_log_dialog = criscostack.msgprint({
			message: criscostack.render_template("change_log", { change_log: change_log }),
			title: __("Updated To A New Version 🎉"),
			wide: true,
		});
		change_log_dialog.keep_open = true;
		change_log_dialog.custom_onhide = function () {
			criscostack.call({
				method: "criscostack.utils.change_log.update_last_known_versions",
			});
			me.show_notes();
		};
	}

	show_update_available() {
		if (criscostack.boot.sysdefaults.disable_system_update_notification) return;

		criscostack.call({
			method: "criscostack.utils.change_log.show_update_popup",
		});
	}

	add_browser_class() {
		$("html").addClass(criscostack.utils.get_browser().name.toLowerCase());
	}

	set_fullwidth_if_enabled() {
		criscostack.ui.toolbar.set_fullwidth_if_enabled();
	}

	show_notes() {
		var me = this;
		if (criscostack.boot.notes.length) {
			criscostack.boot.notes.forEach(function (note) {
				if (!note.seen || note.notify_on_every_login) {
					var d = criscostack.msgprint({ message: note.content, title: note.title });
					d.keep_open = true;
					d.custom_onhide = function () {
						note.seen = true;

						// Mark note as read if the Notify On Every Login flag is not set
						if (!note.notify_on_every_login) {
							criscostack.call({
								method: "criscostack.desk.doctype.note.note.mark_as_seen",
								args: {
									note: note.name,
								},
							});
						}

						// next note
						me.show_notes();
					};
				}
			});
		}
	}

	setup_build_events() {
		if (criscostack.boot.developer_mode) {
			criscostack.require("build_events.bundle.js");
		}
	}

	setup_energy_point_listeners() {
		criscostack.realtime.on("energy_point_alert", (message) => {
			criscostack.show_alert(message);
		});
	}

	setup_copy_doc_listener() {
		$("body").on("paste", (e) => {
			try {
				let pasted_data = criscostack.utils.get_clipboard_data(e);
				let doc = JSON.parse(pasted_data);
				if (doc.doctype) {
					e.preventDefault();
					const sleep = criscostack.utils.sleep;

					criscostack.dom.freeze(__("Creating {0}", [doc.doctype]) + "...");
					// to avoid abrupt UX
					// wait for activity feedback
					sleep(500).then(() => {
						let res = criscostack.model.with_doctype(doc.doctype, () => {
							let newdoc = criscostack.model.copy_doc(doc);
							newdoc.__newname = doc.name;
							delete doc.name;
							newdoc.idx = null;
							newdoc.__run_link_triggers = false;
							criscostack.set_route("Form", newdoc.doctype, newdoc.name);
							criscostack.dom.unfreeze();
						});
						res && res.fail(criscostack.dom.unfreeze);
					});
				}
			} catch (e) {
				//
			}
		});
	}

	setup_moment() {
		moment.updateLocale("en", {
			week: {
				dow: criscostack.datetime.get_first_day_of_the_week_index(),
			},
		});
		moment.locale("en");
		moment.user_utc_offset = moment().utcOffset();
		if (criscostack.boot.timezone_info) {
			moment.tz.add(criscostack.boot.timezone_info);
		}
	}
};

criscostack.get_module = function (m, default_module) {
	var module = criscostack.modules[m] || default_module;
	if (!module) {
		return;
	}

	if (module._setup) {
		return module;
	}

	if (!module.label) {
		module.label = m;
	}

	if (!module._label) {
		module._label = __(module.label);
	}

	module._setup = true;

	return module;
};
