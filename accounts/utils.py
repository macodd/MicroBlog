from django.core.files import File
from PIL import Image, ExifTags
from io import BytesIO
import os


def get_filename_ext(filepath):
    basename = os.path.basename(filepath)
    name, ext = os.path.splitext(basename)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = instance.user.username
    name, ext = get_filename_ext(filename)
    final_filename = f'{new_filename}{ext}'
    return f'images/{new_filename}/{final_filename}'


def rotate_image(instance):
    try:
        pil_image = Image.open(BytesIO(instance.image.read()))
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(pil_image._getexif().items())

        if exif[orientation] == 3:
            pil_image = pil_image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            pil_image = pil_image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            pil_image = pil_image.rotate(90, expand=True)

        output = BytesIO()
        pil_image.save(output, format='JPEG', quality=75)
        output.seek(0)
        instance.image = File(output, instance.image.name)
    except (AttributeError, KeyError, IndexError):
        # cases: image don't have getexif
        pass
