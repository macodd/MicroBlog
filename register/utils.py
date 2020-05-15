from django.core.mail import EmailMessage
from render_block import render_block_to_string


def change_password_confirmation_mail(to_email):
    subject = 'Cambio de contraseña'
    from_email = 'no-reply@fogata.com'
    to_email = to_email
    html_content = render_block_to_string(
        'emails/changed-password.html',
    )
    msg = EmailMessage(
        subject, html_content, from_email, [to_email],
    )
    msg.content_subtype = "html"
    msg.send()