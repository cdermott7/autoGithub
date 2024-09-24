import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from src.utils.logger import main_logger

class Notifier:
    def __init__(self, config):
        self.config = config
        self.smtp_server = config['smtp_server']
        self.smtp_port = config['smtp_port']
        self.sender_email = config['sender_email']
        self.app_password = os.getenv('EMAIL_PASSWORD')
        self.recipient_email = config['recipient_email']

    def send_notification(self, subject, message):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            msg['Subject'] = subject

            msg.attach(MIMEText(message, 'plain'))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                main_logger.debug("Starting TLS for SMTP connection")
                server.login(self.sender_email, self.app_password)
                main_logger.debug("SMTP server login successful")
                server.send_message(msg)
                main_logger.debug("Email sent successfully")

            main_logger.info(f"Notification sent: {subject}")
        except smtplib.SMTPAuthenticationError as e:
            main_logger.error(f"SMTP Authentication Error: {str(e)}")
        except Exception as e:
            main_logger.error(f"Failed to send notification: {str(e)}")
