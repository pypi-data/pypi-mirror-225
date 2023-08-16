import criscostack
from criscostack.cache_manager import clear_defaults_cache


def execute():
	criscostack.db.set_default(
		"suspend_email_queue",
		criscostack.db.get_default("hold_queue", "Administrator") or 0,
		parent="__default",
	)

	criscostack.db.delete("DefaultValue", {"defkey": "hold_queue"})
	clear_defaults_cache()
