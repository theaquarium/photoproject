from utils import *
from config import config
from drive import upload_file
from images import *
import os
from notion import create_notion_page_for

# print('Loading image...')
# image = open_image(os.path.join(
#     config['files']['photos_folder'], config['files']['raw_folder'], 'IMG_0195.HEIC'))
# date = get_image_date(image)
# original_id = create_random_id()

# print('Loaded image...', date, original_id)
# original_filename = date + '-' + original_id + '.png'

# print('Creating BIO for ...', original_filename)
# img_iobase = pil_image_to_io_base(image)


# print('Uploading...', original_filename)
# uploaded = upload_file(config['drive']['originals_id'],
#                        original_filename, img_iobase, 'image/png')

# print('Uploaded', uploaded.get('id'))

# drive_url = 'https://drive.google.com/uc?export=download&id=' + \
#     uploaded.get('id')

# print('Creating page...')

# page = create_notion_page_for(date, drive_url, original_id)
# print('Page:', page)

page = create_notion_page_for(
    '2023-11-23', 'https://drive.google.com/uc?export=download&id=1C45kDkFPIYhxSyeWl3yaSGSjxRy_04KT', 'abcdefgh')
