# message_generator.py (Gemini API version)
import os
from google import genai
from google.genai import types 
from dotenv import load_dotenv

load_dotenv()

# The client will automatically pick up the GEMINI_API_KEY environment variable 
# (which you must add to your .env file).
client = None
try:
    client = genai.Client() 
except Exception as e:
    # This will catch errors if the API key is missing or invalid.
    print(f"❌ Failed to initialize Gemini Client. Make sure GEMINI_API_KEY is set in your .env file: {e}")

# Using gemini-2.5-flash for fast, high-quality text generation
MODEL = "gemini-2.5-flash" 

def generate_gemini_response(prompt: str) -> str:
    if not client:
        return "⚠️ Gemini client not initialized. Check GEMINI_API_KEY."

    try:
        # Configuration for consistent, sales-focused responses
        config = types.GenerateContentConfig(
            # System instruction can improve model consistency for a specific task
            system_instruction="You are a helpful, professional sales assistant.",
            # Lower temperature for less creative, more focused responses
            temperature=0.2 
        )

        # Use generate_content for a single prompt-response turn
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=config
        )
        return response.text.strip()
    except Exception as e:
        print(f"❌ Gemini generation error: {e}")
        return "⚠️ Failed to generate response"

def detect_objection(notes_summary):
    prompt = f"""
Identify the primary sales objection from the notes below.

Here are the notes from the last conversation:
\"\"\"{notes_summary}\"\"\"

Classify the objection using only one of the following exact categories:
- No objection
- Pricing
- Timing
- Not a fit
- Already using a competitor
- Lack of budget
- Needs more info
"""
    # Use the new generalized generation function
    return generate_gemini_response(prompt)

def generate_email(lead_info):
    # IMPORTANT: Replace the bracketed placeholders with your actual details
    my_name = "Tsepang Mabizela" 
    my_title = "Sales Manager" 
    
    prompt = f"""
Draft a re-engagement email.

Lead Name: {lead_info['name']}
Last Contacted: {lead_info['last_contacted']}
Deal Status: {lead_info['status']}
Summary of Notes: {lead_info['notes']}
Objection: {lead_info.get('objection', 'None')}
Product Name: {lead_info.get('product_name', 'our product')}
My Name: {my_name}
My Title: {my_title}

The email must be:
- Friendly and professional.
- Include a clear Call to Action (CTA), e.g., "Book a quick 15-minute call on my calendar link."
- Reference the Product Name in the body.
- End with "Kind regards" and My Name/Title on a new line.

Do NOT include a subject line or any header. Only provide the body of the email.
"""
    # Use the new generalized generation function
    return generate_gemini_response(prompt)