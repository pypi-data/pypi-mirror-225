import criscostack
from criscostack import _
from criscostack.utils import cstr
from criscostack.website.page_renderers.template_page import TemplatePage


class NotPermittedPage(TemplatePage):
	def __init__(self, path=None, http_status_code=None, exception=""):
		criscostack.local.message = cstr(exception)
		super().__init__(path=path, http_status_code=http_status_code)
		self.http_status_code = 403

	def can_render(self):
		return True

	def render(self):
		action = f"/login?redirect-to={criscostack.request.path}"
		if criscostack.request.path.startswith("/app"):
			action = "/login"
		criscostack.local.message_title = _("Not Permitted")
		criscostack.local.response["context"] = dict(
			indicator_color="red", primary_action=action, primary_label=_("Login"), fullpage=True
		)
		self.set_standard_path("message")
		return super().render()
