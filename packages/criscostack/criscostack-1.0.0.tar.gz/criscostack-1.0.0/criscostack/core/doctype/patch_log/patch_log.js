// Copyright (c) 2016, Crisco Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

criscostack.ui.form.on("Patch Log", {
	refresh: function (frm) {
		frm.disable_save();

		frm.add_custom_button(__("Re-Run Patch"), () => {
			frm.call("rerun_patch");
		});
	},
});
