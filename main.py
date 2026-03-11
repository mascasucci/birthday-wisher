import smtplib
import datetime as dt
from random import choice
import pandas as pd
import os

# Get credentials from the environment (GitHub Actions)
# or fall back to local secrets if testing on your PC
try:
    import my_credentials
    MY_EMAIL = my_credentials.MY_EMAIL
    MY_PASSWORD = my_credentials.MY_PASSWORD
except (ImportError, ModuleNotFoundError):
    # If the file isn't there (like on GitHub), look in Environment Variables
    MY_MAIL = os.environ.get("MY_EMAIL")
    MY_PASSWORD = os.environ.get("MY_PASSWORD")

" No PRO email wishes sender (Something hardcoded,"
" not using EmailMessage library, for example ...)"

# --- Configuration ---

TEMPLATES_DIR = "letter_templates"
OUTBOX_DIR = "outbox"

# Ensure outbox directory exists
if not os.path.exists(OUTBOX_DIR):
    os.makedirs(OUTBOX_DIR)

letters_list = ["letter_1.txt", "letter_2.txt", "letter_3.txt"]
# Create a list to hold the final data
birthday_queue = []


month =dt.datetime.now().month
day = dt.datetime.now().day

try:
    df = pd.read_csv('birthdays.csv')
    # Filtering for today
    today_birthdays_df = df[(df['month'] == month) & (df['day'] == day)].copy().reset_index(drop=True)
    # Check if there are any birthdays today
    if not today_birthdays_df.empty:
        for index, row in today_birthdays_df.iterrows():
            person_name = row['name']
            person_email = row['email']

            # Pick random letter template and generate content
            letter_template = f"letter_templates/{choice(letters_list)}"
            with open(letter_template, "r", encoding="utf-8") as file_r:
                final_letter = file_r.read().replace("[NAME]", person_name.title())

            # Save a backup to the outbox for record-keeping
            letter_path = f"outbox/{index}_{person_name}.txt"
            with open(letter_path, "w", encoding="utf-8") as file_w:
                file_w.write(final_letter)

            # Store everything we need for the email in a list of dictionary
            birthday_queue.append({
                "email": person_email,
                "content": final_letter,
                "name": person_name
            })
    else:
        print("No birthdays to celebrate today! 🎂")

except FileNotFoundError:
    print("Error: 'birthdays.csv' or template folder not found.")

# Sending Section
if len(birthday_queue) > 0:
#    answer = input(f"Do you want to send {len(birthday_queue)} mail(s)? (y/n): ")
#    if answer.lower() == "y":
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            # Loop through the today's birthdays' list of dictionaries
            for person in birthday_queue:
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=person["email"],
                    msg=f"Subject:Happy Birthday {person['name']}!\n\n{person['content']}"
                )
        print("Success! All emails dispatched.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
# else:
#     print("Please control the birthday's mail(s)\n"
#           "sending cancelled ...")
