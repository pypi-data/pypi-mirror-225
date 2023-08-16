import criscostack


# no context object is accepted
def get_context():
	context = criscostack._dict()
	context.body = "Custom Content"
	return context
