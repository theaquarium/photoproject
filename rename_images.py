from PIL import Image
from pillow_heif import register_heif_opener
import os
from datetime import datetime
from utils import *
from pathlib import Path
from config import config

register_heif_opener()

INDIR = os.path.join(config['files']['photos_folder'],
                     config['files']['raw_folder'])
OUTDIR = os.path.join(config['files']['photos_folder'],
                      config['files']['originals_folder'])

Path(OUTDIR).mkdir(parents=True, exist_ok=True)

originals = os.listdir(OUTDIR)

for filename in os.listdir(INDIR):
    if not os.path.isfile(os.path.join(INDIR, filename)):
        continue

    print(filename)
    if filename == ".DS_Store":
        continue

    with Image.open(os.path.join(INDIR, filename)) as image:
        date_exif = image.getexif()[0x0132]
        img_date = datetime.strptime(date_exif, '%Y:%m:%d %H:%M:%S')

        dayname = img_date.strftime("%Y-%m-%d")
        filename = next((x for x in originals if x.startswith(dayname)), None)

        if filename:
            print('Skipping', dayname)
            continue

        exif = image.getexif()

        image.save(os.path.join(OUTDIR, img_date.strftime(
            '%Y-%m-%d') + '-' + create_random_id() + '.png'), exif=exif)
