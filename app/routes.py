from flask import Blueprint, render_template, request, jsonify
from .chat_handler import generate_content

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('input')
    response = generate_content(user_input)
    return jsonify({'response': response})
