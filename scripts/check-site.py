#!/usr/bin/env python3
"""Check that local href/src/url() assets referenced by the site exist."""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
# Static pages only. blog/index.html is a Jekyll/Liquid source file (GitHub Pages
# builds it) and is not HTML-validated here. /blog/ nav links still resolve to it.
HTML_FILES = ["index.html", "projects.html", "about.html", "404.html"]
CSS_FILES = ["css/styles.css", "css/fonts.css"]


class AssetParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.refs: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {k: v or "" for k, v in attrs}
        if tag == "a" and "href" in attr_map:
            self.refs.append(("href", attr_map["href"]))
        if tag in {"link", "script", "img", "source"}:
            for key in ("href", "src"):
                if key in attr_map:
                    self.refs.append((key, attr_map[key]))
        if tag == "meta" and attr_map.get("property") in {
            "og:image",
            "og:url",
        } or attr_map.get("name") in {"twitter:image"}:
            if "content" in attr_map:
                self.refs.append(("content", attr_map["content"]))


def is_local(url: str) -> bool:
    if not url or url.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        return False
    if "{{" in url or "{%" in url:
        return False
    parsed = urlparse(url)
    if parsed.scheme in {"http", "https"}:
        return parsed.netloc in {"kailashnelson.com", "www.kailashnelson.com"}
    return not parsed.scheme


def local_path(url: str) -> Path:
    parsed = urlparse(url)
    path = unquote(parsed.path)
    if parsed.netloc in {"kailashnelson.com", "www.kailashnelson.com"}:
        path = path or "/"
    if path.startswith("/"):
        path = path[1:]
    if path in ("", "index.html"):
        return ROOT / "index.html"
    if path.endswith("/"):
        return ROOT / path / "index.html"
    directory = ROOT / path
    if directory.is_dir():
        return directory / "index.html"
    return ROOT / path


def main() -> int:
    missing: list[str] = []
    checked: set[Path] = set()

    def check(label: str, url: str, origin: Path) -> None:
        if not is_local(url):
            return
        target = local_path(url)
        if not target.is_file():
            # url() in CSS is relative to the CSS file
            if origin.suffix == ".css" and not urlparse(url).netloc:
                rel = (origin.parent / url).resolve()
                if rel.is_file():
                    checked.add(rel)
                    return
            missing.append(f"{origin.name}: {label} {url} -> {target.relative_to(ROOT)}")
        else:
            checked.add(target)

    for name in HTML_FILES:
        path = ROOT / name
        parser = AssetParser()
        parser.feed(path.read_text(encoding="utf-8"))
        for kind, url in parser.refs:
            check(kind, url, path)

    css_url_re = re.compile(r"url\((['\"]?)([^)'\"]+)\1\)")
    for name in CSS_FILES:
        path = ROOT / name
        for _, url in css_url_re.findall(path.read_text(encoding="utf-8")):
            check("url", url, path)

    if missing:
        print("Missing local assets:")
        for row in missing:
            print(f"  {row}")
        return 1

    print(f"Checked {len(checked)} local assets. All found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
