#!/usr/bin/env python3
"""
convert_braidense.py -- turn the Braidense catalogue export of Eco's rare books
(/mnt/project-files/eco-sources/braidense_eco_all.csv) into the book list that
fetch_descriptions_eco.py reads.

    python3 convert_braidense.py            # writes books_braidense.json + braidense_id_map.json

books_braidense.json : one lookup per distinct (normalised title, author) pair --
                       multi-volume records collapse into the first record's id.
braidense_id_map.json: {"braidense:<bid>": "braidense:<lookup id>"} for every row,
                       so that fetched descriptions can be expanded back to all bids.

Author: from the responsibility statement, with roles ("a cura di", "par",
"by", "von", "compiled by", honorifics ...) dropped and only the first name
kept. Statements that name no person ("par l'auteur de ...", "par une Société
de professeurs") give author null. Year: first 4-digit year in `date`, else
the catalogue's `year` column. Language: MARC -> ISO for ita/fre/lat/eng/ger/spa;
other MARC codes are passed through unchanged.
"""
import csv
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fetch_descriptions_eco import clean_title, title_key, fold  # noqa: E402

SRC = "/mnt/project-files/eco-sources/braidense_eco_all.csv"
OUT_BOOKS = os.path.join(HERE, "books_braidense.json")
OUT_MAP = os.path.join(HERE, "braidense_id_map.json")

LANGS = {"ita": "it", "fre": "fr", "lat": "la", "eng": "en", "ger": "de", "spa": "es"}

# Role phrases and honorifics that precede the name; stripped repeatedly.
_ROLE = re.compile(r"""^(?:
    a\ cura\ (?:di|de|del|della|dell'\s*)|per\ cura\ (?:di|dell'|del)|edizione\ critica\ a\ cura\ di|
    edited\ by|compiled\ by|collated\ and\ re-told\ by|conceived\ and\ formed\ by|
    with\ an\ introduction\ by|introduction\ and\ commentary\ by|introduction\ by|introduction:|
    catalogue\ rédigé\ par|catalogued\ by|katalogbearbeitung:|redaktion\ des\ katalogs:|
    samenstelling\ van\ tentoonstelling\ en\ catalogus:|eindredactie|
    herausgegeben\ von|hrsg\.?\ von|neubearbeitet\ von|edidit|
    volgarizzato\ da|svelati\ da|raccontata\ al\ popolo\ da|narrate\ e\ descritte\ da|
    compilata\ su\ documenti\ e\ relazioni\ autentiche\ dall'|ed\ esposta\ con\ ordine\ alfabetico\ da|
    tratte\ dalle\ lezioni\ di\ ugo\ blair\ dal|leggenda\ popolare\ pubblicata\ da|
    inventato,\ e\ pubblicato\ dal|inventée\ par|dettato\ dal|ricordi\ di|saggio\ del|studio\ di|
    opera\ del|opera|avvertimenti\ del|prefazione\ di|avant-propos\ de|precede\ d'une\ notice[^ ]*(?:\ [^ ]+)*?\ par|
    publi[ée]e?\ par|démontrée\ \.\.\.\ par|cum\ cura\ et\ studio\ scripsit|
    traduit\ de\ language\ italien\ en\ français\ par|from\ the\ latin\ of(?:\ a\ posthumous\ work\ of)?|
    compuesta\ por\ el|
    par|by|von|di|de|da|dai|dal|dall'\s*|del|dell'\s*|per|
    m\.r\.p\.|r\.p\.|mm\.|m\.|mr\.|sir|dr\.?|docteur|dottor|prof\.|professori|avv\.|avvocato|
    l'abbé|abbé|l'abate|abate|canonico|cav\.|le\ chevalier|chevalier|chavalier|le\ chavalier|conte|barone|
    padre|p\.|d\.|fr\.|colonel|madame|veuve|nobile\ signor|celebre|le\ docteur|le\ dr|le\ p\.|le|the|
    gius\.|giov\.
)\s+""", re.I | re.X)

# A statement that names no person at all.
_ANON = re.compile(r"^(?:l'auteur\b|l'un\b|un\ contemporain|une\ soci[eé]t[eé]|les\ auteurs|auß\b|zum\ ersten|"
                   r"in\ zusammenarbeit|bearbeitet|reproduced|with\ illustrations|\d)", re.I | re.X)
