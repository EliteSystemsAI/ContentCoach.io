# ContentCoach.io

An AI-powered content coaching platform that provides personalized content strategy advice based on your business niche and goals.

## Features

- User authentication and account management
- Personalized content coaching based on your business niche
- Interactive chat interface with GPT-3.5
- Goal-oriented content strategy advice
- Secure user session management
- Modern, responsive UI with Tailwind CSS

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Node.js and npm (for Tailwind CSS)
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ContentCoach.io.git
cd ContentCoach.io
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install Node.js dependencies and build CSS:
```bash
npm install
npm run build
```

4. Create a `.env` file in the root directory with your OpenAI API key and Flask secret key:
```
OPENAI_API_KEY=your_openai_api_key_here
FLASK_SECRET_KEY=your_secret_key_here
```

## Running the Application

1. Start the Tailwind CSS compiler in watch mode (in a separate terminal):
```bash
npm run build-css
```

2. Start the Flask development server:
```bash
python app.py
```

3. Open your web browser and navigate to:
```
http://localhost:5001
```

4. Create an account or login:
   - Sign up with your email and password
   - Complete your profile with:
     - Your name
     - Business niche
     - Content goals
   - Or login with your existing account

5. Start chatting with your AI content coach!

## Security Features

- Secure password hashing using Werkzeug
- Email validation and unique email enforcement
- Protected routes with login_required decorator
- Session-based authentication

## Running Tests

Run the test suite using pytest:
```bash
pytest
```

This will run both unit tests and integration tests, including:
- Chat handler tests
- Route tests
- API integration tests

## Development

The application structure:
```
ContentCoach.io/
├── app/
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   ├── templates/
│   ├── chat_handler.py
│   ├── models.py
│   └── routes.py
├── tests/
├── app.py
└── requirements.txt
```

## Troubleshooting

1. If you encounter database errors, try deleting the `content_coach.db` file and restart the application - it will be recreated automatically.

2. If you get OpenAI API errors:
   - Verify your API key is correct in the `.env` file
   - Check your API usage limits
   - Run `python test_openai.py` to test the API connection

3. For any other issues, check the Flask development server output for error messages.
