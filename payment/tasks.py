from io import BytesIO
from celery import task
import weasyprint

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order


@task
def payment_completed(order_id):
    """task to send email notification when payment is successful"""
    order = Order.objects.get(id=order_id)

    # create invoice e-mail
    subject = f'My shop - EE invoice number. {order.id}'
    message = 'Please find the attached email for your recent purchase.'
    email = EmailMessage(subject,
                         message,
                         'paulmutemi2030@gmail.com',
                         [order.email])

    # generate email
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheet=stylesheets)

    # attach pdf
    email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')

    # send mail
    email.send()
