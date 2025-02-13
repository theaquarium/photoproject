from pillow_heif import register_heif_opener
import os
from PIL import Image, ImageDraw, ImageFont
from utils import *
from pathlib import Path
from config import config

register_heif_opener()

# result_resolution = (1910, 1000)
# result_resolution = (1719, 900)
result_resolution = (1080, 1920)
allowed_area_resolution = (1080, 1080)
mini_size = (
    int(allowed_area_resolution[0] / 12), int(allowed_area_resolution[1] / 31))
vert_centering_offset = int((result_resolution[1] - (mini_size[1] * 31)) / 2)

INDIR = os.path.join(config['files']['photos_folder'],
                     config['files']['originals_folder'])
OUTDIR = os.path.join(config['files']['photos_folder'])

Path(OUTDIR).mkdir(parents=True, exist_ok=True)

originals = os.listdir(INDIR)

YEAR = 2024

result_image = Image.new('RGB', result_resolution)

for month in range(1, 13):
    end_date = date(YEAR, month + 1, 1) if month < 12 else date(YEAR, 12, 31)
    for day in daterange(date(YEAR, month, 1), end_date):
        dayname = day.strftime("%Y-%m-%d")
        filename = next((x for x in originals if x.startswith(dayname)), None)

        print(dayname)
        if filename is None:
            print('Missing', dayname)
            continue

        with Image.open(os.path.join(INDIR, filename)) as image:
            cropped = crop_to_aspect(image,
                                     mini_size[0], mini_size[1])
            cropped.thumbnail(
                (mini_size[0], mini_size[1]))

            result_image.paste(
                cropped, (mini_size[0] * (month - 1), mini_size[1] * (day.day - 1) + vert_centering_offset))

# just december 31
day = date(YEAR, 12, 31)
dayname = day.strftime("%Y-%m-%d")
filename = next((x for x in originals if x.startswith(dayname)), None)

print(dayname)
if filename is None:
    print('Missing', dayname)
else:
    with Image.open(os.path.join(INDIR, filename)) as image:
        cropped = crop_to_aspect(image,
                                 mini_size[0], mini_size[1])
        cropped.thumbnail(
            (mini_size[0], mini_size[1]))

        result_image.paste(
            cropped, (mini_size[0] * (month - 1), mini_size[1] * (day.day - 1) + vert_centering_offset))

print('Saving')

result_image.save(os.path.join(
    OUTDIR, 'yearthumb.jpg'), quality=90, subsampling=0)
