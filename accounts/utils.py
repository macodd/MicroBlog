from django.core.files import File
from PIL import Image, ExifTags
from io import BytesIO
import os

from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model

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


def send_mail_to_user(user_email):
    subject = 'Gracias por registrarse!'
    from_email = 'no-reply@fogata.com'
    to = user_email
    html_content =  '<h3><strong>Bienvenido!</strong></h3>' \
                    '<p>Le damos la bienvenida a La Fogata.</p>' \
                    '<p>Conectese con su comunidad y averigue lo que esta ocurriendo en su alrededor.</p>' \
                    '<p>Que se escuche su voz!</p><br/>' \
                    '<p> - La Fogata</p>'
    msg = EmailMessage(subject, html_content, from_email, [to])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()
