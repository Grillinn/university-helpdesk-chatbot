# backend/services/email_service.py
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
import smtplib

load_dotenv()

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.smtp_username = os.getenv("SMTP_USERNAME")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.sender_email = os.getenv("SENDER_EMAIL")

    def send_email(self, recipient_email: str, subject: str, body: str):
        if not all([self.smtp_server, self.smtp_port, self.smtp_username, self.smtp_password, self.sender_email]):
            print("Error: Email configuration not fully set in environment variables.")
            return False

        try:
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = recipient_email

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Upgrade connection to secure TLS
                server.login(self.smtp_username, self.smtp_password)
                server.sendmail(self.sender_email, recipient_email, msg.as_string())
            print(f"Email sent successfully to {recipient_email}")
            return True
        except Exception as e:
            print(f"Error sending email to {recipient_email}: {e}")
            return False

if __name__ == "__main__":
    # Example usage (ensure you have SMTP credentials in .env file)
    email_service = EmailService()
    recipient = "test.recipient@example.com"  # Replace with a valid email
    subject = "Test Email from Admission Portal"
    body = "This is a test email sent from the University Admission Portal."

    if email_service.send_email(recipient, subject, body):
        print("Test email sent!")
    else:
        print("Failed to send test email.")