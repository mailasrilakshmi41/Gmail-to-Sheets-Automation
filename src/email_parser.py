import base64

def parse_email(message):
    """
    Extracts the Sender, Subject, Date, and plain text Body from a Gmail message object.
    """
    payload = message.get('payload', {})
    headers = payload.get('headers', [])

    # simple helper to find header values
    def get_header(name):
        for h in headers:
            if h['name'].lower() == name.lower():
                return h['value']
        return "Unknown"

    # Extract Metadata
    sender = get_header("From")
    subject = get_header("Subject")
    date = get_header("Date")
    
    # Extract Body (looking for text/plain)
    body = " (No plain text content found) "
    
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data')
                if data:
                    body = base64.urlsafe_b64decode(data).decode('utf-8')
                    break # Found the text, stop looking
    else:
        # Fallback for simple emails with no parts
        data = payload.get('body', {}).get('data')
        if data:
            body = base64.urlsafe_b64decode(data).decode('utf-8')

    # Return the exact dictionary structure needed for our Sheet
    return {
        "From": sender,
        "Subject": subject,
        "Date": date,
        "Content": body.strip()
    }