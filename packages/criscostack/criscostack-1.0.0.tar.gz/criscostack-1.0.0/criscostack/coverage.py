# Copyright (c) 2021, Crisco Technologies Pvt. Ltd. and Contributors
# MIT License. See LICENSE
"""
	criscostack.coverage
	~~~~~~~~~~~~~~~~

	Coverage settings for criscostack
"""

STANDARD_INCLUSIONS = ["*.py"]

STANDARD_EXCLUSIONS = [
	"*.js",
	"*.xml",
	"*.pyc",
	"*.css",
	"*.less",
	"*.scss",
	"*.vue",
	"*.html",
	"*/test_*",
	"*/node_modules/*",
	"*/doctype/*/*_dashboard.py",
	"*/patches/*",
]

# tested via commands' test suite
TESTED_VIA_CLI = [
	"*/criscostack/installer.py",
	"*/criscostack/build.py",
	"*/criscostack/database/__init__.py",
	"*/criscostack/database/db_manager.py",
	"*/criscostack/database/**/setup_db.py",
]

CRISCOSTACK_EXCLUSIONS = [
	"*/tests/*",
	"*/commands/*",
	"*/criscostack/change_log/*",
	"*/criscostack/exceptions*",
	"*/criscostack/coverage.py",
	"*criscostack/setup.py",
	"*/doctype/*/*_dashboard.py",
	"*/patches/*",
] + TESTED_VIA_CLI


class CodeCoverage:
	def __init__(self, with_coverage, app):
		self.with_coverage = with_coverage
		self.app = app or "criscostack"

	def __enter__(self):
		if self.with_coverage:
			import os

			from coverage import Coverage

			from criscostack.utils import get_bench_path

			# Generate coverage report only for app that is being tested
			source_path = os.path.join(get_bench_path(), "apps", self.app)
			omit = STANDARD_EXCLUSIONS[:]

			if self.app == "criscostack":
				omit.extend(CRISCOSTACK_EXCLUSIONS)

			self.coverage = Coverage(source=[source_path], omit=omit, include=STANDARD_INCLUSIONS)
			self.coverage.start()

	def __exit__(self, exc_type, exc_value, traceback):
		if self.with_coverage:
			self.coverage.stop()
			self.coverage.save()
			self.coverage.xml_report()
			print("Saved Coverage")
