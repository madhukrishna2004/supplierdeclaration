from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()

# Stores responses submitted by suppliers
class SupplierResponse(db.Model):
    __tablename__ = 'supplier_responses'
    id = db.Column(db.Integer, primary_key=True)
    recipient_email = db.Column(db.String(120), nullable=False)
    excel_file = db.Column(db.String(120), nullable=False)
    pdf_file = db.Column(db.String(120), nullable=False)
    submitted_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    username = db.Column(db.String(150), nullable=False)  # Scoped to logged-in user


# Logs every email sent via the portal
class EmailLog(db.Model):
    __tablename__ = 'email_logs'
    id = db.Column(db.Integer, primary_key=True)
    recipient = db.Column(db.String, nullable=False)
    subject = db.Column(db.String, nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    username = db.Column(db.String(150), nullable=False)  # Scoped to logged-in user


class ContactGroup(db.Model):
    __tablename__ = 'contact_groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 👈 required

# Individual contacts in a group
class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('contact_groups.id'), nullable=False)
    username = db.Column(db.String(150), nullable=False)  # Scoped to logged-in user
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)