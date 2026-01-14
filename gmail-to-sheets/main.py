from src.gmail_service import get_gmail_service, fetch_unread_emails, mark_as_read
from src.email_parser import parse_email
from src.sheets_service import get_sheets_service, append_row
from src.state_manager import load_processed_ids, save_processed_ids
from config import SPREADSHEET_ID

MAX_CELL_LENGTH = 45000  # Safe limit for Google Sheets


def main():
    gmail_service = get_gmail_service()
    sheets_service = get_sheets_service(gmail_service._http.credentials)

    processed_ids = load_processed_ids()
    messages = fetch_unread_emails(gmail_service)

    if not messages:
        print("No unread emails found.")
        return

    new_processed = set(processed_ids)

    for msg in messages:
        msg_id = msg["id"]

        if msg_id in processed_ids:
            continue

        email_data = parse_email(gmail_service, msg_id)

        content = email_data["content"]
        if len(content) > MAX_CELL_LENGTH:
            content = content[:MAX_CELL_LENGTH] + "\n\n[Content truncated]"

        row = [
            email_data["from"],
            email_data["subject"],
            email_data["date"],
            content
        ]

        append_row(sheets_service, SPREADSHEET_ID, row)
        mark_as_read(gmail_service, msg_id)

        new_processed.add(msg_id)
        print(f"Processed email: {msg_id}")

    save_processed_ids(new_processed)
    print("Run completed successfully.")


if __name__ == "__main__":
    main()
