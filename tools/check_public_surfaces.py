from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

URLS = {
    "demo-hub": "https://ash-intelligence-lab.streamlit.app/",
    "mautam": "https://ash-intelligence-lab.streamlit.app/?product=mautam-evaluation",
    "control-plane": "https://ash-intelligence-lab.streamlit.app/?product=agentic-product-control-plane",
    "risk-decision": "https://ash-intelligence-lab.streamlit.app/?product=fraud-signal-decision-engine",
    "support-knowledge": "https://ash-intelligence-lab.streamlit.app/?product=support-knowledge-os",
    "portfolio": "https://ashbaskaran.netlify.app/",
    "github-profile": "https://github.com/AshIntelligence",
}

REDIRECT_CODES = {301, 302, 303, 307, 308}
AUTH_MARKERS = ("login", "signin", "sign-in", "auth", "oauth")


def _safe_public_redirect(source_url: str, location: str | None) -> bool:
    if not location:
        return False
    target = urljoin(source_url, location)
    source_host = urlparse(source_url).hostname
    target_parsed = urlparse(target)
    target_host = target_parsed.hostname
    target_text = target.lower()
    return source_host == target_host and not any(marker in target_text for marker in AUTH_MARKERS)


def check(name: str, url: str, attempts: int = 2) -> tuple[str, str, bool, str]:
    last_error = "unknown error"
    for attempt in range(1, attempts + 1):
        request = Request(url, headers={"User-Agent": "AshIntelligence-public-surface-check/1.0"})
        try:
            with urlopen(request, timeout=15) as response:
                status = response.getcode()
                body = response.read(1024).decode("utf-8", errors="ignore")
                if status != 200:
                    last_error = f"HTTP {status}"
                elif not body.strip():
                    last_error = "empty response body"
                else:
                    return name, url, True, f"HTTP {status}"
        except HTTPError as exc:
            location = exc.headers.get("Location") if exc.headers else None
            if exc.code in REDIRECT_CODES and _safe_public_redirect(url, location):
                return name, url, True, f"HTTP {exc.code} same-host public redirect"
            last_error = f"HTTPError: HTTP {exc.code}"
        except (URLError, TimeoutError) as exc:
            last_error = f"{type(exc).__name__}: {exc}"

        if attempt < attempts:
            time.sleep(3)

    return name, url, False, last_error


def main() -> int:
    results = []
    with ThreadPoolExecutor(max_workers=len(URLS)) as pool:
        futures = [pool.submit(check, name, url) for name, url in URLS.items()]
        for future in as_completed(futures):
            results.append(future.result())

    failures: list[str] = []
    for name, url, ok, detail in sorted(results):
        marker = "PASS" if ok else "FAIL"
        print(f"{marker:4} {name:20} {detail}  {url}")
        if not ok:
            failures.append(name)

    if failures:
        print("\nPublic surface failures:", ", ".join(failures))
        return 1

    print("\nAll public surfaces are reachable without authentication.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
