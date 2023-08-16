// Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
// MIT License. See license.txt

criscostack.provide("criscostack.views.pageview");
criscostack.provide("criscostack.standard_pages");

criscostack.views.pageview = {
	with_page: function (name, callback) {
		if (criscostack.standard_pages[name]) {
			if (!criscostack.pages[name]) {
				criscostack.standard_pages[name]();
			}
			callback();
			return;
		}

		if (
			(locals.Page && locals.Page[name] && locals.Page[name].script) ||
			name == window.page_name
		) {
			// already loaded
			callback();
		} else if (localStorage["_page:" + name] && criscostack.boot.developer_mode != 1) {
			// cached in local storage
			criscostack.model.sync(JSON.parse(localStorage["_page:" + name]));
			callback();
		} else if (name) {
			// get fresh
			return criscostack.call({
				method: "criscostack.desk.desk_page.getpage",
				args: { name: name },
				callback: function (r) {
					if (!r.docs._dynamic_page) {
						localStorage["_page:" + name] = JSON.stringify(r.docs);
					}
					callback();
				},
				freeze: true,
			});
		}
	},

	show: function (name) {
		if (!name) {
			name = criscostack.boot ? criscostack.boot.home_page : window.page_name;
		}
		criscostack.model.with_doctype("Page", function () {
			criscostack.views.pageview.with_page(name, function (r) {
				if (r && r.exc) {
					if (!r["403"]) criscostack.show_not_found(name);
				} else if (!criscostack.pages[name]) {
					new criscostack.views.Page(name);
				}
				criscostack.container.change_to(name);
			});
		});
	},
};

criscostack.views.Page = class Page {
	constructor(name) {
		this.name = name;
		var me = this;

		// web home page
		if (name == window.page_name) {
			this.wrapper = document.getElementById("page-" + name);
			this.wrapper.label = document.title || window.page_name;
			this.wrapper.page_name = window.page_name;
			criscostack.pages[window.page_name] = this.wrapper;
		} else {
			this.pagedoc = locals.Page[this.name];
			if (!this.pagedoc) {
				criscostack.show_not_found(name);
				return;
			}
			this.wrapper = criscostack.container.add_page(this.name);
			this.wrapper.page_name = this.pagedoc.name;

			// set content, script and style
			if (this.pagedoc.content) this.wrapper.innerHTML = this.pagedoc.content;
			criscostack.dom.eval(this.pagedoc.__script || this.pagedoc.script || "");
			criscostack.dom.set_style(this.pagedoc.style || "");

			// set breadcrumbs
			criscostack.breadcrumbs.add(this.pagedoc.module || null);
		}

		this.trigger_page_event("on_page_load");

		// set events
		$(this.wrapper).on("show", function () {
			window.cur_frm = null;
			me.trigger_page_event("on_page_show");
			me.trigger_page_event("refresh");
		});
	}

	trigger_page_event(eventname) {
		var me = this;
		if (me.wrapper[eventname]) {
			me.wrapper[eventname](me.wrapper);
		}
	}
};

criscostack.show_not_found = function (page_name) {
	criscostack.show_message_page({
		page_name: page_name,
		message: __("Sorry! I could not find what you were looking for."),
		img: "/assets/criscostack/images/ui/bubble-tea-sorry.svg",
	});
};

criscostack.show_not_permitted = function (page_name) {
	criscostack.show_message_page({
		page_name: page_name,
		message: __("Sorry! You are not permitted to view this page."),
		img: "/assets/criscostack/images/ui/bubble-tea-sorry.svg",
		// icon: "octicon octicon-circle-slash"
	});
};

criscostack.show_message_page = function (opts) {
	// opts can include `page_name`, `message`, `icon` or `img`
	if (!opts.page_name) {
		opts.page_name = criscostack.get_route_str();
	}

	if (opts.icon) {
		opts.img = repl('<span class="%(icon)s message-page-icon"></span> ', opts);
	} else if (opts.img) {
		opts.img = repl('<img src="%(img)s" class="message-page-image">', opts);
	}

	var page = criscostack.pages[opts.page_name] || criscostack.container.add_page(opts.page_name);
	$(page).html(
		repl(
			'<div class="page message-page">\
			<div class="text-center message-page-content">\
				%(img)s\
				<p class="lead">%(message)s</p>\
				<a class="btn btn-default btn-sm btn-home" href="/app">%(home)s</a>\
			</div>\
		</div>',
			{
				img: opts.img || "",
				message: opts.message || "",
				home: __("Home"),
			}
		)
	);

	criscostack.container.change_to(opts.page_name);
};
