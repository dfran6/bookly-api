from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from src.config import Config
from pathlib import Path
import httpx
import logging


BASE_DIR = Path(__file__).resolve().parent


mail_config = ConnectionConfig(
    MAIL_USERNAME=Config.MAIL_USERNAME,
    MAIL_PASSWORD=Config.MAIL_PASSWORD,
    MAIL_FROM=Config.MAIL_FROM,
    MAIL_PORT=Config.MAIL_PORT,
    MAIL_SERVER=Config.MAIL_SERVER,
    MAIL_FROM_NAME=Config.MAIL_FROM_NAME,
    MAIL_STARTTLS=Config.MAIL_STARTTLS,
    MAIL_SSL_TLS=Config.MAIL_SSL_TLS,
    USE_CREDENTIALS=Config.USE_CREDENTIALS,
    VALIDATE_CERTS=Config.VALIDATE_CERTS,
    TEMPLATE_FOLDER=Path(BASE_DIR, 'templates')
)

mail = FastMail(
    config=mail_config
)


def create_message(recipients: list[str], subject: str, body: str) -> MessageSchema:
    return MessageSchema(recipients=recipients, subject=subject, body=body, subtype=MessageType.html)



async def _send_via_sendinblue(message: MessageSchema) -> bool:
    """Send using Sendinblue HTTP API. Requires Config.SENDINBLUE_API_KEY.

    Returns True on success, False on failure.
    """
    api_key = Config.SENDINBLUE_API_KEY
    if not api_key:
        return False

    # Normalize recipients: MessageSchema may contain NameEmail objects or strings
    to_list = []
    for r in message.recipients:
        # r can be a string email, a dict, or a pydantic NameEmail object
        if isinstance(r, str):
            to_list.append({"email": r})
        elif isinstance(r, dict) and r.get("email"):
            to_list.append({"email": r.get("email")})
        else:
            # Fallback: try to read `.email` attribute
            email = getattr(r, "email", None)
            if email:
                to_list.append({"email": email})

    data = {
        "sender": {"name": mail_config.MAIL_FROM_NAME or "", "email": mail_config.MAIL_FROM},
        "to": to_list,
        "subject": message.subject,
        "htmlContent": message.body,
    }

    headers = {"api-key": api_key, "Content-Type": "application/json"}

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.post("https://api.sendinblue.com/v3/smtp/email", json=data, headers=headers)
            # Log non-2xx responses for easier debugging
            if r.status_code >= 400:
                logging.error("Sendinblue response status=%s body=%s", r.status_code, r.text)
            r.raise_for_status()
        return True
    except Exception:
        logging.exception("Sendinblue send failed")
        return False


async def safe_send(message: MessageSchema) -> bool:
    """Send message using Sendinblue API when available, otherwise fall back to SMTP.

    Returns True on success, False on failure. Exceptions are logged.
    """
    try:
        # Prefer Sendinblue if configured
        if getattr(Config, "SENDINBLUE_API_KEY", None):
            sent = await _send_via_sendinblue(message)
            if sent:
                return True

        # Fall back to SMTP
        await mail.send_message(message)
        return True
    except Exception:
        logging.exception("Failed to send email via Sendinblue or SMTP")
        return False