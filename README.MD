# 🎂 Automated Birthday Wisher

A Python-based automation script that checks a CSV file for birthdays and sends a personalized email using SMTP.
## 🚀 Features
- **CSV Integration**: Reads names, emails, and birth dates from a `birthdays.csv` file.
- **Dynamic Templates**: Randomly selects one of three letter templates for the birthday wish.
- **Placeholder Replacement**: Automatically replaces `[NAME]` with the recipient's actual name.
- **Auto-Backups**: Saves a copy of every sent email to an `outbox/` folder for record-keeping.

## 🛠️ Installation & Setup
1. **Clone the repository**:
   ```bash
   git clone [https://github.com/mascasucci/birthday-wisher.git](https://github.com/mascasucci/birthday-wisher.git)
   
Configure your credentials:

Create a secrets.py file (not included in this repo for security).

Add your MY_MAIL and MY_PASSWORD (Gmail App Password).

Add your birthdays:

Update birthdays.csv with your friends' and family's details.

📦 Requirements
Python 3.x

Pandas library (pip install pandas)

🛡️ Security Note
This project uses App Passwords for Gmail. Ensure your secrets.py and birthdays.csv are added to your .gitignore to prevent sensitive data leaks.