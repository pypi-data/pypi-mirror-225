import criscostack
import criscostack.share


def execute():
	for user in criscostack.STANDARD_USERS:
		criscostack.share.remove("User", user, user)
