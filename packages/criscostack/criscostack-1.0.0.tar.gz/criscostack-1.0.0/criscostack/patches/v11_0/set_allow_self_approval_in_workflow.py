import criscostack


def execute():
	criscostack.reload_doc("workflow", "doctype", "workflow_transition")
	criscostack.db.sql("update `tabWorkflow Transition` set allow_self_approval=1")
