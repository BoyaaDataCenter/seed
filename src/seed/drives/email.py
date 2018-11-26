import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formatdate


class Email(object):
    def __init__(self, configs):
        self.mail_backend = configs['MAIL_BACKEND']
        self.mail_host = configs['MAIL_HOST']
        self.mail_port = configs['MAIL_PORT']
        self.mail_user = configs['MAIL_USER']
        self.mail_password = configs['MAIL_PASSWORD']
        self.mail_use_tls = configs['MAIL_USE_TLS']
        self.mail_from = configs['MAIL_FROM']

    def send_mail(self, to_mail_list, title, message, message_type='plain', cc_mail_list=[]):
        to_mails = '; '.join(to_mail_list)
        cc_mails = '; '.join(cc_mail_list)

        mime_text = MIMEText(message.encode('utf-8'), message_type, 'utf-8')
        mime_text['Subject'] = Header(title, 'utf-8')
        mime_text['From'] = self.mail_from
        mime_text['To'] = to_mails
        mime_text['Cc'] = cc_mails
        mime_text['Date'] = formatdate()

        smtp = smtplib.SMTP(self.mail_host, self.mail_port)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(self.mail_user, self.mail_password)

        smtp.sendmail(self.mail_from, to_mail_list+cc_mail_list, mime_text.as_string())

        smtp.close()
