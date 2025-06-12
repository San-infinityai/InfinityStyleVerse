from flask import Flask 
from .database import db
from .config import Config
from flask_jwt_extended import JWTManager
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

    from .routes.auth_routes import auth_bp
    from .routes.product_routes import product_bp
    from .routes.main import main_bp
    from .routes.feedback_routes import feedback_bp
    from .routes.recommendation_routes import recommendation_bp  

    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(main_bp) 
    app.register_blueprint(feedback_bp)
    app.register_blueprint(recommendation_bp)  

    return app
