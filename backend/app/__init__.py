import os
from flask import Flask, request, send_from_directory
from .database import db
from .models import RequestLog
from .config import Config
from flask_jwt_extended import JWTManager, get_jwt_identity, verify_jwt_in_request
from flask_cors import CORS  
from flask_migrate import Migrate 

migrate = Migrate()

def create_app():
    base_dir = os.path.dirname(os.path.abspath(__file__))  # backend\app
    template_folder = os.path.join(base_dir, '..', '..', 'Frontend', 'templates')
    static_folder = os.path.join(base_dir, '..', '..', 'Frontend', 'assets')

    app = Flask(
        __name__,
        template_folder=template_folder,
        static_folder=static_folder
    )

    app.config.from_object(Config)

    CORS(app)  
    db.init_app(app)
    migrate.init_app(app, db) 
    jwt = JWTManager(app)

    # Add route to serve scripts folder
    @app.route('/scripts/<path:filename>')
    def serve_scripts(filename):
        scripts_dir = os.path.join(base_dir, '..', '..', 'Frontend', 'scripts')
        return send_from_directory(scripts_dir, filename)

    @app.before_request
    def log_request():
        user_id = None
        try:
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
        except Exception:
            pass

        log = RequestLog(
            user_id=user_id,
            endpoint=request.path
        )
        db.session.add(log)
        db.session.commit()

    # Import and register blueprints
    from .routes.auth_routes import auth_bp
    from .routes.product_routes import product_bp
    from .routes.main import main_bp
    from .routes.feedback_routes import feedback_bp
    from .routes.recommendation_routes import recommendation_bp 
    from .routes.admin_routes import admin_bp
  
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(main_bp) 
    app.register_blueprint(feedback_bp)
    app.register_blueprint(recommendation_bp)  

    with app.app_context():
        db.create_all()

    return app
