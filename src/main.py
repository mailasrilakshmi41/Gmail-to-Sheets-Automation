import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.gmail_service import get_gmail_service
from src.sheets_service import append_to_sheet
from src.email_parser import parse_email
from config import STATE_FILE

def get_processed_ids():
    if not os.path.exists(STATE_FILE):
        return set()
    with open(STATE_FILE, 'r') as f:
        return set(line.strip() for line in f)

def save_processed_id(msg_id):
    with open(STATE_FILE, 'a') as f:
        f.write(f"{msg_id}\n")

def main():
    print("--- 1. STARTING SCRIPT ---")
    
    # Authenticate
    try:
        # CAPTURE BOTH VARIABLES
        service, creds = get_gmail_service()
        print("SUCCESS: Gmail Service Connected.")
    except Exception as e:
        print(f"CRITICAL ERROR: Login failed. {e}")
        return

    processed_ids = get_processed_ids()
    
    # Search for emails
    print("--- 2. SEARCHING FOR EMAILS ---")
    results = service.users().messages().list(
        userId='me', 
        q='is:unread' 
    ).execute()
    
    messages = results.get('messages', [])

    if not messages:
        print("RESULT: No unread emails found.")
        return

    print(f"SUCCESS: Found {len(messages)} unread emails.")

    for msg in messages[:5]:
        msg_id = msg['id']

        if msg_id in processed_ids:
            print(f"Skipping duplicate: {msg_id}")
            continue

        print(f"\nProcessing Email ID: {msg_id}")
        
        # Fetch content
        full_msg = service.users().messages().get(userId='me', id=msg_id).execute()
        email_data = parse_email(full_msg)
        
        print(f" -> Subject: {email_data['Subject']}")
        
        # Write to Sheets
        try:
            # USE THE 'creds' VARIABLE WE CAPTURED EARLIER
            append_to_sheet(creds, email_data)
            print(" -> Written to Sheets: YES")
        except Exception as e:
            print(f" -> Written to Sheets: FAILED ({e})")
            print("CHECK YOUR config.py SPREADSHEET_ID!")
            return

        # Mark as Read
        service.users().messages().modify(
            userId='me', 
            id=msg_id, 
            body={'removeLabelIds': ['UNREAD']}
        ).execute()
        print(" -> Marked as Read: YES")

        save_processed_id(msg_id)

    print("\n--- DONE ---")

if __name__ == '__main__':
    main()