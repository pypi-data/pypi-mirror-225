// Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
// MIT License. See license.txt

if (criscostack.require) {
	criscostack.require("file_uploader.bundle.js");
} else {
	criscostack.ready(function () {
		criscostack.require("file_uploader.bundle.js");
	});
}
