criscostack.listview_settings["Route History"] = {
	onload: function (listview) {
		criscostack.require("logtypes.bundle.js", () => {
			criscostack.utils.logtypes.show_log_retention_message(cur_list.doctype);
		});
	},
};
