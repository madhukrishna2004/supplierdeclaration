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
from google.oauth2 import service_account  # your User model must inherit from UserMixin
import os
from dotenv import load_dotenv
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

import os
import json
import tempfile
from flask import Flask
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
from sqlalchemy import create_engine

# SCOPES for Google OAuth
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# ✅ 1. OAuth function using token.json (used only for OAuth clients, not service account)
# ✅ 1. Local-only OAuth authenticate (fallback if you don't use service account)
def authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = Flow.from_client_secrets_file(
                'client_secret.json', SCOPES)  # For local only
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds

# ✅ 2. Flask App Setup
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret')

# ✅ 3. Google Credentials Loader (Universal: Render or Local)
creds = None

# Prefer file for local dev
cred_file_path = os.getenv("GOOGLE_CREDENTIALS_FILE")

if cred_file_path and os.path.exists(cred_file_path):
    creds = service_account.Credentials.from_service_account_file(cred_file_path, scopes=SCOPES)
    print("✅ Loaded Google credentials from file.")

elif os.getenv("GOOGLE_CREDENTIALS_JSON"):
    try:
        creds_dict = json.loads(os.getenv("GOOGLE_CREDENTIALS_JSON"))
        creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
        creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
        print("✅ Loaded Google credentials from JSON.")
    except Exception as e:
        print("❌ Error loading Google credentials from JSON:", e)
        raise

else:
    # Fallback for local-only testing
    print("⚠️ No service account found — trying local user OAuth flow.")
    creds = authenticate()

# ✅ 4. Upload Folder Config
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'xlsx', 'xls'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# ✅ 5. PostgreSQL Config using DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL not set in environment!")

engine = create_engine(DATABASE_URL)
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
            conn = psycopg2.connect(DATABASE_URL)
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
            conn = psycopg2.connect(DATABASE_URL)
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
        conn = psycopg2.connect(DATABASE_URL)
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
GOOGLE_SHEET_TEMPLATE_ID = "1JO8sp4JlBUOY2m2QMj29LBs8vxuyC1U35QTozXw8WCo"

# 🔹 Load service account credentials
SERVICE_ACCOUNT_FILE = "flask-oauth-app-447004-0697972a144e.json"
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets"
]

HUMAN_OWNER_EMAIL = 'krishnamadhurama@gmail.com'

def create_google_sheet_copy(recipient_email: str, user_id: str) -> str:
    """
    Returns a view-only Google Sheet link and instructs the user to make a copy.
    """
    try:
        sheet_url = "https://docs.google.com/spreadsheets/d/1ZpE2rRzQdxHMfw-LjxMgLVgJIfg4_sc0pUbKo35GOBs/edit?usp=sharing"
        
        logger.info(f"📄 View-only Google Sheet link shared with {recipient_email}")
        logger.info("📌 Instruct the user to make a copy (File → Make a copy) before filling in.")
        
        return sheet_url

    except Exception as e: 
        logger.error(f"❌ Error returning sheet link: {str(e)}")
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
    """User dashboard with email logs and supplier data."""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Get the user's name
        cursor.execute("SELECT name FROM users WHERE id = %s", (user_id,))
        user_record = cursor.fetchone()
        user_name = user_record['name'] if user_record else 'User'

        # 🔁 Join email_logs and supplier_demand using recipient email
        cursor.execute("""
            SELECT 
                e.id,
                e.recipient,
                e.sent_time,
                CONCAT('/view_entries/', s.id) AS commodity_link,

                s.consent
            FROM email_logs e
            LEFT JOIN supplier_demand s ON e.recipient = s.username
            WHERE e.user_id = %s
            ORDER BY e.sent_time DESC
        """, (user_id,))
        
        sent_emails = cursor.fetchall()

    except psycopg2.Error as err:
        logger.error(f"Database fetch error: {err}")
        sent_emails = []
        user_name = "User"

    finally:
        cursor.close()
        conn.close()

    return render_template('dashboard.html', user_name=user_name, sent_emails=sent_emails)

