from re import compile, match
from .ext.url import URLHandler
from .ext.errors import NotAnURL, UnsupportedImageType


class Embed:
	def __init__(self, title: str, description: str = "", color: int = 0x0):
		"""
		Represents a Discord Embed.
		:param title: Embed Title
		:param description: Embed Description
		:param color: Embed Color
		"""
		self.json = {
			"title": title,
			"description": description,
			"color": color,
		}
		
		self.title = title
		self.description = description
		self.color = color
	
	def set_author(self, name: str, url: str = None, icon_url: str = None):
		"""
		Sets the author of the embed
		:param name: Author Name
		:param url: Redirect URL
		:param icon_url: Icon URL
		:return:
		"""
		to_add = {"author": {"name": name}}
		
		if url is not None:
			if not URLHandler.is_url(url):
				raise NotAnURL(f"Invalid URL: {url}")
			
			to_add["author"]["url"] = url
		
		if icon_url is not None:
			if not URLHandler.is_url(icon_url):
				raise NotAnURL(f"Invalid URL: {icon_url}")
			
			if not URLHandler.is_url_image(icon_url):
				raise UnsupportedImageType(
					"Avatar URL was either not a DIRECT link to an image or was not a supported image type."
					"(Hint: Supported Types are: JPEG/JPG, GIF, PNG)"
				)
			
			to_add["author"]["icon_url"] = icon_url
		
		self.json.update(to_add)
	
	def add_field(self, name: str, value: str, inline: bool = True):
		if "fields" not in self.json:
			self.json["fields"] = []
		self.json["fields"].append({"name": name, "value": value, "inline": inline})
	
	def add_image(self, image_url: str):
		if not URLHandler.is_url(image_url):
			raise NotAnURL(f"Invalid URL: {image_url}")
		
		if not URLHandler.is_url_image(image_url):
			raise UnsupportedImageType(
				"Avatar URL was either not a DIRECT link to an image or was not a supported image type."
				"(Hint: Supported Types are: JPEG/JPG, GIF, PNG)"
			)
		if "image" not in self.json:
			self.json["image"] = {}
		self.json["image"]["url"] = image_url
	
	def set_thumbnail(self, image_url):
		if not URLHandler.is_url(image_url):
			raise NotAnURL(f"Invalid URL: {image_url}")
		
		if not URLHandler.is_url_image(image_url):
			raise UnsupportedImageType(
				"Avatar URL was either not a DIRECT link to an image or was not a supported image type."
				"(Hint: Supported Types are: JPEG/JPG, GIF, PNG)"
			)
		if "thumbnail" not in self.json:
			self.json["thumbnail"] = {}
		
		self.json["thumbnail"]["url"] = image_url
	
	def set_footer(self, text: str, icon_url: str = None):
		if "footer" not in self.json:
			self.json["footer"] = {}
		
		if icon_url is not None:
			if not URLHandler.is_url(icon_url):
				raise NotAnURL(f"Invalid URL: {icon_url}")
			
			if not URLHandler.is_url_image(icon_url):
				raise UnsupportedImageType(
					"Avatar URL was either not a DIRECT link to an image or was not a supported image type."
					"(Hint: Supported Types are: JPEG/JPG, GIF, PNG)"
				)
			
			self.json["footer"]["icon_url"] = icon_url
		
		self.json["footer"]["text"] = text
	
	def set_timestamp(self, timestamp: str):
		regex = compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$")
		
		if match(regex, timestamp):
			self.json["timestamp"] = timestamp