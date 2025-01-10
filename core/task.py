from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_success_email(subject, to, context):
    def send_email():
        try:
            html_content = render_to_string('core/success_email.html', context)
            text_content = 'Your registration has been completed successfully.'
            from_email = settings.EMAIL_HOST_USER
            message = EmailMultiAlternatives(subject, text_content, from_email, [to,])
            message.attach_alternative(html_content, "text/html")
            message.send()
            print(f"Email sent to {to}")
        except Exception as e:
            print(f"Error sending email to {to}: {e}")

    send_email()