# Gmail to Google Sheets Automation

Author: Amulya B

---

## 1. Project Overview

This project is a Python-based automation system that reads unread emails from a Gmail inbox and logs them into a Google Sheet. Each email is processed exactly once and stored with sender details, subject, received date, and plain-text content.

The system is designed to be safe to run multiple times without creating duplicate entries.

---

## 2. High-Level Architecture Diagram

```

+---------------------+
|     Gmail Inbox     |
|  (Unread Emails)    |
+----------+----------+
|
v
+---------------------+
|     Gmail API       |
|   (OAuth 2.0)       |
+----------+----------+
|
v
+---------------------+
|   Email Fetcher     |
|  (Message IDs)      |
+----------+----------+
|
v
+---------------------+
|   Email Parser      |
| From | Subject |    |
| Date | Content |    |
+----------+----------+
|
v
+---------------------+
| State Check         |
| processed_emails    |
| .json               |
+----------+----------+
|
v
+---------------------+
| Google Sheets API   |
| (Append Row)        |
+----------+----------+
|
v
+---------------------+
| Mark Email as Read  |
+---------------------+

````

---

## 3. Step-by-Step Setup Instructions

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd gmail-to-sheets
````

### Step 2: Create and Activate Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Google Cloud Configuration

* Create a Google Cloud project
* Enable Gmail API and Google Sheets API
* Configure OAuth consent screen in Testing mode
* Add your Gmail ID as a test user
* Create OAuth Client ID (Desktop App)
* Download `credentials.json`
* Place it inside the `credentials` folder

### Step 5: Google Sheet Setup

* Create a Google Sheet
* Add headers: From, Subject, Date, Content
* Copy the Spreadsheet ID
* Paste it into `config.py`

### Step 6: Run the Script

```bash
python main.py
```

---

## 4. OAuth Flow Used

This project uses **OAuth 2.0 Desktop Application Flow**.

* The user is redirected to a Google login screen
* The user grants permission to access Gmail and Google Sheets
* An access token is generated during the first run
* The token is stored locally and reused for subsequent runs

This approach ensures secure access without hardcoding credentials or using service accounts.

---

## 5. Duplicate Prevention Logic

Each Gmail email has a unique and immutable **message ID**.

* After processing an email, its message ID is saved locally
* On every run, the script checks the stored IDs
* If an ID already exists, the email is skipped

This guarantees:

* No duplicate rows in Google Sheets
* Append-only behavior
* Safe execution on repeated runs

---

## 6. State Persistence Method

State is stored locally in the file:

```
state/processed_emails.json
```

Example:

```json
{
  "processed_ids": [
    "19b7d735f45df285",
    "19b7d559f7aa78be"
  ]
}
```

### Reason for Choosing This Method

* Gmail message IDs are unique and permanent
* Faster than querying Google Sheets
* Simple to maintain and debug
* Does not require an external database

---

## 7. Challenges Faced and Solutions

### Challenge 1: OAuth Permission Errors

Initially, the OAuth token had only Gmail access, which caused permission errors when writing to Google Sheets.

**Solution:**
The existing OAuth token was deleted and regenerated with expanded scopes including Google Sheets access.

### Challenge 2: Email Body Formatting

Some emails contained complex HTML content, leading to poorly formatted output.

**Solution:**
Only the plain-text (`text/plain`) portion of emails was extracted to ensure readable content.


### Challenge 3: content exceeding

Some email bodies exceeded Google Sheets’ 50,000 character limit per cell. This was handled by truncating the email content before appending, ensuring the script does not fail on large emails.

---

## 8. Limitations of the Solution

* Only unread inbox emails are processed
* Attachments are not handled
* HTML emails are converted to plain text
* State is stored locally and not shared across systems
* OAuth is in testing mode and supports only approved users

---

## 9. Proof of Execution

The `proof` folder contains:

* Screenshot of Gmail inbox with unread emails
* Screenshot of Google Sheet populated with email data
* Screenshot of OAuth consent screen
* Screen recording demonstrating:

  * First run of the script
  * Second run without duplicate entries

---

## 10. How to Run the Project

```bash
python main.py
```

The script can be executed multiple times safely without duplicating data.
