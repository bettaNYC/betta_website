#!/usr/bin/env python3
"""
Sync Goodreads shelves into books.json.

Goodreads retired its public developer API in late 2020 (no new keys, program
shut down). Public shelves still expose an RSS feed, which carries everything we
need — title, author, cover, ratings, dates. This reads those feeds and writes
a small books.json the site renders. Standard library only; no API key.

If a shelf fetch fails (network / Goodreads hiccup / blocked runner), that
shelf keeps its previous contents instead of being wiped, and the script exits
non-zero only if *every* shelf failed — so a bad run never publishes an empty
reading list.
"""
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from html import unescape

USER_ID = "194591694"                      # goodreads.com/user/show/194591694-elisabetta-rappo
SHELVES = ["currently-reading", "read"]
FEED = "https://www.goodreads.com/review/list_rss/{uid}?shelf={shelf}&per_page=100"
UA = "Mozilla/5.0 (compatible; elisabettarappo.com books sync)"
OUT = "books.json"


def _text(item, tag):
    el = item.find(tag)
    return unescape(el.text.strip()) if el is not None and el.text else ""


def fetch(shelf):
    url = FEED.format(uid=USER_ID, shelf=shelf)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        root = ET.fromstring(r.read())
    books = []
    for item in root.iter("item"):
        book_id = _text(item, "book_id")
        img = (_text(item, "book_large_image_url")
               or _text(item, "book_medium_image_url")
               or _text(item, "book_small_image_url"))
        link = (f"https://www.goodreads.com/book/show/{book_id}"
                if book_id else _text(item, "link"))
        books.append({
            "title": _text(item, "title"),
            "author": _text(item, "author_name"),
            "image": img,
            "link": link,
            "user_rating": _text(item, "user_rating"),      # "0"–"5"
            "avg_rating": _text(item, "average_rating"),
        })
    return books


def load_existing():
    try:
        with open(OUT, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def main():
    existing = load_existing()
    out, ok = {}, 0
    for shelf in SHELVES:
        try:
            out[shelf] = fetch(shelf)
            ok += 1
            print(f"{shelf}: {len(out[shelf])} books")
        except Exception as e:                              # keep last-known good
            out[shelf] = existing.get(shelf, [])
            print(f"warn: {shelf} failed ({e}); kept {len(out[shelf])} existing",
                  file=sys.stderr)

    if ok == 0:
        print("error: every shelf failed; leaving books.json unchanged", file=sys.stderr)
        sys.exit(1)

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"wrote {OUT}: " + ", ".join(f"{k} {len(v)}" for k, v in out.items()))


if __name__ == "__main__":
    main()
