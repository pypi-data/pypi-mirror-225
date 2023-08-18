class NotAnURL(Exception):
	"""
	Raises when you do not pass a proper webhook url.
	"""
	pass


class DeadWebhook(Exception):
	"""
	Raises when you try to use a deleted/dead webhook.
	"""
	pass


class UnsupportedImageType(Exception):
	"""
	Raises when you try to use an unsupported image type. (Supported: PNG, JPEG/JPG, GIF)
	"""
	pass
