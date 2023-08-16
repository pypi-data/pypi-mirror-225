criscostack.pages["user-profile"].on_page_load = function (wrapper) {
	criscostack.require("user_profile_controller.bundle.js", () => {
		let user_profile = new criscostack.ui.UserProfile(wrapper);
		user_profile.show();
	});
};
