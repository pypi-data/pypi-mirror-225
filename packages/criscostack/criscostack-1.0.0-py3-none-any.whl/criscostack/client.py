# Copyright (c) 2015, Crisco Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE
import json
import os
from typing import TYPE_CHECKING

import criscostack
import criscostack.model
import criscostack.utils
from criscostack import _
from criscostack.desk.reportview import validate_args
from criscostack.model.db_query import check_parent_permission
from criscostack.utils import get_safe_filters

if TYPE_CHECKING:
	from criscostack.model.document import Document

"""
Handle RESTful requests that are mapped to the `/api/resource` route.

Requests via CriscoClient are also handled here.
"""


@criscostack.whitelist()
def get_list(
	doctype,
	fields=None,
	filters=None,
	order_by=None,
	limit_start=None,
	limit_page_length=20,
	parent=None,
	debug=False,
	as_dict=True,
	or_filters=None,
):
	"""Returns a list of records by filters, fields, ordering and limit

	:param doctype: DocType of the data to be queried
	:param fields: fields to be returned. Default is `name`
	:param filters: filter list by this dict
	:param order_by: Order by this fieldname
	:param limit_start: Start at this index
	:param limit_page_length: Number of records to be returned (default 20)"""
	if criscostack.is_table(doctype):
		check_parent_permission(parent, doctype)

	args = criscostack._dict(
		doctype=doctype,
		parent_doctype=parent,
		fields=fields,
		filters=filters,
		or_filters=or_filters,
		order_by=order_by,
		limit_start=limit_start,
		limit_page_length=limit_page_length,
		debug=debug,
		as_list=not as_dict,
	)

	validate_args(args)
	return criscostack.get_list(**args)


@criscostack.whitelist()
def get_count(doctype, filters=None, debug=False, cache=False):
	return criscostack.db.count(doctype, get_safe_filters(filters), debug, cache)


@criscostack.whitelist()
def get(doctype, name=None, filters=None, parent=None):
	"""Returns a document by name or filters

	:param doctype: DocType of the document to be returned
	:param name: return document of this `name`
	:param filters: If name is not set, filter by these values and return the first match"""
	if criscostack.is_table(doctype):
		check_parent_permission(parent, doctype)

	if name:
		doc = criscostack.get_doc(doctype, name)
	elif filters or filters == {}:
		doc = criscostack.get_doc(doctype, criscostack.parse_json(filters))
	else:
		doc = criscostack.get_doc(doctype)  # single

	doc.check_permission()
	doc.apply_fieldlevel_read_permissions()

	return doc.as_dict()


@criscostack.whitelist()
def get_value(doctype, fieldname, filters=None, as_dict=True, debug=False, parent=None):
	"""Returns a value form a document

	:param doctype: DocType to be queried
	:param fieldname: Field to be returned (default `name`)
	:param filters: dict or string for identifying the record"""
	if criscostack.is_table(doctype):
		check_parent_permission(parent, doctype)

	if not criscostack.has_permission(doctype, parent_doctype=parent):
		criscostack.throw(_("No permission for {0}").format(_(doctype)), criscostack.PermissionError)

	filters = get_safe_filters(filters)
	if isinstance(filters, str):
		filters = {"name": filters}

	try:
		fields = criscostack.parse_json(fieldname)
	except (TypeError, ValueError):
		# name passed, not json
		fields = [fieldname]

	# check whether the used filters were really parseable and usable
	# and did not just result in an empty string or dict
	if not filters:
		filters = None

	if criscostack.get_meta(doctype).issingle:
		value = criscostack.db.get_values_from_single(fields, filters, doctype, as_dict=as_dict, debug=debug)
	else:
		value = get_list(
			doctype,
			filters=filters,
			fields=fields,
			debug=debug,
			limit_page_length=1,
			parent=parent,
			as_dict=as_dict,
		)

	if as_dict:
		return value[0] if value else {}

	if not value:
		return

	return value[0] if len(fields) > 1 else value[0][0]


@criscostack.whitelist()
def get_single_value(doctype, field):
	if not criscostack.has_permission(doctype):
		criscostack.throw(_("No permission for {0}").format(_(doctype)), criscostack.PermissionError)

	return criscostack.db.get_single_value(doctype, field)


