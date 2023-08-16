// Copyright (c) 2019, Crisco Technologies and contributors
// For license information, please see license.txt

criscostack.ui.form.on("Google Settings", {
	refresh: function (frm) {
		frm.dashboard.set_headline(
			__("For more information, {0}.", [
				`<a href='https://criscoerp.com/docs/user/manual/en/criscoerp_integration/google_settings'>${__(
					"Click here"
				)}</a>`,
			])
		);
	},
});
