from celery import shared_task
from django.core.mail import BadHeaderError, EmailMessage
from render_block import render_block_to_string

from tweetme.settings import DEFAULT_FROM_EMAIL


@shared_task
def change_password_confirmation_mail(to_email):
    subject = 'Cambio de contraseña'
    from_email = DEFAULT_FROM_EMAIL
    to_email = to_email
    html_content = render_block_to_string(
        'emails/changed-password.html', 'html_main'
    )
    msg = EmailMessage(
        subject, html_content, from_email, [to_email],
    )
    msg.content_subtype = "html"
    try:
        msg.send()
    except BadHeaderError:
        pass
    return None
