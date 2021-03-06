from celery import shared_task

from django.core.mail import EmailMessage
from render_block import render_block_to_string

from tweetme.settings import DEFAULT_FROM_EMAIL


@shared_task
def register_confirmation_mail(first_name, email):
    subject = 'Gracias por registrarse!'
    from_email = DEFAULT_FROM_EMAIL
    to_email = email
    html_content = render_block_to_string(
        'emails/new-user.html',
        'html_main',
        {'first_name': first_name}
    )
    msg = EmailMessage(
        subject, html_content, from_email, [to_email],
    )
    msg.content_subtype = "html"
    msg.send()
    return None
