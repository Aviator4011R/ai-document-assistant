import os
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from routes.document import document_bp
from routes.voice import voice_bp

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app, origins=['*'])

# Register blueprints
app.register_blueprint(document_bp, url_prefix='/api/document')
app.register_blueprint(voice_bp, url_prefix='/api/voice')

@app.route('/')
def serve_frontend():
    """Serve the React frontend"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    """Serve static files (CSS, JS, images, etc.)"""
    try:
        return send_from_directory(app.static_folder, path)
    except:
        # If file not found, serve index.html for client-side routing
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'AI Document Assistant API is running'
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors by serving the frontend"""
    return send_from_directory(app.static_folder, 'index.html')

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'message': 'Something went wrong on our end'
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)

