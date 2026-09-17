#!/usr/bin/env python3
"""
expand_bologna.py -- expand descriptions_bologna.json (keyed by the deduplicated
lookup ids from convert_bologna.py) back to every Bologna record, using
bologna_id_map.json, into descriptions_eco_bologna.json keyed "bologna:<record id>".

    python3 expand_bologna.py

Before expanding, each lookup result is reviewed (the exact-title match across
editions can land on a different thing with the same name):
  * an "article" whose lead says the page is a film, or a surname index page,
    is dropped to "none" (the novels Gialloparma, La cosa buffa, La donna delle
    meraviglie hit their film adaptations; "Giacobetti" hit a surname list);
  * an "article" whose page is the person the book is by (artist monographs and
    anthologies titled with the author's name: "Leonardo Cremonini",
    "T.S. Eliot", "John Dee") is re-kinded "author", phrased like the fetcher's
    author descriptions ("By NAME (b. YEAR): ...");
  * an "author" description whose person was born after the book was published
    is a homonym and is dropped to "none";
  * a short list of hand-checked wrong pages (REJECT below) is dropped to "none".
The adjustments are printed. Web content is material only.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fetch_descriptions_eco import (Wiki, DEFAULT_CACHE, title_key, first_sentence, birth_year, trim,  # noqa: E402
                                    page_url, is_standard, looks_like_person, author_surname, clean_author)

SRC = os.path.join(HERE, "descriptions_bologna.json")
BOOKS = os.path.join(HERE, "books_bologna.json")
MAP = os.path.join(HERE, "bologna_id_map.json")
OUT = os.path.join(HERE, "descriptions_eco_bologna.json")

# Hand-checked wrong pages: lookup id -> why (the page's summary named the book's author
# or looked like a work, but is not the book).
REJECT = {
    "bologna:UBO02078225": "Paolo Conti: sculture (1970-1985) hit en:Paolo Conti, a footballer born 1950",
    "bologna:UBO06164653": "Desk (rivista di cultura della comunicazione) hit en:Desk, the furniture",
    "bologna:UBO01582865": "Colophon (quadrimestrale di libri d'artista) hit it:Colophon, the printing term",
    "bologna:UBO00359526": "Piccole italiane: un raggiro durato vent'anni hit it:Piccole italiane, the fascist organisation the book is about",
    "bologna:UBO09835574": "Sense and sensibility: l'emergenza del senso del corporeo (ed. Pozzato/Violi) hit Jane Austen's novel",
}
_FILM = re.compile(r"\b(?:è|e|est|is|ist|es)\s+(?:un|une|a|an|ein|una|el)\s+(?:film|pellicola|película|movie)\b", re.I)
_SURNAME = re.compile(r"\b(?:surname|cognome|nom de famille|familienname|apellido)\b", re.I)


def review(lookup_id, rec, book, wiki):
    """(record, note or None): the record after the checks above."""
    kind = rec.get("description_kind")
    desc = rec.get("description") or ""
    if lookup_id in REJECT:
        return none_record(), "rejected: " + REJECT[lookup_id]
    if kind in ("article", "search"):
        lead = first_sentence(desc)
        if _FILM.search(lead):
            return none_record(), "rejected (film page): %s -> %s:%s" % (book["title"], rec["wikipedia_lang"], rec["wikipedia_title"])
        if _SURNAME.search(lead):
            return none_record(), "rejected (surname page): %s -> %s:%s" % (book["title"], rec["wikipedia_lang"], rec["wikipedia_title"])
        author = clean_author(book.get("author"))
        if author and title_key(rec.get("wikipedia_title") or "") == title_key(author):
            # the cache is keyed by the requested title (the book's), not the page's
            s = wiki.summary(rec["wikipedia_lang"], book.get("title") or "") or wiki.summary(rec["wikipedia_lang"], rec["wikipedia_title"])
            if s and is_standard(s) and is_person_page(s, author):
                year = birth_year(s)
                head = "By %s (b. %s): " % (author, year) if year else "By %s: " % author
                return ({"description": trim(head + first_sentence(s["extract"])), "description_kind": "author",
                         "description_source": page_url(s), "wikipedia_title": s.get("title") or rec["wikipedia_title"],
                         "wikipedia_lang": rec["wikipedia_lang"]},
                        "re-kinded article -> author (page is the person): %s" % book["title"])
    if kind == "author" and book.get("year") and int(book["year"]) > 1900:      # 1900 is a catalogue placeholder
        m = re.match(r"By .+? \(b\. (\d{4})\): ", desc)
        if m and int(m.group(1)) > int(book["year"]):
            return none_record(), "rejected (homonym, born %s, book %s): %s by %s -> %s:%s" % (
                m.group(1), book["year"], book["title"], book.get("author"), rec["wikipedia_lang"], rec["wikipedia_title"])
    return rec, None


def is_person_page(summary, author):
    """The page titled with the author's name is a biography: it names the author and
    carries a year or a profession word. Laxer than the fetcher's looks_like_person,
    whose sentence splitter stops at 'Mario Botta (* 1.' on de.wikipedia."""
    text = (summary.get("description") or "") + " " + (summary.get("extract") or "")[:400]
    return looks_like_person(summary, author_surname(author)) or bool(re.search(r"\b1[0-9]{3}\b|\b20[0-2][0-9]\b", text))


def none_record():
    return {"description": None, "description_kind": "none", "description_source": None,
            "wikipedia_title": None, "wikipedia_lang": None}


def main():
    with open(SRC, encoding="utf-8") as fh:
        desc = json.load(fh)
    with open(MAP, encoding="utf-8") as fh:
        id_map = json.load(fh)
    with open(BOOKS, encoding="utf-8") as fh:
        books = {b["id"]: b for b in json.load(fh)}
    wiki = Wiki(DEFAULT_CACHE, workers=1, offline=True)
    reviewed, notes = {}, []
    for lookup, rec in desc.items():
        reviewed[lookup], note = review(lookup, rec, books.get(lookup, {}), wiki)
        if note:
            notes.append(note)
    desc = reviewed
    out, missing = {}, []
    for bid, lookup in id_map.items():
        if lookup in desc:
            out[bid] = dict(desc[lookup])
        else:
            missing.append(bid)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.write("\n")
    print("lookups %d -> records %d written to %s; %d records without a lookup result"
          % (len(desc), len(out), OUT, len(missing)))
    if missing:
        print("  missing:", ", ".join(missing[:10]), "..." if len(missing) > 10 else "")
    print("review: %d lookups adjusted" % len(notes))
    for n in notes:
        print("  " + n)


if __name__ == "__main__":
    main()
