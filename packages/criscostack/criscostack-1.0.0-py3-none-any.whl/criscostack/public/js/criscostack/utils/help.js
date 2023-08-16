// Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
// MIT License. See license.txt

criscostack.provide("criscostack.help");

criscostack.help.youtube_id = {};

criscostack.help.has_help = function (doctype) {
	return criscostack.help.youtube_id[doctype];
};

criscostack.help.show = function (doctype) {
	if (criscostack.help.youtube_id[doctype]) {
		criscostack.help.show_video(criscostack.help.youtube_id[doctype]);
	}
};

criscostack.help.show_video = function (youtube_id, title) {
	if (criscostack.utils.is_url(youtube_id)) {
		const expression =
			'(?:youtube.com/(?:[^/]+/.+/|(?:v|e(?:mbed)?)/|.*[?&]v=)|youtu.be/)([^"&?\\s]{11})';
		youtube_id = youtube_id.match(expression)[1];
	}

	// (criscostack.help_feedback_link || "")
	let dialog = new criscostack.ui.Dialog({
		title: title || __("Help"),
		size: "large",
	});

	let video = $(
		`<div class="video-player" data-plyr-provider="youtube" data-plyr-embed-id="${youtube_id}"></div>`
	);
	video.appendTo(dialog.body);

	dialog.show();
	dialog.$wrapper.addClass("video-modal");

	let plyr;
	criscostack.utils.load_video_player().then(() => {
		plyr = new criscostack.Plyr(video[0], {
			hideControls: true,
			resetOnEnd: true,
		});
	});

	dialog.onhide = () => {
		plyr?.destroy();
	};
};

$("body").on("click", "a.help-link", function () {
	var doctype = $(this).attr("data-doctype");
	doctype && criscostack.help.show(doctype);
});
