import base64

def parse_email(message):
    """
    Extracts the Sender, Subject, Date, and plain text Body from a Gmail message object.
    """
    payload = message.get('payload', {})
    headers = payload.get('headers', [])


    def get_header(name):
        for h in headers:
            if h['name'].lower() == name.lower():
                return h['value']
        return "Unknown"


    sender = get_header("From")
    subject = get_header("Subject")
    date = get_header("Date")
    

    body = " (No plain text content found) "
    
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data')
                if data:
                    body = base64.urlsafe_b64decode(data).decode('utf-8')
                    break # Found the text
    else:

        data = payload.get('body', {}).get('data')
        if data:
            body = base64.urlsafe_b64decode(data).decode('utf-8')

    
    return {
        "From": sender,
        "Subject": subject,
        "Date": date,
        "Content": body.strip()
    }