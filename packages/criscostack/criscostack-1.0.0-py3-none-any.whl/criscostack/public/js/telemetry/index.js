import "../lib/posthog.js";

class TelemetryManager {
	constructor() {
		this.enabled = false;

		this.project_id = criscostack.boot.posthog_project_id;
		this.telemetry_host = criscostack.boot.posthog_host;
		this.site_age = criscostack.boot.telemetry_site_age;

		if (cint(criscostack.boot.enable_telemetry) && this.project_id && this.telemetry_host) {
			this.enabled = true;
		}
	}

	initialize() {
		if (!this.enabled) return;
		try {
			posthog.init(this.project_id, {
				api_host: this.telemetry_host,
				autocapture: false,
				capture_pageview: false,
				capture_pageleave: false,
				advanced_disable_decide: true,
			});
			posthog.identify(criscostack.boot.sitename);
			this.send_heartbeat();
			this.register_pageview_handler();
		} catch (e) {
			console.trace("Failed to initialize telemetry", e);
			this.enabled = false;
		}
	}

	capture(event, app, props) {
		if (!this.enabled) return;
		posthog.capture(`${app}_${event}`, props);
	}

	disable() {
		this.enabled = false;
		posthog.opt_out_capturing();
	}

	send_heartbeat() {
		const KEY = "ph_last_heartbeat";
		const now = criscostack.datetime.system_datetime(true);
		const last = localStorage.getItem(KEY);

		if (!last || moment(now).diff(moment(last), "hours") > 12) {
			localStorage.setItem(KEY, now.toISOString());
			this.capture("heartbeat", "criscostack", { criscostack_version: criscostack.boot?.versions?.criscostack });
		}
	}

	register_pageview_handler() {
		if (this.site_age && this.site_age > 5) {
			return;
		}

		criscostack.router.on("change", () => {
			posthog.capture("$pageview");
		});
	}
}

criscostack.telemetry = new TelemetryManager();
criscostack.telemetry.initialize();
