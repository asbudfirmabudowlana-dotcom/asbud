"""Walidacja i skanowanie załączników przed zapisaniem w bazie."""
import socket

from fastapi import HTTPException, status

from app.core.config import get_settings

ALLOWED_CONTENT_TYPES = {
    "application/pdf": b"%PDF-",
    "image/jpeg": b"\xff\xd8\xff",
    "image/png": b"\x89PNG\r\n\x1a\n",
}


def validate_and_scan_attachment(content: bytes, content_type: str | None) -> str:
    normalized_type = (content_type or "").lower().split(";", 1)[0].strip()
    signature = ALLOWED_CONTENT_TYPES.get(normalized_type)
    if not signature or not content.startswith(signature):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Dozwolone są wyłącznie pliki PDF, JPG oraz PNG zgodne z deklarowanym typem.",
        )

    settings = get_settings()
    if not settings.clamav_host:
        if settings.attachment_scanning_required:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Skanowanie załączników nie jest jeszcze skonfigurowane. Plik nie został zapisany.",
            )
        return normalized_type

    try:
        with socket.create_connection((settings.clamav_host, settings.clamav_port), timeout=10) as client:
            client.sendall(b"zINSTREAM\0")
            for offset in range(0, len(content), 65536):
                chunk = content[offset:offset + 65536]
                client.sendall(len(chunk).to_bytes(4, "big") + chunk)
            client.sendall((0).to_bytes(4, "big"))
            result = client.recv(4096).decode("utf-8", "replace")
    except OSError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Nie można teraz przeskanować załącznika. Plik nie został zapisany.",
        ) from exc

    if "OK" not in result:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Załącznik nie przeszedł kontroli bezpieczeństwa.")
    return normalized_type
