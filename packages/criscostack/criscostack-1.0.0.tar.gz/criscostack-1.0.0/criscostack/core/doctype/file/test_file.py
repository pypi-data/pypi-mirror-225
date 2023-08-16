# Copyright (c) 2022, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE
import base64
import json
import os
import shutil
import tempfile
from contextlib import contextmanager
from typing import TYPE_CHECKING

import criscostack
from criscostack import _
from criscostack.core.api.file import (
	create_new_folder,
	get_attached_images,
	get_files_in_folder,
	move_file,
	unzip_file,
)
from criscostack.core.doctype.file.utils import delete_file, get_extension
from criscostack.exceptions import ValidationError
from criscostack.tests.utils import CriscoTestCase
from criscostack.utils import get_files_path

if TYPE_CHECKING:
	from criscostack.core.doctype.file.file import File

test_content1 = "Hello"
test_content2 = "Hello World"


def make_test_doc(ignore_permissions=False):
	d = criscostack.new_doc("ToDo")
	d.description = "Test"
	d.assigned_by = criscostack.session.user
	d.save(ignore_permissions)
	return d.doctype, d.name


@contextmanager
def make_test_image_file():
	file_path = criscostack.get_app_path("criscostack", "tests/data/sample_image_for_optimization.jpg")
	with open(file_path, "rb") as f:
		file_content = f.read()

	test_file = criscostack.get_doc(
		{"doctype": "File", "file_name": "sample_image_for_optimization.jpg", "content": file_content}
	).insert()
	# remove those flags
	_test_file: "File" = criscostack.get_doc("File", test_file.name)

	try:
		yield _test_file
	finally:
		_test_file.delete()


class TestSimpleFile(CriscoTestCase):
	def setUp(self):
		self.attached_to_doctype, self.attached_to_docname = make_test_doc()
		self.test_content = test_content1
		_file = criscostack.get_doc(
			{
				"doctype": "File",
				"file_name": "test1.txt",
				"attached_to_doctype": self.attached_to_doctype,
				"attached_to_name": self.attached_to_docname,
				"content": self.test_content,
			}
		)
		_file.save()
		self.saved_file_url = _file.file_url

	def test_save(self):
		_file = criscostack.get_doc("File", {"file_url": self.saved_file_url})
		content = _file.get_content()
		self.assertEqual(content, self.test_content)


class TestFSRollbacks(CriscoTestCase):
	def test_rollback_from_file_system(self):
		file_name = content = criscostack.generate_hash()
		file = criscostack.new_doc("File", file_name=file_name, content=content).insert()
		self.assertTrue(file.exists_on_disk())

		criscostack.db.rollback()
		self.assertFalse(file.exists_on_disk())


class TestBase64File(CriscoTestCase):
	def setUp(self):
		self.attached_to_doctype, self.attached_to_docname = make_test_doc()
		self.test_content = base64.b64encode(test_content1.encode("utf-8"))
		_file: "File" = criscostack.get_doc(
			{
				"doctype": "File",
				"file_name": "test_base64.txt",
				"attached_to_doctype": self.attached_to_doctype,
				"attached_to_name": self.attached_to_docname,
				"content": self.test_content,
				"decode": True,
			}
		)
		_file.save()
		self.saved_file_url = _file.file_url

	def test_saved_content(self):
		_file = criscostack.get_doc("File", {"file_url": self.saved_file_url})
		content = _file.get_content()
		self.assertEqual(content, test_content1)


