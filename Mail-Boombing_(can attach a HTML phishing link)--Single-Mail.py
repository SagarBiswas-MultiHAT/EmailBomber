import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from getpass import getpass
import time

def send_email(server, from_email, to_email, subject, body):
    # Construct the email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    # Convert the message to string once
    message_text = msg.as_string()

    # Send the email
    server.sendmail(from_email, to_email, message_text)

# Email details
from_email = input("\n..:: Enter your email\t\t\t: ")
app_password = getpass("\n..:: Enter your email's app password\t: ")
to_email = input("\n..:: Enter the target email's address\t\t\t\t: ")
subject = "Verify Your Account (H4CK3R)! 🚨"
body = """
<html>
<body>
    <h1 style="color: #2d89ef;">Verify Your Account</h1>
    <p>Dear User,</p>
    <p>We noticed suspicious activity in your account and need you to verify your account details to ensure continued access. 
    Please click the link below to confirm your account:</p>
    <p><a href="https://example.com/verify-account" style="color: #1d70b8; text-decoration: none;">Verify My Account</a></p>
    <p>If you did not initiate this request, please contact our support team immediately.</p>
    <p>Thank you,<br>Your Security Team</p>
</body>
</html>
"""

# Setup the SMTP server
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(from_email, app_password)

# start_time = time.time()

# Send the email
send_email(server, from_email, to_email, subject, body)

# end_time = time.time()
# print(f"\n\t==> Email sent in {end_time - start_time:.2f} seconds.")

# Quit the server
server.quit()

print()
