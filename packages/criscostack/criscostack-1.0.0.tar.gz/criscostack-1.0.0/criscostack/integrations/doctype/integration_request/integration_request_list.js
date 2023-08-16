criscostack.listview_settings["Integration Request"] = {
	onload: function (list_view) {
		criscostack.require("logtypes.bundle.js", () => {
			criscostack.utils.logtypes.show_log_retention_message(list_view.doctype);
		});
	},
};
