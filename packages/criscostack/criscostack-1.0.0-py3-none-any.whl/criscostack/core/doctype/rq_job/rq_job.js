// Copyright (c) 2022, Crisco Technologies and contributors
// For license information, please see license.txt

criscostack.ui.form.on("RQ Job", {
	refresh: function (frm) {
		// Nothing in this form is supposed to be editable.
		frm.disable_form();
		frm.dashboard.set_headline_alert(
			"This is a virtual doctype and data is cleared periodically."
		);

		if (["started", "queued"].includes(frm.doc.status)) {
			frm.add_custom_button(__("Force Stop job"), () => {
				criscostack.confirm(
					"This will terminate the job immediately and might be dangerous, are you sure? ",
					() => {
						criscostack
							.xcall("criscostack.core.doctype.rq_job.rq_job.stop_job", {
								job_id: frm.doc.name,
							})
							.then((r) => {
								criscostack.show_alert("Job Stopped Succefully");
								frm.reload_doc();
							});
					}
				);
			});
		}
	},
});
