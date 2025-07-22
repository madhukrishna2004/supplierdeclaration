import os
import base64
import logging
from flask import Flask, render_template, request, redirect, url_for, session, flash
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from werkzeug.utils import secure_filename
import bcrypt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account

from email.mime.base import MIMEBase
from email import encoders
import mimetypes
import traceback
import os
import base64
import logging
from googleapiclient.discovery import build
from google.oauth2 import service_account
import datetime
import logging
import threading
import time
import google.auth
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from werkzeug.utils import secure_filename
import mimetypes
from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import bcrypt
import logging
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/gmail.send']
CLIENT_SECRET_FILE = 'credentials.json'

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from googleapiclient.http import MediaIoBaseUpload
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from flask import Flask, request, redirect, url_for, session, flash, render_template  # ✅ Import Flask `request`
from google.auth.transport.requests import Request

# OAuth function to authenticate
def authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = Flow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds


# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret')
from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = "flask-oauth-app-447004-0697972a144e.json"
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)

# Configurations
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'xlsx', 'xls'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# PostgreSQL Database Configuration (Render)
db_config = {
    "host": "dpg-cv59gt8gph6c73apj7qg-a.singapore-postgres.render.com",
    "port": 5432,  # Default PostgreSQL port
    "user": "central_db_gpb1_user",
    "password": "9SiZ5xmQi6OB8NOl6HvK6XAjrXvEO62F",
    "database": "central_db_gpb1"
}

# Ensure necessary folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("user_tokens", exist_ok=True)  # Store per-user OAuth tokens

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Allow OAuth for local development (Prevents HTTPS restriction)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']  # New field to store name
        organization = request.form['organization']  # New field to store organization name

        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            # Connect to PostgreSQL
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            # Check if user already exists
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user:
                flash("Email is already registered. Please use a different email.", "danger")
                return redirect(url_for('register'))

            # Insert new user
            cursor.execute("""
                INSERT INTO users (email, password_hash, name, organization) 
                VALUES (%s, %s, %s, %s)
            """, (email, hashed_password.decode('utf-8'), name, organization))
            conn.commit()

            flash("Registration successful! You can now login.", "success")
            return redirect(url_for('login'))  # Redirect to login page after successful registration

        except psycopg2.Error as err:
            logger.error(f"Database error: {err}")
            flash(f"Database error: {err}", "danger")
        finally:
            cursor.close()
            conn.close()

    return render_template('register.html')

# Store link in DB (assumed from your original code, adjust as needed)
def store_link_in_db(user_id, recipient, link, link_type):
    """Mock function to store the link in a database."""
    logger.info(f"Storing {link_type} link for {recipient} (User ID: {user_id}): {link}")
    # Replace with your actual DB logic

'''def create_google_sheet_copy(recipient, user_id):
    """Create a unique Google Sheet copy from a template for each recipient."""
    try:
        # Authenticate with both Sheets and Drive scopes
        creds = authenticate()
        drive_service = build('drive', 'v3', credentials=creds)

        # Template Sheet ID (your original sheet with the Apps Script)
        TEMPLATE_SHEET_ID = 'YOUR_TEMPLATE_SHEET_ID'  # Replace with your template sheet ID

        # Create a copy of the template sheet
        copy_metadata = {
            'name': f"Supplier Form for {recipient}",
            'parents': []  # Optional: specify a folder ID if you want to organize copies
        }
        copied_file = drive_service.files().copy(
            fileId=TEMPLATE_SHEET_ID,
            body=copy_metadata
        ).execute()
        sheet_id = copied_file.get('id')
        sheet_link = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"

        # Transfer ownership to a human account to avoid service account issues
        owner_permission = {
            'type': 'user',
            'role': 'owner',
            'emailAddress': 'krishnamadhurama@gmail.com'  # Your human Google account
        }
        drive_service.permissions().create(
            fileId=sheet_id,
            body=owner_permission,
            transferOwnership=True,
            fields='id'
        ).execute()

        # Share with the recipient as an editor
        user_permission = {
            'type': 'user',
            'role': 'writer',
            'emailAddress': recipient  # Assuming recipient is an email address
        }
        drive_service.permissions().create(
            fileId=sheet_id,
            body=user_permission,
            fields='id'
        ).execute()

        # Store the sheet link in your database
        store_link_in_db(user_id, recipient, sheet_link, 'sheet')

        logger.info(f"Created and shared sheet for {recipient}: {sheet_link}")
        return sheet_link

    except HttpError as err:
        logger.error(f"Error creating Google Sheet copy: {err}")
        return None'''
    
