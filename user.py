# User Model
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# This is a placeholder for the db instance. It will be initialized in main.py
# from main import db
# However, to avoid circular imports during model definition, we define it as SQLAlchemy()
# and it will be properly initialized and linked in main.py

# Check if db is already defined (e.g. by a test runner or another import)
if 'db' not in globals():
    db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False) # Increased length for stronger hashes
    full_name = db.Column(db.String(100), nullable=True)
    # Add other fields as necessary, e.g., phone_number, roles
    # role = db.Column(db.String(50), default='user', nullable=False) # e.g., user, agent, admin

    # Relationships (example)
    # listings = db.relationship('Listing', backref='agent', lazy=True)

    def __init__(self, email, password, full_name=None):
        self.email = email.lower()
        self.set_password(password)
        self.full_name = full_name

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'full_name': self.full_name
            # Do not include password_hash in to_dict responses
        }

