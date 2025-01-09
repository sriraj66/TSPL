from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

@shared_task
def send_success_email(subject, to, context):
    print("Sending Email")
    html_content = render_to_string('core/success_email.html', context)
    text_content = 'Your registration has been completed successfully.'
    from_email = settings.EMAIL_HOST_USER

    message = EmailMultiAlternatives(subject, text_content, from_email, [to,])
    message.attach_alternative(html_content, "text/html")
    
    message.send()
