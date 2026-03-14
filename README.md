# Origin Hacks 2026 - Email Automation

This repository contains the email automation script designed to streamline sending invitations and correspondence for the Origin Hacks 2026 event. 

It handles two specific use cases:
1. **Call for Sponsorship**: Sends customized emails to potential sponsors.
2. **Call for Guest**: Sends personalized guest of honor invitations to prospective guests.

## Files
- `email_automation.py` - The main Python script that handles reading the contacts, substituting names into the HTML templates, and securely sending the emails via Zoho SMTP.
- `Call_for_Sponsorship.html` - The HTML email template sent to potential sponsors.
- `Call_for_Guest.html` - The HTML email template sent to prospective guests of honor.
- `Company list.csv` (Not included in repo by default) - A CSV file containing the recipient list.

## Prerequisites
Ensure you have Python installed. The script relies on standard library modules (`csv`, `smtplib`, `ssl`, `argparse`, `email.message`), so no external packages like `pip install` are necessary.

## CSV Format
Your CSV file must include the following columns at a minimum:
- `Company name` or `company_name` 
- `Email` or `email`

**Example:**
```csv
Company name,Email
Acme Corp,contact@acmecorp.com
Tech Solutions,info@techsolutions.io
```

## Configuration
The script is configured to use Zoho SMTP (`smtp.zoho.in` on port `587`) using the sender email `info@originhacks.in`.
The App Password for authentication is retrieved from the `SMTP_APP_PASSWORD` environment variable or falls back to a default value inside the script.

To keep your credentials secure, it is recommended to set the environment variable in your terminal before running:
```bash
# Windows (Command Prompt)
set SMTP_APP_PASSWORD=your_app_password

# Windows (PowerShell)
$env:SMTP_APP_PASSWORD="your_app_password"

# macOS/Linux
export SMTP_APP_PASSWORD="your_app_password"
```

## How to Usage

Open a terminal or command prompt in the folder containing the files.

### 1. Sending Sponsorship Emails
To send the "Call for Sponsorship" email, use the `--type sponsorship` flag:
```bash
python email_automation.py --type sponsorship --csv "Company list.csv"
```
*Note: If your CSV file is named exactly `Company list.csv`, you can omit the `--csv` argument.*

### 2. Sending Guest Invitations
To send the "Call for Guest" email, use the `--type guest` flag:
```bash
python email_automation.py --type guest --csv "Company list.csv"
```

## Modifying the Templates
Both `Call_for_Sponsorship.html` and `Call_for_Guest.html` use a placeholder `{{company_name}}`. 
You can edit these HTML files to change the formatting, colors, or wording of the emails. As long as you keep `{{company_name}}` in the text, the script will automatically replace it with the individual company name from your CSV file for each recipient.