class TestSameFileName(CriscoTestCase):
	def test_saved_content(self):
		self.attached_to_doctype, self.attached_to_docname = make_test_doc()
		self.test_content1 = test_content1
		self.test_content2 = test_content2
		_file1 = criscostack.get_doc(
			{
				"doctype": "File",
				"file_name": "testing.txt",
				"attached_to_doctype": self.attached_to_doctype,
				"attached_to_name": self.attached_to_docname,
				"content": self.test_content1,
			}
		)
		_file1.save()
		_file2 = criscostack.get_doc(
			{
				"doctype": "File",
				"file_name": "testing.txt",
				"attached_to_doctype": self.attached_to_doctype,
				"attached_to_name": self.attached_to_docname,
				"content": self.test_content2,
			}
		)
		_file2.save()
		self.saved_file_url1 = _file1.file_url
		self.saved_file_url2 = _file2.file_url

		_file = criscostack.get_doc("File", {"file_url": self.saved_file_url1})
		content1 = _file.get_content()
		self.assertEqual(content1, self.test_content1)
		_file = criscostack.get_doc("File", {"file_url": self.saved_file_url2})
		content2 = _file.get_content()
		self.assertEqual(content2, self.test_content2)

	def test_saved_content_private(self):
		_file1 = criscostack.get_doc(
			{
				"doctype": "File",
				"file_name": "testing-private.txt",
				"content": test_content1,
				"is_private": 1,
			}
		).insert()
		_file2 = criscostack.get_doc(
			{
				"doctype": "File",
				"file_name": "testing-private.txt",
				"content": test_content2,
				"is_private": 1,
			}
		).insert()

		_file = criscostack.get_doc("File", {"file_url": _file1.file_url})
		self.assertEqual(_file.get_content(), test_content1)

		_file = criscostack.get_doc("File", {"file_url": _file2.file_url})
		self.assertEqual(_file.get_content(), test_content2)


class TestSameContent(CriscoTestCase):
	def setUp(self):
		self.attached_to_doctype1, self.attached_to_docname1 = make_test_doc()
		self.attached_to_doctype2, self.attached_to_docname2 = make_test_doc()
		self.test_content1 = test_content1
		self.test_content2 = test_content1
		self.orig_filename = "hello.txt"
		self.dup_filename = "hello2.txt"
		_file1 = criscostack.get_doc(
			{
				"doctype": "File",
				"file_name": self.orig_filename,
				"attached_to_doctype": self.attached_to_doctype1,
				"attached_to_name": self.attached_to_docname1,
				"content": self.test_content1,
			}
		)
		_file1.save()

		_file2 = criscostack.get_doc(
			{
				"doctype": "File",
				"file_name": self.dup_filename,
				"attached_to_doctype": self.attached_to_doctype2,
				"attached_to_name": self.attached_to_docname2,
				"content": self.test_content2,
			}
		)

		_file2.save()

	def test_saved_content(self):
		self.assertFalse(os.path.exists(get_files_path(self.dup_filename)))

	def test_attachment_limit(self):
		doctype, docname = make_test_doc()
		from criscostack.custom.doctype.property_setter.property_setter import make_property_setter

		limit_property = make_property_setter(
			"ToDo", None, "max_attachments", 1, "int", for_doctype=True
		)
		file1 = criscostack.get_doc(
			{
				"doctype": "File",
				"file_name": "test-attachment",
				"attached_to_doctype": doctype,
				"attached_to_name": docname,
				"content": "test",
			}
		)

		file1.insert()

		file2 = criscostack.get_doc(
			{
				"doctype": "File",
				"file_name": "test-attachment",
				"attached_to_doctype": doctype,
				"attached_to_name": docname,
				"content": "test2",
			}
		)

		self.assertRaises(criscostack.exceptions.AttachmentLimitReached, file2.insert)
		limit_property.delete()
		criscostack.clear_cache(doctype="ToDo")


