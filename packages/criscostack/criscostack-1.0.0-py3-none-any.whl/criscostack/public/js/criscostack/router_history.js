criscostack.route_history_queue = [];
const routes_to_skip = ["Form", "social", "setup-wizard", "recorder"];

const save_routes = criscostack.utils.debounce(() => {
	if (criscostack.session.user === "Guest") return;
	const routes = criscostack.route_history_queue;
	if (!routes.length) return;

	criscostack.route_history_queue = [];

	criscostack
		.xcall("criscostack.desk.doctype.route_history.route_history.deferred_insert", {
			routes: routes,
		})
		.catch(() => {
			criscostack.route_history_queue.concat(routes);
		});
}, 10000);

criscostack.router.on("change", () => {
	const route = criscostack.get_route();
	if (is_route_useful(route)) {
		criscostack.route_history_queue.push({
			creation: criscostack.datetime.now_datetime(),
			route: criscostack.get_route_str(),
		});

		save_routes();
	}
});

function is_route_useful(route) {
	if (!route[1]) {
		return false;
	} else if ((route[0] === "List" && !route[2]) || routes_to_skip.includes(route[0])) {
		return false;
	} else {
		return true;
	}
}
