from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask import Blueprint, request, jsonify
from .models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"msg": "Username already exists"}), 400
    
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"msg": "Email already exists"}), 400
    
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"msg": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return jsonify({"msg": "Invalid username or password"}), 401
    
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@auth_bp.route('/change_password', methods=['POST'])
@jwt_required()
def change_password():
    current_user = get_jwt_identity()
    current_password = request.json.get('current_password')
    new_password = request.json.get('new_password')

    user = User.query.filter_by(username=current_user).first()

    if user is None or not user.check_password(current_password):
        return jsonify({"msg": "Current password is incorrect"}), 401

    if not new_password:
        return jsonify({"msg": "New password must be provided"}), 400

    user.set_password(new_password)
    db.session.commit()

    return jsonify({"msg": "Password updated successfully"}), 200