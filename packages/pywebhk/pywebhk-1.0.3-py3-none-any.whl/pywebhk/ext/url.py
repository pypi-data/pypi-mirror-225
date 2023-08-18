from validators import url as check_url
from requests import head, get
from requests.exceptions import RequestException


class URLHandler:
	@staticmethod
	def is_url_image(image_url: str):
		"""
		Checks if a given URL leads to a direct image.
		Supported image types: JPEG/JPG, PNG, GIF
		:param image_url:
		:return: True if URL leads to a supported image format, else False
		"""
		image_formats = ("image/jpeg", "image/png", "image/gif")
		
		try:
			request = head(image_url)
			if request.headers["content-type"] in image_formats:
				return True
			return False
		except RequestException:
			return False
	
	@staticmethod
	def is_url(url: str):
		"""
		Checks if a given URL is actually a valid URL
		:param url:
		:return: True if the URL is valid, else False
		"""
		return check_url(url)
	
	@staticmethod
	def is_dead(webhook_url: str):
		"""
		Check if a given webhook URL is deleted or not.
		:param webhook_url:
		:return: True if the webhook is dead, else False
		"""
		try:
			response = get(webhook_url, headers={"Content-Type": "application/json"})
			response.raise_for_status()  # Check if the webhook is dead or not
			return False
		except RequestException:
			return True