@app.route("/get_group_emails", methods=["POST"])
def get_group_emails():
    group_name = request.json.get("group_name")
    emails = ContactGroup.query.filter_by(group_name=group_name).all()
    return jsonify([e.email for e in emails])
from flask import Flask, render_template, request, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, EmailLog, ContactGroup,Contact
import os
from dotenv import load_dotenv
from email.message import EmailMessage
import smtplib
'''@app.route('/api/groups')
def get_groups():
    groups = ContactGroup.query.all()
    return jsonify([{'id': g.id, 'name': g.name} for g in groups])
@app.route('/api/group_contacts/<int:group_id>')
def group_contacts(group_id):
    contacts = Contact.query.filter_by(group_id=group_id).all()
    return jsonify([c.email for c in contacts])
@app.route('/api/add_contact', methods=['POST'])
def add_contact():
    data = request.get_json()
    email = data.get('email')
    group_id = data.get('group_id')

    if not email or not group_id:
        return jsonify({'status': 'error', 'message': 'Missing data'}), 400

    existing = Contact.query.filter_by(email=email, group_id=group_id).first()
    if existing:
        return jsonify({'status': 'exists', 'message': 'Already exists'})

    contact = Contact(email=email, group_id=group_id)
    db.session.add(contact)
    db.session.commit()
    return jsonify({'status': 'success'})
@app.route('/api/suggestions')
def suggestions():
    q = request.args.get('q', '')
    if not q:
        return jsonify([])
    matches = Contact.query.filter(Contact.email.ilike(f'%{q}%')).limit(10).all()
    return jsonify([c.email for c in matches])'''

@app.route('/api/import_contacts', methods=['POST'])
def import_contacts():
    file = request.files['file']
    group_id = request.form.get('group_id')

    if not file or not group_id:
        return jsonify({'status': 'error', 'message': 'Missing file or group ID'}), 400

    import pandas as pd
    df = pd.read_excel(file) if file.filename.endswith('.xlsx') else pd.read_csv(file)
    
    added = 0
    for email in df.iloc[:,0]:  # assuming first column has emails
        if isinstance(email, str) and '@' in email:
            existing = Contact.query.filter_by(email=email, group_id=group_id).first()
            if not existing:
                contact = Contact(email=email, group_id=group_id)
                db.session.add(contact)
                added += 1
    db.session.commit()

    return jsonify({'status': 'success', 'added': added})


'''@app.route("/save_contacts_group", methods=["POST"])
def save_contacts_group():
    group_name = request.form.get("group_name")
    emails = request.form.get("emails", "")
    for email in emails.split(","):
        contact = ContactGroup(group_name=group_name, email=email.strip())
        db.session.add(contact)
    db.session.commit()
    return "Saved", 200'''

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
        conn = psycopg2.connect(DATABASE_URL)
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
import hashlib
from datetime import datetime


from flask import request, jsonify, session, render_template_string, redirect, url_for, flash
import hashlib
from datetime import datetime
import os
import json
import psycopg2
from werkzeug.utils import secure_filename
from google_auth_oauthlib.flow import Flow

# Credential Generator
from datetime import datetime
import hashlib
#from flask_login import login_required, current_user

import hashlib
import uuid
from datetime import datetime

#from flask_login import login_required

 
def generate_credentials(email):
    """
    Generate a unique username and password for the recipient,
    and store them in the `supplier_demand` table.
    """
    unique_suffix = str(uuid.uuid4())[:8]  # Use UUID for uniqueness
    username = f"tradesphere_supplier_{unique_suffix}"
    
    # Password is SHA1 of email + timestamp (first 12 characters)
    raw = email + str(datetime.now())
    password = hashlib.sha1(raw.encode()).hexdigest()[:12]
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # Insert into supplier_demand
        cur.execute("""
            INSERT INTO supplier_demand (username, password)
            VALUES (%s, %s)
        """, (username, password))

        conn.commit()
        cur.close()
        conn.close()
    except Exception as err:
        logger.error(f"❌ Failed to insert into supplier_demand: {err}")

    return username, password, datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@app.route('/supplier_logout')