def upload_file_to_drive(file, folder_id):
    """Upload a file to Google Drive and return the file URL."""
    try:
        creds = authenticate()
        service = build('drive', 'v3', credentials=creds)
        
        file_metadata = {
            'name': file.filename,
            'parents': [folder_id]
        }
        media = MediaFileUpload(file, mimetype='application/pdf')
        
        uploaded_file = service.files().create(
            media_body=media, body=file_metadata).execute()
        
        file_url = f"https://drive.google.com/file/d/{uploaded_file['id']}/view"
        return file_url
    except HttpError as err:
        logger.error(f"Error uploading file: {err}")
        return None

# Helper Functions
def allowed_file(filename):
    """Check if a file is allowed based on its extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

import os
import base64
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os


import base64
import mimetypes
from email.message import EmailMessage
from googleapiclient.errors import HttpError

import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

'''def create_message_with_attachment(to, subject, message_body, sheet_link, form_link, attachments):
    """Creates an email message with an HTML body and optional attachments."""
    
    # ✅ Inject variables into the template
    email_html = f"""\
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                background-color: #001F3F;
                color: #E3F2FD;
                font-family: 'Arial', sans-serif;
                line-height: 1.8;
                margin: 0;
                padding: 0;
            }}
            .container {{
                width: 90%;
                max-width: 800px;
                margin: auto;
                padding: 20px;
                background: linear-gradient(135deg, rgba(0,36,61,0.9), rgba(0,10,20,0.9));
                border-radius: 15px;
                box-shadow: 0 0 25px rgba(0, 183, 255, 0.8);
            }}
            .header {{
                text-align: center;
                padding: 10px;
                background: url('https://source.unsplash.com/800x200/?ocean,blue,water') no-repeat center center;
                background-size: cover;
                border-radius: 15px 15px 0 0;
            }}
            h1 {{
                color: #00CFFD;
                font-size: 28px;
                text-transform: uppercase;
                text-shadow: 0 0 10px #00CFFD;
            }}
            .content {{
                padding: 20px;
            }}
            .highlight {{
                color: #00E5FF;
                font-weight: bold;
                font-size: 20px;
            }}
            .cta {{
                text-align: center;
                margin-top: 20px;
            }}
            .cta a {{
                display: inline-block;
                padding: 12px 20px;
                font-size: 18px;
                color: #001F3F;
                background: #00CFFD;
                text-decoration: none;
                font-weight: bold;
                border-radius: 8px;
                box-shadow: 0 0 15px rgba(0, 229, 255, 0.9);
                transition: all 0.3s ease;
            }}
            .cta a:hover {{
                background: #00E5FF;
                box-shadow: 0 0 20px rgba(0, 229, 255, 1);
            }}
            .footer {{
                text-align: center;
                margin-top: 30px;
                font-size: 14px;
                color: #A9D9FF;
            }}
        </style>
    </head>
    <body>

    <div class="container">
        <div class="header">
            <h1>TRADESPHERE GLOBAL</h1>
        </div>

        <div class="content">
            <p>🌊 Welcome to the <strong>Next Era of Global Trade.</strong></p>

            <p>Dear Supplier,</p>

            <p>{message_body}</p>

            <p class="highlight">📜 <strong>Step 1: Read the Supplier Guidelines</strong></p>

            <p>📄 <strong>Google Sheet:</strong> <a href="{sheet_link}" style="color:#00E5FF;" target="_blank">{sheet_link}</a></p>
            <p>📨 <strong>Google Form:</strong> <a href="{form_link}" style="color:#00E5FF;" target="_blank">{form_link}</a></p>

            <div class="cta">
                <a href="https://trade-sphereglobal.com/origin">🔍 Check Eligibility Now</a>
            </div>
        </div>

        <div class="footer">
            <p><strong>TradeSphere Global - The Future of Trade is Here.</strong></p>
            <p>📩 <strong>For Support:</strong> <a href="mailto:support@trade-sphereglobal.com" style="color:#00E5FF;">Contact Us</a></p>
        </div>
    </div>

    </body>
    </html>
    """

    # ✅ Create MIME message
    message = MIMEMultipart()
    message["to"] = ", ".join(to)
    message["subject"] = subject
    message.attach(MIMEText(email_html, "html"))

    # ✅ Attach files if any
    for file_path in attachments:
        part = MIMEBase("application", "octet-stream")
        with open(file_path, "rb") as attachment:
            part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(file_path)}")
        message.attach(part)

    return {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")}
'''
def send_message(service, user_id, message):
    """Sends an email via Gmail API and returns success status."""
    try:
        message_sent = service.users().messages().send(userId=user_id, body=message).execute()
        return True if message_sent.get("id") else False  # ✅ Return True only if email is sent
    except Exception as error:
        logger.error(f"❌ Failed to send email: {error}")
        return False

# Routes
@app.route('/')
def landing():
    """Landing page."""
    return render_template('landing.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            # Connect to PostgreSQL
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            # Fetch user details
            cursor.execute("SELECT id, email, name, password_hash FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

            if user:
                user_id, user_email, user_name, hashed_password = user

                if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                    session['user_id'] = user_id
                    session['email'] = user_email
                    session['user_name'] = user_name  # Store user name in session
                    return redirect(url_for('dashboard'))
                else:
                    flash('Invalid email or password.', 'danger')
            else:
                flash('Invalid email or password.', 'danger')

        except psycopg2.Error as err:
            logger.error(f"Database error: {err}")
            flash(f"Database error: {err}", 'danger')

        finally:
            cursor.close()
            conn.close()

    return render_template('login.html')

# Email Logging Function
def log_sent_email(user_id, recipient, sheet_link):
    """Log sent email in the database and return the email ID."""
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        query = """
        INSERT INTO email_logs (user_id, recipient, sheet_link, status, sent_time) 
        VALUES (%s, %s, %s, 'Pending', NOW()) RETURNING id;
        """
        cursor.execute(query, (user_id, recipient, sheet_link))
        email_id = cursor.fetchone()[0]  # ✅ Get the inserted email's ID
        conn.commit()

        return email_id

    except psycopg2.Error as err:
        logger.error(f"Database insert error: {err}")
        return None

    finally:
        cursor.close()
        conn.close()


from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import shutil

# 🔹 Define Google Sheets template ID
#GOOGLE_SHEET_TEMPLATE_ID = "1z7bjcpn3gUm78B9JsjZvqgUEUQGu3hJxjaUTIwG8RiM"
#GOOGLE_SHEET_TEMPLATE_ID = "1ZpE2rRzQdxHMfw-LjxMgLVgJIfg4_sc0pUbKo35GOBs"
GOOGLE_SHEET_TEMPLATE_ID = "1WwvdBNGtGO91vjRvfVeps1hje047jR7MJLIl0zP5m-Q"

# 🔹 Load service account credentials
SERVICE_ACCOUNT_FILE = "flask-oauth-app-447004-0697972a144e.json"
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets"
]

HUMAN_OWNER_EMAIL = 'krishnamadhurama@gmail.com'

def create_google_sheet_copy(recipient_email: str, user_id: str, expiration_days: int = 2):
    """Creates a copy of the Google Sheet, shares it with the recipient, and sets an expiration."""
    try:
        if not recipient_email:
            logger.error("❌ Missing recipient_email.")
            return None

        # Load credentials
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        drive_service = build("drive", "v3", credentials=creds)

        # Generate a new sheet name
        new_sheet_name = f"Supplier_Form_{recipient_email.split('@')[0]}_{user_id}"

        # Copy the template Google Sheet
        copied_file = drive_service.files().copy(
            fileId=GOOGLE_SHEET_TEMPLATE_ID,
            body={"name": new_sheet_name}
        ).execute()

        # Get the new Sheet ID
        new_sheet_id = copied_file["id"]

        # Share with the recipient as an editor
        user_permission = {
            "type": "user",
            "role": "writer",
            "emailAddress": recipient_email
        }
        permission_response = drive_service.permissions().create(
            fileId=new_sheet_id,
            body=user_permission,
            fields='id'  # Get the permission ID for revocation
        ).execute()
        permission_id = permission_response.get('id')

        # Calculate expiration time
        creation_time = datetime.datetime.now()
        expiration_time = creation_time + datetime.timedelta(days=expiration_days)

        # Log the details
        logger.info(f"Sheet created: {new_sheet_id}, Expires: {expiration_time}")

        # Schedule access revocation
        def revoke_access():
            time_to_wait = (expiration_time - datetime.datetime.now()).total_seconds()
            if time_to_wait > 0:
                time.sleep(time_to_wait)
            try:
                # Revoke recipient's permission
                drive_service.permissions().delete(
                    fileId=new_sheet_id,
                    permissionId=permission_id
                ).execute()
                logger.info(f"Access revoked for Sheet: {new_sheet_id} (User: {recipient_email})")
            except Exception as e:
                logger.error(f"❌ Error revoking access: {str(e)}")

        # Run revocation in a background thread
        threading.Thread(target=revoke_access, daemon=True).start()

        # Return the Google Sheet URL
        sheet_url = f"https://docs.google.com/spreadsheets/d/{new_sheet_id}"
        logger.info(f"Sheet URL for {recipient_email}: {sheet_url}")
        return sheet_url

    except Exception as e:
        logger.error(f"❌ Error creating Google Sheet: {str(e)}")
        return None


from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# Google Drive & Sheets API Scopes
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']

def get_drive_service():
    """Authenticate and return the Google Drive API service."""
    creds = Credentials.from_service_account_file("flask-oauth-app-447004-0697972a144e.json", scopes=SCOPES)
    return build("drive", "v3", credentials=creds)

def get_sheets_service():
    return build("sheets", "v4", credentials=creds)


import os
import base64
from googleapiclient.http import MediaIoBaseUpload
from io import BytesIO

def upload_pdf_to_drive(file_data, file_name):
    """Uploads a PDF file to Google Drive and returns its link."""
    try:
        drive_service = get_drive_service()  # ✅ Ensure Drive service is initialized

        folder_id = "14BLdtpwodH-p75biqvDNXYRVvm-TIUojyoi0V1r-LOXeI74boE-Tta1ZhklbG0WhSckAMnIa"  # Replace with your Google Drive folder ID

        # Decode Base64 content
        file_content = base64.b64decode(file_data.split(",")[1])

        # Upload file to Google Drive
        media = MediaIoBaseUpload(BytesIO(file_content), mimetype="application/pdf", resumable=True)
        file_metadata = {
            "name": file_name,
            "parents": [folder_id]
        }
        uploaded_file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id"
        ).execute()

        file_url = f"https://drive.google.com/file/d/{uploaded_file['id']}/view"
        return file_url

    except Exception as e:
        print(f"Error uploading PDF: {e}")
        return None
def save_pdf_link_to_sheet(sheet_id, row, file_url):
    """Saves the uploaded PDF link to Google Sheets."""
    try:
        sheets_service = get_sheets_service()

        sheet_range = f"Sheet1!J{row}"  # Column J for uploaded PDFs

        values = [[f'=HYPERLINK("{file_url}", "📎 Open PDF")']]
        body = {"values": values}

        sheets_service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range=sheet_range,
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()

        print("✅ PDF link saved successfully to Google Sheets!")
    except Exception as e:
        print(f"Error updating sheet: {e}")
def log_pdf_upload(row, file_name, file_url):
    """Logs uploaded PDF details to an internal tracking file."""
    with open("upload_logs.txt", "a") as log_file:
        log_file.write(f"{row}, {file_name}, {file_url}\n")
    print("✅ PDF upload logged successfully!")

def send_pdf_email_notification(file_name, file_url, recipient_email):
    """Sends an email notification when a PDF is uploaded."""
    subject = "📢 New File Uploaded"
    body = f"A new file has been uploaded:\n\n- File Name: {file_name}\n- File URL: {file_url}"

    print(f"Sending email to {recipient_email}:\n{body}")
    # Use your email-sending function here

@app.route('/dashboard')
def dashboard():
    """User dashboard."""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)  # Fetch as dictionary

        # Retrieve email logs for the logged-in user
        cursor.execute("""
            SELECT * FROM email_logs WHERE user_id = %s ORDER BY sent_time DESC
        """, (user_id,))
        sent_emails = cursor.fetchall()  # Fetch email logs

    except psycopg2.Error as err:
        logger.error(f"Database fetch error: {err}")
        sent_emails = []
    
    finally:
        cursor.close()
        conn.close()

    return render_template('dashboard.html', email=session['email'], sent_emails=sent_emails)

SCOPES = ['https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/drive']
@app.route('/logout')
def logout():
    """Logs the user out by clearing the session and redirects to the Supplier Dashboard."""
    # Clear the session
    session.clear()

    # Flash a message to indicate successful logout
    flash("You have been logged out successfully.", "success")

    # Redirect to Supplier Dashboard or any page you want
    return redirect(url_for('dashboard'))

import psycopg2
import psycopg2.extras

def store_link_in_db(user_id, recipient, link, link_type):
    """Store the generated link (Sheet/Form) in the PostgreSQL database."""
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Update the correct column based on link type
        if link_type == 'sheet':
            cursor.execute("""
                UPDATE email_logs
                SET sheet_link = %s
                WHERE user_id = %s AND recipient = %s
            """, (link, user_id, recipient))
        elif link_type == 'form':
            cursor.execute("""
                UPDATE email_logs
                SET form_link = %s
                WHERE user_id = %s AND recipient = %s
            """, (link, user_id, recipient))

        conn.commit()  # Save changes

    except psycopg2.Error as err:
        logger.error(f"Database error: {err}")

    finally:
        cursor.close()
        conn.close()

from flask import Flask, render_template, request, session, redirect, url_for, flash
import os
import logging
from werkzeug.utils import secure_filename
from google_auth_oauthlib.flow import Flow
from email.mime.text import MIMEText
import base64



SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",  # Sending emails
    "https://www.googleapis.com/auth/drive.file",  # Access to files created/modified by the app
    "https://www.googleapis.com/auth/drive"        # Full Drive access (if needed)
]


from flask import render_template_string  # Import to process inline HTML templates

from flask import render_template_string  # Import to process inline HTML templates

@app.route('/send_email', methods=['GET', 'POST'])
def send_email():
    """Handles sending emails with unique Google Sheets and Google Forms to suppliers."""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    uploads_folder = app.config['UPLOAD_FOLDER']
    preloaded_attachments = [
        os.path.join(uploads_folder, 'TradeSphere_Supplier_Guide.pdf'),
        os.path.join(uploads_folder, 'SampleData.xlsx')
    ]
    preloaded_subject = "🚀 Official Request: Supplier Declaration Submission"
    preloaded_message = "Dear Supplier, we invite you to be part of the next-generation trade ecosystem. Please complete the attached form to verify compliance and streamline trade operations."

    uploaded_attachments = []

    if request.method == 'POST':
        recipients = request.form.get('recipients', '').strip().split(',')
        subject = request.form.get('subject', preloaded_subject).strip()
        message_body = request.form.get('message', preloaded_message).strip()

        # Process uploaded files
        if 'file' in request.files:
            files = request.files.getlist('file')
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(uploads_folder, filename)
                    file.save(file_path)
                    uploaded_attachments.append(file_path)

        # ✅ Generate unique Google Sheets and Forms for each recipient
        sheet_links = {}
        form_links = {}

        for recipient in recipients:
            recipient = recipient.strip()
            sheet_links[recipient] = create_google_sheet_copy(recipient, user_id)

        # ✅ Store email details in session before OAuth redirect
        session["email_details"] = {
            "recipients": recipients,
            "subject": subject,
            "message_body": message_body,
            "attachments": preloaded_attachments + uploaded_attachments,
            "sheet_links": sheet_links,
            "form_links": form_links
        }

        # ✅ High-End Email Body with Traditional and Corporate Branding
        session['email_body'] = render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {
                    background-color: #001F3F;
                    color: #E3F2FD;
                    font-family: 'Arial', sans-serif;
                    line-height: 1.8;
                    margin: 0;
                    padding: 0;
                }
                .container {
                    width: 90%;
                    max-width: 800px;
                    margin: auto;
                    padding: 20px;
                    background: linear-gradient(135deg, rgba(0,36,61,0.95), rgba(0,10,20,0.95));
                    border-radius: 15px;
                    box-shadow: 0 0 25px rgba(0, 183, 255, 0.8);
                }
                .header {
                    text-align: center;
                    padding: 10px;
                    background: url('https://source.unsplash.com/800x200/?business,technology,global') no-repeat center center;
                    background-size: cover;
                    border-radius: 15px 15px 0 0;
                }
                h1 {
                    color: #00CFFD;
                    font-size: 28px;
                    text-transform: uppercase;
                    text-shadow: 0 0 10px #00CFFD;
                }
                .content {
                    padding: 20px;
                }
                .highlight {
                    color: #00E5FF;
                    font-weight: bold;
                    font-size: 20px;
                }
                .cta {
                    text-align: center;
                    margin-top: 20px;
                }
                .cta a {
                    display: inline-block;
                    padding: 12px 20px;
                    font-size: 18px;
                    color: #001F3F;
                    background: #00CFFD;
                    text-decoration: none;
                    font-weight: bold;
                    border-radius: 8px;
                    box-shadow: 0 0 15px rgba(0, 229, 255, 0.9);
                    transition: all 0.3s ease;
                }
                .cta a:hover {
                    background: #00E5FF;
                    box-shadow: 0 0 20px rgba(0, 229, 255, 1);
                }
                .footer {
                    text-align: center;
                    margin-top: 30px;
                    font-size: 14px;
                    color: #A9D9FF;
                }
            </style>
        </head>
        <body>

        <div class="container">
            <div class="header">
                <h1>TRADESPHERE GLOBAL</h1>
            </div>

            <div class="content">
                <p>🌍 **Revolutionizing Global Trade with Technology**</p>

                <p>Dear Valued Supplier,</p>

                <p>Welcome to **TradeSphere Global – the future of seamless international trade.** To ensure smooth compliance and operational efficiency, we require your input on the **Supplier Declaration Form.**</p>

                <p class="highlight">📜 **Step 1: Access Your Personalized Forms**</p>

                {% for recipient in recipients %}
                <p>📄 **Google Sheet:** <a href="{{ sheet_links.get(recipient, 'Not Available') }}" style="color:#00E5FF;">View & Edit</a></p>
                <p>📨 **Google Form:** <a href="{{ form_links.get(recipient, 'Not Available') }}" style="color:#00E5FF;">Submit Now</a></p>
                {% endfor %}

                <p class="highlight">📌 **Why This Matters?**</p>
                <ul>
                    <li>📊 **Automated Compliance:** Instant verification & validation of your details.</li>
                    <li>⚡ **AI-Powered Data Processing:** Speeds up trade approvals by 80%.</li>
                    <li>🌎 **Global Standardization:** Adheres to EU-UK Trade Agreements & international norms.</li>
                    <li>📂 **Effortless Documentation:** No paperwork. Just **upload & submit digitally**.</li>
                </ul>

                <p class="highlight">🚀 **Act Now & Stay Ahead in Global Trade!**</p>

                <div class="cta">
                    <a href="https://trade-sphereglobal.com/origin">🔍 Check Your Trade Eligibility</a>
                </div>
            </div>

            <div class="footer">
                <p>**TradeSphere Global - The Future of Trade is Here.**</p>
                <p>📩 **For Support:** <a href="mailto:support@trade-sphereglobal.com" style="color:#00E5FF;">Contact Us</a></p>
            </div>
        </div>

        </body>
        </html>
        """, recipients=recipients, sheet_links=sheet_links, form_links=form_links)

        try:
            flow = Flow.from_client_secrets_file(
                'credentials.json', scopes=SCOPES,
                redirect_uri=url_for('oauth_callback', _external=True)
            )
            auth_url, state = flow.authorization_url(prompt='consent')
            session['flow'] = {'state': state}
            return redirect(auth_url)
        except Exception as e:
            logger.error(f"OAuth error: {e}")
            flash('OAuth authentication failed. Try again.', 'danger')
            return redirect(url_for('send_email'))

    return render_template('send_email.html', preloaded_subject=preloaded_subject, preloaded_message=preloaded_message)