# A statement that names only a preface or introduction writer, not the author.
_PREFACE = re.compile(r"^(?:prefazione|prefaz\.|introduzione|introduction|avant-propos|préface|preface|vorwort|"
                      r"with\ an\ introduction|introduction\ and\ commentary|edited\ with\ an\ introduction)\b", re.I | re.X)


def clean_author(resp):
    s = re.sub(r"\s+", " ", resp or "").strip()
    if not s:
        return None
    # "[i.e. Real Name]" / "[i.e. Real Name!" : the cataloguer's identification wins
    m = re.search(r"\[i\.e\.\s*([^\]!]+)", s)
    if m:
        s = m.group(1)
    s = s.replace("\\", "").replace("!", "").replace("[", "").replace("]", "")
    s = s.split(";")[0]
    s = re.sub(r"\.\.\..*$", "", s)                     # "Umberto Eco ... [et al.]"
    s = re.sub(r"\s*\([^)]*\)", "", s)                  # "(avv. Emilio Bossi)", "(G. Encausse)"
    s = s.strip(" .,:")
    if _PREFACE.match(s):
        return None
    # elided-article roles glued to the name: "a cura dell'Instituo", "dall'avvocato ..."
    s = re.sub(r"^(?:a cura |per cura |compilata su documenti e relazioni autentiche )?d[ae]ll'\s*", "", s, flags=re.I)
    for _ in range(6):
        t = _ROLE.sub("", s).strip()
        if t == s:
            break
        s = t
    if not s or _ANON.match(s):
        return None
    # first person only
    s = re.split(r"\s*(?:,|/|\s&\s|\s(?:e|et|and|und|y)\s(?=[A-ZÀ-Þ]))", s, 1)[0]
    s = re.sub(r"\s+(?:dit|de la Compagnie|author of|dottore in|également)\b.*$", "", s, flags=re.I)
    s = s.strip(" .,:-")
    if not s or len(s) > 60 or len(s.split()) > 7 or re.search(r"\d", s):
        return None
    return s


def year_of(row):
    m = re.search(r"\b(1[0-9]{3}|20[0-2][0-9])\b", row.get("date") or "")
    if m:
        return int(m.group(1))
    m = re.search(r"\b(1[0-9]{3}|20[0-2][0-9])\b", row.get("year") or "")
    return int(m.group(1)) if m else None


def main():
    with open(SRC, encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    books, id_map, groups = [], {}, {}
    for r in rows:
        bid = "braidense:%s" % r["bid"].strip()
        title = re.sub(r"\s+", " ", r["title"]).strip()
        author = clean_author(r["responsibility"])
        akey = fold(author or "")
        tkey = title_key(clean_title(title))
        if tkey and not re.fullmatch(r"(?:[0-9]+|[ivxlcdm]+)(?: [0-9ivxlcdm]+)*", tkey):
            key = ("t", tkey, akey)
        else:   # bare volume records ("Vol. 1.", "2"): one lookup per author + shelfmark set
            key = ("v", akey, r.get("all_shelfmarks") or r.get("shelfmark") or bid)
        if key in groups:
            id_map[bid] = groups[key]
            continue
        groups[key] = bid
        id_map[bid] = bid
        books.append({
            "id": bid, "title": title, "author": author,
            "language": LANGS.get((r.get("lang") or "").strip().lower(), (r.get("lang") or "").strip().lower() or None),
            "year": year_of(r), "publisher": None,
            "source_kind": "catalog", "confidence": "high",
        })
    with open(OUT_BOOKS, "w", encoding="utf-8") as fh:
        json.dump(books, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    with open(OUT_MAP, "w", encoding="utf-8") as fh:
        json.dump(id_map, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.write("\n")
    print("rows %d -> lookups %d (%d authors, %d without); wrote %s and %s"
          % (len(rows), len(books), sum(1 for b in books if b["author"]),
             sum(1 for b in books if not b["author"]), OUT_BOOKS, OUT_MAP))


if __name__ == "__main__":
    main()
