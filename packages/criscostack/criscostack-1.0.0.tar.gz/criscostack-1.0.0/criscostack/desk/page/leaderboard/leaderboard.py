# Copyright (c) 2017, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE
import criscostack


@criscostack.whitelist()
def get_leaderboard_config():
	leaderboard_config = criscostack._dict()
	leaderboard_hooks = criscostack.get_hooks("leaderboards")
	for hook in leaderboard_hooks:
		leaderboard_config.update(criscostack.get_attr(hook)())

	return leaderboard_config
