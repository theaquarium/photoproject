#!/bin/bash

# Activate the virtual environment
source ./venv/bin/activate

# Your script commands that use the virtual environment go here
echo "STARTING RENAME IMAGES TASK"
python3 rename_images.py

echo "STARTING MAKE THUMBS TASK"
python3 make_thumbs.py

echo "STARTING FACE PROCESS TASK"
python3 center_faces.py


# Deactivate the virtual environment (optional)
deactivate
