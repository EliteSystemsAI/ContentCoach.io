from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
import os
from dotenv import load_dotenv
from app.models import db, User
from app.chat_handler import generate_content
import json

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__,
           template_folder='/workspaces/ContentCoach.io/app/templates',
           static_folder='/workspaces/ContentCoach.io/app/static')

# Configure Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////workspaces/ContentCoach.io/content_coach.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-key-change-in-production')

# Initialize database
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('chat_page'))
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    
    data = request.get_json()
    
    try:
        print("Received signup data:", data)
        if not data:
            print("No JSON data received")
            return jsonify({"success": False, "error": "No data provided"}), 400
            
        required_fields = ['email', 'password', 'name', 'business_niche', 'content_goals']
        for field in required_fields:
            if field not in data:
                print(f"Missing required field: {field}")
                return jsonify({"success": False, "error": f"Missing required field: {field}"}), 400
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({"success": False, "error": "Email already registered"}), 400
        
        user = User(
            email=data['email'],
            name=data['name'],
            business_niche=data['business_niche'],
            content_goals=data['content_goals']
        )
        user.set_password(data['password'])
        
        print("Created user object:", user)
        
        db.session.add(user)
        print("Added user to session")
        
        db.session.commit()
        print("Committed to database")
        
        session['user_id'] = user.id
        print("Added user_id to session:", user.id)
        
        return jsonify({"success": True})
    except Exception as e:
        print(f"Error creating user: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print("Traceback:", traceback.format_exc())
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            return render_template('login.html', error="Please fill in all fields")
        
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return render_template('login.html', error="Invalid email or password")
        
        session['user_id'] = user.id
        return redirect(url_for('chat_page'))
        
    except Exception as e:
        print(f"Login error: {str(e)}")
        return render_template('login.html', error="An error occurred. Please try again.")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/chat')
@login_required
def chat_page():
    user = db.session.get(User, session['user_id'])
    if not user:
        session.clear()
        return redirect(url_for('login'))
    
    return render_template('chat.html', user=user)

@app.route('/chat', methods=['POST'])
@login_required
def chat():
    try:
        user = db.session.get(User, session['user_id'])
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        user_message = request.form.get('message')
        if not user_message:
            raise ValueError("No message provided")
        
        print(f"Received message from {user.name}: {user_message}")
        
        print("Attempting to call OpenAI API...")
        ai_response = generate_content(user, user_message)
        print(f"Received response from OpenAI: {ai_response[:100]}...")
        
        if ai_response.startswith("An error occurred:"):
            return jsonify({"error": ai_response}), 500
            
        return jsonify({"response": ai_response})
        
    except Exception as e:
        error_message = f"Server Error: {str(e)}"
        print(f"Server Error details: {error_message}")
        return jsonify({"error": error_message}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)
