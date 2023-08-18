# import pprint
# from os import PathLike
# from os.path import basename
from requests import post
from requests.exceptions import RequestException
from .ext.errors import NotAnURL, DeadWebhook, UnsupportedImageType
from .ext.url import URLHandler
from .embed import Embed


class Webhook:
	def __init__(self, webhook_url: str):
		"""
		Represents a Discord Webhook.
		:param webhook_url:
		"""
		self.webhook_url = webhook_url
		
		if not URLHandler.is_url(self.webhook_url):
			raise NotAnURL(f"Invalid URL: {self.webhook_url}")
		
		if URLHandler.is_dead(self.webhook_url):
			raise DeadWebhook(f"Invalid Webhook: {self.webhook_url}. Was it deleted?")
	
		self._payload = {}
		# self._file_part = {}
		self._embeds = []
	
	def set_name(self, new_name: str):
		"""
		Set the name the webhook username
		:param new_name: The new name of the webhook username
		:return: None
		"""
		self._payload['username'] = new_name
	
	def set_content(self, message: str):
		"""
		Set the message content of the webhook message.
		:param message: Message Content
		:return: None
		"""
		self._payload['content'] = message
	
	def set_avatar(self, direct_avatar_url: str):
		"""
		Sets the webhook avatar, using a direct avatar url.
		Supported image formats: JPEG/JPG, GIF, and PNG
		:param direct_avatar_url: Image URL
		:return: None
		:raises UnsupportedImageType: If the image type is not supported or not a direct link to image.
		"""
		if URLHandler.is_url(direct_avatar_url) and URLHandler.is_url_image(direct_avatar_url):
			self._payload['avatar_url'] = direct_avatar_url
		else:
			raise UnsupportedImageType(
				"Avatar URL was either not a DIRECT link to an image or was not a supported image type."
				"(Hint: Supported Types are: JPEG/JPG, GIF, PNG)"
			)
	
	# def add_attachment(self, file_directory: str | PathLike):
	# 	with open(file_directory, "rb") as f:
	# 		file_name = basename(file_directory)
	# 		contents = f.read()
	# 		self._file_part = {'file': (file_name, contents)}
	
	def add_embed(self, embed: Embed):
		"""
		Add a embed to the message. 10 Embed limit per message!
		:param embed: Embed Class
		:return:
		"""
		if len(self._embeds) < 10:  # Discord supports up to 10 embeds per message
			self._embeds.append(embed.json)
		else:
			raise ValueError("Maximum number of embeds (10) reached for this message.")
	
	def send(self):
		"""
		Send the webhook message
		:return:
		"""
		# We need to construct the final payload
		payload = {}
		
		if self._payload:
			payload.update(self._payload)
		
		if self._embeds:
			payload["embeds"] = self._embeds
		
		# pprint.pprint(payload)
		
		try:
			response = post(self.webhook_url, json=payload)
			if response.status_code != 204:
				raise Exception("Webhook request failed with status code:", response.status_code)
		except RequestException as e:
			print("Webhook request failed:", e)
