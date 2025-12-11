import csv
from pipedrive_api import get_deals, get_person, get_notes
from message_generator import generate_email, detect_objection

def export_to_csv():
    with open("pilot_output.csv", mode="w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Contact Name", "Email", "Subject Line", "Generated Message", "Confidence Score", "Sent?", "Needs Edit?", "Notes"])

        deals = get_deals(10)
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
            subject_line = f"Hey {lead_info['name']}, just checking in"

            writer.writerow([
                lead_info["name"],
                lead_info["email"],
                subject_line,
                email_body,
                "High",  
                "No",     
                "",      
                ""
            ])

def mark_email_sent(contact_email):
    rows = []
    with open("pilot_output.csv", newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["Email"] == contact_email:
                row["Sent?"] = "Yes"
            rows.append(row)

    with open("pilot_output.csv", "w", newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(rows)

if __name__ == "__main__":
    export_to_csv()
    print("Export complete: pilot_output.csv")