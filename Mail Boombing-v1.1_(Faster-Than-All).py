import smtplib
from getpass import getpass
from time import sleep
import re

def is_valid_email(email):
    # Simple regex for email validation
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email)

print("\n\n..:: Welcome to the Email Boombing Program ::..\n")
print("=" * 50)

# Input email and password securely with validation
while True:
    email = input("\n..:: Enter your email\t\t\t: ")
    if is_valid_email(email):
        break
    else:
        print("Invalid email format. Please try again.")

password = getpass("\n..:: Enter your email's app password\t: ")

try:
    # Set up the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    
    print("\n\t ( $ _ $ ) Login successful!\n")
    
    # Input for email subject and body
    targeted_email = input("..:: Enter the target email's address\t\t\t\t: ")
    subject = input("\n..:: Enter the subject of the email (press enter to skip)\t: ")
    msg_body = input("\n..:: Enter the message to be sent (need for visibility)\t\t: ")
    n = int(input("\n..:: Enter the number of times to send the email\t\t: "))
    
    # Prepare the email message
    msg = f"Subject: {subject}\n\n{msg_body}"

    print("\nSending emails...\n")
    
    # Send the email 10 times with a delay between each
    for i in range(n):
        try:
            server.sendmail(email, targeted_email, msg)
            print(f"\t==> Email {i + 1} sent successfully!")
            sleep(1)  # Sleep for 1 second between emails (adjust as necessary)
        except Exception as e:
            print(f"Error sending email {i + 1}: {e}")
    
    print("\nAll emails sent successfully!")
    
except smtplib.SMTPAuthenticationError:
    print("\nAuthentication failed. Please check your credentials and try again.")
except Exception as e:
    print(f"\nAn error occurred: {e}")
finally:
    # Quit the server if it's connected
    if 'server' in locals():
        server.quit()
    print("\nProgram terminated.\n")
