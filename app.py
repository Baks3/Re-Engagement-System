
from flask import Flask, jsonify
from pipedrive_api import get_deals, get_person, get_notes, add_note
from message_generator import generate_email, detect_objection
from email_sender import send_email
import datetime

app = Flask(__name__)

@app.route('/generate-emails', methods=['GET'])
def generate_emails():
    results = []
    deals = get_deals(10)

    if not deals:
        return "❌ No deals retrieved from Pipedrive or an error occurred.", 500
    
    for deal in deals:
        person = get_person(deal["person_id"]["value"])
        notes = get_notes(deal["id"])
        notes_text = " ".join(note["content"] for note in notes) if notes else ""
        objection = detect_objection(notes_text)

        lead_info = {
            "name": person["name"],
            "email": person["email"][0]["value"],
            "last_contacted": deal.get("last_activity_date", "Unknown"),
            "status": deal["status"],
            "notes": notes_text,
            "objection": objection if objection != "No objection" else None
        }

        email_body = generate_email(lead_info)
        subject = f"Hey {lead_info['name']}, just checking in"
        sent = send_email(lead_info["email"], subject, email_body)
        add_note(deal["id"], f"Re-engagement email sent to {lead_info['email']} on {datetime.date.today()}")

        results.append({"to": lead_info["email"], "subject": subject, "sent": sent, "body": email_body})

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)