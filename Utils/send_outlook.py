import pandas as pd
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

EXCEL_FILE = "tasks.xlsx"

SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587
SENDER_EMAIL = "vamseekanthr@juniper.net"
PASSWORD = "KkmAcl@4526"   # ⚠️ Or use app password

def send_email(to_email, subject, body):
    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())

def main():
    df = pd.read_excel(EXCEL_FILE)
    today = datetime.today().date()

    for _, row in df.iterrows():
        due_date = row["DueDate"].date()
        email = row["OwnerEmail"]
        task = row["Task"]

        if due_date <= today:
            subject = f"⚠ Task Due: {task}"
            body = f"Reminder: Task '{task}' was due on {due_date}"
            send_email(email, subject, body)
            print(f"✅ Sent reminder to {email}")

if __name__ == "__main__":
    main()

