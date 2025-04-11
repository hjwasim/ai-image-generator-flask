from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from .image_generation.image_generation import image_gen_bp
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SECRET_KEY'] = 'priya#123$yoga'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yogapriya.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    
    app.config['JWT_SECRET_KEY'] = 'kln_!1234!_priya'
    
    jwt = JWTManager(app)
    
    from .auth.auth import auth_bp
    from .user.user import user_bp
    
    db.init_app(app)    

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(image_gen_bp, url_prefix='/image')
    # app.register_blueprint(voice_bp, url_prefix='/voice') --- TODO
    app.register_blueprint(user_bp, url_prefix='/user')
    
    with app.app_context():
        db.create_all()
    
    return app