import warnings
import google.auth.transport.requests

warnings.filterwarnings("ignore", category=DeprecationWarning)  # ✅ Suppress file_cache warning

from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import pickle


from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import pickle
import os

from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import pickle
import psycopg2
conn = psycopg2.connect(**db_config)

@app.route('/oauth_callback')
def oauth_callback():
    """Handles OAuth callback, sends branded emails, and logs activity."""
    try:
        if 'error' in request.args:
            flash("OAuth authorization failed. Please try again.", "danger")
            return redirect(url_for("send_email"))

        if "flow" not in session or "state" not in session["flow"]:
            flash("OAuth session expired. Restart authentication.", "danger")
            return redirect(url_for("send_email"))

        # ✅ Restore OAuth flow
        flow = Flow.from_client_secrets_file(
            'credentials.json',
            scopes=SCOPES,
            redirect_uri=url_for('oauth_callback', _external=True)
        )
        flow.oauth2session.state = session["flow"]["state"]
        flow.fetch_token(authorization_response=request.url)
        creds = flow.credentials

        # ✅ Store credentials securely
        user_id = session.get("user_id")
        if not user_id:
            flash("Session expired. Please log in again.", "danger")
            return redirect(url_for("login"))

        token_path = f"user_tokens/{user_id}_token.json"
        os.makedirs(os.path.dirname(token_path), exist_ok=True)
        with open(token_path, "w") as token_file:
            token_file.write(creds.to_json())

        # ✅ Build Gmail API service
        service = build("gmail", "v1", credentials=creds)

        # ✅ Retrieve email details
        email_details = session.pop("email_details", None)
        if not email_details:
            flash("Email details missing. Restart the process.", "warning")
            return redirect(url_for("dashboard"))

        if isinstance(email_details, str):
            import json
            try:
                email_details = json.loads(email_details)
            except json.JSONDecodeError:
                flash("Invalid email session data. Restart the process.", "danger")
                return redirect(url_for("dashboard"))

        recipients = email_details.get("recipients", [])
        subject = email_details.get("subject", "Supplier Declaration Request")
        message_body = email_details.get("message_body", "Please complete the attached form and submit it.")
        attachments = email_details.get("attachments", [])
        sheet_links = email_details.get("sheet_links", {})
        form_links = email_details.get("form_links", {})

        if not recipients:
            flash("No recipients found. Restart the process.", "warning")
            return redirect(url_for("dashboard"))

        # ✅ Establish Database Connection
        conn = psycopg2.connect(**db_config)

        cursor = conn.cursor()

        # ✅ Send emails and log each one in the database
        for recipient in recipients:
            recipient = recipient.strip()
            sheet_link = sheet_links.get(recipient, "Not Available")
           # form_link = form_links.get(recipient, "Not Available")

            print(f"📧 Sending Email - {recipient}: Sheet -> {sheet_link}")

            email_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{
                        background-color: #1E1E1E;
                        font-family: 'Arial', sans-serif;
                        color: #EAEAEA;
                        line-height: 1.6;
                        margin: 0;
                        padding: 20px;
                    }}
                    .container {{
                        max-width: 700px;
                        margin: auto;
                        background: #292929;
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 0 0 15px rgba(255, 255, 255, 0.1);
                    }}
                    .header {{
                        text-align: center;
                        padding: 15px;
                        background: #0077CC;
                        color: #ffffff;
                        border-radius: 10px 10px 0 0;
                    }}
                    h1 {{
                        font-size: 24px;
                        margin: 0;
                        color: #ffffff;
                    }}
                    .content {{
                        padding: 20px;
                    }}
                    .highlight {{
                        font-size: 18px;
                        font-weight: bold;
                        color: #00CFFF;
                    }}
                    .info-box {{
                        text-align: center;
                        background: #333;
                        padding: 10px;
                        border-radius: 5px;
                        margin-top: 15px;
                        color: #EAEAEA;
                    }}
                    .footer {{
                        text-align: center;
                        margin-top: 30px;
                        font-size: 14px;
                        color: #CCCCCC;
                    }}
                    .footer a {{
                        color: #00CFFF;
                        text-decoration: none;
                    }}
                    a {{
                        color: #FFD700;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>TRADESPHERE GLOBAL</h1>
                    </div>
                    <div class="content">
                        <p style="color: #FFD700;"><strong>Seamless Trade. Intelligent Compliance. Limitless Possibilities.</strong></p>
                        <p style="color: #FFFFFF;"><strong>Dear Supplier,</strong></p>
                        <p style="color: #EAEAEA;">We invite you to be part of the next-generation trade ecosystem. Please complete the attached form to verify compliance and streamline trade operations.</p>
                        <p class="highlight">📜 <strong>Steps to Complete Your Supplier Declaration:</strong></p>
                        <ol>
                            <li>📥 <strong style="color: #FFD700;">Download the Attached Documents</strong></li>
                            <li>✍️ <strong style="color: #FFD700;">Fill in the Required Details</strong></li>
                            <li>📄 <strong style="color: #00CFFF;">Google Sheet:</strong> <a href="{sheet_link}" target="_blank">{sheet_link}</a></li>
                            <li>📧 <strong style="color: #FFD700;">Submit Completed Form to Us</strong></li>
                        </ol>
                        <div class="info-box">
                            <p>📑 Get your <strong>EU-UK Preferential Agreement Report</strong> <a href="https://trade-sphereglobal.com/origin" style="color: #00CFFF;">here</a>.</p>
                        </div>
                    </div>
                    <div class="footer">
                        <p><strong>TradeSphere Global - Empowering Trade, Simplifying Compliance.</strong></p>
                        <p>📩 Need Assistance? <a href="mailto:support@trade-sphereglobal.com">Contact Support</a></p>
                    </div>
                </div>
            </body>
            </html>
            """

            # ✅ Create and send email
            message = create_message_with_attachment([recipient], subject, email_content, attachments)
            sent_status = send_message(service, "me", message)

            if sent_status:
                cursor.execute("""
                    INSERT INTO email_logs (user_id, recipient, subject, sheet_link,sent_time)
                    VALUES (%s, %s, %s, %s, NOW())
                """, (user_id, recipient, subject, sheet_link))
                conn.commit()
                print(f"✅ Logged Email: {recipient}")

        flash("✅ Emails sent successfully!", "success")

    except Exception as e:
        logger.error(f"❌ OAuth callback error: {e}")
        flash("⚠️ Failed to process OAuth callback. Try again.", "danger")

    finally:
        session.pop("flow", None)
        cursor.close()
        conn.close()

    return redirect(url_for("dashboard"))


'''@app.route('/oauth_callback')
def oauth_callback():
    """Handles OAuth callback, sends branded emails, and logs activity."""
    try:
        if 'error' in request.args:
            flash("OAuth authorization failed. Please try again.", "danger")
            return redirect(url_for("send_email"))

        if "flow" not in session or "state" not in session["flow"]:
            flash("OAuth session expired. Restart authentication.", "danger")
            return redirect(url_for("send_email"))

        # ✅ Restore OAuth flow
        flow = Flow.from_client_secrets_file(
            'credentials.json',
            scopes=SCOPES,
            redirect_uri=url_for('oauth_callback', _external=True)
        )
        flow.oauth2session.state = session["flow"]["state"]
        flow.fetch_token(authorization_response=request.url)
        creds = flow.credentials

        # ✅ Store credentials securely
        user_id = session.get("user_id")
        if not user_id:
            flash("Session expired. Please log in again.", "danger")
            return redirect(url_for("login"))

        token_path = f"user_tokens/{user_id}_token.json"
        os.makedirs(os.path.dirname(token_path), exist_ok=True)
        with open(token_path, "w") as token_file:
            token_file.write(creds.to_json())

        # ✅ Build Gmail API service
        service = build("gmail", "v1", credentials=creds)

        # ✅ Retrieve email details and ensure it's a dictionary
        email_details = session.pop("email_details", None)

        if not email_details:
            flash("Email details missing. Restart the process.", "warning")
            return redirect(url_for("dashboard"))

        if isinstance(email_details, str):  # 🔹 Convert string to dictionary if needed
            import json
            try:
                email_details = json.loads(email_details)
            except json.JSONDecodeError:
                flash("Invalid email session data. Restart the process.", "danger")
                return redirect(url_for("dashboard"))

        # ✅ Extract email data safely
        recipients = email_details.get("recipients", [])
        subject = email_details.get("subject", "Supplier Declaration Request")
        message_body = email_details.get("message_body", "Please complete the attached form and submit it.")
        attachments = email_details.get("attachments", [])
        sheet_links = email_details.get("sheet_links", {})
        form_links = email_details.get("form_links", {})

        if not recipients:
            flash("No recipients found. Restart the process.", "warning")
            return redirect(url_for("dashboard"))

        # ✅ Send emails (Refined Format)
        for recipient in recipients:
            recipient = recipient.strip()
            sheet_link = sheet_links.get(recipient, "Not Available")

            print(f"📧 Sending Email - {recipient}: Sheet -> {sheet_link}, Form -> {form_link}")

            email_content = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            background-color: #1E1E1E;
            font-family: 'Arial', sans-serif;
            color: #EAEAEA;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 700px;
            margin: auto;
            background: #292929;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(255, 255, 255, 0.1);
        }}
        .header {{
            text-align: center;
            padding: 15px;
            background: #0077CC;
            color: #ffffff;
            border-radius: 10px 10px 0 0;
        }}
        h1 {{
            font-size: 24px;
            margin: 0;
            color: #ffffff;
        }}
        .content {{
            padding: 20px;
        }}
        .highlight {{
            font-size: 18px;
            font-weight: bold;
            color: #00CFFF;
        }}
        .info-box {{
            text-align: center;
            background: #333;
            padding: 10px;
            border-radius: 5px;
            margin-top: 15px;
            color: #EAEAEA;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            font-size: 14px;
            color: #CCCCCC;
        }}
        .footer a {{
            color: #00CFFF;
            text-decoration: none;
        }}
        a {{
            color: #FFD700;
        }}
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <h1>TRADESPHERE GLOBAL</h1>
    </div>

    <div class="content">
        <p style="color: #FFD700;"><strong>Seamless Trade. Intelligent Compliance. Limitless Possibilities.</strong></p>

        <p style="color: #FFFFFF;"><strong>Dear Supplier,</strong></p>

        <p style="color: #EAEAEA;">We invite you to be part of the next-generation trade ecosystem. Please complete the attached form to verify compliance and streamline trade operations.</p>

        <p class="highlight">📜 <strong>Steps to Complete Your Supplier Declaration:</strong></p>
        <ol>
            <li>📥 <strong style="color: #FFD700;">Download the Attached Documents</strong></li>
            <li>✍️ <strong style="color: #FFD700;">Fill in the Required Details</strong></li>
            <li>📄 <strong style="color: #00CFFF;">Google Sheet:</strong> <a href="{sheet_link}" target="_blank">{sheet_link}</a></li>
            <li>📨 <strong style="color: #00CFFF;">Google Form Submission:</strong> <a href="{form_link}" target="_blank">{form_link}</a></li>
            <li>📧 <strong style="color: #FFD700;">Submit Completed Form to Us</strong></li>
        </ol>

        <div class="info-box">
            <p>📑 Get your <strong>EU-UK Preferential Agreement Report</strong> <a href="https://trade-sphereglobal.com/origin" style="color: #00CFFF;">here</a>.</p>
        </div>
    </div>

    <div class="footer">
        <p><strong>TradeSphere Global - Empowering Trade, Simplifying Compliance.</strong></p>
        <p>📩 Need Assistance? <a href="mailto:support@trade-sphereglobal.com">Contact Support</a></p>
    </div>
</div>

</body>
</html>
"""

            message = create_message_with_attachment([recipient], subject, email_content, attachments)
            send_message(service, "me", message)

        flash("✅ Emails sent successfully!", "success")

    except Exception as e:
        logger.error(f"❌ OAuth callback error: {e}")
        flash("⚠️ Failed to process OAuth callback. Try again.", "danger")

    session.pop("flow", None)
    return redirect(url_for("dashboard"))'''

def create_message_with_attachment(to, subject, html_body, attachments=[]):
    message = MIMEMultipart()
    message["to"] = ", ".join(to)
    message["subject"] = subject

    # Use HTML format for the email body
    msg = MIMEText(html_body, "html")
    message.attach(msg)

    for attachment_path in attachments:
        part = MIMEBase("application", "octet-stream")
        with open(attachment_path, "rb") as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(attachment_path)}")
        message.attach(part)

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {"raw": raw}

def update_email_status(email_id, status):
    """Update the email's status in the database."""
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        query = "UPDATE email_logs SET status = %s WHERE id = %s"
        cursor.execute(query, (status, email_id))
        conn.commit()

    except psycopg2.Error as err:
        logger.error(f"Database update error: {err}")

    finally:
        cursor.close()
        conn.close()

# Main
if __name__ == '__main__':
    app.run(debug=True)