def supplier_logout():
    session.pop('supplier_logged_in', None)
    session.pop('supplier_username', None)
    flash("Logged out successfully.")
    return redirect(url_for('supplier_login'))

from datetime import datetime

 
@app.route('/supplier_demand')
def supplier_portal():
    if not session.get('supplier_logged_in'):
        flash("You must log in to access this page.")
        return redirect(url_for('supplier_login'))

    username = session.get('supplier_username')

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Fetch the logged-in user's records (consent + commodity link)
        cursor.execute("""
            SELECT * FROM supplier_demand WHERE username = %s
        """, (username,))
        supplier_data = cursor.fetchone()

    except Exception as e:
        flash("Error loading your data: " + str(e), "error")
        supplier_data = None

    finally:
        cursor.close()
        conn.close()

    return render_template('supplier_demand.html', supplier=supplier_data)



from flask import request, redirect, url_for, render_template, session, flash
import psycopg2
import psycopg2.extras

@app.route('/supplier_login', methods=['GET', 'POST'])
def supplier_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            # Match username and password from supplier_demand table
            cursor.execute("""
                SELECT * FROM supplier_demand 
                WHERE username = %s AND password = %s
            """, (username, password))
            
            user = cursor.fetchone()

            if user:
                session['supplier_logged_in'] = True
                session['supplier_username'] = username
                return redirect(url_for('supplier_portal'))
            else:
                flash("Invalid username or password.", "error")

        except Exception as e:
            flash("Database error: " + str(e), "error")

        finally:
            cursor.close()
            conn.close()

    return render_template('supplier_login.html')


from flask import request, redirect, url_for, render_template, session, flash, jsonify, render_template_string
import json
import os
from werkzeug.utils import secure_filename

