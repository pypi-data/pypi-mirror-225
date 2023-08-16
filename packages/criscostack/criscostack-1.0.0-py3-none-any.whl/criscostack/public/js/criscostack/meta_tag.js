criscostack.provide("criscostack.model");
criscostack.provide("criscostack.utils");

/**
 * Opens the Website Meta Tag form if it exists for {route}
 * or creates a new doc and opens the form
 */
criscostack.utils.set_meta_tag = function (route) {
	criscostack.db.exists("Website Route Meta", route).then((exists) => {
		if (exists) {
			criscostack.set_route("Form", "Website Route Meta", route);
		} else {
			// new doc
			const doc = criscostack.model.get_new_doc("Website Route Meta");
			doc.__newname = route;
			criscostack.set_route("Form", doc.doctype, doc.name);
		}
	});
};
