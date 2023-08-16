criscostack.listview_settings["Activity Log"] = {
	get_indicator: function (doc) {
		if (doc.operation == "Login" && doc.status == "Success") return [__(doc.status), "green"];
		else if (doc.operation == "Login" && doc.status == "Failed")
			return [__(doc.status), "red"];
	},
	onload: function (listview) {
		criscostack.require("logtypes.bundle.js", () => {
			criscostack.utils.logtypes.show_log_retention_message(cur_list.doctype);
		});
	},
};
