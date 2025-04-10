
import imaplib
import email
from email.header import decode_header
import csv

def decode_mime_words(s):
    if not s:
        return ""
    decoded = decode_header(s)
    return ''.join([
        part.decode(enc if enc and enc.lower() != 'unknown-8bit' else 'utf-8', errors='replace')
        if isinstance(part, bytes) else part
        for part, enc in decoded
    ])

def get_email_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if content_type == "text/plain" and "attachment" not in content_disposition:
                try:
                    return part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8', errors='replace')
                except:
                    return "[Error decoding body]"
    else:
        try:
            return msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8', errors='replace')
        except:
            return "[Error decoding body]"
    return "[No plain text body found]"

# Credentials
EMAIL = "akashsinghatg@gmail.com"
PASSWORD = "vvkunaveffyitdby"

# Connect to Gmail
mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(EMAIL, PASSWORD)
mail.select("inbox")

# Search all emails
status, messages = mail.search(None, 'ALL')
email_ids = messages[0].split()

# Prepare CSV for UNREAD emails
with open("unread_emails.csv", "w", newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["From", "Subject", "Date", "Body"])  # CSV Header

    print(f"📬 Total Emails Found: {len(email_ids)}\n")

    for e_id in reversed(email_ids):  # optional: reverse to show recent first
        res, msg_data = mail.fetch(e_id, '(BODY.PEEK[] FLAGS)')

        if res != 'OK':
            continue

        msg = None
        flags = []
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                flags = imaplib.ParseFlags(response_part[0])
                msg = email.message_from_bytes(response_part[1])
                break

        if msg:
            sender = decode_mime_words(msg["from"])
            subject = decode_mime_words(msg["subject"])
            date = decode_mime_words(msg["date"])
            body = get_email_body(msg).strip()

            print("📩 Email:")
            print(f"From   : {sender}")
            print(f"Subject: {subject}")
            print(f"Date   : {date}")
            print(f"Body   : {body[:200]}...\n")  # Preview first 200 chars

            # Save only UNREAD to CSV
            if b'\\Seen' not in flags:
                writer.writerow([sender, subject, date, body])
                mail.store(e_id, '+FLAGS', '\\Seen')  # ✅ Mark as read

            

mail.logout()
