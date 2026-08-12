"""Wysyłka wiadomości transakcyjnych wyłącznie przez skonfigurowane SMTP."""
import smtplib
from email.message import EmailMessage

from fastapi import HTTPException, status

from app.core.config import get_settings


def send_password_reset_email(recipient: str, reset_link: str) -> None:
    settings = get_settings()
    if not all((settings.smtp_host, settings.smtp_username, settings.smtp_password, settings.smtp_from_email)):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Reset hasła nie jest jeszcze skonfigurowany. Skontaktuj się z administratorem.",
        )
    message = EmailMessage()
    message["Subject"] = "Reset hasła — BuildSmart AI"
    message["From"] = settings.smtp_from_email
    message["To"] = recipient
    message.set_content(
        "Otrzymaliśmy prośbę o zmianę hasła do BuildSmart AI.\n\n"
        f"Ustaw nowe hasło: {reset_link}\n\n"
        "Link jest ważny przez 30 minut. Jeśli to nie Ty zleciłeś zmianę, zignoruj tę wiadomość."
    )
    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=15) as server:
            if settings.smtp_use_tls:
                server.starttls()
            server.login(settings.smtp_username, settings.smtp_password)
            server.send_message(message)
    except (OSError, smtplib.SMTPException) as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Nie udało się wysłać wiadomości resetującej. Spróbuj ponownie później.",
        ) from exc
