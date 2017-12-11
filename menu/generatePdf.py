from io import StringIO
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

        static_path = getattr(settings, "STATICFILES_DIRS")
        print("static_path")
        print(static_path)
        if not static_path
            print("stat file is empty 1")
            static_path = getattr(settings, "STATIC_ROOT")
        print("static_path")
        print(static_path)
        if not static_path
            print("stat file is empty 2")
            static_path.append("/home/vincentlegoff2004/menu/menu_semaine/static")
        print("static_path")
        print(static_path)
        css = path.join(static_path[0], "css/pdf_style.css")
        print(css)
        print("css")
        html = self.template.render(ctxt)
        print("html")
        print(html)
        self.pdf = pdfkit.from_string(html, False, configuration=config, css=css, options=options)

    def download(self):
        """Call this method if you want the user to download the PDF document generated"""
        response = http.HttpResponse(content_type='application/pdf')
        response[
            'Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(self.filename)
        response.write(self.pdf)
        return response

    def inline(self):
        """Call this method if you want the user to be able to view the in the browser"""
        response = http.HttpResponse(content_type='application/pdf')
        response[
            'Content-Disposition'] = 'inline; filename="{}.pdf"'.format(self.filename)
        response.write(self.pdf)
        return response

    def send_pdf(self, subject, email_template, ctxt, from_email=getattr(settings, "DEFAULT_FROM_EMAIL"),
                 to=("valid_email",), **kwargs):
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
        message_text = get_template(
            "{}".format(email_template)).render(ctxt)
        email_message = EmailMultiAlternatives(
            subject, message_text, from_email, to, **kwargs)
        print("email_message")
        print(email_message)
        try:
            message_html = get_template(
                "{}".format(email_template)).render(ctxt)
            email_message.attach_alternative(message_html, 'text/html')
        except TemplateDoesNotExist:
            print("Error")

        email_message.attach(
            filename="{}.pdf".format(self.filename), content=self.pdf, mimetype="application/pdf")
        email_message.send()

        # text_content = 'This is an important message.'
        # html_content = '<p>This is an <strong>important</strong> message.</p>'
        # msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        # msg.attach_alternative(html_content, "text/html")
        # msg.send()



class PDFResponseMixin(TemplateResponseMixin):
    """
    The base view for PDF generation and view.

    The childs of this object should define a get method, assign the following values::
            `pdf_filename` (str) - name of the PDF file to be generated

            `pdf_template` (str) - location of the html template to be used for generation of
                the `pdf_filename`.pdf

            `context` (dict) - The context data to be passed by Django template engine to `pdf_template`

    Examples:
        Suppose we want to create a view for viewing PDF document inline::
            >>> from django.views.generic import View
            >>> from sendpdf.topdf import PDFResponseMixin
            >>> class DownloadPDF(PDFResponseMixin, View):
                        pdf_filename = "account_statement"
                        pdf_template = "account_statement.html"
                        context = demo_data()
                        def get(self, request, *args, **kwargs):
                            self.get_pdf()
                            return self.pdfgen.inline()
    """
    pdf_filename = None
    pdf_template = None
    context = {}
    pdfgen = None
    pdf = None

    def get_pdfgen(self):
        if self.pdfgen is not None:
            return self.pdfgen
        self.pdfgen = GeneratePDF(self.pdf_template)
        return self.pdfgen

    def get_pdf(self):
        if self.pdf is not None:
            return self.pdf
        pdfg = self.get_pdfgen()
        self.pdf = pdfg._make_pdf(self.context, self.pdf_filename)
        return self.pdf


class DownloadPDF(PDFResponseMixin, View):
    """
    The base view for PDF generation and downloading.

    The childs of this object should assign the following values::
            `pdf_filename` (str) - name of the PDF file to be generated

            `pdf_template` (str) - location of the html template to be used for generation the `pdf_filename`.pdf

            `context` (dict) - The context data to be passed by Django template engine to `pdf_template`

    Examples:
        Suppose we want to create a view for viewing PDF document inline::
            >>> from sendpdf.topdf import DownloadPDF
            >>> class DownloadDemo(DownloadPDF):
                        pdf_filename = "account_statement"
                        pdf_template = "account_statement.html"
                        context = demo_data()
    """
    def get(self, request, *args, **kwargs):
        self.get_pdf()
        return self.pdfgen.download()


class ShowPDF(PDFResponseMixin, View):
    """
    The base view for PDF generation and downloading.

    The childs of this object should assign the following values::
            `pdf_filename` (str) - name of the PDF file to be generated

            `pdf_template` (str) - location of the html template to be used for generation the `pdf_filename`.pdf

            `context` (dict) - The context data to be passed by Django template engine to `pdf_template`

    Examples:
        Suppose we want to create a view for viewing PDF document inline::
            >>> from sendpdf.topdf import ShowPDF
            >>> class ShowDemo(ShowPDF):
                        pdf_filename = "account_statement"
                        pdf_template = "account_statement.html"
                        context = demo_data()
    """
    def get(self, request, *args, **kwargs):
        self.get_pdf()
        return self.pdfgen.inline()
