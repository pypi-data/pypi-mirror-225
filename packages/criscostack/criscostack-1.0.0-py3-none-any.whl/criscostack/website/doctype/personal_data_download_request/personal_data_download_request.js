// Copyright (c) 2019, Crisco Technologies and contributors
// For license information, please see license.txt

criscostack.ui.form.on("Personal Data Download Request", {
	onload: function (frm) {
		if (frm.is_new()) {
			frm.doc.user = criscostack.session.user;
		}
	},
});
