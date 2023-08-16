// Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
// MIT License. See license.txt

// for translation
criscostack._ = function (txt, replace, context = null) {
	if (!txt) return txt;
	if (typeof txt != "string") return txt;

	let translated_text = "";

	let key = txt; // txt.replace(/\n/g, "");
	if (context) {
		translated_text = criscostack._messages[`${key}:${context}`];
	}

	if (!translated_text) {
		translated_text = criscostack._messages[key] || txt;
	}

	if (replace && typeof replace === "object") {
		translated_text = $.format(translated_text, replace);
	}
	return translated_text;
};

window.__ = criscostack._;

criscostack.get_languages = function () {
	if (!criscostack.languages) {
		criscostack.languages = [];
		$.each(criscostack.boot.lang_dict, function (lang, value) {
			criscostack.languages.push({ label: lang, value: value });
		});
		criscostack.languages = criscostack.languages.sort(function (a, b) {
			return a.value < b.value ? -1 : 1;
		});
	}
	return criscostack.languages;
};
