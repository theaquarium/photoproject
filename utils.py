import math
from os import stat
import random
import string
from datetime import date, timedelta

alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits


def create_random_id(length=8):
    return ''.join(random.choices(alphabet, k=8))


def scale_image(im, factor):
    width, height = im.size
    return im.resize((int(width * factor), int(height * factor)))


def scale_point(p, factor):
    a, b = p
    return ((int(a * factor), int(b * factor)))


def scale_dims(factor, top, right, bottom, left):
    width = right - left
    height = bottom - top
    return (top * factor, (left + width) * factor, (top + height) * factor, left * factor)


def polygon_center(points):
    left = 0
    top = 0

    for point in points:
        left += point[0]
        top += point[1]

    return (int(left / len(points)), int(top / len(points)))


def distance_between(a, b):
    return math.sqrt(math.pow((b[0] - a[0]), 2) + math.pow((b[1] - a[1]), 2))


def point_angle(a, b):
    return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))


def get_file_bytes_size(filename):
    file_stats = stat(filename)
    print('File Size in Bytes is {}'.format(file_stats.st_size))
    return file_stats.st_size


def get_io_base_size(bio):
    return bio.getbuffer().nbytes


def daterange(start_date: date, end_date: date):
    days = int((end_date - start_date).days)
    for n in range(days):
        yield start_date + timedelta(n)


def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def crop_to_aspect(image, aspect, divisor=1, alignx=0.5, aligny=0.5):
    """Crops an image to a given aspect ratio.
    Args:
        aspect (float): The desired aspect ratio.
        divisor (float): Optional divisor. Allows passing in (w, h) pair as the first two arguments.
        alignx (float): Horizontal crop alignment from 0 (left) to 1 (right)
        aligny (float): Vertical crop alignment from 0 (left) to 1 (right)
    Returns:
        Image: The cropped Image object.
    """
    if image.width / image.height > aspect / divisor:
        newwidth = int(image.height * (aspect / divisor))
        newheight = image.height
    else:
        newwidth = image.width
        newheight = int(image.width / (aspect / divisor))
    img = image.crop((alignx * (image.width - newwidth),
                     aligny * (image.height - newheight),
                     alignx * (image.width - newwidth) + newwidth,
                     aligny * (image.height - newheight) + newheight))
    return img


def random_color():
    return tuple(random.choices(range(256), k=3))
