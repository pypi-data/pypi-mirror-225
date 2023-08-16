# Copyright (c) 2021, Crisco Technologies Pvt. Ltd. and Contributors
# MIT License. See LICENSE

from criscostack.exceptions import ValidationError


class NewsletterAlreadySentError(ValidationError):
	pass


class NoRecipientFoundError(ValidationError):
	pass


class NewsletterNotSavedError(ValidationError):
	pass
