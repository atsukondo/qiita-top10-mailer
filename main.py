from client.mail_handler import MailHandler
from client.qiita import QiitaAPIClient
from config import settings


def run():
    client = QiitaAPIClient()
    items = client.get_items(per_page=10, query="LLM")
    email_content = QiitaAPIClient.format_items_for_email(items)
    subject = QiitaAPIClient.generate_email_subject(items, query="LLM")
    mail_handler = MailHandler(
        email_address=settings.EMAIL_ADDRESS,
        app_password=settings.APP_PASSWORD
    )
    mail_handler.send_email(
        subject=subject,
        body=email_content
    )


if __name__ == "__main__":
    run()