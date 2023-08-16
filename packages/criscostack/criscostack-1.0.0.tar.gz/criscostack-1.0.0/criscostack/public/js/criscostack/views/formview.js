// Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
// MIT License. See license.txt

criscostack.provide("criscostack.views.formview");

criscostack.views.FormFactory = class FormFactory extends criscostack.views.Factory {
	make(route) {
		var doctype = route[1],
			doctype_layout = criscostack.router.doctype_layout || doctype;

		if (!criscostack.views.formview[doctype_layout]) {
			criscostack.model.with_doctype(doctype, () => {
				this.page = criscostack.container.add_page(doctype_layout);
				criscostack.views.formview[doctype_layout] = this.page;
				this.make_and_show(doctype, route);
			});
		} else {
			this.show_doc(route);
		}

		this.setup_events();
	}

	make_and_show(doctype, route) {
		if (criscostack.router.doctype_layout) {
			criscostack.model.with_doc("DocType Layout", criscostack.router.doctype_layout, () => {
				this.make_form(doctype);
				this.show_doc(route);
			});
		} else {
			this.make_form(doctype);
			this.show_doc(route);
		}
	}

	make_form(doctype) {
		this.page.frm = new criscostack.ui.form.Form(
			doctype,
			this.page,
			true,
			criscostack.router.doctype_layout
		);
	}

	setup_events() {
		if (!this.initialized) {
			$(document).on("page-change", function () {
				criscostack.ui.form.close_grid_form();
			});
		}
		this.initialized = true;
	}

	show_doc(route) {
		var doctype = route[1],
			doctype_layout = criscostack.router.doctype_layout || doctype,
			name = route.slice(2).join("/");

		if (criscostack.model.new_names[name]) {
			// document has been renamed, reroute
			name = criscostack.model.new_names[name];
			criscostack.set_route("Form", doctype_layout, name);
			return;
		}

		const doc = criscostack.get_doc(doctype, name);
		if (
			doc &&
			criscostack.model.get_docinfo(doctype, name) &&
			(doc.__islocal || criscostack.model.is_fresh(doc))
		) {
			// is document available and recent?
			this.render(doctype_layout, name);
		} else {
			this.fetch_and_render(doctype, name, doctype_layout);
		}
	}

	fetch_and_render(doctype, name, doctype_layout) {
		criscostack.model.with_doc(doctype, name, (name, r) => {
			if (r && r["403"]) return; // not permitted

			if (!(locals[doctype] && locals[doctype][name])) {
				if (name && name.substr(0, 3) === "new") {
					this.render_new_doc(doctype, name, doctype_layout);
				} else {
					criscostack.show_not_found();
				}
				return;
			}
			this.render(doctype_layout, name);
		});
	}

	render_new_doc(doctype, name, doctype_layout) {
		const new_name = criscostack.model.make_new_doc_and_get_name(doctype, true);
		if (new_name === name) {
			this.render(doctype_layout, name);
		} else {
			criscostack.route_flags.replace_route = true;
			criscostack.set_route("Form", doctype_layout, new_name);
		}
	}

	render(doctype_layout, name) {
		criscostack.container.change_to(doctype_layout);
		criscostack.views.formview[doctype_layout].frm.refresh(name);
	}
};
