import os
import sys
# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.document import document_bp
from src.routes.voice import voice_bp
from src.routes.poh import poh_bp

def create_app():
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'asdf#FGSgvasgf$5$WGT')

    # Enable CORS for all routes
    CORS(app, origins="*")

    # Register blueprints
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(document_bp, url_prefix='/api/document')
    app.register_blueprint(voice_bp, url_prefix='/api/voice')
    app.register_blueprint(poh_bp, url_prefix='/api/poh')

    # Database setup
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    # Create database directory if it doesn't exist
    os.makedirs(os.path.join(os.path.dirname(__file__), 'database'), exist_ok=True)
    
    with app.app_context():
        db.create_all()
    
    # Serve frontend static files
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')
    
    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

