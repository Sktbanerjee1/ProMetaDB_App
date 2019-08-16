import os
import secrets
import pydicom
from PIL import Image
from rapid_ct_app import app
from rapid_ct_app.models import File
from flask_login import current_user
import numpy as np

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/assets/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def format_datetime(value, format="%d %b %Y %I:%M %p"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    if value is None:
        return ""
    return value.strftime(format)


def get_pixels_hu(dcmfile):
    arr = dcmfile.pixel_array
    # Convert to int16 (from sometimes int16), 
    # should be possible as values should always be low enough (<32k)
    arr = arr.astype(np.int16)
    # Set outside-of-scan pixels to 0
    # The intercept is usually -1024, so air is approximately 0
    arr[arr == -2000] = 0
    # Convert to Hounsfield units (HU)
    intercept = dcmfile.RescaleIntercept
    slope = dcmfile.RescaleSlope
    if slope != 1:
        arr = slope * arr.astype(np.float64)
        arr = arr.astype(np.int16)
    arr += np.int16(intercept)
    return np.array(arr, dtype=np.int16)


def normal_windowing(image, MIN_BOUND=-20, MAX_BOUND=80):
    image[image>MAX_BOUND] = MAX_BOUND
    image[image<MIN_BOUND] = MIN_BOUND
    return image