import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
print(f"Testing OpenAI API connection...")
print(f"API Key found: {'Yes' if api_key else 'No'}")
print(f"API Key length: {len(api_key) if api_key else 0}")
print(f"API Key starts with: {api_key[:10]}... ends with: ...{api_key[-10:]}")

try:
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello!"}
        ]
    )
    print("\nAPI Test successful!")
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print("\nAPI Test failed!")
    print(f"Error: {str(e)}")
