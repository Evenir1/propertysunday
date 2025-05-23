import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify # Added jsonify
from flask_cors import CORS # Import CORS
from flask_jwt_extended import JWTManager # Import JWTManager

from src.models.user import db # Assuming db is initialized in user.py or a shared models.py
from src.routes.user import user_bp
from src.routes.auth import auth_bp # Import auth blueprint
from src.routes.listing import listing_bp # Import listing blueprint
from src.routes.payment import payment_bp # Import payment blueprint
from src.routes.advertisement import advertisement_bp # Import advertisement blueprint

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configuration
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'default_super_secret_key_for_dev_!@#$%^&*()')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'default_jwt_secret_key_for_dev_!@#$%^&*()') # For JWT

# Initialize extensions
CORS(app) # Enable CORS for all routes
jwt = JWTManager(app) # Initialize JWT

# Register Blueprints
app.register_blueprint(user_bp, url_prefix='/api/users') # Changed prefix for clarity
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(listing_bp, url_prefix='/api/listings') # Changed prefix for consistency
app.register_blueprint(payment_bp, url_prefix='/api/payments') 
app.register_blueprint(advertisement_bp, url_prefix='/api/advertisements') # Added advertisement blueprint

# Database Configuration
DB_USERNAME = 'propsundayuser'
DB_PASSWORD = 'f22adada45a6e5426994cdeb06c01583' # Retrieved from db_credentials.txt
DB_HOST = 'localhost'
DB_PORT = '3307' # Updated port
DB_NAME = 'propertysunday'
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create database tables if they don't exist
with app.app_context():
    db.create_all()
    # Link the db.session to the placeholder in listing.py, payment.py and advertisement.py for standalone script execution simulation
    # This is a HACK for the current placeholder setup and should NOT be in production code.
    # In a real app, db would be imported directly into those files from this initialized instance.
    if hasattr(sys.modules.get('src.routes.listing'), 'db_placeholder'):
        sys.modules['src.routes.listing'].db_placeholder.session = db.session
        sys.modules['src.routes.listing'].Listing.query = db.session.query_property()
        sys.modules['src.routes.listing'].User.query = db.session.query_property()

    if hasattr(sys.modules.get('src.routes.payment'), 'db_placeholder'):
        sys.modules['src.routes.payment'].db_placeholder.session = db.session
        sys.modules['src.routes.payment'].Listing.query = db.session.query_property()
        sys.modules['src.routes.payment'].User.query = db.session.query_property()
        
    if hasattr(sys.modules.get('src.routes.advertisement'), 'db_placeholder'):
        sys.modules['src.routes.advertisement'].db_placeholder.session = db.session
        sys.modules['src.routes.advertisement'].Advertisement.query = db.session.query_property()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            # Fallback for API routes if not serving static files
            if path.startswith("api/"):
                 return jsonify({"message": "API endpoint not found. Please check the URL."}), 404
            return "index.html not found and not an API route", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