class TestFile(CriscoTestCase):
	def setUp(self):
		criscostack.set_user("Administrator")
		self.delete_test_data()
		self.upload_file()

	def tearDown(self):
		try:
			criscostack.get_doc("File", {"file_name": "file_copy.txt"}).delete()
		except criscostack.DoesNotExistError:
			pass

	def delete_test_data(self):
		test_file_data = criscostack.get_all(
			"File",
			pluck="name",
			filters={"is_home_folder": 0, "is_attachments_folder": 0},
			order_by="creation desc",
		)
		for f in test_file_data:
			criscostack.delete_doc("File", f)

	def upload_file(self):
		_file = criscostack.get_doc(
			{
				"doctype": "File",
				"file_name": "file_copy.txt",
				"attached_to_name": "",
				"attached_to_doctype": "",
				"folder": self.get_folder("Test Folder 1", "Home").name,
				"content": "Testing file copy example.",
			}
		)
		_file.save()
		self.saved_folder = _file.folder
		self.saved_name = _file.name
		self.saved_filename = get_files_path(_file.file_name)

	def get_folder(self, folder_name, parent_folder="Home"):
		return criscostack.get_doc(
			{"doctype": "File", "file_name": _(folder_name), "is_folder": 1, "folder": _(parent_folder)}
		).insert()

	def tests_after_upload(self):
		self.assertEqual(self.saved_folder, _("Home/Test Folder 1"))
		file_folder = criscostack.db.get_value("File", self.saved_name, "folder")
		self.assertEqual(file_folder, _("Home/Test Folder 1"))

	def test_file_copy(self):
		folder = self.get_folder("Test Folder 2", "Home")

		file = criscostack.get_doc("File", {"file_name": "file_copy.txt"})
		move_file([{"name": file.name}], folder.name, file.folder)
		file = criscostack.get_doc("File", {"file_name": "file_copy.txt"})

		self.assertEqual(_("Home/Test Folder 2"), file.folder)

	def test_folder_depth(self):
		result1 = self.get_folder("d1", "Home")
		self.assertEqual(result1.name, "Home/d1")
		result2 = self.get_folder("d2", "Home/d1")
		self.assertEqual(result2.name, "Home/d1/d2")
		result3 = self.get_folder("d3", "Home/d1/d2")
		self.assertEqual(result3.name, "Home/d1/d2/d3")
		result4 = self.get_folder("d4", "Home/d1/d2/d3")
		_file = criscostack.get_doc(
			{
				"doctype": "File",
				"file_name": "folder_copy.txt",
				"attached_to_name": "",
				"attached_to_doctype": "",
				"folder": result4.name,
				"content": "Testing folder copy example",
			}
		)
		_file.save()

	def test_folder_copy(self):
		folder = self.get_folder("Test Folder 2", "Home")
		folder = self.get_folder("Test Folder 3", "Home/Test Folder 2")
		_file = criscostack.get_doc(
			{
				"doctype": "File",
				"file_name": "folder_copy.txt",
				"attached_to_name": "",
				"attached_to_doctype": "",
				"folder": folder.name,
				"content": "Testing folder copy example",
			}
		)
		_file.save()

		move_file([{"name": folder.name}], "Home/Test Folder 1", folder.folder)

		file = criscostack.get_doc("File", {"file_name": "folder_copy.txt"})
		file_copy_txt = criscostack.get_value("File", {"file_name": "file_copy.txt"})
		if file_copy_txt:
			criscostack.get_doc("File", file_copy_txt).delete()

		self.assertEqual(_("Home/Test Folder 1/Test Folder 3"), file.folder)

	def test_default_folder(self):
		d = criscostack.get_doc({"doctype": "File", "file_name": _("Test_Folder"), "is_folder": 1})
		d.save()
		self.assertEqual(d.folder, "Home")

	def test_on_delete(self):
		file = criscostack.get_doc("File", {"file_name": "file_copy.txt"})
		file.delete()

		self.assertEqual(criscostack.db.get_value("File", _("Home/Test Folder 1"), "file_size"), 0)

		folder = self.get_folder("Test Folder 3", "Home/Test Folder 1")
		_file = criscostack.get_doc(
			{
				"doctype": "File",
				"file_name": "folder_copy.txt",
				"attached_to_name": "",
				"attached_to_doctype": "",
				"folder": folder.name,
				"content": "Testing folder copy example",
			}
		)
		_file.save()

		folder = criscostack.get_doc("File", "Home/Test Folder 1/Test Folder 3")
		self.assertRaises(ValidationError, folder.delete)

	def test_same_file_url_update(self):
		attached_to_doctype1, attached_to_docname1 = make_test_doc()
		attached_to_doctype2, attached_to_docname2 = make_test_doc()

		file1 = criscostack.get_doc(
			{
				"doctype": "File",
				"file_name": "file1.txt",
				"attached_to_doctype": attached_to_doctype1,
				"attached_to_name": attached_to_docname1,
				"is_private": 1,
				"content": test_content1,
			}
		).insert()

		file2 = criscostack.get_doc(
			{
				"doctype": "File",
				"file_name": "file2.txt",
				"attached_to_doctype": attached_to_doctype2,
				"attached_to_name": attached_to_docname2,
				"is_private": 1,
				"content": test_content1,
			}
		).insert()

		self.assertEqual(file1.is_private, file2.is_private, 1)
		self.assertEqual(file1.file_url, file2.file_url)
		self.assertTrue(os.path.exists(file1.get_full_path()))

		file1.is_private = 0
		file1.save()

		file2 = criscostack.get_doc("File", file2.name)

		self.assertEqual(file1.is_private, file2.is_private, 0)
		self.assertEqual(file1.file_url, file2.file_url)
		self.assertTrue(os.path.exists(file2.get_full_path()))

	def test_parent_directory_validation_in_file_url(self):
		file1 = criscostack.get_doc(
			{
				"doctype": "File",
				"file_name": "parent_dir.txt",
				"is_private": 1,
				"content": test_content1,
			}
		).insert()

		file1.file_url = "/private/files/../test.txt"
		self.assertRaises(ValidationError, file1.save)

		# No validation to see if file exists
		file1.reload()
		file1.file_url = "/private/files/parent_dir2.txt"
		self.assertRaises(OSError, file1.save)

	def test_file_url_validation(self):
		test_file: "File" = criscostack.new_doc("File")
		test_file.update({"file_name": "logo", "file_url": "https://criscostack.io/files/criscostack.png"})

		self.assertIsNone(test_file.validate())

		# bad path
		test_file.file_url = "/usr/bin/man"
		self.assertRaisesRegex(
			ValidationError, f"Cannot access file path {test_file.file_url}", test_file.validate
		)

		test_file.file_url = None
		test_file.file_name = "/usr/bin/man"
		self.assertRaisesRegex(
			ValidationError, "There is some problem with the file url", test_file.validate
		)

		test_file.file_url = None
		test_file.file_name = "_file"
		self.assertRaisesRegex(IOError, "does not exist", test_file.validate)

		test_file.file_url = None
		test_file.file_name = "/private/files/_file"
		self.assertRaisesRegex(ValidationError, "File name cannot have", test_file.validate)

	def test_make_thumbnail(self):
		# test web image
		test_file: "File" = criscostack.get_doc(
			{
				"doctype": "File",
				"file_name": "logo",
				"file_url": criscostack.utils.get_url("/_test/assets/image.jpg"),
			}
		).insert(ignore_permissions=True)

		test_file.make_thumbnail()
		self.assertEqual(test_file.thumbnail_url, "/files/image_small.jpg")

		# test web image without extension
		test_file = criscostack.get_doc(
			{
				"doctype": "File",
				"file_name": "logo",
				"file_url": criscostack.utils.get_url("/_test/assets/image"),
			}
		).insert(ignore_permissions=True)

		test_file.make_thumbnail()
		self.assertTrue(test_file.thumbnail_url.endswith("_small.jpg"))

		# test local image
		test_file.db_set("thumbnail_url", None)
		test_file.reload()
		test_file.file_url = "/files/image_small.jpg"
		test_file.make_thumbnail(suffix="xs", crop=True)
		self.assertEqual(test_file.thumbnail_url, "/files/image_small_xs.jpg")

		criscostack.clear_messages()
		test_file.db_set("thumbnail_url", None)
		test_file.reload()
		test_file.file_url = criscostack.utils.get_url("unknown.jpg")
		test_file.make_thumbnail(suffix="xs")
		self.assertEqual(
			json.loads(criscostack.message_log[0]).get("message"),
			f"File '{criscostack.utils.get_url('unknown.jpg')}' not found",
		)
		self.assertEqual(test_file.thumbnail_url, None)

	def test_file_unzip(self):
		file_path = criscostack.get_app_path("criscostack", "www/_test/assets/file.zip")
		public_file_path = criscostack.get_site_path("public", "files")
		try:
			import shutil

			shutil.copy(file_path, public_file_path)
		except Exception:
			pass

		test_file = criscostack.get_doc(
			{
				"doctype": "File",
				"file_url": "/files/file.zip",
			}
		).insert(ignore_permissions=True)

		self.assertListEqual(
			[file.file_name for file in unzip_file(test_file.name)],
			["css_asset.css", "image.jpg", "js_asset.min.js"],
		)

		test_file = criscostack.get_doc(
			{
				"doctype": "File",
				"file_url": criscostack.utils.get_url("/_test/assets/image.jpg"),
			}
		).insert(ignore_permissions=True)
		self.assertRaisesRegex(ValidationError, "not a zip file", test_file.unzip)

	def test_create_file_without_file_url(self):
		test_file = criscostack.get_doc(
			{
				"doctype": "File",
				"file_name": "logo",
				"content": "criscostack",
			}
		).insert()
		assert test_file is not None

	def test_symlinked_files_folder(self):
		files_dir = os.path.abspath(get_files_path())
		with convert_to_symlink(files_dir):
			file = criscostack.get_doc(
				{
					"doctype": "File",
					"file_name": "symlinked_folder_test.txt",
					"content": "42",
				}
			)
			file.save()
			file.content = ""
			file._content = ""
			file.save().reload()
			self.assertIn("42", file.get_content())


