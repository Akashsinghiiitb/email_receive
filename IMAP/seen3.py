import imaplib
import email
from email.header import decode_header

def decode_mime_words(s):
    if not s:
        return ""
    decoded = decode_header(s)
    return ''.join([
        part.decode(enc if enc and enc.lower() != 'unknown-8bit' else 'utf-8', errors='replace')
        if isinstance(part, bytes) else part
        for part, enc in decoded
    ])

EMAIL = "akashsinghatg@gmail.com"
PASSWORD = "vvkunaveffyitdby"

mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(EMAIL, PASSWORD)
mail.select("inbox")

# Fetch ALL emails
status, messages = mail.search(None, 'ALL')
email_ids = messages[0].split()

print(f"📬 Total Emails Found: {len(email_ids)}\n")

for e_id in email_ids:
    # Fetch flags and full message
    res, msg_data = mail.fetch(e_id, '(BODY.PEEK[] FLAGS)')

    if res != 'OK':
        continue

    # Extract raw message and flags line
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            flags = imaplib.ParseFlags(response_part[0])
            msg = email.message_from_bytes(response_part[1])
            break

    # Check if message is read or unread
    read_status = "Read" if b'\\Seen' in flags else "Unread"

    sender = decode_mime_words(msg["from"])
    subject = decode_mime_words(msg["subject"])

    print(f"📩 Email ({read_status})")
    print(f"From   : {sender}")
    print(f"Subject: {subject}\n")

mail.logout()
