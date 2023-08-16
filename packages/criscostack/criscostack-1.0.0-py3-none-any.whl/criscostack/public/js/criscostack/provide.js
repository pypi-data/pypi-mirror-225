// Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
// MIT License. See license.txt

// provide a namespace
if (!window.criscostack) window.criscostack = {};

criscostack.provide = function (namespace) {
	// docs: create a namespace //
	var nsl = namespace.split(".");
	var parent = window;
	for (var i = 0; i < nsl.length; i++) {
		var n = nsl[i];
		if (!parent[n]) {
			parent[n] = {};
		}
		parent = parent[n];
	}
	return parent;
};

criscostack.provide("locals");
criscostack.provide("criscostack.flags");
criscostack.provide("criscostack.settings");
criscostack.provide("criscostack.utils");
criscostack.provide("criscostack.ui.form");
criscostack.provide("criscostack.modules");
criscostack.provide("criscostack.templates");
criscostack.provide("criscostack.test_data");
criscostack.provide("criscostack.utils");
criscostack.provide("criscostack.model");
criscostack.provide("criscostack.user");
criscostack.provide("criscostack.session");
criscostack.provide("criscostack._messages");
criscostack.provide("locals.DocType");

// for listviews
criscostack.provide("criscostack.listview_settings");
criscostack.provide("criscostack.tour");
criscostack.provide("criscostack.listview_parent_route");

// constants
window.NEWLINE = "\n";
window.TAB = 9;
window.UP_ARROW = 38;
window.DOWN_ARROW = 40;

// proxy for user globals defined in desk.js

// API globals
window.cur_frm = null;
