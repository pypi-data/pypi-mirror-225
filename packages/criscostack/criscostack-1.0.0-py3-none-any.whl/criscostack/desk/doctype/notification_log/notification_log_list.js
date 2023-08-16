criscostack.listview_settings["Notification Log"] = {
	onload: function (listview) {
		criscostack.require("logtypes.bundle.js", () => {
			criscostack.utils.logtypes.show_log_retention_message(cur_list.doctype);
		});
	},
};
