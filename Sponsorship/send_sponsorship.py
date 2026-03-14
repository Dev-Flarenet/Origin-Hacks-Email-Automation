import csv
import smtplib
import ssl
import time
import os

from email.message import EmailMessage

# ============================================================
# CONFIGURATION  – edit these before running
# ============================================================

SMTP_SERVER   = "smtp.zoho.in"
SMTP_PORT     = 587

SENDER_EMAIL  = "info@originhacks.in"
APP_PASSWORD  = "brSSWgKXYRRK"       # Zoho App Password

SENDER_NAME   = "Bhuvanesh H(Tech Lead)"  # Replaces [Your Name] in the signature

BASE_DIR           = os.path.dirname(os.path.abspath(__file__))
HTML_TEMPLATE_PATH = os.path.join(BASE_DIR, "mail.html")
CSV_FILE_PATH      = os.path.join(BASE_DIR, "sponsors.csv")

# Delay (seconds) between each email to avoid spam-flagging
SEND_DELAY = 4

# ============================================================
# HELPERS
# ============================================================

def load_template() -> str:
    """Read the HTML template once and return it as a string."""
    with open(HTML_TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()


def personalise(template: str, recipient_name: str, company_name: str) -> str:
    """
    Replace every placeholder in the template with real values.

    Placeholders used in mail.html
    ─────────────────────────────
    [Recipient Name]  → contact person's name
    [Company Name]    → organisation / company name
    [Your Name]       → sender's name (from SENDER_NAME constant)
    """
    html = template
    html = html.replace("[Recipient Name]", recipient_name)
    html = html.replace("[Company Name]",   company_name)
    html = html.replace("[Your Name]",      SENDER_NAME)
    return html


def send_email(to_email: str, recipient_name: str, company_name: str,
               html_template: str) -> None:
    """Build and dispatch a single personalised email."""
    msg = EmailMessage()
    msg["From"]    = f"Origin Hacks 2026 <{SENDER_EMAIL}>"
    msg["To"]      = to_email
    msg["Subject"] = f"Invitation to {company_name} – Prize Sponsor | Origin 2026"

    personalised_html = personalise(html_template, recipient_name, company_name)

    # Plain-text fallback
    msg.set_content(
        f"Dear {recipient_name},\n\n"
        "You have been invited to sponsor Origin 2026 – a 24 Hours Non-Stop AI Hackathon.\n"
        "Please view this email in an HTML-capable client for the full invitation.\n\n"
        f"Regards,\n{SENDER_NAME}\nOrganizing Team – Origin 2026\n"
        "info@originhacks.in | www.originhacks.in"
    )
    msg.add_alternative(personalised_html, subtype="html")

    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)


# ============================================================
# MAIN
# ============================================================

def main():
    if not os.path.exists(CSV_FILE_PATH):
        print(f"[ERROR] CSV not found: {CSV_FILE_PATH}")
        print("  Create 'sponsors.csv' with columns: email, recipient_name, company_name")
        return

    html_template = load_template()
    print(f"[INFO] Template loaded  : {HTML_TEMPLATE_PATH}")
    print(f"[INFO] Reading CSV from : {CSV_FILE_PATH}\n")

    success_count = 0
    fail_count    = 0

    with open(CSV_FILE_PATH, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            email          = row["email"].strip()
            recipient_name = row["recipient_name"].strip()
            company_name   = row["company_name"].strip()

            if not email:
                print(f"[SKIP] Empty email row – {row}")
                continue

            try:
                send_email(email, recipient_name, company_name, html_template)
                print(f"[✓] Sent  → {recipient_name} <{email}>  ({company_name})")
                success_count += 1
            except Exception as err:
                print(f"[✗] FAILED → {email}  |  {err}")
                fail_count += 1

            time.sleep(SEND_DELAY)

    print(f"\n{'='*50}")
    print(f"  Done!  ✓ {success_count} sent   ✗ {fail_count} failed")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
