#!/usr/bin/env python3
"""
Legacy HTML SMTP sender (Educational Reference).
Copyright (C) 2026 Sagar Biswas. All rights reserved.
SPDX-License-Identifier: GPL-3.0-or-later
"""

import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from getpass import getpass
from time import sleep


def is_valid_email(email):
    regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(regex, email)


print("\n..:: HTML Email Sender Demo ::..\n")
print("=" * 50)

while True:
    from_email = input("\n..:: Enter your email: ").strip()
    if is_valid_email(from_email):
        break
    print("Invalid email format. Please try again.")

app_password = getpass("\n..:: Enter your email app password: ")

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(from_email, app_password)
    print("\n\tLogin successful!\n")

    while True:
        to_email = input("\n..:: Enter recipient email: ").strip()
        if is_valid_email(to_email):
            break
        print("Invalid email format. Please try again.")

    subject = input("\n..:: Enter email subject: ").strip() or "HTML Email Test"

    body = """<!DOCTYPE html>
<html>
<body style="font-family: Arial, sans-serif; color: #333;">
    <h2 style="color: #2d89ef;">Test Email Notification</h2>
    <p>This is a test notification generated to verify HTML email formatting and delivery.</p>
    <p>Timestamp: Automated transmission test.</p>
</body>
</html>"""

    num_emails = int(input("\n..:: Enter number of emails to send: ") or "1")

    print("\nSending...")
    for i in range(num_emails):
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html"))

        server.sendmail(from_email, to_email, msg.as_string())
        print(f"\t==> Email {i + 1} sent successfully.")
        if i < num_emails - 1:
            sleep(1)

    print("\nAll emails sent successfully.")

except Exception as e:
    print(f"\nAn error occurred: {e}")
finally:
    try:
        server.quit()
    except Exception:
        pass