@criscostack.whitelist(methods=["POST", "PUT"])
def set_value(doctype, name, fieldname, value=None):
	"""Set a value using get_doc, group of values

	:param doctype: DocType of the document
	:param name: name of the document
	:param fieldname: fieldname string or JSON / dict with key value pair
	:param value: value if fieldname is JSON / dict"""

	if fieldname in (criscostack.model.default_fields + criscostack.model.child_table_fields):
		criscostack.throw(_("Cannot edit standard fields"))

	if not value:
		values = fieldname
		if isinstance(fieldname, str):
			try:
				values = json.loads(fieldname)
			except ValueError:
				values = {fieldname: ""}
	else:
		values = {fieldname: value}

	# check for child table doctype
	if not criscostack.get_meta(doctype).istable:
		doc = criscostack.get_doc(doctype, name)
		doc.update(values)
	else:
		doc = criscostack.db.get_value(doctype, name, ["parenttype", "parent"], as_dict=True)
		doc = criscostack.get_doc(doc.parenttype, doc.parent)
		child = doc.getone({"doctype": doctype, "name": name})
		child.update(values)

	doc.save()

	return doc.as_dict()


@criscostack.whitelist(methods=["POST", "PUT"])
def insert(doc=None):
	"""Insert a document

	:param doc: JSON or dict object to be inserted"""
	if isinstance(doc, str):
		doc = json.loads(doc)

	return insert_doc(doc).as_dict()


@criscostack.whitelist(methods=["POST", "PUT"])
def insert_many(docs=None):
	"""Insert multiple documents

	:param docs: JSON or list of dict objects to be inserted in one request"""
	if isinstance(docs, str):
		docs = json.loads(docs)

	if len(docs) > 200:
		criscostack.throw(_("Only 200 inserts allowed in one request"))

	out = []
	for doc in docs:
		out.append(insert_doc(doc).name)

	return out


@criscostack.whitelist(methods=["POST", "PUT"])
def save(doc):
	"""Update (save) an existing document

	:param doc: JSON or dict object with the properties of the document to be updated"""
	if isinstance(doc, str):
		doc = json.loads(doc)

	doc = criscostack.get_doc(doc)
	doc.save()

	return doc.as_dict()


@criscostack.whitelist(methods=["POST", "PUT"])
def rename_doc(doctype, old_name, new_name, merge=False):
	"""Rename document

	:param doctype: DocType of the document to be renamed
	:param old_name: Current `name` of the document to be renamed
	:param new_name: New `name` to be set"""
	new_name = criscostack.rename_doc(doctype, old_name, new_name, merge=merge)
	return new_name


@criscostack.whitelist(methods=["POST", "PUT"])
def submit(doc):
	"""Submit a document

	:param doc: JSON or dict object to be submitted remotely"""
	if isinstance(doc, str):
		doc = json.loads(doc)

	doc = criscostack.get_doc(doc)
	doc.submit()

	return doc.as_dict()


@criscostack.whitelist(methods=["POST", "PUT"])
def cancel(doctype, name):
	"""Cancel a document

	:param doctype: DocType of the document to be cancelled
	:param name: name of the document to be cancelled"""
	wrapper = criscostack.get_doc(doctype, name)
	wrapper.cancel()

	return wrapper.as_dict()


@criscostack.whitelist(methods=["DELETE", "POST"])
def delete(doctype, name):
	"""Delete a remote document

	:param doctype: DocType of the document to be deleted
	:param name: name of the document to be deleted"""
	delete_doc(doctype, name)


@criscostack.whitelist(methods=["POST", "PUT"])
def bulk_update(docs):
	"""Bulk update documents

	:param docs: JSON list of documents to be updated remotely. Each document must have `docname` property"""
	docs = json.loads(docs)
	failed_docs = []
	for doc in docs:
		doc.pop("flags", None)
		try:
			existing_doc = criscostack.get_doc(doc["doctype"], doc["docname"])
			existing_doc.update(doc)
			existing_doc.save()
		except Exception:
			failed_docs.append({"doc": doc, "exc": criscostack.utils.get_traceback()})

	return {"failed_docs": failed_docs}


@criscostack.whitelist()
def has_permission(doctype, docname, perm_type="read"):
	"""Returns a JSON with data whether the document has the requested permission

	:param doctype: DocType of the document to be checked
	:param docname: `name` of the document to be checked
	:param perm_type: one of `read`, `write`, `create`, `submit`, `cancel`, `report`. Default is `read`"""
	# perm_type can be one of read, write, create, submit, cancel, report
	return {"has_permission": criscostack.has_permission(doctype, perm_type.lower(), docname)}


@criscostack.whitelist()
def get_doc_permissions(doctype, docname):
	"""Returns an evaluated document permissions dict like `{"read":1, "write":1}`

	:param doctype: DocType of the document to be evaluated
	:param docname: `name` of the document to be evaluated
	"""
	doc = criscostack.get_doc(doctype, docname)
	return {"permissions": criscostack.permissions.get_doc_permissions(doc)}


@criscostack.whitelist()
def get_password(doctype, name, fieldname):
	"""Return a password type property. Only applicable for System Managers

	:param doctype: DocType of the document that holds the password
	:param name: `name` of the document that holds the password
	:param fieldname: `fieldname` of the password property
	"""
	criscostack.only_for("System Manager")
	return criscostack.get_doc(doctype, name).get_password(fieldname)