@contextmanager
def convert_to_symlink(directory):
	"""Moves a directory to temp directory and symlinks original path for testing"""
	try:
		new_directory = shutil.move(directory, tempfile.mkdtemp())
		os.symlink(new_directory, directory)
		yield
	finally:
		os.unlink(directory)
		shutil.move(new_directory, directory)


class TestAttachment(CriscoTestCase):
	test_doctype = "Test For Attachment"

	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		criscostack.get_doc(
			doctype="DocType",
			name=cls.test_doctype,
			module="Custom",
			custom=1,
			fields=[
				{"label": "Title", "fieldname": "title", "fieldtype": "Data"},
				{"label": "Attachment", "fieldname": "attachment", "fieldtype": "Attach"},
			],
		).insert(ignore_if_duplicate=True)

	@classmethod
	def tearDownClass(cls):
		criscostack.db.rollback()
		criscostack.delete_doc("DocType", cls.test_doctype)

	def test_file_attachment_on_update(self):
		doc = criscostack.get_doc(doctype=self.test_doctype, title="test for attachment on update").insert()

		file = criscostack.get_doc(
			{"doctype": "File", "file_name": "test_attach.txt", "content": "Test Content"}
		).save()

		doc.attachment = file.file_url
		doc.save()

		exists = criscostack.db.exists(
			"File",
			{
				"file_name": "test_attach.txt",
				"file_url": file.file_url,
				"attached_to_doctype": self.test_doctype,
				"attached_to_name": doc.name,
				"attached_to_field": "attachment",
			},
		)

		self.assertTrue(exists)


