import os.path
import base64
import csv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email import message_from_bytes
from bs4 import BeautifulSoup

# If modifying these SCOPES, delete the file token.json
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def get_unread_emails(service):
    results = service.users().messages().list(userId='me', labelIds=['UNREAD'], maxResults=100).execute()
    messages = results.get('messages', [])
    return messages

def get_message_details(service, msg_id):
    msg = service.users().messages().get(userId='me', id=msg_id, format='raw').execute()
    msg_raw = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
    mime_msg = message_from_bytes(msg_raw)

    sender = mime_msg.get('From')
    subject = mime_msg.get('Subject')
    date = mime_msg.get('Date')

    # Extract plain text or HTML body
    body = ""
    if mime_msg.is_multipart():
        for part in mime_msg.walk():
            if part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True).decode(errors='ignore')
                break
            elif part.get_content_type() == 'text/html':
                html = part.get_payload(decode=True).decode(errors='ignore')
                body = BeautifulSoup(html, "html.parser").get_text()
                break
    else:
        body = mime_msg.get_payload(decode=True).decode(errors='ignore')

    return sender, subject, date, body.strip()

def save_to_csv(data, filename='unread_emails_gmail_api.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['From', 'Subject', 'Date', 'Body'])
        for row in data:
            writer.writerow(row)

def main():
    service = authenticate_gmail()
    unread_msgs = get_unread_emails(service)

    print(f"📬 Unread Messages: {len(unread_msgs)}\n")
    email_data = []

    for msg in unread_msgs:
        sender, subject, date, body = get_message_details(service, msg['id'])

        print(f"From   : {sender}")
        print(f"Subject: {subject}")
        print(f"Date   : {date}")
        print(f"Body   : {body[:200]}...\n")

        email_data.append([sender, subject, date, body])

    save_to_csv(email_data)
    print("✅ Unread emails saved to CSV.")

if __name__ == '__main__':
    main()
