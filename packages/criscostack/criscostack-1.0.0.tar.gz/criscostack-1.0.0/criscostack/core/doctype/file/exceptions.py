import criscostack


class MaxFileSizeReachedError(criscostack.ValidationError):
	pass


class FolderNotEmpty(criscostack.ValidationError):
	pass


from criscostack.exceptions import *
