// Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
// MIT License. See license.txt

criscostack.provide("criscostack.pages");
criscostack.provide("criscostack.views");

criscostack.views.Factory = class Factory {
	constructor(opts) {
		$.extend(this, opts);
	}

	show() {
		this.route = criscostack.get_route();
		this.page_name = criscostack.get_route_str();

		if (this.before_show && this.before_show() === false) return;

		if (criscostack.pages[this.page_name]) {
			criscostack.container.change_to(this.page_name);
			if (this.on_show) {
				this.on_show();
			}
		} else {
			if (this.route[1]) {
				this.make(this.route);
			} else {
				criscostack.show_not_found(this.route);
			}
		}
	}

	make_page(double_column, page_name) {
		return criscostack.make_page(double_column, page_name);
	}
};

criscostack.make_page = function (double_column, page_name) {
	if (!page_name) {
		page_name = criscostack.get_route_str();
	}

	const page = criscostack.container.add_page(page_name);

	criscostack.ui.make_app_page({
		parent: page,
		single_column: !double_column,
	});

	criscostack.container.change_to(page_name);
	return page;
};
