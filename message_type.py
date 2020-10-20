from rfc3987 import parse
import requests

def get_message_type(message):
    try:
        parse(message, rule='IRI')
        if is_url_image(message):
            return "image"
        else:
            return "url"
    except ValueError:
        return "text"

def is_url_image(image_url):
   image_formats = ("image/png", "image/jpeg", "image/jpg")
   r = requests.head(image_url)
   if r.headers["content-type"] in image_formats:
      return True
   return False