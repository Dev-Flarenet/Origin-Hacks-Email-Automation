import csv
import smtplib
import ssl
import time
import os

from email.message import EmailMessage

# ============================================================
# CONFIGURATION
# ============================================================

SMTP_SERVER  = "smtp.zoho.in"
SMTP_PORT    = 587

SENDER_EMAIL = "info@originhacks.in"
APP_PASSWORD = "brSSWgKXYRRK"

SENDER_NAME  = "Bhuvanesh H (Tech Lead)"   # Replaces [Your Name] in template

BASE_DIR           = os.path.dirname(os.path.abspath(__file__))
HTML_TEMPLATE_PATH = os.path.join(BASE_DIR, "email.html")
CSV_FILE_PATH      = os.path.join(BASE_DIR, "mentors.csv")

SEND_DELAY = 4   # seconds between emails

# ============================================================
# HELPERS
# ============================================================

def load_template() -> str:
    with open(HTML_TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()


def personalise(template: str, mentor_name: str) -> str:
    """Replace placeholders: [Mentor Name] and [Your Name]."""
    html = template
    html = html.replace("[Mentor Name]", mentor_name)
    html = html.replace("[Your Name]",   SENDER_NAME)
    return html


def send_email(to_email: str, mentor_name: str, html_template: str) -> None:
    msg = EmailMessage()
    msg["From"]    = f"Origin Hacks 2026 <{SENDER_EMAIL}>"
    msg["To"]      = to_email
    msg["Subject"] = "Mentorship Invitation | Origin 2026 – 24 Hours AI Hackathon"

    personalised_html = personalise(html_template, mentor_name)

    msg.set_content(
        f"Dear {mentor_name},\n\n"
        "You are invited as a Mentor for Origin 2026 – 24 Hours Non-Stop AI Hackathon.\n"
        "Please view this email in an HTML-capable client for the full invitation.\n\n"
        f"Warm regards,\n{SENDER_NAME}\nOrganizing Team – Origin 2026\n"
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
    html_template = load_template()
    print(f"[INFO] Template : {HTML_TEMPLATE_PATH}")
    print(f"[INFO] CSV      : {CSV_FILE_PATH}\n")

    success, fail = 0, 0

    with open(CSV_FILE_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            email       = row["email"].strip()
            mentor_name = row["mentor_name"].strip()

            if not email:
                continue

            try:
                send_email(email, mentor_name, html_template)
                print(f"[✓] Sent  → {mentor_name} <{email}>")
                success += 1
            except Exception as err:
                print(f"[✗] FAILED → {email}  |  {err}")
                fail += 1

            time.sleep(SEND_DELAY)

    print(f"\n{'='*50}")
    print(f"  Done!  ✓ {success} sent   ✗ {fail} failed")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
