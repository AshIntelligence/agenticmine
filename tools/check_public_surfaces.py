from __future__ import annotations

import sys
import time
from urllib.error import HTTPError, URLError
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


def check(name: str, url: str, attempts: int = 3) -> tuple[bool, str]:
    last_error = "unknown error"
    for attempt in range(1, attempts + 1):
        request = Request(url, headers={"User-Agent": "AshIntelligence-public-surface-check/1.0"})
        try:
            with urlopen(request, timeout=30) as response:
                status = response.getcode()
                body = response.read(4096).decode("utf-8", errors="ignore").lower()
                if status != 200:
                    last_error = f"HTTP {status}"
                elif not body.strip():
                    last_error = "empty response body"
                else:
                    return True, f"HTTP {status}"
        except (HTTPError, URLError, TimeoutError) as exc:
            last_error = f"{type(exc).__name__}: {exc}"

        if attempt < attempts:
            time.sleep(5 * attempt)

    return False, last_error


def main() -> int:
    failures: list[str] = []
    for name, url in URLS.items():
        ok, detail = check(name, url)
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
