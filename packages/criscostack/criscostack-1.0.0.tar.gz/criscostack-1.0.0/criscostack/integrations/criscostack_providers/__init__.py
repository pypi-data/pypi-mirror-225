# imports - standard imports
import sys

# imports - module imports
from criscostack.integrations.criscostack_providers.criscostackcloud import criscostackcloud_migrator


def migrate_to(local_site, criscostack_provider):
	if criscostack_provider in ("criscostack.cloud", "criscostackcloud.com"):
		return criscostackcloud_migrator(local_site)
	else:
		print(f"{criscostack_provider} is not supported yet")
		sys.exit(1)
