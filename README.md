📧 Gmail Email Scraper & Data Export Tool

A Python-based automation tool that securely fetches unread emails from Gmail using the Gmail API, extracts relevant content, and exports structured data to a CSV file for easy analysis and record keeping.

🚀 Features

Secure Gmail authentication using OAuth 2.0

Automatically fetches unread emails

Extracts sender, subject, date, and email body

Supports both plain text and HTML emails

Exports data to a CSV file

Handles token refresh and session persistence

🛠 Tech Stack

Python

Gmail API

Google OAuth

BeautifulSoup

CSV

email module

📦 Installation

Clone the repository:

git clone https://github.com/your-username/gmail-email-scraper.git
cd gmail-email-scraper
Install dependencies:
pip install google-auth google-auth-oauthlib google-api-python-client beautifulsoup4


Enable the Gmail API and download credentials.json from Google Cloud Console.

Place credentials.json in the project root directory.

▶️ Usage
python main.py


On first run, a browser window will open for Gmail authentication. After successful login, unread emails will be fetched and saved to a CSV file.

📁 Output

unread_emails_gmail_api.csv — Contains:

From

Subject

Date

Body

🔐 Security

OAuth tokens are stored locally in token.json

No passwords are stored or shared

📌 Use Cases

Email data analysis

Inbox automation

Email archiving

Building email-based dashboards

🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss improvements.

📄 License

This project is licensed under the MIT License.
