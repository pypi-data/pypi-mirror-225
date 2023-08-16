criscostack.ui.form.ControlText = class ControlText extends criscostack.ui.form.ControlData {
	static html_element = "textarea";
	static horizontal = false;
	make_wrapper() {
		super.make_wrapper();
		this.$wrapper.find(".like-disabled-input").addClass("for-description");
	}
	make_input() {
		super.make_input();
		this.$input.css({ height: "300px" });
		if (this.df.max_height) {
			this.$input.css({ "max-height": this.df.max_height });
		}
	}
};

criscostack.ui.form.ControlLongText = criscostack.ui.form.ControlText;
criscostack.ui.form.ControlSmallText = class ControlSmallText extends criscostack.ui.form.ControlText {
	make_input() {
		super.make_input();
		this.$input.css({ height: "150px" });
	}
};
