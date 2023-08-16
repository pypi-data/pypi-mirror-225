import criscostack


def execute():
	criscostack.reload_doctype("Translation")
	criscostack.db.sql(
		"UPDATE `tabTranslation` SET `translated_text`=`target_name`, `source_text`=`source_name`, `contributed`=0"
	)
