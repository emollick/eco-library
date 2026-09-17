#!/usr/bin/env python3
"""
convert_bologna.py -- turn the Bologna (BUB) catalogue harvest of Eco's modern
books (/mnt/project-files/eco-sources/bologna_eco_modern.jsonl, 3,047 records)
into the book list that fetch_descriptions_eco.py reads.

    python3 convert_bologna.py            # writes books_bologna.json + bologna_id_map.json

books_bologna.json : one lookup per distinct (normalised title, author) pair --
                     the second volume of a work, or a second edition, collapses
                     into the first record's id.
bologna_id_map.json: {"bologna:<record id>": "bologna:<lookup id>"} for every
                     record, so that fetched descriptions can be expanded back.

Title: UNIMARC 200 $a with the SBN sorting markers ("Il *nome", "<<Les >>")
removed, a trailing " / responsibility" dropped, leading volume numbering
("1: ", "2.1.: ", "[v.] 2: ", "Vol. 1.") stripped and then
fetch_descriptions_eco.clean_title (subtitle after " : ", trailing volume
markers, edition notes). A record whose own title is only a volume number
("1", "2", "Vol. 1") takes the title of its parent record (461 $a) instead,
so that volumes of one work share a lookup.
Author: the main author (700, "Surname, Given" -> "Given Surname"; SBN
qualifiers "Bruyne, Edgar : de" -> "Edgar de Bruyne", "Giraldus : Cambrensis"
-> "Giraldus Cambrensis", "William : of#Ockham" -> "William of Ockham"), else
a 702 with author role 070, else the responsibility statement when it is a
bare personal name (no "a cura di", "edited by", "et al.", ...). Editors and
translators are never promoted to author.
Year: the harvest's `year`. Language: MARC -> ISO for ita/fre/lat/eng/ger/spa;
other codes are passed through (the fetcher treats them as English-only).
Publisher: the first 210 $c, "[s.n.]" dropped.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fetch_descriptions_eco import clean_title, title_key, fold  # noqa: E402

SRC = "/mnt/project-files/eco-sources/bologna_eco_modern.jsonl"
OUT_BOOKS = os.path.join(HERE, "books_bologna.json")
OUT_MAP = os.path.join(HERE, "bologna_id_map.json")

LANGS = {"ita": "it", "fre": "fr", "lat": "la", "eng": "en", "ger": "de", "spa": "es"}

# Name particles that a SBN qualifier may start with: "Bruyne, Edgar : de" -> "Edgar de Bruyne".
PARTICLES = {"de", "di", "da", "del", "della", "dello", "degli", "dei", "delle", "von", "van", "der", "den",
             "le", "la", "du", "des", "of", "y", "d'", "dell'", "d’", "dell’", "af", "zu", "zum", "ten", "ter"}
_VOLUME_ONLY = re.compile(r"^(?:(?:vol|volume|volumi|tomo|tomi|tome|parte|part|teil|band|bd|libro|libri|livre|book)s?\.?\s*)*"
                          r"[\d.,\-–\s]*(?:[ivxlcdm]+[.\-–\s]*)*$", re.I)
_BARE_NAME_WORD = r"(?:[A-ZÀ-Þ][\w'’.\-]*|d'[\w\-]+|d’[\w\-]+|de|di|da|del|della|von|van|der|den|le|la|du|des|of|y|e)"
_BARE_NAME = re.compile(r"^%s(?:\s+%s){1,5}$" % (_BARE_NAME_WORD, _BARE_NAME_WORD))
_ROLE_WORDS = re.compile(r"\b(?:cura|edited|editor|ed\.|eds\.|hrsg|herausgegeben|edición|édition|introduzione|introduction|"
                         r"prefazione|préface|prologo|prólogo|traduzione|translated|traduit|trad\.|testi|texte|textes|"
                         r"scritti|saggi|essays|contributi|catalogo|catalogue|comitato|società|société|society|university|"
                         r"universidad|università|biblioteca|bibliothèque|istituto|institut|centro|centre|museo|museum|"
                         r"al\.|altri|others|autres|par|by|von|and|und|with|avec|con|group|groupe|gruppo|compiled|"
                         r"ministero|ministerio|ministère|comune|città|city|fondazione|foundation|associazione|regione|"
                         r"direzione|redazione|direction|presentazione|presentación|presentation|introducción|selected|scelti|raccolti)\b", re.I)


def subfields(rec, tag):
    return [x for x in rec.get("unimarc") or [] if x.get("tag") == tag]


def strip_markers(t):
    t = re.sub(r"\s+", " ", t or "").strip()
    t = t.replace("<<", "").replace(">>", "").replace("*", "")
    t = re.sub(r"\s+/.*$", "", t)                                          # " / Arno Borst", " /Ramusio"
    # "1: ", "2.1.: ", "[v.] 2: ", "t. 2: ", "°1!: " (SBN-escaped brackets), "\\1!:"
    t = re.sub(r"^\s*(?:\[v\.\]\s*|t\.\s*|vol\.\s*)?[°\\]?\d+(?:\.\d+)*!?\.?\s*:\s*", "", t)
    m = re.match(r"^\[(.+)\]$", t.strip())                                   # "[Poesie]": a supplied title
    if m:
        t = m.group(1)
    return t.strip()


def parent_title(rec):
    """Title of the parent record (461 $a, first occurrence) for a volume record."""
    for x in subfields(rec, "461"):
        for k, v in x.get("sub") or []:
            if k == "a" and v.strip():
                return strip_markers(v)
    return ""


def is_volume_only(t):
    return not t or bool(_VOLUME_ONLY.match(t))


def book_title(rec):
    """(cleaned title, used_parent). Falls back to the parent record's title for bare volumes."""
    own = clean_title(strip_markers(rec.get("title") or ""))
    if not is_volume_only(own):
        return own, False
    parent = clean_title(parent_title(rec))
    if parent and not is_volume_only(parent):
        return parent, True
    return own or strip_markers(rec.get("title") or ""), False


