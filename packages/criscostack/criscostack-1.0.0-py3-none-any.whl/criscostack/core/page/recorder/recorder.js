criscostack.pages["recorder"].on_page_load = function (wrapper) {
	criscostack.ui.make_app_page({
		parent: wrapper,
		title: __("Recorder"),
		single_column: true,
		card_layout: true,
	});

	criscostack.recorder = new Recorder(wrapper);
	$(wrapper).bind("show", function () {
		criscostack.recorder.show();
	});

	criscostack.require("recorder.bundle.js");
};

class Recorder {
	constructor(wrapper) {
		this.wrapper = $(wrapper);
		this.container = this.wrapper.find(".layout-main-section");
		this.container.append($('<div class="recorder-container"></div>'));
	}

	show() {
		if (!this.route || this.route.name == "RecorderDetail") return;
		this.router?.replace({ name: "RecorderDetail" });
	}
}
