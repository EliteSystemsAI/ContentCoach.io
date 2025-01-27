import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_content(user, user_input):
    """
    Generate content using OpenAI's chat completion API.
    
    Args:
        user: User object containing name, business_niche, and content_goals
        user_input: String containing the user's message
        
    Returns:
        String containing the AI's response
    """
    try:
        # Create a personalized system message based on user data
        system_message = (
            f"You are a helpful content coach specializing in {user.business_niche}. "
            f"Your client is {user.name}, who wants to {user.content_goals}. "
            f"Provide specific, actionable advice tailored to their niche and goals. "
            f"Focus on practical strategies that can help them achieve their content objectives.\n\n"
            f"Format your responses with:\n"
            f"- Clear paragraphs separated by blank lines\n"
            f"- Bullet points for lists and steps (use - or • symbols)\n"
            f"- Short, focused paragraphs for readability\n"
            f"- No markdown or special formatting symbols\n"
            f"- Natural, conversational tone"
        )
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_input}
            ]
        )
        
        if not response.choices:
            raise ValueError("No response choices returned from OpenAI")
            
        return response.choices[0].message.content
        
    except Exception as e:
        return f"An error occurred: {str(e)}"
