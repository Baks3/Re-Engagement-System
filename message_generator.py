# message_generator.py (Ollama version)
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"

def generate_ollama_response(prompt: str) -> str:
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        })
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except requests.exceptions.RequestException as e:
        print(f"❌ Ollama generation error: {e}")
        return "⚠️ Failed to generate response"

def detect_objection(notes_summary):
    prompt = f"""
You are a helpful assistant that identifies objections from sales notes.

Here are the notes from the last conversation:
\"\"\"{notes_summary}\"\"\"

Classify whether there's an objection. If so, state the category:
- No objection
- Pricing
- Timing
- Not a fit
- Already using a competitor
- Lack of budget
- Needs more info
"""
    return generate_ollama_response(prompt)

def generate_email(lead_info):
    prompt = f"""
You are a sales assistant. Draft a re-engagement email using the info below.

Lead Name: {lead_info['name']}
Last Contacted: {lead_info['last_contacted']}
Deal Status: {lead_info['status']}
Summary of Notes: {lead_info['notes']}
Objection: {lead_info.get('objection', 'None')}
Product Name: {lead_info.get('product_name', 'our product')}

The email should include:
- Friendly, professional tone
- A clear CTA (e.g., Book a call)
- Include the product or service name from pipedrive
- A closing signature like "Kind regards" and use my full names from pipedrive
- Do NOT include a subject line or any header. Only provide the body of the email.

Do NOT include a subject line or any header. Only provide the body of the email.
"""
    return generate_ollama_response(prompt)
