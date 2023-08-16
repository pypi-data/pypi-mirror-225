criscostack.user_info = function (uid) {
	if (!uid) uid = criscostack.session.user;

	let user_info;
	if (!(criscostack.boot.user_info && criscostack.boot.user_info[uid])) {
		user_info = { fullname: uid || "Unknown" };
	} else {
		user_info = criscostack.boot.user_info[uid];
	}

	user_info.abbr = criscostack.get_abbr(user_info.fullname);
	user_info.color = criscostack.get_palette(user_info.fullname);

	return user_info;
};

criscostack.update_user_info = function (user_info) {
	for (let user in user_info) {
		if (criscostack.boot.user_info[user]) {
			Object.assign(criscostack.boot.user_info[user], user_info[user]);
		} else {
			criscostack.boot.user_info[user] = user_info[user];
		}
	}
};

criscostack.provide("criscostack.user");

$.extend(criscostack.user, {
	name: "Guest",
	full_name: function (uid) {
		return uid === criscostack.session.user
			? __(
					"You",
					null,
					"Name of the current user. For example: You edited this 5 hours ago."
			  )
			: criscostack.user_info(uid).fullname;
	},
	image: function (uid) {
		return criscostack.user_info(uid).image;
	},
	abbr: function (uid) {
		return criscostack.user_info(uid).abbr;
	},
	has_role: function (rl) {
		if (typeof rl == "string") rl = [rl];
		for (var i in rl) {
			if ((criscostack.boot ? criscostack.boot.user.roles : ["Guest"]).indexOf(rl[i]) != -1)
				return true;
		}
	},
	get_desktop_items: function () {
		// hide based on permission
		var modules_list = $.map(criscostack.boot.allowed_modules, function (icon) {
			var m = icon.module_name;
			var type = criscostack.modules[m] && criscostack.modules[m].type;

			if (criscostack.boot.user.allow_modules.indexOf(m) === -1) return null;

			var ret = null;
			if (type === "module") {
				if (criscostack.boot.user.allow_modules.indexOf(m) != -1 || criscostack.modules[m].is_help)
					ret = m;
			} else if (type === "page") {
				if (criscostack.boot.allowed_pages.indexOf(criscostack.modules[m].link) != -1) ret = m;
			} else if (type === "list") {
				if (criscostack.model.can_read(criscostack.modules[m]._doctype)) ret = m;
			} else if (type === "view") {
				ret = m;
			} else if (type === "setup") {
				if (
					criscostack.user.has_role("System Manager") ||
					criscostack.user.has_role("Administrator")
				)
					ret = m;
			} else {
				ret = m;
			}

			return ret;
		});

		return modules_list;
	},

	is_report_manager: function () {
		return criscostack.user.has_role(["Administrator", "System Manager", "Report Manager"]);
	},

	get_formatted_email: function (email) {
		var fullname = criscostack.user.full_name(email);

		if (!fullname) {
			return email;
		} else {
			// to quote or to not
			var quote = "";

			// only if these special characters are found
			// why? To make the output same as that in python!
			if (fullname.search(/[\[\]\\()<>@,:;".]/) !== -1) {
				quote = '"';
			}

			return repl("%(quote)s%(fullname)s%(quote)s <%(email)s>", {
				fullname: fullname,
				email: email,
				quote: quote,
			});
		}
	},

	get_emails: () => {
		return Object.keys(criscostack.boot.user_info).map((key) => criscostack.boot.user_info[key].email);
	},

	/* Normally criscostack.user is an object
	 * having properties and methods.
	 * But in the following case
	 *
	 * if (criscostack.user === 'Administrator')
	 *
	 * criscostack.user will cast to a string
	 * returning criscostack.user.name
	 */
	toString: function () {
		return this.name;
	},
});

criscostack.session_alive = true;
$(document).bind("mousemove", function () {
	if (criscostack.session_alive === false) {
		$(document).trigger("session_alive");
	}
	criscostack.session_alive = true;
	if (criscostack.session_alive_timeout) clearTimeout(criscostack.session_alive_timeout);
	criscostack.session_alive_timeout = setTimeout("criscostack.session_alive=false;", 30000);
});