@app.route('/send_email', methods=['GET', 'POST'])
def send_email():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    uploads_folder = app.config['UPLOAD_FOLDER']
    preloaded_subject = "🌐 Access Your Supplier Portal – TradeSphere Global Invitation"
    preloaded_message = (
        "Dear Supplier,\n\n"
        "On behalf of your partnering company,TradeSphere Global invites you to digitize your compliance process with cutting-edge automation.\n\n"
        "We’re here to help you streamline Supplier Declarations, reduce manual work, and ensure seamless international trade operations.\n\n"
        "🔐 Your Secure Portal Access:\n"
        "👉 Login:  https://supplierdeclarations.com/supplier_login\n\n"
        "🎓 Need help getting started? Watch our step-by-step video guide:\n"
        "1. How to log into the Supplier Portal\n"
        "2. How to fill the Supplier Declaration Form\n"
        "3. How to complete the Commodity Compliance Sheet\n\n"
        "📺 Watch here: https://www.youtube.com/watch?v=YOUR_VIDEO_ID\n\n"
        "💬 Need Help?\n"
        "Reach out to our support team anytime at: support@trade-sphereglobal.com\n\n"
        "Thank you for being a part of the new trade era.\n\n"
        "Warm regards,\n"
        "Team TradeSphere Global"
    )

    uploaded_attachments = []

    if request.method == 'POST':
        # ✅ FIX: Handle Tagify recipient JSON properly
        raw_recipients = request.form.get('recipients', '[]')
        try:
            tagify_data = json.loads(raw_recipients)
            recipients = [item['value'].strip() for item in tagify_data if 'value' in item]
        except Exception as e:
            flash(f"❌ Failed to parse recipient emails: {e}", 'danger')
            return redirect(url_for('send_email'))

        subject = request.form.get('subject', preloaded_subject).strip()
        message_body = request.form.get('message', preloaded_message).strip()

        if not recipients:
            flash("⚠️ No valid email recipients provided.", 'danger')
            return redirect(url_for('send_email'))

        # ✅ Handle file uploads
        if 'file' in request.files:
            files = request.files.getlist('file')
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(uploads_folder, filename)
                    file.save(file_path)
                    uploaded_attachments.append(file_path)

        # ✅ Generate a shared sheet link
        common_sheet_link = create_google_sheet_copy("common_supplier_sheet", user_id)

        # ✅ Generate and store login credentials
        credentials_dict = {}
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            for recipient in recipients:
                username, password, sent_time = generate_credentials(recipient)
                credentials_dict[recipient] = {
                    "username": username,
                    "password": password,
                    "sent_time": sent_time
                }

                cur.execute("""
                    INSERT INTO email_logs (user_id, recipient, subject, message, username, password, sent_time)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (user_id, recipient, subject, message_body, username, password, sent_time))

                cur.execute("""
                    INSERT INTO supplier_demand (username, password)
                    VALUES (%s, %s)
                """, (username, password))

            conn.commit()
            cur.close()
            conn.close()
        except Exception as db_err:
            flash("Database error occurred while saving logs.", 'danger')
            return jsonify({"error": str(db_err)}), 500

        # ✅ Prepare HTML templates per user
        rendered_email_templates = {}
        for recipient in recipients:
            cred = credentials_dict[recipient]
            rendered_email_templates[recipient] = render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

        body {
            font-family: 'Inter', sans-serif;
            background-color: #ffffff;
            color: #333333;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 700px;
            margin: 40px auto;
            background-color: #ffffff;
            border-radius: 12px;
            box-shadow: 0 0 40px rgba(0, 82, 204, 0.05);
            padding: 30px;
        }
        .header {
            text-align: center;
        }
        .logo {
            max-width: 160px;
            margin-bottom: 10px;
        }
        .header h1 {
            font-size: 26px;
            color: #0052cc;
            margin: 10px 0 5px;
        }
        .tagline {
            font-size: 15px;
            color: #555;
            margin-bottom: 20px;
        }
        .credentials-card {
            background-color: #f9f9fb;
            border-radius: 10px;
            padding: 20px;
            margin-top: 25px;
            border: 1px solid #e0e6ed;
        }
        .credentials-card h3 {
            color: #0052cc;
            font-size: 18px;
            margin-bottom: 12px;
        }
        .credentials-card p {
            margin: 6px 0;
            font-size: 15px;
        }
        .cta-buttons {
            margin-top: 35px;
            text-align: center;
        }
        .cta-buttons a {
            display: inline-block;
            margin: 10px;
            padding: 14px 24px;
            background-color: #0052cc;
            color: #ffffff;
            text-decoration: none;
            font-weight: 600;
            border-radius: 8px;
            transition: background-color 0.3s ease;
        }
        .cta-buttons a:hover {
            background-color: #003d99;
        }
        .footer {
            text-align: center;
            font-size: 13px;
            color: #777777;
            margin-top: 40px;
        }
        .footer-links {
            margin-top: 10px;
        }
        .footer-links a {
            margin: 0 8px;
            color: #0052cc;
            text-decoration: none;
            font-size: 13px;
        }
        .branding {
            font-size: 14px;
            font-weight: 600;
            margin-top: 10px;
        }
        .logo {
    width: 100px;
    margin-bottom: 15px;
}

    </style>
</head>
<body>
    <div class="container">
    <div class="header">
        <img src="{{ url_for('static', filename='images/logo.png') }}" alt="TradeSphere Global Logo" class="logo">

        <h1>TRADE<span style="color:#00bcd4;">SPHERE</span> GLOBAL</h1>
        <p class="tagline">Seamless Trade. Intelligent Compliance. Limitless Possibilities.</p>
    </div>


        <p>Dear Supplier,</p>
        <p>{{ message_body }}</p>

        <div class="credentials-card">
            <h3>🔐 Login Credentials</h3>
            <p><strong>Email:</strong> {{ recipient }}</p>
            <p><strong>Username:</strong> {{ cred.username }}</p>
            <p><strong>Password:</strong> {{ cred.password }}</p>
            <p><strong>Generated:</strong> {{ cred.sent_time }}</p>
            <p>👉 <a href="https://supplierdeclarations.com/" target="_blank" style="color:#0052cc;">Login to Supplier Portal</a></p>
        </div>

        <div class="cta-buttons">
            <a href="https://trade-sphereglobal.com/origin" target="_blank">🔍 Check Trade Eligibility</a>
            <a href="https://trade-sphereglobal.com" target="_blank" style="background-color:#28c76f;">🌐 Explore TradeSphere Global</a>
        </div>

        <div class="footer">
            <div class="footer-links">
                <a href="https://krislynx.com/smart-questionnaire">Smart Questionnaire</a> |
                <a href="https://krislynx.com/contact">Contact</a> |
                <a href="https://krislynx.com/privacy">Privacy Policy</a> |
                <a href="https://krislynx.com/terms">Terms of Service</a>
            </div>
            <p>📩 <a href="mailto:connect@krislynx.com">connect@krislynx.com</a> | 📞 +91 93817 57484</p>
            <p>🏢 Kurnool, Andhra Pradesh, India</p>
            <p>
                🌐 <a href="https://krislynx.com" target="_blank">www.krislynx.com</a> |
                🔗 <a href="https://linkedin.com/company/krislynx" target="_blank">Follow us on LinkedIn</a>
            </p>
            <p class="branding">✨ Building trust globally, delivering local — <strong>KrisLynx</strong><br> <em>Igniting Tomorrow’s Solutions</em></p>
        </div>
    </div>
</body>
</html>
""",  
                message_body=message_body,
                recipient=recipient,
                cred=cred
            )

        # ✅ Store session data for OAuth callback
        session['email_details'] = {
            "recipients": recipients,
            "subject": subject,
            "message_body": message_body,
            "attachments": uploaded_attachments,
            "rendered_email_templates": rendered_email_templates
        }

        # ✅ OAuth flow
        try:
            client_secret_json = os.environ.get("CLIENT_SECRET_JSON")
            if not client_secret_json:
                flash("Google OAuth credentials not found in environment.", 'danger')
                return redirect(url_for('send_email'))

            client_config = json.loads(client_secret_json)

            flow = Flow.from_client_config(
                client_config,
                scopes=SCOPES,
                redirect_uri=url_for('oauth_callback', _external=True)
            )

            auth_url, state = flow.authorization_url(prompt='consent')
            session['flow'] = {'state': state}
            return redirect(auth_url)

        except Exception as e:
            flash("OAuth Authentication failed.", 'danger')
            logger.error(f"❌ OAuth Init Error: {e}")
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
conn = psycopg2.connect(DATABASE_URL)

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import base64