class TestAttachmentsAccess(CriscoTestCase):
	def setUp(self) -> None:
		criscostack.db.delete("File", {"is_folder": 0})

	def test_list_private_attachments(self):
		criscostack.set_user("test4@example.com")
		self.attached_to_doctype, self.attached_to_docname = make_test_doc()

		criscostack.new_doc(
			"File",
			file_name="test_user_attachment.txt",
			attached_to_doctype=self.attached_to_doctype,
			attached_to_name=self.attached_to_docname,
			content="Testing User",
			is_private=1,
		).insert()

		criscostack.new_doc(
			"File",
			file_name="test_user_standalone.txt",
			content="User Home",
			is_private=1,
		).insert()

		criscostack.set_user("test@example.com")

		criscostack.new_doc(
			"File",
			file_name="test_sm_attachment.txt",
			attached_to_doctype=self.attached_to_doctype,
			attached_to_name=self.attached_to_docname,
			content="Testing System Manager",
			is_private=1,
		).insert()

		criscostack.new_doc(
			"File",
			file_name="test_sm_standalone.txt",
			content="System Manager Home",
			is_private=1,
		).insert()

		system_manager_files = [file.file_name for file in get_files_in_folder("Home")["files"]]
		system_manager_attachments_files = [
			file.file_name for file in get_files_in_folder("Home/Attachments")["files"]
		]

		criscostack.set_user("test4@example.com")
		user_files = [file.file_name for file in get_files_in_folder("Home")["files"]]
		user_attachments_files = [
			file.file_name for file in get_files_in_folder("Home/Attachments")["files"]
		]

		self.assertIn("test_sm_standalone.txt", system_manager_files)
		self.assertNotIn("test_sm_standalone.txt", user_files)

		self.assertIn("test_user_standalone.txt", user_files)
		self.assertNotIn("test_user_standalone.txt", system_manager_files)

		self.assertIn("test_sm_attachment.txt", system_manager_attachments_files)
		self.assertIn("test_sm_attachment.txt", user_attachments_files)
		self.assertIn("test_user_attachment.txt", system_manager_attachments_files)
		self.assertIn("test_user_attachment.txt", user_attachments_files)

	def test_list_public_single_file(self):
		"""Ensure that users are able to list public standalone files."""
		criscostack.set_user("test@example.com")
		criscostack.new_doc(
			"File",
			file_name="test_public_single.txt",
			content="Public single File",
			is_private=0,
		).insert()

		criscostack.set_user("test4@example.com")
		files = [file.file_name for file in get_files_in_folder("Home")["files"]]
		self.assertIn("test_public_single.txt", files)

	def test_list_public_attachment(self):
		"""Ensure that users are able to list public attachments."""
		criscostack.set_user("test@example.com")
		self.attached_to_doctype, self.attached_to_docname = make_test_doc()
		criscostack.new_doc(
			"File",
			file_name="test_public_attachment.txt",
			attached_to_doctype=self.attached_to_doctype,
			attached_to_name=self.attached_to_docname,
			content="Public Attachment",
			is_private=0,
		).insert()

		criscostack.set_user("test4@example.com")
		files = [file.file_name for file in get_files_in_folder("Home/Attachments")["files"]]
		self.assertIn("test_public_attachment.txt", files)

	def tearDown(self) -> None:
		criscostack.set_user("Administrator")
		criscostack.db.rollback()


