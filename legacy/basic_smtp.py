#!/usr/bin/env python3
"""
Legacy basic SMTP sender (Educational Reference).
Copyright (C) 2026 Sagar Biswas. All rights reserved.
SPDX-License-Identifier: GPL-3.0-or-later
"""

import smtplib
from getpass import getpass

print("\n..:: Basic SMTP Sending Demo ::..\n")
print("=" * 50)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()

email = input("\n..:: Enter your email: ").strip()
password = getpass("\n..:: Enter your email app password: ")
recipient = input("\n..:: Enter the recipient email: ").strip()
n = int(input("\n..:: Enter number of test emails to send: "))

server.login(email, password)

msg = "Subject: Test Notification\n\nHello, this is a test notification."

for i in range(n):
    server.sendmail(email, recipient, msg)
    print(f"\t==> Test email {i + 1} sent successfully.")

server.quit()
print("\nDone.")

