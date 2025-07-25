import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("PIPEDRIVE_API_TOKEN")
BASE_URL = "https://api.pipedrive.com/v1"

# Debugging: Show a portion of the API token to confirm it's loaded
print("🔑 Loaded Pipedrive API Token:", API_TOKEN[:4] + "..." if API_TOKEN else "❌ Token NOT loaded!")

def get_deals(limit=100):
    url = f"{BASE_URL}/deals?limit={limit}&api_token={API_TOKEN}"
    print(f"🌐 Requesting deals from: {url}")

    try:
        res = requests.get(url)
        if res.status_code != 200:
            print(f"❌ Failed to fetch deals! Status code: {res.status_code}")
            print("Response:", res.text)
            return []

        deals = res.json().get("data", [])
        if not deals:
            print("✅ Connected, but no deals returned from Pipedrive.")
        else:
            print(f"✅ Retrieved {len(deals)} deals from Pipedrive.")
        return deals
    except Exception as e:
        print(f"🚨 Exception occurred while fetching deals: {e}")
        return []

def get_person(person_id):
    url = f"{BASE_URL}/persons/{person_id}?api_token={API_TOKEN}"
    res = requests.get(url)
    return res.json().get("data", {})

def get_notes(deal_id):
    url = f"{BASE_URL}/notes?deal_id={deal_id}&api_token={API_TOKEN}"
    res = requests.get(url)
    return res.json().get("data", [])

def add_note(deal_id, content):
    url = f"{BASE_URL}/notes?api_token={API_TOKEN}"
    payload = {"content": content, "deal_id": deal_id}
    res = requests.post(url, json=payload)
    return res.status_code == 201