def swap_name(base):
    """'Surname, Given <1932-2016>' -> 'Given Surname'. Unlike fetch_descriptions_eco.clean_author
    this never strips a leading 'De'/'Di'/'Von' that is part of the surname ('De Sanctis, Francesco')."""
    a = re.sub(r"\s*<[^>]*>|\s*\([^)]*\)", "", base).strip()
    a = re.sub(r",?\s*\b\d{3,4}\s*[\-–]\s*\d{0,4}\s*$", "", a)
    if "," in a:
        parts = [p.strip() for p in a.split(",") if p.strip()]
        if len(parts) >= 2 and not re.search(r"\d", parts[1]):
            a = "%s %s" % (parts[1], parts[0])
        elif parts:
            a = parts[0]
    return re.sub(r"\s+", " ", a).strip(" .,;:")


def clean_name(name):
    """SBN heading -> 'Given Surname'. Handles the ' : qualifier' form."""
    s = re.sub(r"\s+", " ", (name or "").replace("_", " ").replace("#", " ")).strip()
    if not s:
        return None
    base, _, qual = s.partition(" : ")
    base, qual = base.strip(), qual.strip(" .,")
    had_comma = "," in base
    given_surname = swap_name(base)                # "Surname, Given" -> "Given Surname"; dates stripped
    if not given_surname:
        return None
    if qual:
        qw = qual.split()
        if had_comma:
            if qw[0].lower() in PARTICLES or re.match(r"^d[’']", qw[0], re.I):
                # "Bruyne, Edgar : de" -> "Edgar de Bruyne"; "Ormesson, Jean : d'" -> "Jean d'Ormesson"
                parts = [p.strip() for p in base.split(",", 1)]
                surname, given = parts[0], (parts[1] if len(parts) > 1 else "")
                joiner = "" if re.match(r".*[’']$", qual) else " "
                given_surname = ("%s %s%s%s" % (given, qual, joiner, surname)).strip()
            # "Monboddo, James : Burnett, Lord": the qualifier is not a name particle; ignore it
        else:
            # "Giraldus : Cambrensis", "William : of Ockham", "Tommaso : d'Aquino"
            given_surname = given_surname + " " + qual
    given_surname = re.sub(r"\s+", " ", given_surname).strip(" .,")
    if not given_surname or re.search(r"\d", given_surname):
        return None
    return given_surname


def bare_name(resp):
    """The responsibility statement when it names one person and nothing else."""
    s = re.sub(r"\s+", " ", resp or "").strip(" .")
    if not s or any(c in s for c in "[]\\!;,&/()"):
        return None
    if "..." in s or _ROLE_WORDS.search(s):
        return None
    s = re.sub(r"^(?:di|by|par|von|de)\s+(?=[A-ZÀ-Þ])", "", s)
    if not _BARE_NAME.match(s):
        return None
    words = s.split()
    if len(words) < 2 or len(words) > 5 or not any(w[0].isupper() for w in words[1:]):
        return None
    return s


def book_author(rec):
    a = clean_name(rec.get("author"))
    if a:
        return a
    for p in rec.get("persons") or []:
        if p.get("tag") == "702" and p.get("role") == "070" and not p.get("bub_only"):
            a = clean_name(p.get("name"))
            if a:
                return a
    return bare_name(rec.get("responsibility"))


def book_publisher(rec):
    pubs = rec.get("publisher") or []
    for p in pubs:
        p = re.sub(r"\s+", " ", p).split(" ; ")[0].strip(" .,[]()")
        if p and not re.match(r"^s\.\s*n\.?$", p, re.I):
            return p
    return None


def book_language(rec):
    langs = rec.get("language") or []
    code = (langs[0] if langs else "").strip().lower()
    return LANGS.get(code, code or None)


def main():
    with open(SRC, encoding="utf-8") as fh:
        rows = [json.loads(line) for line in fh if line.strip()]
    books, id_map, groups = [], {}, {}
    n_parent = 0
    for r in rows:
        bid = "bologna:%s" % r["id"].strip()
        title, used_parent = book_title(r)
        n_parent += used_parent
        author = book_author(r)
        tkey = title_key(title)
        key = ("t", tkey, fold(author or "")) if tkey else ("v", bid)
        if key in groups:
            id_map[bid] = groups[key]
            continue
        groups[key] = bid
        id_map[bid] = bid
        books.append({
            "id": bid, "title": title, "author": author,
            "language": book_language(r), "year": r.get("year"), "publisher": book_publisher(r),
            "source_kind": "catalog", "confidence": "high",
        })
    with open(OUT_BOOKS, "w", encoding="utf-8") as fh:
        json.dump(books, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    with open(OUT_MAP, "w", encoding="utf-8") as fh:
        json.dump(id_map, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.write("\n")
    print("records %d -> lookups %d (%d with an author, %d without; %d volume records took their parent's title); wrote %s and %s"
          % (len(rows), len(books), sum(1 for b in books if b["author"]),
             sum(1 for b in books if not b["author"]), n_parent, OUT_BOOKS, OUT_MAP))


if __name__ == "__main__":
    main()
