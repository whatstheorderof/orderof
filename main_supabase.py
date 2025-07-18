import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
import logging

# Import Supabase routes
from src.routes.supabase_franchise import supabase_franchise_bp
from src.routes.supabase_affiliate import supabase_affiliate_bp
from src.routes.supabase_sync import supabase_sync_bp

# Import legacy routes (keep for compatibility)
from src.routes.user import user_bp
from src.routes.franchise import franchise_bp
from src.routes.sync import sync_bp
from src.routes.affiliate import affiliate_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for all routes
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Register Supabase blueprints (new primary routes)
app.register_blueprint(supabase_franchise_bp, url_prefix='/api')
app.register_blueprint(supabase_affiliate_bp, url_prefix='/api')
app.register_blueprint(supabase_sync_bp, url_prefix='/api')

# Register legacy blueprints (for backward compatibility)
app.register_blueprint(user_bp, url_prefix='/api/legacy')
app.register_blueprint(franchise_bp, url_prefix='/api/legacy')
app.register_blueprint(sync_bp, url_prefix='/api/legacy')
app.register_blueprint(affiliate_bp, url_prefix='/api/legacy')

@app.route('/api/health')
def health_check():
    return jsonify({'status': 'healthy', 'backend': 'supabase'})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return jsonify({'message': 'OrderOf.org API with Supabase - Ready!'}), 200

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return jsonify({'message': 'OrderOf.org API with Supabase - Ready!'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

