import criscostack
from criscostack.website.page_renderers.error_page import ErrorPage
from criscostack.website.page_renderers.not_found_page import NotFoundPage
from criscostack.website.page_renderers.not_permitted_page import NotPermittedPage
from criscostack.website.page_renderers.redirect_page import RedirectPage
from criscostack.website.path_resolver import PathResolver


def get_response(path=None, http_status_code=200):
	"""Resolves path and renders page"""
	response = None
	path = path or criscostack.local.request.path
	endpoint = path

	try:
		path_resolver = PathResolver(path)
		endpoint, renderer_instance = path_resolver.resolve()
		response = renderer_instance.render()
	except criscostack.Redirect:
		return RedirectPage(endpoint or path, http_status_code).render()
	except criscostack.PermissionError as e:
		response = NotPermittedPage(endpoint, http_status_code, exception=e).render()
	except criscostack.PageDoesNotExistError:
		response = NotFoundPage(endpoint, http_status_code).render()
	except Exception as e:
		response = ErrorPage(exception=e).render()

	return response


def get_response_content(path=None, http_status_code=200):
	response = get_response(path, http_status_code)
	return str(response.data, "utf-8")
