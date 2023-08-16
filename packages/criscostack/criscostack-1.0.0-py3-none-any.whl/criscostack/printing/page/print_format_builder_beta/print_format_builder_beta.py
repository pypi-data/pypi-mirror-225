# Copyright (c) 2021, Crisco Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt


import functools

import criscostack


@criscostack.whitelist()
def get_google_fonts():
	return _get_google_fonts()


@functools.lru_cache
def _get_google_fonts():
	file_path = criscostack.get_app_path("criscostack", "data", "google_fonts.json")
	return criscostack.parse_json(criscostack.read_file(file_path))
