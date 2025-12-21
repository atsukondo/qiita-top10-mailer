import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MailHandler:
    def __init__(
        self,
        email_address,
        app_password,
        smtp_server="smtp.gmail.com",
        smtp_port=587
    ):
        self.email_address = email_address
        self.app_password = app_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
    
    def send_email(self, subject, body):
        msg = MIMEMultipart()
        msg['From'] = self.email_address
        msg['To'] = self.email_address
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        try:
            server.starttls()
            
            server.login(self.email_address, self.app_password)
            
            server.send_message(msg)
            print("Email sent successfully!")
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
            
        finally:
            server.quit()

