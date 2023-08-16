import click

import criscostack


def execute():
	criscostack.delete_doc_if_exists("DocType", "Chat Message")
	criscostack.delete_doc_if_exists("DocType", "Chat Message Attachment")
	criscostack.delete_doc_if_exists("DocType", "Chat Profile")
	criscostack.delete_doc_if_exists("DocType", "Chat Token")
	criscostack.delete_doc_if_exists("DocType", "Chat Room User")
	criscostack.delete_doc_if_exists("DocType", "Chat Room")
	criscostack.delete_doc_if_exists("Module Def", "Chat")

	click.secho(
		"Chat Module is moved to a separate app and is removed from Crisco in version-13.\n"
		"Please install the app to continue using the chat feature: https://github.com/criscostack/chat",
		fg="yellow",
	)
