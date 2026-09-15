#!/usr/bin/env python3
"""Validate the static liqd369 policy site without third-party dependencies."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
PAGES = [
    "index.html",
    "tile-coach.html",
    "anagram-wizard.html",
    "daily-word.html",
]
POLICY_PAGES = PAGES[1:]


class MarkupParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[str] = []
        self.links: list[str] = []
        self.meta: list[dict[str, str]] = []
        self.html_lang: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append(tag)
        attrs_dict = {key: value or "" for key, value in attrs}
        if tag == "a" and "href" in attrs_dict:
            self.links.append(attrs_dict["href"])
        if tag == "meta":
            self.meta.append(attrs_dict)
        if tag == "html":
            self.html_lang = attrs_dict.get("lang")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_page(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    parser = MarkupParser()
    parser.feed(text)

    if "<!doctype html>" not in text.lower():
        fail(errors, f"{path.name}: missing HTML5 doctype")
    if parser.html_lang != "en":
        fail(errors, f"{path.name}: expected <html lang=\"en\">")
    if "title" not in parser.tags:
        fail(errors, f"{path.name}: missing <title>")
    if "h1" not in parser.tags:
        fail(errors, f"{path.name}: missing <h1>")
    if not any(meta.get("charset", "").lower() == "utf-8" for meta in parser.meta):
        fail(errors, f"{path.name}: missing UTF-8 charset metadata")
    if not any(meta.get("name", "").lower() == "viewport" for meta in parser.meta):
        fail(errors, f"{path.name}: missing viewport metadata")
    if not (ROOT / "styles.css").exists():
        fail(errors, "styles.css: missing local stylesheet")

    if path.name in POLICY_PAGES:
        required = (
            "Data controller",
            "GitHub Pages",
            "IP address",
            "Policy version",
            "Last updated",
            "general-audience",
            "liqdmetal369@pm.me",
            "href=\"index.html\"",
        )
        for phrase in required:
            if phrase not in text:
                fail(errors, f"{path.name}: missing required disclosure or navigation: {phrase}")
        if "github.com/BartMassey/wordlists/blob/main/README-enable2k.txt" in text:
            # The source attribution is expected to remain HTTPS and explicit.
            pass

    for href in parser.links:
        parsed = urlparse(href)
        if not href or href.startswith("#") or parsed.scheme in {"mailto", "tel"}:
            continue
        if parsed.scheme:
            if parsed.scheme != "https":
                fail(errors, f"{path.name}: non-HTTPS external link: {href}")
            continue
        if parsed.scheme == "" and href.startswith("//"):
            fail(errors, f"{path.name}: protocol-relative link is not allowed: {href}")
            continue
        target_path = parsed.path or "index.html"
        target = (ROOT / target_path).resolve()
        if ROOT not in target.parents and target != ROOT:
            fail(errors, f"{path.name}: link escapes repository: {href}")
        elif not target.exists():
            fail(errors, f"{path.name}: broken internal link: {href}")


def main() -> int:
    errors: list[str] = []
    for name in PAGES:
        path = ROOT / name
        if not path.exists():
            fail(errors, f"missing required page: {name}")
        else:
            validate_page(path, errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"Validated {len(PAGES)} HTML pages and their internal links.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
