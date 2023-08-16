// Copyright (c) 2017, Crisco Technologies and contributors
// For license information, please see license.txt

criscostack.ui.form.on("Print Style", {
	refresh: function (frm) {
		frm.add_custom_button(__("Print Settings"), () => {
			criscostack.set_route("Form", "Print Settings");
		});
	},
});
