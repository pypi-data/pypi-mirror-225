import types

import criscostack
from criscostack.tests.utils import CriscoTestCase
from criscostack.utils.safe_exec import get_safe_globals, safe_exec


class TestSafeExec(CriscoTestCase):
	def test_import_fails(self):
		self.assertRaises(ImportError, safe_exec, "import os")

	def test_internal_attributes(self):
		self.assertRaises(SyntaxError, safe_exec, "().__class__.__call__")

	def test_utils(self):
		_locals = dict(out=None)
		safe_exec("""out = criscostack.utils.cint("1")""", None, _locals)
		self.assertEqual(_locals["out"], 1)

	def test_safe_eval(self):
		self.assertEqual(criscostack.safe_eval("1+1"), 2)
		self.assertRaises(AttributeError, criscostack.safe_eval, "criscostack.utils.os.path", get_safe_globals())

	def test_sql(self):
		_locals = dict(out=None)
		safe_exec(
			"""out = criscostack.db.sql("select name from tabDocType where name='DocType'")""", None, _locals
		)
		self.assertEqual(_locals["out"][0][0], "DocType")

		self.assertRaises(
			criscostack.PermissionError, safe_exec, 'criscostack.db.sql("update tabToDo set description=NULL")'
		)

	def test_query_builder(self):
		_locals = dict(out=None)
		safe_exec(
			script="""out = criscostack.qb.from_("User").select(criscostack.qb.terms.PseudoColumn("Max(name)")).run()""",
			_globals=None,
			_locals=_locals,
		)
		self.assertEqual(criscostack.db.sql("SELECT Max(name) FROM tabUser"), _locals["out"])

	def test_safe_query_builder(self):
		self.assertRaises(
			criscostack.PermissionError, safe_exec, """criscostack.qb.from_("User").delete().run()"""
		)

	def test_call(self):
		# call non whitelisted method
		self.assertRaises(criscostack.PermissionError, safe_exec, """criscostack.call("criscostack.get_user")""")

		# call whitelisted method
		safe_exec("""criscostack.call("ping")""")

	def test_enqueue(self):
		# enqueue non whitelisted method
		self.assertRaises(
			criscostack.PermissionError, safe_exec, """criscostack.enqueue("criscostack.get_user", now=True)"""
		)

		# enqueue whitelisted method
		safe_exec("""criscostack.enqueue("ping", now=True)""")

	def test_ensure_getattrable_globals(self):
		def check_safe(objects):
			for obj in objects:
				if isinstance(obj, (types.ModuleType, types.CodeType, types.TracebackType, types.FrameType)):
					self.fail(f"{obj} wont work in safe exec.")
				elif isinstance(obj, dict):
					check_safe(obj.values())

		check_safe(get_safe_globals().values())

	def test_unsafe_objects(self):
		unsafe_global = {"criscostack": criscostack}
		self.assertRaises(SyntaxError, safe_exec, """criscostack.msgprint("Hello")""", unsafe_global)

	def test_attrdict(self):
		# jinja
		criscostack.render_template("{% set my_dict = _dict() %} {{- my_dict.works -}}")

		# RestrictedPython
		safe_exec("my_dict = _dict()")