@criscostack.whitelist()
def get_js(items):
	"""Load JS code files.  Will also append translations
	and extend `criscostack._messages`

	:param items: JSON list of paths of the js files to be loaded."""
	items = json.loads(items)
	out = []
	for src in items:
		src = src.strip("/").split("/")

		if ".." in src or src[0] != "assets":
			criscostack.throw(_("Invalid file path: {0}").format("/".join(src)))

		contentpath = os.path.join(criscostack.local.sites_path, *src)
		with open(contentpath) as srcfile:
			code = criscostack.utils.cstr(srcfile.read())

		out.append(code)

	return out


@criscostack.whitelist(allow_guest=True)
def get_time_zone():
	"""Returns default time zone"""
	return {"time_zone": criscostack.defaults.get_defaults().get("time_zone")}


@criscostack.whitelist(methods=["POST", "PUT"])
def attach_file(
	filename=None,
	filedata=None,
	doctype=None,
	docname=None,
	folder=None,
	decode_base64=False,
	is_private=None,
	docfield=None,
):
	"""Attach a file to Document

	:param filename: filename e.g. test-file.txt
	:param filedata: base64 encode filedata which must be urlencoded
	:param doctype: Reference DocType to attach file to
	:param docname: Reference DocName to attach file to
	:param folder: Folder to add File into
	:param decode_base64: decode filedata from base64 encode, default is False
	:param is_private: Attach file as private file (1 or 0)
	:param docfield: file to attach to (optional)"""

	doc = criscostack.get_doc(doctype, docname)
	doc.check_permission()

	file = criscostack.get_doc(
		{
			"doctype": "File",
			"file_name": filename,
			"attached_to_doctype": doctype,
			"attached_to_name": docname,
			"attached_to_field": docfield,
			"folder": folder,
			"is_private": is_private,
			"content": filedata,
			"decode": decode_base64,
		}
	).save()

	if docfield and doctype:
		doc.set(docfield, file.file_url)
		doc.save()

	return file


@criscostack.whitelist()
def is_document_amended(doctype, docname):
	if criscostack.permissions.has_permission(doctype):
		try:
			return criscostack.db.exists(doctype, {"amended_from": docname})
		except criscostack.db.InternalError:
			pass

	return False


@criscostack.whitelist()
def validate_link(doctype: str, docname: str, fields=None):
	if not isinstance(doctype, str):
		criscostack.throw(_("DocType must be a string"))

	if not isinstance(docname, str):
		criscostack.throw(_("Document Name must be a string"))

	if doctype != "DocType" and not (
		criscostack.has_permission(doctype, "select") or criscostack.has_permission(doctype, "read")
	):
		criscostack.throw(
			_("You do not have Read or Select Permissions for {}").format(criscostack.bold(doctype)),
			criscostack.PermissionError,
		)

	values = criscostack._dict()
	values.name = criscostack.db.get_value(doctype, docname, cache=True)

	fields = criscostack.parse_json(fields)
	if not values.name or not fields:
		return values

	try:
		values.update(get_value(doctype, fields, docname))
	except criscostack.PermissionError:
		criscostack.clear_last_message()
		criscostack.msgprint(
			_("You need {0} permission to fetch values from {1} {2}").format(
				criscostack.bold(_("Read")), criscostack.bold(doctype), criscostack.bold(docname)
			),
			title=_("Cannot Fetch Values"),
			indicator="orange",
		)

	return values


def insert_doc(doc) -> "Document":
	"""Inserts document and returns parent document object with appended child document
	if `doc` is child document else returns the inserted document object

	:param doc: doc to insert (dict)"""

	doc = criscostack._dict(doc)
	if criscostack.is_table(doc.doctype):
		if not (doc.parenttype and doc.parent and doc.parentfield):
			criscostack.throw(_("Parenttype, Parent and Parentfield are required to insert a child record"))

		# inserting a child record
		parent = criscostack.get_doc(doc.parenttype, doc.parent)
		parent.append(doc.parentfield, doc)
		parent.save()
		return parent

	return criscostack.get_doc(doc).insert()


def delete_doc(doctype, name):
	"""Deletes document
	if doctype is a child table, then deletes the child record using the parent doc
	so that the parent doc's `on_update` is called
	"""

	if criscostack.is_table(doctype):
		values = criscostack.db.get_value(doctype, name, ["parenttype", "parent", "parentfield"])
		if not values:
			raise criscostack.DoesNotExistError
		parenttype, parent, parentfield = values
		parent = criscostack.get_doc(parenttype, parent)
		for row in parent.get(parentfield):
			if row.name == name:
				parent.remove(row)
				parent.save()
				break
	else:
		criscostack.delete_doc(doctype, name, ignore_missing=False)
