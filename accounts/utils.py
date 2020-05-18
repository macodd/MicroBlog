from django.core.files import File
from PIL import Image, ExifTags
from io import BytesIO
import os

from django.contrib.auth import get_user_model

from django.core.mail import EmailMessage
from render_block import render_block_to_string

from tweetme.settings import DEFAULT_FROM_EMAIL

User = get_user_model()


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


def register_confirmation_mail(user):
    subject = 'Gracias por registrarse!'
    from_email = DEFAULT_FROM_EMAIL
    to_email = user.email
    html_content = render_block_to_string(
        'emails/new-user.html',
        'html_main',
        {'first_name': user.first_name}
    )
    msg = EmailMessage(
        subject, html_content, from_email, [to_email],
    )
    msg.content_subtype = "html"
    msg.send()
