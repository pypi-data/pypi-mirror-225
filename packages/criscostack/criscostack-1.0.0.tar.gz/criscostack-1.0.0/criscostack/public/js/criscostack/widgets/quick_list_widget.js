import Widget from "./base_widget.js";

criscostack.provide("criscostack.utils");

export default class QuickListWidget extends Widget {
	constructor(opts) {
		opts.shadow = true;
		super(opts);
	}

	get_config() {
		return {
			document_type: this.document_type,
			label: this.label,
			quick_list_filter: this.quick_list_filter,
		};
	}

	set_actions() {
		if (this.in_customize_mode) return;

		this.setup_add_new_button();
		this.setup_refresh_list_button();
		this.setup_filter_list_button();
	}

	setup_add_new_button() {
		this.add_new_button = $(
			`<div class="add-new btn btn-xs pull-right"
			title="${__("Add New")}  ${__(this.document_type)}
			">
				${criscostack.utils.icon("add", "sm")}
			</div>`
		);

		this.add_new_button.appendTo(this.action_area);
		this.add_new_button.on("click", () => {
			criscostack.set_route(
				criscostack.utils.generate_route({
					type: "doctype",
					name: this.document_type,
					doc_view: "New",
				})
			);
		});
	}

	setup_refresh_list_button() {
		this.refresh_list = $(
			`<div class="refresh-list btn btn-xs pull-right" title="${__("Refresh List")}">
				${criscostack.utils.icon("refresh", "sm")}
			</div>`
		);

		this.refresh_list.appendTo(this.action_area);
		this.refresh_list.on("click", () => {
			this.body.empty();
			this.set_body();
		});
	}

	setup_filter_list_button() {
		this.filter_list = $(
			`<div class="filter-list btn btn-xs pull-right" title="${__("Add/Update Filter")}">
				${criscostack.utils.icon("filter", "sm")}
			</div>`
		);

		this.filter_list.appendTo(this.action_area);
		this.filter_list.on("click", () => this.setup_filter_dialog());
	}

	setup_filter(doctype) {
		if (this.filter_group) {
			this.filter_group.wrapper.empty();
			delete this.filter_group;
		}

		this.filters = criscostack.utils.get_filter_from_json(this.quick_list_filter, doctype);

		this.filter_group = new criscostack.ui.FilterGroup({
			parent: this.dialog.get_field("filter_area").$wrapper,
			doctype: doctype,
			on_change: () => {},
		});

		criscostack.model.with_doctype(doctype, () => {
			this.filter_group.add_filters_to_filter_group(this.filters);
			this.dialog.set_df_property("filter_area", "hidden", false);
		});
	}

	setup_filter_dialog() {
		let fields = [
			{
				fieldtype: "HTML",
				fieldname: "filter_area",
			},
		];
		let me = this;
		this.dialog = new criscostack.ui.Dialog({
			title: __("Set Filters for {0}", [__(this.document_type)]),
			fields: fields,
			primary_action: function () {
				let old_filter = me.quick_list_filter;
				let filters = me.filter_group.get_filters();
				me.quick_list_filter = criscostack.utils.get_filter_as_json(filters);

				this.hide();

				if (old_filter != me.quick_list_filter) {
					me.body.empty();
					me.set_footer();
					me.set_body();
				}
			},
			primary_action_label: __("Set"),
		});

		this.dialog.show();
		this.setup_filter(this.document_type);
	}

	render_loading_state() {
		this.body.empty();
		this.loading = $(`<div class="list-loading-state text-muted">${__("Loading...")}</div>`);
		this.loading.appendTo(this.body);
	}

	render_no_data_state() {
		this.loading = $(`<div class="list-no-data-state text-muted">${__("No Data...")}</div>`);
		this.loading.appendTo(this.body);
	}

	setup_quick_list_item(doc) {
		const indicator = criscostack.get_indicator(doc, this.document_type);

		let $quick_list_item = $(`
			<div class="quick-list-item">
				<div class="ellipsis left">
					<div class="ellipsis title"
						title="${strip_html(doc[this.title_field_name])}">
						${strip_html(doc[this.title_field_name])}
					</div>
					<div class="timestamp text-muted">
						${criscostack.datetime.prettyDate(doc.modified)}
					</div>
				</div>
			</div>
		`);

		if (indicator) {
			$(`
				<div class="status indicator-pill ${indicator[1]} ellipsis">
					${__(indicator[0])}
				</div>
			`).appendTo($quick_list_item);
		}

		$(`<div class="right-arrow">${criscostack.utils.icon("right", "xs")}</div>`).appendTo(
			$quick_list_item
		);

		$quick_list_item.click((e) => {
			if (e.ctrlKey || e.metaKey) {
				criscostack.open_in_new_tab = true;
			}
			criscostack.set_route(`${criscostack.utils.get_form_link(this.document_type, doc.name)}`);
		});

		return $quick_list_item;
	}

	set_body() {
		this.widget.addClass("quick-list-widget-box");

		this.render_loading_state();

		criscostack.model.with_doctype(this.document_type, () => {
			let fields = ["name"];

			// get name of title field
			if (!this.title_field_name) {
				let meta = criscostack.get_meta(this.document_type);
				this.title_field_name = (meta && meta.title_field) || "name";
			}

			if (this.title_field_name && this.title_field_name != "name") {
				fields.push(this.title_field_name);
			}

			// check doctype has status field
			this.has_status_field = criscostack.meta.has_field(this.document_type, "status");

			if (this.has_status_field) {
				fields.push("status");
				fields.push("docstatus");

				// add workflow state field if workflow exist & is active
				let workflow_fieldname = criscostack.workflow.get_state_fieldname(this.document_type);
				workflow_fieldname && fields.push(workflow_fieldname);
			}

			fields.push("modified");

			let quick_list_filter = criscostack.utils.get_filter_from_json(this.quick_list_filter);

			let args = {
				method: "criscostack.desk.reportview.get",
				args: {
					doctype: this.document_type,
					fields: fields,
					filters: quick_list_filter,
					order_by: "modified desc",
					start: 0,
					page_length: 4,
				},
			};

			criscostack.call(args).then((r) => {
				if (!r.message) return;
				let data = r.message;

				this.body.empty();
				data = !Array.isArray(data) ? criscostack.utils.dict(data.keys, data.values) : data;

				if (!data.length) {
					this.render_no_data_state();
					return;
				}

				this.quick_list = data.map((doc) => this.setup_quick_list_item(doc));
				this.quick_list.forEach(($quick_list_item) =>
					$quick_list_item.appendTo(this.body)
				);
			});
		});
	}

	set_footer() {
		this.footer.empty();

		let filters = criscostack.utils.get_filter_from_json(this.quick_list_filter);
		let route = criscostack.utils.generate_route({ type: "doctype", name: this.document_type });
		this.see_all_button = $(`
			<div class="see-all btn btn-xs">${__("View List")}</div>
		`).appendTo(this.footer);

		this.see_all_button.click((e) => {
			if (e.ctrlKey || e.metaKey) {
				criscostack.open_in_new_tab = true;
			}
			if (filters) {
				criscostack.route_options = filters;
			}
			criscostack.set_route(route);
		});
	}
}
