from __future__ import annotations

import httpx

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)
DEFAULT_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
}


def http_get(
    url: str,
    *,
    timeout_sec: float = 90.0,
    headers: dict[str, str] | None = None,
    referer: str | None = None,
) -> httpx.Response:
    req_headers = dict(DEFAULT_HEADERS)
    if headers:
        req_headers.update(headers)
    if referer:
        req_headers["Referer"] = referer
    with httpx.Client(
        timeout=httpx.Timeout(timeout_sec),
        headers=req_headers,
        follow_redirects=True,
    ) as client:
        return client.get(url)
