"""Lekki limit żądań dla pojedynczej instancji aplikacji.

Chroni logowanie i kosztowne funkcje AI przed prostym nadużyciem. Dla wielu
instancji należy zastąpić go limitem opartym o Redis lub bramę sieciową.
"""
from collections import defaultdict, deque
from threading import Lock
from time import monotonic

from fastapi import HTTPException, Request, status

_requests: dict[str, deque[float]] = defaultdict(deque)
_lock = Lock()


def client_address(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for", "")
    if forwarded:
        return forwarded.split(",", 1)[0].strip() or "unknown"
    return request.client.host if request.client else "unknown"


def enforce_rate_limit(key: str, maximum: int, window_seconds: int) -> None:
    now = monotonic()
    with _lock:
        entries = _requests[key]
        cutoff = now - window_seconds
        while entries and entries[0] <= cutoff:
            entries.popleft()
        if len(entries) >= maximum:
            retry_after = max(1, int(window_seconds - (now - entries[0])))
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Za dużo prób. Spróbuj ponownie później.",
                headers={"Retry-After": str(retry_after)},
            )
        entries.append(now)
