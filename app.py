
from flask import Flask, render_template, request
import openai
import os

app = Flask(__name__, template_folder='app/templates')

# Load OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['message']
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Supported OpenAI model
            messages=[
                {"role": "system", "content": "You are a helpful content coach."},
                {"role": "user", "content": user_message}
            ]
        )
        ai_response = response['choices'][0]['message']['content']
        return {"response": ai_response}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    app.run(debug=True)