from flask import request, redirect, url_for, session, flash
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import base64
import os
import json
import logging
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

@app.route('/oauth_callback')
def oauth_callback():
    logger.info("➡️ Reached /oauth_callback")

    # ✅ Step 1: Retrieve state
    state = session.get('flow', {}).get('state')
    if not state:
        flash("OAuth session state missing. Please try again.", 'danger')
        logger.warning("⚠️ Missing OAuth state.")
        return redirect(url_for('send_email'))

    try:
        # ✅ Step 2: Load client config from environment
        client_secret_json = os.environ.get("CLIENT_SECRET_JSON")
        if not client_secret_json:
            flash("OAuth credentials missing in server environment.", 'danger')
            logger.error("❌ CLIENT_SECRET_JSON not set.")
            return redirect(url_for('send_email'))

        client_config = json.loads(client_secret_json)

        # ✅ Step 3: Resume OAuth flow
        flow = Flow.from_client_config(
            client_config,
            scopes=SCOPES,
            state=state,
            redirect_uri=url_for('oauth_callback', _external=True)
        )
        flow.fetch_token(authorization_response=request.url)
        credentials = flow.credentials
        service = build('gmail', 'v1', credentials=credentials)
        logger.info("✅ Gmail API connected")

    except Exception as e:
        logger.exception("❌ OAuth flow error")
        flash("Google login failed. Try again.", 'danger')
        return redirect(url_for('send_email'))

    # ✅ Step 4: Extract session data
    email_details = session.get('email_details', {})
    recipients = email_details.get("recipients", [])
    subject = email_details.get("subject", "")
    attachments = email_details.get("attachments", [])
    rendered_templates = email_details.get("rendered_email_templates", {})

    success = []
    failed = []

    # ✅ Step 5: Loop through recipients
    for recipient in recipients:
        try:
            logger.info(f"📤 Preparing email to {recipient}")

            # Create MIME message
            message = MIMEMultipart("alternative")
            message["to"] = recipient
            message["subject"] = subject

            # HTML body
            html_content = rendered_templates.get(recipient, "")
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)

            # Attach uploaded files
            for file_path in attachments:
                try:
                    with open(file_path, "rb") as f:
                        part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
                        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                        message.attach(part)
                except Exception as file_err:
                    logger.warning(f"⚠️ Failed to attach {file_path}: {file_err}")

            # Encode and send
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            service.users().messages().send(userId="me", body={"raw": raw_message}).execute()

            logger.info(f"✅ Email sent to {recipient}")
            success.append(recipient)

        except Exception as e:
            logger.exception(f"❌ Failed to send to {recipient}")
            failed.append(f"{recipient} — {str(e)}")

    # ✅ Step 6: Flash success/failure
    if success:
        flash(f"✅ Sent to: {', '.join(success)}", 'success')
    if failed:
        flash(f"❌ Failed for: {', '.join(failed)}", 'danger')

    return redirect(url_for("dashboard"))


