criscostack.ui.form.ControlHeading = class ControlHeading extends criscostack.ui.form.ControlHTML {
	get_content() {
		return "<h4>" + __(this.df.label) + "</h4>";
	}
};
