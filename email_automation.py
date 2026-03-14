"""
Project Summary
===============
This project ("Email-Auto") is a unified email automation tool to streamline sending
invitations and correspondence for the Origin Hacks 2026 event.
It is designed to handle two specific use cases efficiently:

1. Call for Sponsorship: Sends customized emails from a template ("Call_for_Sponsorship.html")
   to potential sponsors.
2. Call for Guest: Sends personalized guest of honor invitations from a template 
   ("Call_for_Guest.html") to prospective guests.

Features:
- Reads recipient data (Email, Company name) from a specified CSV file.
- Replaces the `{{company_name}}` placeholder in the HTML templates with the actual name.
- Connects securely using TLS over Zoho SMTP (smtp.zoho.in).
- Provides rate limiting to avoid triggering spam filters.
- Uses command-line arguments to quickly toggle between "sponsorship" and "guest" modes.

Usage:
  python email_automation.py --type sponsorship --csv "Company list.csv"
  python email_automation.py --type guest --csv "Company list.csv"
"""

import csv
import smtplib
import ssl
import time
import os
import argparse
from email.message import EmailMessage

# ==============================
# CONFIGURATION
# ==============================
SMTP_SERVER = "smtp.zoho.in"
SMTP_PORT = 587
SENDER_EMAIL = "info@originhacks.in"
# Hardcoded App Password
APP_PASSWORD = "brSSWgKXYRRK" 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ==============================
# HELPER FUNCTIONS
# ==============================
def load_template(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Template not found at: {file_path}")
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def send_bulk_emails(csv_path, template_path, subject):
    """Reads a CSV and sends an email to each entry using the given template."""
    try:
        html_template = load_template(template_path)
    except Exception as e:
        print(f"[CRITICAL] Error loading template: {e}")
        return

    if not os.path.exists(csv_path):
        print(f"[CRITICAL] CSV file not found: {csv_path}")
        return

    # Count rows
    with open(csv_path, encoding="utf-8") as f:
        total_rows = sum(1 for line in f) - 1

    print(f"Starting email process for {total_rows} recipients...")
    context = ssl.create_default_context()

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(SENDER_EMAIL, APP_PASSWORD)
            print("[SUCCESS] SMTP Login Successful.")

            with open(csv_path, newline='', encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                count = 0
                
                # Support different column names for robustness
                for row in reader:
                    # Try to fetch company name from a few potential column names
                    company_name = row.get("Company name", row.get("company_name", "")).strip()
                    email = row.get("Email", row.get("email", "")).strip()

                    if not email or "@" not in email:
                        print(f"[SKIPPED] Invalid or missing email for '{company_name}': {email}")
                        continue

                    try:
                        msg = EmailMessage()
                        msg["From"] = SENDER_EMAIL
                        msg["To"] = email
                        msg["Subject"] = subject
                        
                        # Personalize template
                        personalized_html = html_template.replace("{{company_name}}", company_name)
                        
                        msg.set_content("Your email client does not support HTML emails.")
                        msg.add_alternative(personalized_html, subtype="html")

                        server.send_message(msg)
                        count += 1
                        print(f"[SENT] {count}/{total_rows} -> {company_name} ({email})")
                        
                        time.sleep(2) # Rate limiting
                    except Exception as e:
                        print(f"[FAILED] Error sending to {company_name} ({email}): {e}")

            print("Bulk email process completed.")
    except Exception as e:
        print(f"[CRITICAL] SMTP Connection Error: {e}")

# ==============================
# MAIN CLI
# ==============================
def main():
    parser = argparse.ArgumentParser(description="Origin Hacks 2026 Email Automation Robot")
    parser.add_argument("--type", choices=["sponsorship", "guest"], required=True,
                        help="Select the type of email to send (sponsorship or guest)")
    parser.add_argument("--csv", default="Company list.csv",
                        help="Path to the recipient CSV file (default: 'Company list.csv')")
    
    args = parser.parse_args()
    
    csv_file_path = os.path.join(BASE_DIR, args.csv)
    
    if args.type == "sponsorship":
        template_file = os.path.join(BASE_DIR, "Call_for_Sponsorship.html")
        subject = "Partner with Origin Hacks 2026 - National Level 24hr AI Hackathon"
    elif args.type == "guest":
        template_file = os.path.join(BASE_DIR, "Call_for_Guest.html")
        subject = "Invitation to Grace Origin Hacks 2026 as Guest of Honor"
        
    print(f"=== EMAIL AUTOMATION ===")
    print(f"Mode       : {args.type.upper()}")
    print(f"CSV File   : {args.csv}")
    print(f"Template   : {os.path.basename(template_file)}")
    print(f"========================")
    
    send_bulk_emails(csv_file_path, template_file, subject)

if __name__ == "__main__":
    main()