from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import uuid
from hmrc_lookup import lookup_commodity_details

app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/autofill', methods=['POST'])
def autofill():
    try:
        data = request.get_json(force=True)
        commodity_code = data.get("commodity_code", "").strip()

        print(f"\n📨 Auto-fill request received for code: {commodity_code}")
        if not commodity_code or len(commodity_code) != 10:
            return jsonify({"error": "Invalid commodity code"}), 400

        lookup = lookup_commodity_details(commodity_code)

        result = {
            "short_code": lookup.get("short_code", commodity_code[:4]),
            "heading": lookup.get("heading", "N/A"),
            "hmrc_description": lookup.get("hmrc_description", "N/A"),
            "duty": lookup.get("duty", "N/A"),
            "doc_path": f"/documents/{commodity_code}.pdf"  # You can customize this
        }

        print(f"✅ Autofill Result: {result}")
        return jsonify(result)

    except Exception as e:
        print("❌ Error in /autofill:", str(e))
        return jsonify({"error": "Invalid request format"}), 400

@app.route('/submitform', methods=['POST'])
def submit_form():
    data = request.form
    files = request.files
    supplier_id = data.get("supplier_id")
    username = session.get('username', 'anonymous')

    rows = zip(
        data.getlist("husq[]"),
        data.getlist("description[]"),
        data.getlist("commodity_code[]"),
        data.getlist("origin[]"),
        data.getlist("preference[]")
    )

    for i, (husq, desc, code, origin, pref) in enumerate(rows):
        lookup = lookup_commodity_details(code)
        upload_url = None

        if pref == "Yes":
            file_key = f'doc[{i}]'
            doc = files.get(file_key)

            if doc and allowed_file(doc.filename):
                filename = secure_filename(f"{uuid.uuid4()}_{doc.filename}")
                user_dir = os.path.join(app.config['UPLOAD_FOLDER'], "preference_reports", username)
                os.makedirs(user_dir, exist_ok=True)

                filepath = os.path.join(user_dir, f"{code}.pdf")
                doc.save(filepath)

                upload_url = f"/download/{username}/{code}.pdf"
            else:
                return "❌ Invalid file format. Only PDF allowed.", 400

        # INSERT INTO DB
        db.execute("""
            INSERT INTO supplier_entries (
                supplier_id, husq_part_number, description, commodity_code,
                origin, preference, short_code, heading, hmrc_description,
                duty, document_path
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            supplier_id, husq, desc, code, origin, pref,
            lookup.get("short_code", code[:4]),
            lookup.get("heading", "N/A"),
            lookup.get("hmrc_description", "N/A"),
            lookup.get("duty", "N/A"),
            upload_url
        ))

    db.commit()
    return "Entries submitted successfully"

 
@app.route('/entry/<int:supplier_id>')
def supplier_form(supplier_id):
    supplier = db.execute("SELECT * FROM supplier_demand WHERE id = %s", (supplier_id,)).fetchone()
    if not supplier:
        return "Invalid Supplier ID", 404
    return render_template("form.html", supplier_id=supplier_id)


@app.route('/view_entries/<int:supplier_id>')
def view_supplier_entries(supplier_id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM supplier_entries
        WHERE supplier_id = %s
        ORDER BY submission_time DESC
    """, (supplier_id,))
    entries = cursor.fetchall()
    return render_template("view_entries.html", entries=entries, supplier_id=supplier_id)



