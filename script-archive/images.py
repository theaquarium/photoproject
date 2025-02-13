import io
from pillow_heif import register_heif_opener
from datetime import datetime
from utils import *
from PIL import Image

register_heif_opener()


def open_image(path):
    with Image.open(path) as image:
        return image


def pil_image_to_io_base(img):
    """Converts a PIL Image to an io.BytesIO object."""

    bio = io.BytesIO()
    img.save(bio, format="PNG")  # You can change the format if needed
    bio.seek(0)  # Reset the file pointer to the beginning
    return bio


def get_image_date(img):
    date_exif = img.getexif()[0x0132]
    date = datetime.strptime(date_exif, '%Y:%m:%d %H:%M:%S')
    return date.strftime('%Y-%m-%d')