class TestFileUtils(CriscoTestCase):
	def test_extract_images_from_doc(self):
		# with filename in data URI
		todo = criscostack.get_doc(
			{
				"doctype": "ToDo",
				"description": 'Test <img src="data:image/png;filename=pix.png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=">',
			}
		).insert()
		self.assertTrue(criscostack.db.exists("File", {"attached_to_name": todo.name}))
		self.assertIn('<img src="/files/pix.png">', todo.description)
		self.assertListEqual(get_attached_images("ToDo", [todo.name])[todo.name], ["/files/pix.png"])

		# without filename in data URI
		todo = criscostack.get_doc(
			{
				"doctype": "ToDo",
				"description": 'Test <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=">',
			}
		).insert()
		filename = criscostack.db.exists("File", {"attached_to_name": todo.name})
		self.assertIn(f'<img src="{criscostack.get_doc("File", filename).file_url}', todo.description)

	def test_create_new_folder(self):
		folder = create_new_folder("test_folder", "Home")
		self.assertTrue(folder.is_folder)


class TestFileOptimization(CriscoTestCase):
	def test_optimize_file(self):
		with make_test_image_file() as test_file:
			original_size = test_file.file_size
			original_content_hash = test_file.content_hash

			test_file.optimize_file()
			optimized_size = test_file.file_size
			updated_content_hash = test_file.content_hash

			self.assertLess(optimized_size, original_size)
			self.assertNotEqual(original_content_hash, updated_content_hash)

	def test_optimize_svg(self):
		file_path = criscostack.get_app_path("criscostack", "tests/data/sample_svg.svg")
		with open(file_path, "rb") as f:
			file_content = f.read()
		test_file = criscostack.get_doc(
			{"doctype": "File", "file_name": "sample_svg.svg", "content": file_content}
		).insert()
		self.assertRaises(TypeError, test_file.optimize_file)
		test_file.delete()

	def test_optimize_textfile(self):
		test_file = criscostack.get_doc(
			{"doctype": "File", "file_name": "sample_text.txt", "content": "Text files cannot be optimized"}
		).insert()
		self.assertRaises(NotImplementedError, test_file.optimize_file)
		test_file.delete()

	def test_optimize_folder(self):
		test_folder = criscostack.get_doc("File", "Home/Attachments")
		self.assertRaises(TypeError, test_folder.optimize_file)

	def test_revert_optimized_file_on_rollback(self):
		with make_test_image_file() as test_file:
			image_path = test_file.get_full_path()
			size_before_optimization = os.stat(image_path).st_size
			test_file.optimize_file()
			criscostack.db.rollback()
			size_after_rollback = os.stat(image_path).st_size

			self.assertEqual(size_before_optimization, size_after_rollback)

	def test_image_header_guessing(self):
		file_path = criscostack.get_app_path("criscostack", "tests/data/sample_image_for_optimization.jpg")
		with open(file_path, "rb") as f:
			file_content = f.read()

		self.assertEqual(get_extension("", None, file_content), "jpg")


