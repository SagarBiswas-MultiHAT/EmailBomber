# EmailBomber

![EmailBomber](https://scontent.fdac178-1.fna.fbcdn.net/v/t39.30808-6/474010287_601023285867089_3456624333383565357_n.jpg?_nc_cat=111&ccb=1-7&_nc_sid=aa7b47&_nc_eui2=AeH89rCnyamT_-X5Jud97ynZzLcFlrGnxg7MtwWWsafGDuT46Nxyl_d4p95NxC66-xN-DMO8HT2DMb-acxdGa1Xr&_nc_ohc=y5szHWDQl2kQ7kNvgH7cwn6&_nc_zt=23&_nc_ht=scontent.fdac178-1.fna&_nc_gid=A6tghOkqA_ddkKfrtHOyAzg&oh=00_AYCeajmYxE-LYbxkB7fZa1ri0WTw00q6lRQYFdTD7JiLnQ&oe=67900145)

## Overview
**EmailBomber** is a Python-based script that allows you to send multiple emails in a loop using a Gmail SMTP server. This script includes basic email validation, secure password handling, and HTML-formatted email content. Designed for educational and testing purposes, this script demonstrates how to automate email sending via Python.

## Features
- **Email Validation:** Ensures the format of both sender and recipient emails is correct.
- **Secure Password Input:** Uses `getpass` for securely handling email passwords.
- **HTML Email Support:** Sends HTML-formatted emails with a customizable message.
- **Multiple Email Sending:** Allows sending a specified number of emails in a loop.
- **SMTP Authentication:** Utilizes Gmail's SMTP server for sending emails securely.

## Prerequisites
- Python 3.x
- A Gmail account
- An app password for Gmail (due to the less secure app access policy)

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/SagarBiswas-MultiHAT/EmailBomber.git
    ```
2. Navigate to the project directory:
    ```bash
    cd EmailBomber
    ```

## Usage
1. Run the script:
    ```bash
    python email_bomber.py
    ```
2. Follow the prompts to enter:
    - Your Gmail address
    - Your Gmail app password
    - The recipient's email address
    - The email subject
    - The number of emails to send

3. The script will send the specified number of emails to the recipient with a 1-second delay between each email.

## Notes
- **Educational Purpose Only:** This script is meant for educational purposes. Misuse of this tool for spamming or unauthorized email sending is strictly prohibited and may lead to legal consequences.
- **App Password Required:** Ensure that you generate an app password in your Gmail account settings for this script to work.

