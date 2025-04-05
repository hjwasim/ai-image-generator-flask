from flask import Blueprint, request, jsonify
import openai

image_gen_bp = Blueprint('image_generation', __name__)

# Configure OpenAI API key
openai.api_key = 'fake_key'

@image_gen_bp.route('/generate_image', methods=['POST'])
def generate_image():
    prompt = request.json.get('prompt')
    if not prompt:
        return jsonify({"msg": "Prompt is required"}), 400

    try:
        response = openai.images.generate(prompt=prompt, n=1, size="512x512", response_format='url')
        image_url = response.data[0].url
        return jsonify({image_url:image_url, 'used_prompt': prompt})
    
    except Exception as e:
        return jsonify({"msg": "Error generating image", "error": str(e)}), 500
