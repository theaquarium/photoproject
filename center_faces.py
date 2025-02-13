from pillow_heif import register_heif_opener
import face_recognition
import numpy as np
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from utils import *
from pathlib import Path
import yaml
from config import config

register_heif_opener()

# --- New 4:5 Aspect ---

# result_resolution = (1080, 1350)

# bottom_text_offset = 80
# side_text_offset = 80
# line_offset = 60

# ---

# --- Standard Square ---

result_resolution = (1080, 1080)

bottom_text_offset = 80
side_text_offset = 80
line_offset = 60

# ---

# --- Insta Story ---

# result_resolution = (1080, 1920)

# bottom_text_offset = 310
# side_text_offset = 80
# line_offset = 60

# ---

target_eye_width = 60
scale_factor = 4

INDIR = os.path.join(config['files']['photos_folder'],
                     config['files']['originals_folder'])
OUTDIR = os.path.join(config['files']['photos_folder'],
                      config['files']['processed_folder'])

Path(OUTDIR).mkdir(parents=True, exist_ok=True)

originals = os.listdir(INDIR)

notes = {}
stored_landmarks = {}
locations = {}

# Read stored landmarks
try:
    with open(os.path.join(config['files']['photos_folder'],
                           config['files']['stored_landmarks'])) as stream:
        try:
            stored_landmarks = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
except:
    print('No Stored Landmarks file found')

# Read notes
try:
    with open(os.path.join(config['files']['photos_folder'],
                           config['files']['notes'])) as stream:
        try:
            notes = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
except:
    print('No Notes file found')

# Read locations
try:
    with open(os.path.join(config['files']['photos_folder'],
                           config['files']['locations'])) as stream:
        try:
            locations = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
except:
    print('No Locations file found')


with Image.open(os.path.join(config['files']['photos_folder'],
                             config['files']['reference'])) as known_image:
    small_known_image = known_image.copy()
    small_known_image.convert("RGB")
    small_known_image.thumbnail((512, 512))
    small_known_image = np.array(small_known_image)
    known_encoding = face_recognition.face_encodings(small_known_image)[0]

start_date = config['start_date']
end_date = config['end_date']

for day in daterange(start_date, end_date):
    dayname = day.strftime("%Y-%m-%d")
    filename = next((x for x in originals if x.startswith(dayname)), None)

    if filename is None:
        print('Missing', dayname)
        continue

    print('Processing...', dayname)

    with Image.open(os.path.join(INDIR, filename)) as image:
        # Use stored landmarks if available
        stored = stored_landmarks.get(day, None)

        if stored is not None:
            left_eye = stored_landmarks[day]['left_eye']
            right_eye = stored_landmarks[day]['right_eye']
            lips = stored_landmarks[day]['lips']
        else:
            small_image = scale_image(image, 1/scale_factor)
            small_image.convert("RGB")
            small_image = np.array(small_image)

            face_locations = face_recognition.face_locations(small_image)

            if len(face_locations) > 0:
                face_encodings = face_recognition.face_encodings(
                    small_image, face_locations)

                match_index = -1
                for index, face_encoding in enumerate(face_encodings):
                    matches = face_recognition.compare_faces(
                        [known_encoding], face_encoding)
                    if matches[0]:
                        match_index = index

                face_landmarks = face_recognition.face_landmarks(
                    small_image, [face_locations[match_index]])[0]

                dims = face_locations[match_index]
                top, right, bottom, left = scale_dims(scale_factor, *dims)
                cropped_image = image.crop((left, top, right, bottom))

                left_eye = scale_point(polygon_center(
                    face_landmarks['left_eye']), scale_factor)
                right_eye = scale_point(polygon_center(
                    face_landmarks['right_eye']), scale_factor)
                top_lip = scale_point(polygon_center(
                    face_landmarks['top_lip']), scale_factor)
                bottom_lip = scale_point(polygon_center(
                    face_landmarks['bottom_lip']), scale_factor)
                lips = polygon_center([top_lip, bottom_lip])
                nose_tip = scale_point(polygon_center(
                    face_landmarks['nose_tip']), scale_factor)
            else:
                print("No face detected in", dayname, filename)

        face_center = polygon_center([left_eye, right_eye])
        eye_width = distance_between(left_eye, right_eye)
        result_scale_factor = target_eye_width/eye_width

        result_image = Image.new('RGB', result_resolution)

        scaled_image = scale_image(image, result_scale_factor)

        # Paste face center to 20 above image center
        # 20 number used to align to previous face centering algo
        # places tip of nose (instead of eyes) into center of image
        result_image.paste(scaled_image, (int(result_resolution[0] / 2) - int(face_center[0] * result_scale_factor), int(
            result_resolution[1] / 2) - int(face_center[1] * result_scale_factor) - 20))

        result_image = result_image.rotate(point_angle(left_eye, right_eye))

        date_exif = image.getexif()[0x0132]
        date = datetime.strptime(date_exif, '%Y:%m:%d %H:%M:%S')

        fnt = ImageFont.truetype("assets/RobotoMono-Regular.ttf", 40)
        draw = ImageDraw.Draw(result_image)
        draw.text((result_resolution[0] - side_text_offset, result_resolution[1] - bottom_text_offset), date.strftime(
            '%b %d, %Y').upper(), font=fnt, fill="white", anchor='rs', stroke_width=1, stroke_fill='black')

        loc = locations.get(day, None)
        if loc is not None:
            draw.text((result_resolution[0] - side_text_offset, result_resolution[1] - bottom_text_offset - line_offset), loc,
                      font=fnt, fill="white", anchor='rs', stroke_width=1, stroke_fill='black')

        note = notes.get(day, None)
        if note is not None:
            draw.text((side_text_offset, result_resolution[1] - bottom_text_offset), note,
                      font=fnt, fill="white", anchor='ls', stroke_width=1, stroke_fill='black')

        original_stem = Path(filename).stem

        result_image.save(os.path.join(OUTDIR, original_stem + '-' +
                          create_random_id() + '.jpg'), quality=90, subsampling=0)
