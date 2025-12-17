import os
import json
from flask import Flask
from flask_cors import CORS
from firebase_admin import credentials, firestore, initialize_app, _apps
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
    initialize_firebase(app)
    from .routes.upload import upload_bp
    from .routes.search import search_bp
    from .routes.save import save_bp
    from .routes.history import history_bp
    from .routes.dcma import dcma_bp
    app.register_blueprint(upload_bp, url_prefix="/api/upload")
    app.register_blueprint(search_bp, url_prefix="/api/search")
    app.register_blueprint(save_bp, url_prefix="/api/save")
    app.register_blueprint(history_bp, url_prefix="/api/history")
    app.register_blueprint(dcma_bp, url_prefix='/api/dcma')
    return app

def initialize_firebase(app):
    if not _apps:
        firebase_config = app.config.get("FIREBASE_CONFIG", '{"type":"service_account","project_id":"example-project","private_key_id":"EXAMPLE_KEY_ID","private_key":"-----BEGIN PRIVATE KEY-----\\nEXAMPLE\\n-----END PRIVATE KEY-----\\n","client_email":"firebase-adminsdk@example.iam.gserviceaccount.com","client_id":"EXAMPLE_CLIENT_ID","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url":"https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk"}')
        cred = credentials.Certificate(json.loads(firebase_config))
        initialize_app(cred)
    app.db = firestore.client()
    app.app_id = app.config.get("id", "ex_id")
