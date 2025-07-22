import os
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Gmail API Scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Load or generate token
def get_credentials():
    creds = None
    # Token.json stores the user's access and refresh tokens
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If no valid credentials, prompt the user to log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def send_email_with_gmail_oauth2(recipients, subject, message_body, attachments=None):
    creds = get_credentials()
    access_token = creds.token

    # Automatically extract sender's email from credentials
    sender_email = creds.id_token.get('email')

    if not sender_email:
        print("Error: Could not retrieve sender's email. Check your credentials.")
        return

    # Set up the SMTP connection with OAuth2
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    try:
        # Initialize SMTP connection
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.ehlo()

        # Use the OAuth2 token to authenticate
        auth_string = f"user={sender_email}\1auth=Bearer {access_token}\1\1"
        server.docmd("AUTH XOAUTH2", base64.b64encode(auth_string.encode()).decode())

        # Prepare the email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject

        # Add message body
        msg.attach(MIMEText(message_body, 'plain'))

        # Add attachments (if any)
        if attachments:
            for file_path in attachments:
                with open(file_path, 'rb') as file:
                    mime_base = MIMEBase('application', 'octet-stream')
                    mime_base.set_payload(file.read())
                    encoders.encode_base64(mime_base)
                    mime_base.add_header(
                        'Content-Disposition', f'attachment; filename={os.path.basename(file_path)}')
                    msg.attach(mime_base)

        # Send email
        server.send_message(msg)
        print("Email sent successfully!")

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        server.quit()
