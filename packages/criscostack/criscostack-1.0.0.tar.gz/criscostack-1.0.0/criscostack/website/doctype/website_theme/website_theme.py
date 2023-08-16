# Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and contributors
# License: MIT. See LICENSE

from os.path import abspath
from os.path import exists as path_exists
from os.path import join as join_path
from os.path import splitext
from typing import Optional

import criscostack
from criscostack import _
from criscostack.model.document import Document
from criscostack.utils import get_path


class WebsiteTheme(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from criscostack.types import DF
		from criscostack.website.doctype.website_theme_ignore_app.website_theme_ignore_app import (
			WebsiteThemeIgnoreApp,
		)

		background_color: DF.Link | None
		button_gradients: DF.Check
		button_rounded_corners: DF.Check
		button_shadows: DF.Check
		custom: DF.Check
		custom_overrides: DF.Code | None
		custom_scss: DF.Code | None
		dark_color: DF.Link | None
		font_properties: DF.Data | None
		font_size: DF.Data | None
		google_font: DF.Data | None
		ignored_apps: DF.Table[WebsiteThemeIgnoreApp]
		js: DF.Code | None
		light_color: DF.Link | None
		module: DF.Link
		primary_color: DF.Link | None
		text_color: DF.Link | None
		theme: DF.Data
		theme_scss: DF.Code | None
		theme_url: DF.Data | None
	# end: auto-generated types
	def validate(self):
		self.validate_if_customizable()
		self.generate_bootstrap_theme()

	def on_update(self):
		if (
			not self.custom
			and criscostack.local.conf.get("developer_mode")
			and not (criscostack.flags.in_import or criscostack.flags.in_test)
		):

			self.export_doc()

		self.clear_cache_if_current_theme()

	def is_standard_and_not_valid_user(self):
		return (
			not self.custom
			and not criscostack.local.conf.get("developer_mode")
			and not (criscostack.flags.in_import or criscostack.flags.in_test or criscostack.flags.in_migrate)
		)

	def on_trash(self):
		if self.is_standard_and_not_valid_user():
			criscostack.throw(
				_("You are not allowed to delete a standard Website Theme"), criscostack.PermissionError
			)

	def validate_if_customizable(self):
		if self.is_standard_and_not_valid_user():
			criscostack.throw(_("Please Duplicate this Website Theme to customize."))

	def export_doc(self):
		"""Export to standard folder `[module]/website_theme/[name]/[name].json`."""
		from criscostack.modules.export_file import export_to_files

		export_to_files(record_list=[["Website Theme", self.name]], create_init=True)

	def clear_cache_if_current_theme(self):
		if criscostack.flags.in_install == "criscostack":
			return
		website_settings = criscostack.get_doc("Website Settings", "Website Settings")
		if getattr(website_settings, "website_theme", None) == self.name:
			website_settings.clear_cache()

	def generate_bootstrap_theme(self):
		from subprocess import PIPE, Popen

		# create theme file in site public files folder
		folder_path = abspath(criscostack.utils.get_files_path("website_theme", is_private=False))
		# create folder if not exist
		criscostack.create_folder(folder_path)

		if self.custom:
			self.delete_old_theme_files(folder_path)

		# add a random suffix
		suffix = criscostack.generate_hash(length=8) if self.custom else "style"
		file_name = criscostack.scrub(self.name) + "_" + suffix + ".css"
		output_path = join_path(folder_path, file_name)

		self.theme_scss = content = get_scss(self)
		content = content.replace("\n", "\\n")
		command = ["node", "generate_bootstrap_theme.js", output_path, content]

		process = Popen(command, cwd=criscostack.get_app_path("criscostack", ".."), stdout=PIPE, stderr=PIPE)

		stderr = process.communicate()[1]

		if stderr:
			stderr = criscostack.safe_decode(stderr)
			stderr = stderr.replace("\n", "<br>")
			criscostack.throw(f'<div style="font-family: monospace;">{stderr}</div>')
		else:
			self.theme_url = "/files/website_theme/" + file_name

		criscostack.msgprint(_("Compiled Successfully"), alert=True)

	def delete_old_theme_files(self, folder_path):
		import os

		for fname in os.listdir(folder_path):
			if fname.startswith(criscostack.scrub(self.name) + "_") and fname.endswith(".css"):
				os.remove(os.path.join(folder_path, fname))

	@criscostack.whitelist()
	def set_as_default(self):
		self.save()
		website_settings = criscostack.get_doc("Website Settings")
		website_settings.website_theme = self.name
		website_settings.ignore_validate = True
		website_settings.save()

	@criscostack.whitelist()
	def get_apps(self):
		from criscostack.utils.change_log import get_versions

		apps = get_versions()
		out = []
		for app, values in apps.items():
			out.append({"name": app, "title": values["title"]})
		return out


def get_active_theme() -> Optional["WebsiteTheme"]:
	if website_theme := criscostack.get_website_settings("website_theme"):
		try:
			return criscostack.get_cached_doc("Website Theme", website_theme)
		except criscostack.DoesNotExistError:
			criscostack.clear_last_message()
			pass


def get_scss(website_theme):
	"""
	Render `website_theme_template.scss` with the values defined in Website Theme.

	params:
	website_theme - instance of a Website Theme
	"""
	apps_to_ignore = tuple((d.app + "/") for d in website_theme.ignored_apps)
	available_imports = get_scss_paths()
	imports_to_include = [d for d in available_imports if not d.startswith(apps_to_ignore)]
	context = website_theme.as_dict()
	context["website_theme_scss"] = imports_to_include
	return criscostack.render_template(
		"criscostack/website/doctype/website_theme/website_theme_template.scss", context
	)


def get_scss_paths():
	"""
	Return a set of SCSS import paths from all apps that provide `website.scss`.

	If `$BENCH_PATH/apps/criscostack/criscostack/public/scss/website[.bundle].scss` exists, the
	returned set will contain 'criscostack/public/scss/website[.bundle]'.
	"""
	import_path_list = []
	bench_path = criscostack.utils.get_bench_path()

	scss_files = ["public/scss/website.scss", "public/scss/website.bundle.scss"]
	for app in criscostack.get_installed_apps():
		for scss_file in scss_files:
			relative_path = join_path(app, scss_file)
			full_path = get_path("apps", app, relative_path, base=bench_path)
			if path_exists(full_path):
				import_path = splitext(relative_path)[0]
				import_path_list.append(import_path)

	return import_path_list


def after_migrate():
	"""
	Regenerate Active Theme CSS file after migration.

	Necessary to reflect possible changes in the imported SCSS files. Called at
	the end of every `bench migrate`.
	"""
	website_theme = criscostack.db.get_single_value("Website Settings", "website_theme")
	if not website_theme or website_theme == "Standard":
		return

	doc = criscostack.get_doc("Website Theme", website_theme)
	doc.save()  # Just re-saving re-generates the theme.
