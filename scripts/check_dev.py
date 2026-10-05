#!/usr/bin/env python3
"""Read-only availability probe for the authorized DEV host."""
import json
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

DEV_URL = "https://dev.gcreation.agency/"


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def check():
    request = Request(DEV_URL, headers={"User-Agent": "gCreation-DEV-Availability/0.1"})
    with build_opener(NoRedirect).open(request, timeout=20) as response:
        html = response.read(1024 * 1024).decode("utf-8", errors="replace")
        title = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
        return {
            "url": DEV_URL,
            "status": response.status,
            "title": title.group(1).strip() if title else None,
            "wordpress_api_advertised": "api.w.org" in response.headers.get("Link", ""),
            "noindex_present": bool(re.search(r'<meta\b[^>]*name=[\"\']robots[\"\'][^>]*content=[\"\'][^\"\']*noindex', html, re.I)),
            "mvp_acceptance_verified": False,
        }


if __name__ == "__main__":
    try:
        print(json.dumps(check(), indent=2))
    except (HTTPError, URLError, TimeoutError, OSError) as error:
        print(json.dumps({"url": DEV_URL, "error": str(error)}), file=sys.stderr)
        sys.exit(1)
