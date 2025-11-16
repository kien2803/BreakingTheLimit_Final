from flask import Flask, jsonify
from flask_cors import CORS
from config import config
from models import db, User, Journal, DailyMessage
from routes.auth import auth_bp
from routes.journal import journal_bp
from routes.family import family_bp
from routes.admin import admin_bp
from routes.ai_analysis import ai_bp
from datetime import datetime
import os

def create_app(config_name='development'):
    """Create and configure Flask app"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    CORS(app)
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(journal_bp, url_prefix='/api')
    app.register_blueprint(family_bp, url_prefix='/api/family')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')
    
    # Activities routes
    @app.route('/api/activities/message/today', methods=['GET'])
    def get_daily_message():
        """Get today's daily message"""
        today = datetime.utcnow().date()
        message = DailyMessage.query.filter_by(
            display_date=today,
            status='published'
        ).first()
        
        if not message:
            # Fallback to latest published message
            message = DailyMessage.query.filter_by(status='published')\
                .order_by(DailyMessage.display_date.desc()).first()
        
        if message:
            return jsonify(message.to_dict())
        else:
            # Default message
            return jsonify({
                'id': 0,
                'message': 'Hít thật sâu, thở ra từ từ, bạn xứng đáng được bình yên.',
                'author': 'Breaking The Limits',
                'date': today.isoformat()
            })
    
    # Create tables
    with app.app_context():
        db.create_all()
        # Create default admin if not exists
        if not User.query.filter_by(email='admin@btl.com').first():
            admin = User(
                name='Admin User',
                email='admin@btl.com',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
    
    # Health check
    @app.route('/api/health', methods=['GET'])
    def health():
        try:
            # Count actual tables in database
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            table_count = len(inspector.get_table_names())
            
            return jsonify({
                'status': 'healthy',
                'database': 'connected',
                'tables': table_count,
                'models_loaded': len(db.metadata.tables)
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'database': 'disconnected',
                'error': str(e)
            }), 500
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

if __name__ == '__main__':
    try:
        app = create_app()
        print("=" * 50)
        print("Breaking The Limits Backend Server")
        print("=" * 50)
        print("Server running at: http://localhost:5000")
        print("API Health: http://localhost:5000/api/health")
        print("Press CTRL+C to stop the server")
        print("=" * 50)
        app.run(debug=True, port=5000, host='0.0.0.0')
    except Exception as e:
        print(f"Error starting server: {e}")
        print("\nPlease make sure:")
        print("1. All dependencies are installed: pip install -r requirements.txt")
        print("2. Database is initialized: python init_db.py")
        import traceback
        traceback.print_exc()
