# Neurolytix\backend\alerts\alert_service.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

logger = logging.getLogger(__name__)

class AlertService:
    def __init__(self, smtp_server="smtp.gmail.com", smtp_port=587, email_user=None, email_pass=None):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email_user = email_user
        self.email_pass = email_pass

    def send_email(self, to_email, subject, message):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_user
            msg['To'] = to_email
            msg['Subject'] = subject

            msg.attach(MIMEText(message, 'plain'))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_user, self.email_pass)
            server.sendmail(self.email_user, to_email, msg.as_string())
            server.quit()
            logger.info(f"Alert email sent to {to_email}")
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
