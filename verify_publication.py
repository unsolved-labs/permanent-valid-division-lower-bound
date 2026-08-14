#!/usr/bin/env python3
"""Post-publication HTTP verification for Unsolved Labs R014."""
from __future__ import annotations

from urllib.request import Request, urlopen

URLS = {
    "release": "https://unsolved-labs.github.io/results/r014-permanent-valid-division/",
    "repository": "https://github.com/unsolved-labs/permanent-valid-division-lower-bound",
    "theorem": "https://github.com/unsolved-labs/permanent-valid-division-lower-bound/blob/main/THEOREM.md",
    "claim": "https://github.com/unsolved-labs/permanent-valid-division-lower-bound/blob/main/claim.json",
    "source_audit": "https://github.com/unsolved-labs/permanent-valid-division-lower-bound/blob/main/SOURCE_AUDIT.md",
    "obligations": "https://github.com/unsolved-labs/permanent-valid-division-lower-bound/blob/main/proof_obligations.json",
    "verifier": "https://github.com/unsolved-labs/permanent-valid-division-lower-bound/blob/main/verify.py",
    "independent_verifier": "https://github.com/unsolved-labs/permanent-valid-division-lower-bound/blob/main/verify_independent.py",
    "stress_suite": "https://github.com/unsolved-labs/permanent-valid-division-lower-bound/blob/main/stress_rational_circuits.py",
    "workflow": "https://github.com/unsolved-labs/permanent-valid-division-lower-bound/blob/main/.github/workflows/verify.yml",
}


def fetch(name: str, url: str) -> str:
    req = Request(url, headers={"User-Agent": "unsolved-labs-r014-publication-check/1.0"})
    with urlopen(req, timeout=30) as response:
        assert response.status == 200, (name, response.status, url)
        return response.read().decode("utf-8", "replace")


release = fetch("release", URLS["release"])
assert "Permanent lower bound with valid division" in release
assert "R014" in release
assert "n²/144" in release
assert URLS["repository"] in release

for name, url in URLS.items():
    if name == "release":
        continue
    fetch(name, url)

print("PASS live R014 release route")
print("PASS canonical repository link")
print("PASS all public R014 artifact links")
