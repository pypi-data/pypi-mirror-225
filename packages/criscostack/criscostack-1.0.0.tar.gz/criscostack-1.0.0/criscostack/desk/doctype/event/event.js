// Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
// MIT License. See license.txt
criscostack.provide("criscostack.desk");

criscostack.ui.form.on("Event", {
	onload: function (frm) {
		frm.set_query("reference_doctype", "event_participants", function () {
			return {
				filters: {
					issingle: 0,
				},
			};
		});
		frm.set_query("google_calendar", function () {
			return {
				filters: {
					owner: criscostack.session.user,
				},
			};
		});
	},
	refresh: function (frm) {
		if (frm.doc.event_participants) {
			frm.doc.event_participants.forEach((value) => {
				frm.add_custom_button(
					__(value.reference_docname),
					function () {
						criscostack.set_route("Form", value.reference_doctype, value.reference_docname);
					},
					__("Participants")
				);
			});
		}

		frm.page.set_inner_btn_group_as_primary(__("Add Participants"));

		frm.add_custom_button(
			__("Add Contacts"),
			function () {
				new criscostack.desk.eventParticipants(frm, "Contact");
			},
			__("Add Participants")
		);

		const [ends_on_date] = frm.doc.ends_on
			? frm.doc.ends_on.split(" ")
			: frm.doc.starts_on.split(" ");

		if (frm.doc.google_meet_link && criscostack.datetime.now_date() <= ends_on_date) {
			frm.dashboard.set_headline(
				__("Join video conference with {0}", [
					`<a target='_blank' href='${frm.doc.google_meet_link}'>Google Meet</a>`,
				])
			);
		}
	},
	repeat_on: function (frm) {
		if (frm.doc.repeat_on === "Every Day") {
			["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"].map(
				function (v) {
					frm.set_value(v, 1);
				}
			);
		}
	},
});

criscostack.ui.form.on("Event Participants", {
	event_participants_remove: function (frm, cdt, cdn) {
		if (cdt && !cdn.includes("New Event Participants")) {
			criscostack.call({
				type: "POST",
				method: "criscostack.desk.doctype.event.event.delete_communication",
				args: {
					event: frm.doc,
					reference_doctype: cdt,
					reference_docname: cdn,
				},
				freeze: true,
				callback: function (r) {
					if (r.exc) {
						criscostack.show_alert({
							message: __("{0}", [r.exc]),
							indicator: "orange",
						});
					}
				},
			});
		}
	},
});

criscostack.desk.eventParticipants = class eventParticipants {
	constructor(frm, doctype) {
		this.frm = frm;
		this.doctype = doctype;
		this.make();
	}

	make() {
		let me = this;

		let table = me.frm.get_field("event_participants").grid;
		new criscostack.ui.form.LinkSelector({
			doctype: me.doctype,
			dynamic_link_field: "reference_doctype",
			dynamic_link_reference: me.doctype,
			fieldname: "reference_docname",
			target: table,
			txt: "",
		});
	}
};
