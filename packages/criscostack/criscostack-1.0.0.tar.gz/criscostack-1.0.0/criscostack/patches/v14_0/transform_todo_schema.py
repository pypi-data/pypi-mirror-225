import criscostack
from criscostack.query_builder.utils import DocType


def execute():
	# Email Template & Help Article have owner field that doesn't have any additional functionality
	# Only ToDo has to be updated.

	ToDo = DocType("ToDo")
	criscostack.reload_doctype("ToDo", force=True)

	criscostack.qb.update(ToDo).set(ToDo.allocated_to, ToDo.owner).run()
