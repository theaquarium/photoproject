from pillow_heif import register_heif_opener
import os
from PIL import Image, ImageDraw, ImageFont
from utils import *
from pathlib import Path
from config import config

register_heif_opener()

# result_resolution = (1910, 1000)
# result_resolution = (1719, 900)
result_resolution = (1080, 1080)
# result_resolution = (1080, 1350)
mini_size = (int(result_resolution[0] / 3), int(result_resolution[1] / 3))

INDIR = os.path.join(config['files']['photos_folder'],
                     config['files']['originals_folder'])
OUTDIR = os.path.join(config['files']['photos_folder'],
                      config['files']['thumbnails_folder'])

Path(OUTDIR).mkdir(parents=True, exist_ok=True)

originals = os.listdir(INDIR)

start_date = config['start_date']
end_date = config['end_date']
weeks = divide_chunks(list(daterange(start_date, end_date)), 7)

image_placements = [
    (0, 0),
    (1, 0),
    (2, 0),
    (0, 1),
    (1, 1),
    (2, 1),
    (0, 2),
]

for week in weeks:
    result_image = Image.new('RGB', result_resolution)

    for index, day in enumerate(week):
        dayname = day.strftime("%Y-%m-%d")
        filename = next((x for x in originals if x.startswith(dayname)), None)

        if filename is None:
            print('Missing', dayname)
            continue

        with Image.open(os.path.join(INDIR, filename)) as image:
            cropped = crop_to_aspect(image,
                                     mini_size[0], mini_size[1])
            cropped.thumbnail(
                (mini_size[0], mini_size[1]))

            result_image.paste(
                cropped, (mini_size[0] * image_placements[index][0], mini_size[1] * image_placements[index][1]))

    fnt = ImageFont.truetype("RobotoMono-Regular.ttf", 60)
    draw = ImageDraw.Draw(result_image)

    # Rect
    # draw.text((result_resolution[0] - 100, result_resolution[1] - 100), week[0].strftime(
    #     '%m/%d/%Y') + ' thru ' + week[-1].strftime(
    #     '%m/%d/%Y'), font=fnt, fill="white", anchor='rs', stroke_width=1, stroke_fill='black')

    # Square
    draw.text((result_resolution[0] - 70, result_resolution[1] - 150), week[0].strftime(
        '%m/%d/%Y'), font=fnt, fill="white", anchor='rs', stroke_width=1, stroke_fill='black')
    draw.text((result_resolution[0] - 70, result_resolution[1] - 80), 'thru ' + week[-1].strftime(
        '%m/%d/%Y'), font=fnt, fill="white", anchor='rs', stroke_width=1, stroke_fill='black')

    print('Saving', week[0].strftime(
        '%m/%d/%Y') + ' thru ' + week[-1].strftime(
        '%m/%d/%Y'))

    result_image.save(os.path.join(OUTDIR, week[0].strftime(
        '%Y-%m-%d') + '---' + week[-1].strftime(
        '%Y-%m-%d') + '.jpg'), quality=90, subsampling=0)