class TestGuestFileAndAttachments(CriscoTestCase):
	def setUp(self) -> None:
		criscostack.db.delete("File", {"is_folder": 0})
		criscostack.get_doc(
			doctype="DocType",
			name="Test For Attachment",
			module="Custom",
			custom=1,
			fields=[
				{"label": "Title", "fieldname": "title", "fieldtype": "Data"},
				{"label": "Attachment", "fieldname": "attachment", "fieldtype": "Attach"},
			],
		).insert(ignore_if_duplicate=True)

	def tearDown(self) -> None:
		criscostack.set_user("Administrator")
		criscostack.db.rollback()
		criscostack.delete_doc("DocType", "Test For Attachment")

	def test_attach_unattached_guest_file(self):
		"""Ensure that unattached files are attached on doc update."""
		f = criscostack.new_doc(
			"File",
			file_name="test_private_guest_attachment.txt",
			content="Guest Home",
			is_private=1,
		).insert(ignore_permissions=True)

		d = criscostack.new_doc("Test For Attachment")
		d.title = "Test for attachment on update"
		d.attachment = f.file_url
		d.assigned_by = criscostack.session.user
		d.save()

		self.assertTrue(
			criscostack.db.exists(
				"File",
				{
					"file_name": "test_private_guest_attachment.txt",
					"file_url": f.file_url,
					"attached_to_doctype": "Test For Attachment",
					"attached_to_name": d.name,
					"attached_to_field": "attachment",
				},
			)
		)

	def test_list_private_guest_single_file(self):
		"""Ensure that guests are not able to read private standalone guest files."""
		criscostack.set_user("Guest")

		file = criscostack.new_doc(
			"File",
			file_name="test_private_guest_single_txt",
			content="Private single File",
			is_private=1,
		).insert(ignore_permissions=True)

		self.assertFalse(file.is_downloadable())

	def test_list_private_guest_attachment(self):
		"""Ensure that guests are not able to read private guest attachments."""
		criscostack.set_user("Guest")

		self.attached_to_doctype, self.attached_to_docname = make_test_doc(ignore_permissions=True)

		file = criscostack.new_doc(
			"File",
			file_name="test_private_guest_attachment.txt",
			attached_to_doctype=self.attached_to_doctype,
			attached_to_name=self.attached_to_docname,
			content="Private Attachment",
			is_private=1,
		).insert(ignore_permissions=True)

		self.assertFalse(file.is_downloadable())
