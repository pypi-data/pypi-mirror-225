import re

import click
from werkzeug.routing import Rule

import criscostack
from criscostack.website.page_renderers.document_page import DocumentPage
from criscostack.website.page_renderers.list_page import ListPage
from criscostack.website.page_renderers.not_found_page import NotFoundPage
from criscostack.website.page_renderers.print_page import PrintPage
from criscostack.website.page_renderers.redirect_page import RedirectPage
from criscostack.website.page_renderers.static_page import StaticPage
from criscostack.website.page_renderers.template_page import TemplatePage
from criscostack.website.page_renderers.web_form import WebFormPage
from criscostack.website.router import evaluate_dynamic_routes
from criscostack.website.utils import can_cache, get_home_page


class PathResolver:
	__slots__ = ("path",)

	def __init__(self, path):
		self.path = path.strip("/ ")

	def resolve(self):
		"""Returns endpoint and a renderer instance that can render the endpoint"""
		request = criscostack._dict()
		if hasattr(criscostack.local, "request"):
			request = criscostack.local.request or request

		# check if the request url is in 404 list
		if request.url and can_cache() and criscostack.cache.hget("website_404", request.url):
			return self.path, NotFoundPage(self.path)

		try:
			resolve_redirect(self.path, request.query_string)
		except criscostack.Redirect:
			return criscostack.flags.redirect_location, RedirectPage(self.path)

		endpoint = resolve_path(self.path)

		# WARN: Hardcoded for better performance
		if endpoint == "app":
			return endpoint, TemplatePage(endpoint, 200)

		custom_renderers = self.get_custom_page_renderers()
		renderers = custom_renderers + [
			StaticPage,
			WebFormPage,
			DocumentPage,
			TemplatePage,
			ListPage,
			PrintPage,
		]

		for renderer in renderers:
			renderer_instance = renderer(endpoint, 200)
			if renderer_instance.can_render():
				return endpoint, renderer_instance

		return endpoint, NotFoundPage(endpoint)

	def is_valid_path(self):
		_endpoint, renderer_instance = self.resolve()
		return not isinstance(renderer_instance, NotFoundPage)

	@staticmethod
	def get_custom_page_renderers():
		custom_renderers = []
		for renderer_path in criscostack.get_hooks("page_renderer") or []:
			try:
				renderer = criscostack.get_attr(renderer_path)
				if not hasattr(renderer, "can_render"):
					click.echo(f"{renderer.__name__} does not have can_render method")
					continue
				if not hasattr(renderer, "render"):
					click.echo(f"{renderer.__name__} does not have render method")
					continue

				custom_renderers.append(renderer)

			except Exception:
				click.echo(f"Failed to load page renderer. Import path: {renderer_path}")

		return custom_renderers


def resolve_redirect(path, query_string=None):
	"""
	Resolve redirects from hooks

	Example:

	                website_redirect = [
	                                # absolute location
	                                {"source": "/from", "target": "https://mysite/from"},

	                                # relative location
	                                {"source": "/from", "target": "/main"},

	                                # use regex
	                                {"source": r"/from/(.*)", "target": r"/main/\1"}
	                                # use r as a string prefix if you use regex groups or want to escape any string literal
	                ]
	"""
	redirects = criscostack.get_hooks("website_redirects")
	redirects += criscostack.get_all("Website Route Redirect", ["source", "target"], order_by=None)

	if not redirects:
		return

	redirect_to = criscostack.cache.hget("website_redirects", path)

	if redirect_to:
		criscostack.flags.redirect_location = redirect_to
		raise criscostack.Redirect

	for rule in redirects:
		pattern = rule["source"].strip("/ ") + "$"
		path_to_match = path
		if rule.get("match_with_query_string"):
			path_to_match = path + "?" + criscostack.safe_decode(query_string)

		try:
			match = re.match(pattern, path_to_match)
		except re.error as e:
			criscostack.log_error("Broken Redirect: " + pattern)

		if match:
			redirect_to = re.sub(pattern, rule["target"], path_to_match)
			criscostack.flags.redirect_location = redirect_to
			criscostack.cache.hset("website_redirects", path_to_match, redirect_to)
			raise criscostack.Redirect


def resolve_path(path):
	if not path:
		path = "index"

	if path.endswith(".html"):
		path = path[:-5]

	if path == "index":
		path = get_home_page()

	criscostack.local.path = path

	if path != "index":
		path = resolve_from_map(path)

	return path


def resolve_from_map(path):
	"""transform dynamic route to a static one from hooks and route defined in doctype"""
	rules = [
		Rule(r["from_route"], endpoint=r["to_route"], defaults=r.get("defaults"))
		for r in get_website_rules()
	]

	return evaluate_dynamic_routes(rules, path) or path


def get_website_rules():
	"""Get website route rules from hooks and DocType route"""

	def _get():
		rules = criscostack.get_hooks("website_route_rules")
		for d in criscostack.get_all("DocType", "name, route", dict(has_web_view=1)):
			if d.route:
				rules.append(dict(from_route="/" + d.route.strip("/"), to_route=d.name))

		return rules

	if criscostack.local.dev_server:
		# dont cache in development
		return _get()

	return criscostack.cache.get_value("website_route_rules", _get)
