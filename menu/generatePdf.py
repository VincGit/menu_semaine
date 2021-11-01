""" from io import StringIO
from django import http
from django.conf import settings
from django.views.generic import View
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.views.generic.base import TemplateResponseMixin
from os import path
import pdfkit

#settings.configure() #: I use this during sphinx document generation

# Get the path to the wkhtmltopdf binary from the settings
path_wkthmltopdf = getattr(settings, "WKTHMLTOPDF_PATH")
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)


class GeneratePDF:
    """PDF generator"""

    data = []

    connection = None
    pdf = None
    filename = "Liste"

    def __init__(self, template):
        self.template = get_template("{}".format(template))

    def _make_pdf(self, ctxt):
        print("_make_pdf")

        options = {
            'page-size': 'A5',
            'margin-top': '0.25in',
            'margin-right': '0.50in',
            'margin-bottom': '0.05in',
            'margin-left': '0.50in',
            'orientation': 'Portrait',
        }
        production_mode = getattr(settings, "PROD")
        if not production_mode:
            static_path = getattr(settings, "STATICFILES_DIRS")

        else:
            static_path = getattr(settings, "STATIC_ROOT")

        print("static_path")
        print(static_path)
        css = path.join(static_path, "css/pdf_style.css")

        html = self.template.render(ctxt)
        self.pdf = pdfkit.from_string(html, False, configuration=config, css=css, options=options)

    def send_pdf(self, subject, email_template, ctxt, from_email=getattr(settings, "DEFAULT_FROM_EMAIL"),
                 to=getattr(settings, "EMAIL_TO_LIST"), **kwargs):
        """
        Call this method if you want the user to send the PDF to one or more email addresses.
        This method is compliant with the Django's EmailMultiAlternatives. This means that `**kwargs` can define the following::
           bcc - which is `bcc = None` by default
           cc - which is `cc = None` by default
           reply_to - which is `reply_to = None` by default
           headers - which is `headers = None` by default
           connection - which is `connection = None` by default
        It is advisable that you set up SMTP settings for an outbound email.
        Args:
           subject (str) - Subject of the email you want to send.
           email_template (str) - The html template that can be access by DJango template engine.
           ctxt (dict or Django context object) - Data that is to be populated in the `email_template`.
           from_email (Optional[str]) - A valid email address that is allowed to send email. By default it is defined at the Django settins `DEFAULT_FROM_EMAIL`.
           to (tuple) - A tuple of the recipients' email addresses.

        Examples:
           Suppose you want to send generated PDF to `john@doe.com`::
                >>> from django import http
                >>> from django.views.generic import View
                >>> from sendpdf.topdf import GeneratePDF
                >>> class SendDemo(View):
                            def get(self, *args, **kwargs):
                                s = GeneratePDF(template="account_statement.html")
                                s._make_pdf(ctxt=demo_data(20), filename="account_statement")
                                email_ctx = {"name": "John Doe", "month": "April"}
                                s.send_pdf(subject="Monthly statement", email_template="statement", ctxt=email_ctx, to=("john@doe.com",))
                                return http.HttpResponse("Email sent")


        """
        message_text = get_template("{}".format(email_template)).render(ctxt)
        email_message = EmailMultiAlternatives(subject, message_text, from_email, to, **kwargs)
        try:
            message_html = get_template("{}".format(email_template)).render(ctxt)
            email_message.attach_alternative(message_html, 'text/html')
        except TemplateDoesNotExist:
            print("Error")

        email_message.attach(
            filename="{}.pdf".format(self.filename), content=self.pdf, mimetype="application/pdf")
        email_message.send() """