criscostack.provide("criscostack.ui.misc");
criscostack.ui.misc.about = function () {
	if (!criscostack.ui.misc.about_dialog) {
		var d = new criscostack.ui.Dialog({ title: __("Crisco Framework") });

		$(d.body).html(
			repl(
				`<div>
					<p>${__("Open Source Applications for the Web")}</p>
					<p><i class='fa fa-globe fa-fw'></i>
						${__("Website")}:
						<a href='https://criscostackframework.com' target='_blank'>https://criscostackframework.com</a></p>
					<p><i class='fa fa-github fa-fw'></i>
						${__("Source")}:
						<a href='https://github.com/criscostack' target='_blank'>https://github.com/criscostack</a></p>
					<p><i class='fa fa-linkedin fa-fw'></i>
						Linkedin: <a href='https://linkedin.com/company/criscostack-tech' target='_blank'>https://linkedin.com/company/criscostack-tech</a></p>
					<p><i class='fa fa-facebook fa-fw'></i>
						Facebook: <a href='https://facebook.com/criscoerp' target='_blank'>https://facebook.com/criscoerp</a></p>
					<p><i class='fa fa-twitter fa-fw'></i>
						Twitter: <a href='https://twitter.com/criscostacktech' target='_blank'>https://twitter.com/criscostacktech</a></p>
					<p><i class='fa fa-youtube fa-fw'></i>
						YouTube: <a href='https://www.youtube.com/@criscostacktech' target='_blank'>https://www.youtube.com/@criscostacktech</a></p>
					<hr>
					<h4>${__("Installed Apps")}</h4>
					<div id='about-app-versions'>${__("Loading versions...")}</div>
					<hr>
					<p class='text-muted'>${__("&copy; Crisco Technologies Pvt. Ltd. and contributors")} </p>
					</div>`,
				criscostack.app
			)
		);

		criscostack.ui.misc.about_dialog = d;

		criscostack.ui.misc.about_dialog.on_page_show = function () {
			if (!criscostack.versions) {
				criscostack.call({
					method: "criscostack.utils.change_log.get_versions",
					callback: function (r) {
						show_versions(r.message);
					},
				});
			} else {
				show_versions(criscostack.versions);
			}
		};

		var show_versions = function (versions) {
			var $wrap = $("#about-app-versions").empty();
			$.each(Object.keys(versions).sort(), function (i, key) {
				var v = versions[key];
				let text;
				if (v.branch) {
					text = $.format("<p><b>{0}:</b> v{1} ({2})<br></p>", [
						v.title,
						v.branch_version || v.version,
						v.branch,
					]);
				} else {
					text = $.format("<p><b>{0}:</b> v{1}<br></p>", [v.title, v.version]);
				}
				$(text).appendTo($wrap);
			});

			criscostack.versions = versions;
		};
	}

	criscostack.ui.misc.about_dialog.show();
};
