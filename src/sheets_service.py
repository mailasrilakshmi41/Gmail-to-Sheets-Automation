from googleapiclient.discovery import build
from config import SPREADSHEET_ID, RANGE_NAME

# from the Gmail login flow in main.py.

def append_to_sheet(creds, data):
    """
    Appends a single row of email data to the Google Sheet.
    """
    try:
        service = build('sheets', 'v4', credentials=creds)
        

        values = [[
            data['From'],
            data['Subject'],
            data['Date'],
            data['Content']
        ]]
        
        body = {'values': values}

        result = service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()
        
        print(f" -> Added to Sheet: {result.get('updates').get('updatedCells')} cells updated.")
        
    except Exception as e:
        print(f"Error writing to Google Sheets: {e}")