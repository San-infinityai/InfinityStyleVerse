from flask import Flask, request
from .database import db
from .models import RequestLog
from .config import Config
from flask_jwt_extended import JWTManager, get_jwt_identity, verify_jwt_in_request
from flask_cors import CORS  
from flask_migrate import Migrate 

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)  
    db.init_app(app)
    migrate.init_app(app, db) 
    jwt = JWTManager(app)

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

    # Import blueprints using relative import
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
