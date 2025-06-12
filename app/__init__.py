from flask import Flask 
from app.database import db
from app.config import Config
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

    from app.routes.auth import auth_bp
    from app.routes.product_routes import product_bp
    from app.routes.main import main_bp 
    from app.routes.feedback_routes import feedback_bp 



    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(main_bp) 
    app.register_blueprint(feedback_bp)
    # with app.app_context():
    #     db.create_all()

    return app
