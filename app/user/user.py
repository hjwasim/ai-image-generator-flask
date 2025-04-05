from flask import Blueprint, request, jsonify
from .models import db, UserPrompt

user_bp = Blueprint('user', __name__)

@user_bp.route('/track_prompt', methods=['POST'])
def track_prompt():
    username = request.json.get('username')
    prompt = request.json.get('prompt')
    
    if not username or not prompt:
        return jsonify({"msg": "Username and prompt are required"}), 400
    
    try:
        new_prompt = UserPrompt(username=username, prompt=prompt)
        db.session.add(new_prompt)
        db.session.commit()
        return jsonify({"msg": "Prompt tracked successfully"}), 201
    except Exception as e:
        return jsonify({"msg": "Error tracking prompt", "error": str(e)}), 500

@user_bp.route('/get_prompts/<username>', methods=['GET'])
def get_prompts_by_username(username):
    try:
        prompts = UserPrompt.query.filter_by(username=username).all()
        
        prompt_list = [{'id': prompt.id, 'prompt': prompt.prompt} for prompt in prompts]
        
        return jsonify(prompts=prompt_list), 200
    except Exception as e:
        return jsonify({"msg": "Error retrieving prompts", "error": str(e)}), 500