'''@app.route('/oauth_callback')
def oauth_callback():
    """Handles OAuth callback, sends branded emails, and logs activity."""
    try:
        if 'error' in request.args:
            flash("OAuth authorization failed. Please try again.", "danger")
            return redirect(url_for("send_email"))
6
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
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        query = "UPDATE email_logs SET status = %s WHERE id = %s"
        cursor.execute(query, (status, email_id))
        conn.commit()

    except psycopg2.Error as err:
        logger.error(f"Database update error: {err}")

    finally:
        cursor.close()
        conn.close()


 



def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

 

# Parse the DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set in environment variables")
from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
result = urlparse(DATABASE_URL)
db_config = {
    "host": result.hostname,
    "port": result.port,
    "dbname": result.path.lstrip("/"),
    "user": result.username,
    "password": result.password
}

@app.route("/")
def index():
    return render_template("index.html")

import os
from werkzeug.utils import secure_filename

@app.route("/submit", methods=["POST"])
def submit():
    if not session.get("supplier_logged_in"):
        flash("You must log in first.", "danger")
        return redirect(url_for("supplier_login"))

    username = session.get("supplier_username", "").strip()
    consent_file = request.files.get("consent")
    commodity_link = request.form.get("commodity_link")

    consent_filename = None
    if consent_file:
        consent_filename = secure_filename(consent_file.filename)
        upload_path = os.path.join(app.config["UPLOAD_FOLDER"], consent_filename)
        consent_file.save(upload_path)

    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()

        # ✅ Update supplier_demand
        cur.execute("""
            UPDATE supplier_demand
            SET consent = %s, commodity_link = %s
            WHERE username = %s
        """, (consent_filename, commodity_link, username))

        # ✅ Update email_logs
        print("Updating email_logs for:", username)
        print("PDF file:", consent_filename)
        print("Form link:", commodity_link)

        cur.execute("""
            UPDATE email_logs
            SET pdf_link = %s, form_link = %s
            WHERE username = %s
        """, (consent_filename, commodity_link, username))

        print("Rows affected in email_logs:", cur.rowcount)

        conn.commit()
        cur.close()
        conn.close()
        flash("Documents updated successfully!", "success")
    except Exception as e:
        flash(f"Error saving: {e}", "danger")

    return redirect(url_for("supplier_portal"))


# --------- SUPPLIER UPLOAD ---------
@app.route('/supplier_upload', methods=['GET', 'POST'])
def supplier_upload():
    if 'supplier_user' not in session:
        return redirect(url_for('supplier_login'))

    if request.method == 'POST':
        file = request.files['file']
        if file:
            upload_folder = 'uploads'
            os.makedirs(upload_folder, exist_ok=True)
            filepath = os.path.join(upload_folder, file.filename)
            file.save(filepath)
            flash('File uploaded successfully!', 'success')

    return render_template('upload.html', username=session['supplier_user'])


 

# Main
if __name__ == '__main__':
    app.run(debug=True)