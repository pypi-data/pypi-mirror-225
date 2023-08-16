criscostack.ui.form.on("User", {
	before_load: function (frm) {
		var update_tz_select = function (user_language) {
			frm.set_df_property("time_zone", "options", [""].concat(criscostack.all_timezones));
		};

		if (!criscostack.all_timezones) {
			criscostack.call({
				method: "criscostack.core.doctype.user.user.get_timezones",
				callback: function (r) {
					criscostack.all_timezones = r.message.timezones;
					update_tz_select();
				},
			});
		} else {
			update_tz_select();
		}
	},

	time_zone: function (frm) {
		if (frm.doc.time_zone && frm.doc.time_zone.startsWith("Etc")) {
			frm.set_df_property(
				"time_zone",
				"description",
				__("Note: Etc timezones have their signs reversed.")
			);
		}
	},

	role_profile_name: function (frm) {
		if (frm.doc.role_profile_name) {
			criscostack.call({
				method: "criscostack.core.doctype.user.user.get_role_profile",
				args: {
					role_profile: frm.doc.role_profile_name,
				},
				callback: function (data) {
					frm.set_value("roles", []);
					$.each(data.message || [], function (i, v) {
						var d = frm.add_child("roles");
						d.role = v.role;
					});
					frm.roles_editor.show();
				},
			});
		}
	},

	module_profile: function (frm) {
		if (frm.doc.module_profile) {
			criscostack.call({
				method: "criscostack.core.doctype.user.user.get_module_profile",
				args: {
					module_profile: frm.doc.module_profile,
				},
				callback: function (data) {
					frm.set_value("block_modules", []);
					$.each(data.message || [], function (i, v) {
						let d = frm.add_child("block_modules");
						d.module = v.module;
					});
					frm.module_editor && frm.module_editor.show();
				},
			});
		}
	},

	onload: function (frm) {
		frm.can_edit_roles = has_access_to_edit_user();

		if (frm.is_new() && frm.roles_editor) {
			frm.roles_editor.reset();
		}

		if (
			frm.can_edit_roles &&
			!frm.is_new() &&
			in_list(["System User", "Website User"], frm.doc.user_type)
		) {
			if (!frm.roles_editor) {
				const role_area = $('<div class="role-editor">').appendTo(
					frm.fields_dict.roles_html.wrapper
				);

				frm.roles_editor = new criscostack.RoleEditor(
					role_area,
					frm,
					frm.doc.role_profile_name ? 1 : 0
				);

				if (frm.doc.user_type == "System User") {
					var module_area = $("<div>").appendTo(frm.fields_dict.modules_html.wrapper);
					frm.module_editor = new criscostack.ModuleEditor(frm, module_area);
				}
			} else {
				frm.roles_editor.show();
			}
		}
	},
	refresh: function (frm) {
		let doc = frm.doc;

		if (frm.is_new()) {
			frm.set_value("time_zone", criscostack.sys_defaults.time_zone);
		}

		if (
			in_list(["System User", "Website User"], frm.doc.user_type) &&
			!frm.is_new() &&
			!frm.roles_editor &&
			frm.can_edit_roles
		) {
			frm.reload_doc();
			return;
		}

		const hasChanged = (doc_attr, boot_attr) => {
			return doc_attr && boot_attr && doc_attr !== boot_attr;
		};

		if (
			doc.name === criscostack.session.user &&
			!doc.__unsaved &&
			criscostack.all_timezones &&
			(hasChanged(doc.language, criscostack.boot.user.language) ||
				hasChanged(doc.time_zone, criscostack.boot.time_zone.user))
		) {
			criscostack.msgprint(__("Refreshing..."));
			window.location.reload();
		}

		frm.toggle_display(["sb1", "sb3", "modules_access"], false);

		if (!frm.is_new()) {
			if (has_access_to_edit_user()) {
				frm.add_custom_button(
					__("Set User Permissions"),
					function () {
						criscostack.route_options = {
							user: doc.name,
						};
						criscostack.set_route("List", "User Permission");
					},
					__("Permissions")
				);

				frm.add_custom_button(
					__("View Permitted Documents"),
					() =>
						criscostack.set_route("query-report", "Permitted Documents For User", {
							user: frm.doc.name,
						}),
					__("Permissions")
				);

				frm.toggle_display(["sb1", "sb3", "modules_access"], true);
			}

			frm.add_custom_button(
				__("Reset Password"),
				function () {
					criscostack.call({
						method: "criscostack.core.doctype.user.user.reset_password",
						args: {
							user: frm.doc.name,
						},
					});
				},
				__("Password")
			);

			if (criscostack.user.has_role("System Manager")) {
				criscostack.db.get_single_value("LDAP Settings", "enabled").then((value) => {
					if (value === 1 && frm.doc.name != "Administrator") {
						frm.add_custom_button(
							__("Reset LDAP Password"),
							function () {
								const d = new criscostack.ui.Dialog({
									title: __("Reset LDAP Password"),
									fields: [
										{
											label: __("New Password"),
											fieldtype: "Password",
											fieldname: "new_password",
											reqd: 1,
										},
										{
											label: __("Confirm New Password"),
											fieldtype: "Password",
											fieldname: "confirm_password",
											reqd: 1,
										},
										{
											label: __("Logout All Sessions"),
											fieldtype: "Check",
											fieldname: "logout_sessions",
										},
									],
									primary_action: (values) => {
										d.hide();
										if (values.new_password !== values.confirm_password) {
											criscostack.throw(__("Passwords do not match!"));
										}
										criscostack.call(
											"criscostack.integrations.doctype.ldap_settings.ldap_settings.reset_password",
											{
												user: frm.doc.email,
												password: values.new_password,
												logout: values.logout_sessions,
											}
										);
									},
								});
								d.show();
							},
							__("Password")
						);
					}
				});
			}

			if (
				cint(criscostack.boot.sysdefaults.enable_two_factor_auth) &&
				(criscostack.session.user == doc.name || criscostack.user.has_role("System Manager"))
			) {
				frm.add_custom_button(
					__("Reset OTP Secret"),
					function () {
						criscostack.call({
							method: "criscostack.twofactor.reset_otp_secret",
							args: {
								user: frm.doc.name,
							},
						});
					},
					__("Password")
				);
			}

			frm.trigger("enabled");

			if (frm.roles_editor && frm.can_edit_roles) {
				frm.roles_editor.disable = frm.doc.role_profile_name ? 1 : 0;
				frm.roles_editor.show();
			}

			frm.module_editor && frm.module_editor.show();

			if (criscostack.session.user == doc.name) {
				// update display settings
				if (doc.user_image) {
					criscostack.boot.user_info[criscostack.session.user].image = criscostack.utils.get_file_link(
						doc.user_image
					);
				}
			}
		}
		if (frm.doc.user_emails && criscostack.model.can_create("Email Account")) {
			var found = 0;
			for (var i = 0; i < frm.doc.user_emails.length; i++) {
				if (frm.doc.email == frm.doc.user_emails[i].email_id) {
					found = 1;
				}
			}
			if (!found) {
				frm.add_custom_button(__("Create User Email"), function () {
					frm.events.create_user_email(frm);
				});
			}
		}

		if (criscostack.route_flags.unsaved === 1) {
			delete criscostack.route_flags.unsaved;
			for (let i = 0; i < frm.doc.user_emails.length; i++) {
				frm.doc.user_emails[i].idx = frm.doc.user_emails[i].idx + 1;
			}
			frm.dirty();
		}
		frm.trigger("time_zone");
	},
	validate: function (frm) {
		if (frm.roles_editor) {
			frm.roles_editor.set_roles_in_table();
		}
	},
	enabled: function (frm) {
		var doc = frm.doc;
		if (!frm.is_new() && has_access_to_edit_user()) {
			frm.toggle_display(["sb1", "sb3", "modules_access"], doc.enabled);
			frm.set_df_property("enabled", "read_only", 0);
		}

		if (criscostack.session.user !== "Administrator") {
			frm.toggle_enable("email", frm.is_new());
		}
	},
	create_user_email: function (frm) {
		criscostack.call({
			method: "criscostack.core.doctype.user.user.has_email_account",
			args: {
				email: frm.doc.email,
			},
			callback: function (r) {
				if (!Array.isArray(r.message)) {
					criscostack.route_options = {
						email_id: frm.doc.email,
						awaiting_password: 1,
						enable_incoming: 1,
					};
					criscostack.model.with_doctype("Email Account", function (doc) {
						doc = criscostack.model.get_new_doc("Email Account");
						criscostack.route_flags.linked_user = frm.doc.name;
						criscostack.route_flags.delete_user_from_locals = true;
						criscostack.set_route("Form", "Email Account", doc.name);
					});
				} else {
					criscostack.route_flags.create_user_account = frm.doc.name;
					criscostack.set_route("Form", "Email Account", r.message[0]["name"]);
				}
			},
		});
	},
	generate_keys: function (frm) {
		criscostack.call({
			method: "criscostack.core.doctype.user.user.generate_keys",
			args: {
				user: frm.doc.name,
			},
			callback: function (r) {
				if (r.message) {
					criscostack.msgprint(__("Save API Secret: {0}", [r.message.api_secret]));
					frm.reload_doc();
				}
			},
		});
	},
	on_update: function (frm) {
		if (criscostack.boot.time_zone && criscostack.boot.time_zone.user !== frm.doc.time_zone) {
			// Clear cache after saving to refresh the values of boot.
			criscostack.ui.toolbar.clear_cache();
		}
	},
});

criscostack.ui.form.on("User Email", {
	email_account(frm, cdt, cdn) {
		let child_row = locals[cdt][cdn];
		criscostack.model.get_value(
			"Email Account",
			child_row.email_account,
			"auth_method",
			(value) => {
				child_row.used_oauth = value.auth_method === "OAuth";
				frm.refresh_field("user_emails", cdn, "used_oauth");
			}
		);
	},
});

function has_access_to_edit_user() {
	return has_common(criscostack.user_roles, get_roles_for_editing_user());
}

function get_roles_for_editing_user() {
	return (
		criscostack
			.get_meta("User")
			.permissions.filter((perm) => perm.permlevel >= 1 && perm.write)
			.map((perm) => perm.role) || ["System Manager"]
	);
}
