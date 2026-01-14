import base64
from email.utils import parsedate_to_datetime


def _get_header(headers, name):
    for header in headers:
        if header["name"].lower() == name.lower():
            return header["value"]
    return ""


def parse_email(service, message_id):
    message = service.users().messages().get(
        userId="me",
        id=message_id,
        format="full"
    ).execute()

    payload = message.get("payload", {})
    headers = payload.get("headers", [])

    sender = _get_header(headers, "From")
    subject = _get_header(headers, "Subject")
    date_raw = _get_header(headers, "Date")

    try:
        date = parsedate_to_datetime(date_raw).isoformat()
    except Exception:
        date = date_raw

    body = ""

    def extract_text(parts):
        nonlocal body
        for part in parts:
            mime_type = part.get("mimeType", "")
            data = part.get("body", {}).get("data")

            if mime_type == "text/plain" and data:
                body = base64.urlsafe_b64decode(data).decode("utf-8")
                return

            if "parts" in part:
                extract_text(part["parts"])

    if "parts" in payload:
        extract_text(payload["parts"])
    else:
        data = payload.get("body", {}).get("data")
        if data:
            body = base64.urlsafe_b64decode(data).decode("utf-8")

    return {
        "from": sender,
        "subject": subject,
        "date": date,
        "content": body.strip()
    }
