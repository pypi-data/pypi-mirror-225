// Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
// MIT License. See license.txt

criscostack.ui.form.on("DocType", {
	before_save: function (frm) {
		let form_builder = criscostack.form_builder;
		if (form_builder?.store) {
			let fields = form_builder.store.update_fields();

			// if fields is a string, it means there is an error
			if (typeof fields === "string") {
				criscostack.throw(fields);
			}
		}
	},
	after_save: function (frm) {
		if (
			criscostack.form_builder &&
			criscostack.form_builder.doctype === frm.doc.name &&
			criscostack.form_builder.store
		) {
			criscostack.form_builder.store.fetch();
		}
	},
	refresh: function (frm) {
		frm.set_query("role", "permissions", function (doc) {
			if (doc.custom && criscostack.session.user != "Administrator") {
				return {
					query: "criscostack.core.doctype.role.role.role_query",
					filters: [["Role", "name", "!=", "All"]],
				};
			}
		});

		if (criscostack.session.user !== "Administrator" || !criscostack.boot.developer_mode) {
			if (frm.is_new()) {
				frm.set_value("custom", 1);
			}
			frm.toggle_enable("custom", 0);
			frm.toggle_enable("is_virtual", 0);
			frm.toggle_enable("beta", 0);
		}

		if (!frm.is_new() && !frm.doc.istable) {
			if (frm.doc.issingle) {
				frm.add_custom_button(__("Go to {0}", [__(frm.doc.name)]), () => {
					window.open(`/app/${criscostack.router.slug(frm.doc.name)}`);
				});
			} else {
				frm.add_custom_button(__("Go to {0} List", [__(frm.doc.name)]), () => {
					window.open(`/app/${criscostack.router.slug(frm.doc.name)}`);
				});
			}
		}

		const customize_form_link = "<a href='/app/customize-form'>Customize Form</a>";
		if (!criscostack.boot.developer_mode && !frm.doc.custom) {
			// make the document read-only
			frm.set_read_only();
			frm.dashboard.clear_comment();
			frm.dashboard.add_comment(
				__("DocTypes can not be modified, please use {0} instead", [customize_form_link]),
				"blue",
				true
			);
		} else if (criscostack.boot.developer_mode) {
			frm.dashboard.clear_comment();
			let msg = __(
				"This site is running in developer mode. Any change made here will be updated in code."
			);
			msg += "<br>";
			msg += __("If you just want to customize for your site, use {0} instead.", [
				customize_form_link,
			]);
			frm.dashboard.add_comment(msg, "yellow", true);
		}

		if (frm.is_new()) {
			frm.events.set_default_permission(frm);
			frm.set_value("default_view", "List");
		} else {
			frm.toggle_enable("engine", 0);
		}

		// set label for "In List View" for child tables
		frm.get_docfield("fields", "in_list_view").label = frm.doc.istable
			? __("In Grid View")
			: __("In List View");

		frm.cscript.autoname(frm);
		frm.cscript.set_naming_rule_description(frm);
		frm.trigger("setup_default_views");

		render_form_builder(frm);
	},

	istable: (frm) => {
		if (frm.doc.istable && frm.is_new()) {
			frm.set_value("default_view", null);
		} else if (!frm.doc.istable && !frm.is_new()) {
			frm.events.set_default_permission(frm);
		}
	},

	set_default_permission: (frm) => {
		if (!(frm.doc.permissions && frm.doc.permissions.length)) {
			frm.add_child("permissions", { role: "System Manager" });
		}
	},

	is_tree: (frm) => {
		frm.trigger("setup_default_views");
	},

	is_calendar_and_gantt: (frm) => {
		frm.trigger("setup_default_views");
	},

	setup_default_views: (frm) => {
		criscostack.model.set_default_views_for_doctype(frm.doc.name, frm);
	},
});

criscostack.ui.form.on("DocField", {
	form_render(frm, doctype, docname) {
		frm.trigger("setup_fetch_from_fields", doctype, docname);
	},

	fieldtype: function (frm) {
		frm.trigger("max_attachments");
	},

	fields_add: (frm) => {
		frm.trigger("setup_default_views");
	},
});

function render_form_builder_message(frm) {
	$(frm.fields_dict["try_form_builder_html"].wrapper).empty();
	if (!frm.is_new() && frm.fields_dict["try_form_builder_html"]) {
		let title = __("Use Form Builder to visually edit your form layout");
		let msg = __(
			"You can drag and drop fields to create your form layout, add tabs, sections and columns to organize your form and update field properties all from one screen."
		);

		let message = `
		<div class="flex form-message blue p-3">
			<div class="mr-3"><img style="border-radius: var(--border-radius-md)" width="360" src="/assets/criscostack/images/form-builder.gif"></div>
			<div>
				<p style="font-size: var(--text-lg)">${title}</p>
				<p>${msg}</p>
				<div>
					<a class="btn btn-primary btn-sm" href="/app/form-builder/${frm.doc.name}">
						${__("Form Builder")} ${criscostack.utils.icon("right", "xs")}
					</a>
				</div>
			</div>
		</div>
		`;

		$(frm.fields_dict["try_form_builder_html"].wrapper).html(message);
	}
}

function render_form_builder(frm) {
	if (criscostack.form_builder && criscostack.form_builder.doctype === frm.doc.name) {
		criscostack.form_builder.setup_page_actions();
		criscostack.form_builder.store.fetch();
		return;
	}

	if (criscostack.form_builder) {
		criscostack.form_builder.wrapper = $(frm.fields_dict["form_builder"].wrapper);
		criscostack.form_builder.frm = frm;
		criscostack.form_builder.doctype = frm.doc.name;
		criscostack.form_builder.customize = false;
		criscostack.form_builder.init(true);
		criscostack.form_builder.store.fetch();
	} else {
		criscostack.require("form_builder.bundle.js").then(() => {
			criscostack.form_builder = new criscostack.ui.FormBuilder({
				wrapper: $(frm.fields_dict["form_builder"].wrapper),
				frm: frm,
				doctype: frm.doc.name,
				customize: false,
			});
		});
	}
}

extend_cscript(cur_frm.cscript, new criscostack.model.DocTypeController({ frm: cur_frm }));
