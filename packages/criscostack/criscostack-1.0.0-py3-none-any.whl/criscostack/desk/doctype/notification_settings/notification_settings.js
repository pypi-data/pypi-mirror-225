// Copyright (c) 2019, Crisco Technologies and contributors
// For license information, please see license.txt

criscostack.ui.form.on("Notification Settings", {
	onload: (frm) => {
		criscostack.breadcrumbs.add({
			label: __("Settings"),
			route: "#modules/Settings",
			type: "Custom",
		});
		frm.set_query("subscribed_documents", () => {
			return {
				filters: {
					istable: 0,
				},
			};
		});
	},

	refresh: (frm) => {
		if (criscostack.user.has_role("System Manager")) {
			frm.add_custom_button(__("Go to Notification Settings List"), () => {
				criscostack.set_route("List", "Notification Settings");
			});
		}
	},
});
