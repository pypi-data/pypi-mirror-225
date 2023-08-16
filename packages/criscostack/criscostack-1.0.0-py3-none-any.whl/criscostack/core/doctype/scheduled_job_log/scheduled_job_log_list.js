criscostack.listview_settings["Scheduled Job Log"] = {
	onload: function (listview) {
		criscostack.require("logtypes.bundle.js", () => {
			criscostack.utils.logtypes.show_log_retention_message(cur_list.doctype);
		});
	},
};
