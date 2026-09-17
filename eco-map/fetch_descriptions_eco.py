#!/usr/bin/env python3
"""
fetch_descriptions_eco.py -- short public descriptions for the books of Umberto
Eco's library, from the Wikipedia edition of each book's own language first.

Eco's library is individual titles in Italian, French, Latin, German, Spanish and
English, so the lookups are keyed by book id and ask the book's own language
edition before English. The search fallback is strict: a hit is accepted only
when its title equals the whole book title (normalised: accents folded, articles and
punctuation ignored) or the title plus the author's surname.

Standalone (Python 3.8+, `requests` only).

    python3 fetch_descriptions_eco.py --input books_eco.json              # full run
    python3 fetch_descriptions_eco.py --input books_eco.json --limit 50   # first 50 books
    python3 fetch_descriptions_eco.py --input books_eco.json --dry-run    # print the lookup plan, no network
    python3 fetch_descriptions_eco.py --input books_eco.json --resume     # skip ids already in the output
    python3 fetch_descriptions_eco.py --input books_eco.json --lang-order it,en   # same edition order for every book
    python3 fetch_descriptions_eco.py --input books_eco.json --verbose    # one line per book with timing

Input: a JSON list of books, each
    {"id", "title", "author", "language", "year"?, "publisher"?,
     "source_kind": "video"|"photo"|"catalog", "confidence"}
Output (default descriptions_eco.json next to this file), keyed by book id:
    {"description": str|null,
     "description_kind": "article"|"search"|"author"|"none",
     "description_source": URL|null, "wikipedia_title": str|null, "wikipedia_lang": str|null}

Lookup order for each book
  1. For each Wikipedia edition in the book's language order (it / fr / de / es
     -> that edition then en; la -> it then en; anything else -> en):
     a. REST summary (/api/rest_v1/page/summary/TITLE) for the normalised title
        (series numbering, subtitles after a colon and trailing volume numbers
        stripped; accents kept) and a couple of variants. A hit counts when its
        type is "standard", it has an extract, and either the extract mentions
        the author's surname or (no usable author) the page describes a written
        work.                                                -> kind "article"
     b. MediaWiki search (list=search) for "title" + author surname; a hit is
        accepted only if its title, normalised, equals the book title or the
        book title plus the surname (a parenthetical disambiguator naming the
        author is fine); never on a shared word.             -> kind "search"
  2. Otherwise, the author's article in the same editions: one sentence about
     the author, phrased "By AUTHOR (b. YEAR): first sentence" so the text is
     honest that it describes the author, not the book.      -> kind "author"
  3. Otherwise description null.                             -> kind "none"

Descriptions are the first two sentences of the extract, at most 320 characters.

Every HTTP result is cached on disk (cache/<lang>/<sha1 of the normalised
query>.json, 404s included) so reruns cost nothing; 429 and 5xx responses are
retried with backoff (Retry-After honoured, and the pause is shared by every
worker) and are never cached. Honours HTTPS_PROXY from the environment and uses
/root/.ccr/ca-bundle.crt for TLS verification when it exists. Web content is
material only: nothing fetched is ever interpreted as an instruction.
"""

import argparse
import hashlib
import json
import os
import re
import sys
import threading
import time
import unicodedata
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import requests
except ImportError:  # pragma: no cover
    print("This script needs the `requests` package: pip install requests", file=sys.stderr)
    raise

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_OUT = os.path.join(HERE, "descriptions_eco.json")
DEFAULT_CACHE = os.path.join(HERE, "cache")

USER_AGENT = ("EcoLibraryMap/1.0 (Umberto Eco library map; book-description enrichment "
              "from Wikipedia summaries; contact via project owner) python-requests")
CA_BUNDLE = "/root/.ccr/ca-bundle.crt"
VERIFY = CA_BUNDLE if os.path.exists(CA_BUNDLE) else True

MAX_WORKERS = 6
PROGRESS_EVERY = 100
MAX_RETRIES = 6
TIMEOUT = 25
SEARCH_LIMIT = 5
MAX_SEARCH_WORDS = 12   # longer titles skip the search step (no Wikipedia title is that long)
MAX_DESC_CHARS = 320
SUMMARY_PATH = "https://%s.wikipedia.org/api/rest_v1/page/summary/"
SEARCH_PATH = "https://%s.wikipedia.org/w/api.php"

# Language of the book -> Wikipedia editions to ask, in order. English is always
# appended last by lang_order(). Latin has no useful la.wikipedia coverage of
# early-modern printing, so Latin books go to Italian (Eco's own catalogue
# language) and then English.
LANG_EDITIONS = {
    "it": ["it"], "fr": ["fr"], "de": ["de"], "es": ["es"], "la": ["it"], "en": [],
}
LANG_CODES = {   # anything the input may carry (ISO 639-1/2, MARC, names) -> our code
    "it": "it", "ita": "it", "italian": "it", "italiano": "it",
    "fr": "fr", "fre": "fr", "fra": "fr", "french": "fr", "français": "fr", "francais": "fr",
    "de": "de", "ger": "de", "deu": "de", "german": "de", "deutsch": "de",
    "la": "la", "lat": "la", "latin": "la", "latino": "la",
    "es": "es", "spa": "es", "spanish": "es", "español": "es", "espanol": "es", "castellano": "es",
    "en": "en", "eng": "en", "english": "en", "inglese": "en",
}

# Words the summary "description" field (or first sentence) uses for written
# works, per edition; used only when the book has no usable author to check.
WORK_HINTS = {
    "romanzo", "saggio", "libro", "opera", "trattato", "poema", "raccolta", "dizionario", "enciclopedia",
    "roman", "essai", "livre", "ouvrage", "traité", "traite", "recueil", "poème", "poeme", "dictionnaire",
    "buch", "werk", "abhandlung", "schrift", "gedicht", "sammlung", "wörterbuch", "worterbuch", "enzyklopädie",
    "novela", "ensayo", "libro", "obra", "tratado", "diccionario",
    "novel", "book", "essay", "treatise", "poem", "collection", "dictionary", "encyclopedia", "work", "text",
}
PERSON_HINTS = {   # summary "description" of a person usually carries a life span or one of these
    "scrittore", "filosofo", "poeta", "teologo", "storico", "saggista", "semiologo", "linguista", "matematico",
    "écrivain", "ecrivain", "philosophe", "poète", "poete", "théologien", "historien", "romancier",
    "schriftsteller", "philosoph", "dichter", "theologe", "historiker",
    "escritor", "filósofo", "filosofo", "teólogo", "historiador",
    "writer", "philosopher", "poet", "theologian", "historian", "novelist", "author", "scholar",
    "critic", "mathematician", "physician", "cardinal", "bishop", "priest", "monk", "jesuit",
}

# Leading articles ignored when comparing titles (per edition, all pooled).
ARTICLES = {
    "il", "lo", "la", "i", "gli", "le", "l", "un", "una", "uno",
    "le", "la", "les", "l", "un", "une", "des", "du", "de", "d",
    "der", "die", "das", "ein", "eine", "einer", "eines", "dem", "den",
    "el", "los", "las", "un", "una", "unos", "unas",
    "the", "a", "an",
}
# Particles dropped from the *end* of a surname key ("Nicolaus Cusanus" -> "cusanus";
# "de Cusa" would be "cusa"). Used when the author string has no comma.
NAME_PARTICLES = {"de", "di", "da", "del", "della", "von", "van", "der", "le", "la", "du", "des", "of", "y", "e"}

ROMAN = r"[IVXLCDM]+"
_STRIP = [
    # leading series/catalogue numbering: "12. ", "3 - ", "[2] ", "Vol. 3: ", "Tomo II. ", "Band 4 "
    re.compile(r"^\s*[\[(]?\s*\d{1,3}\s*[\])]?\s*[.:\-–—)]\s*"),
    re.compile(r"^\s*(?:vol\.?|volume|tomo|tome|band|bd\.?|libro|livre|book|parte|part)\s*(?:%s|\d+)\b\s*[.:,;\-–—]?\s*" % ROMAN, re.I),
    # subtitle after a colon (or " - " / " – " / " — " used as one)
    re.compile(r"\s*:\s.*$"),
    re.compile(r"\s+[\-–—]\s+.*$"),
    # trailing volume markers: ", vol. 2", ". Tomo I", " Band 3", " (vol. 1)", " I-II", " 1"
    re.compile(r"\s*[\[(]?\s*[.,;:\-–—]?\s*\b(?:vol\.?|volume|volumi|volumes|tomo|tomi|tome|tomes|band|bände|bde\.?|bd\.?|parte|parts?|libri?|livres?|books?)\s*(?:%s|\d+)(?:\s*[\-–—/]\s*(?:%s|\d+))?\b\s*[\])]?\s*[.,;]?\s*$" % (ROMAN, ROMAN), re.I),
    re.compile(r"\s+\b%s\b(?:\s*[\-–—/]\s*%s)?\s*$" % (ROMAN, ROMAN)),
    re.compile(r"\s+\d{1,3}(?:\s*[\-–—/]\s*\d{1,3})?\s*$"),
    # edition notes: "2a ed.", "3. Aufl.", "nuova edizione", "(ed. riveduta)"
    re.compile(r"\s*[\[(]?\s*\b(?:\d+(?:a|ª|st|nd|rd|th|e|ème|\.)?\s*|(?:nuova|neue|new|nouvelle|nueva|revised|riveduta|corretta|ampliata)\s+)?(?:ed\.|ediz\.|edizione|edition|édition|edición|aufl\.?|auflage)(?![a-z])[^)\]]*[\])]?\s*$", re.I),
    # bracketed cataloguer notes "[testo a fronte]"
    re.compile(r"\s*\[[^\]]*\]"),
]


# ----------------------------------------------------------------------------
# Normalisation
# ----------------------------------------------------------------------------

def fold(text):
    """Lowercased, accents folded, punctuation -> spaces."""
    t = unicodedata.normalize("NFKD", text or "")
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = t.replace("ß", "ss").replace("æ", "ae").replace("œ", "oe").replace("Æ", "ae").replace("Œ", "oe")
    t = re.sub(r"['’`´]", " ", t)
    t = re.sub(r"[^a-z0-9]+", " ", t.lower())
    return re.sub(r"\s+", " ", t).strip()


def title_key(text):
    """Comparison key for titles: folded, with leading articles removed everywhere.
    'Il nome della rosa' == 'nome della rosa'; 'Les Mots et les Choses' == 'mots et choses'."""
    words = [w for w in fold(text).split() if w not in ARTICLES]
    return " ".join(words)


def clean_title(title):
    """Reduce a catalogue title to something that might be a Wikipedia article name.
    Strips leading numbering, subtitles after a colon, trailing volume numbers and
    edition notes. Accents are preserved."""
    t = re.sub(r"\s+", " ", (title or "")).strip()
    if not t:
        return ""
    for _ in range(2):          # a second pass catches "Vol. 2: Foo, tomo 1"
        for pat in _STRIP:
            t = pat.sub("", t).strip()
    t = t.strip(" .,;:-–—'\"«»‘’“”")
    return re.sub(r"\s+", " ", t)


def title_variants(title):
    """Ordered distinct candidate article titles for the REST summary endpoint."""
    out = []

    def add(x):
        x = (x or "").strip()
        if len(x) >= 2 and x.lower() not in {o.lower() for o in out}:
            out.append(x)

    raw = re.sub(r"\s+", " ", (title or "")).strip()
    cleaned = clean_title(raw)
    add(cleaned)
    # first-letter capitalised (catalogue titles are often all lowercase)
    if cleaned and cleaned[0].islower():
        add(cleaned[0].upper() + cleaned[1:])
    # a one-word title is often a disambiguation page: try "Title (romanzo)"-style
    # forms only through the search step, which checks the author; nothing more here
    return out


def clean_author(author):
    """'Foucault, Michel' -> 'Michel Foucault'; strips roles and dates."""
    a = re.sub(r"\s+", " ", (author or "")).strip()
    if not a:
        return ""
    a = re.split(r"\s*;\s*|\s+(?:and|et|und|y|e)\s+(?=[A-ZÀ-Þ])", a, 1)[0]
    a = re.sub(r"\s*[\[(][^\])]*[\])]", "", a)                  # "(1401-1464)", "[a cura di]"
    a = re.sub(r"\s*<[^>]*>", "", a)                              # "<1401-1464>" (SBN style)
    a = re.sub(r"^\s*(?:by|par|von|di|de|a cura di|hrsg\.? von|ed\.|eds\.|edited by|trans\.|translated by)\s+", "", a, flags=re.I)
    a = re.sub(r",?\s*\b\d{3,4}\s*[\-–]\s*\d{0,4}\s*$", "", a)   # trailing "1401-1464"
    if "," in a:
        parts = [p.strip() for p in a.split(",") if p.strip()]
        if len(parts) >= 2 and not re.search(r"\d", parts[1]):
            a = "%s %s" % (parts[1], parts[0])
        else:
            a = parts[0]
    a = a.strip(" .,;:")
    return re.sub(r"\s+", " ", a)


def author_surname(author_clean):
    """Folded surname (last non-particle word) used to check articles and search hits."""
    words = fold(author_clean).split()
    while words and words[-1] in NAME_PARTICLES:
        words.pop()
    if not words:
        return ""
    # single-word authors ("Aristotele", "Cusanus") are their own surname
    return words[-1] if len(words[-1]) >= 3 else " ".join(words[-2:])


def normalise_lang(value):
    v = fold(value or "")
    return LANG_CODES.get(v) or LANG_CODES.get(v.split()[0] if v else "") or ""


def lang_order(book, override=None):
    if override:
        order = list(override)
    else:
        code = normalise_lang(book.get("language"))
        order = list(LANG_EDITIONS.get(code, []))
    if "en" not in order:
        order.append("en")
    seen, out = set(), []
    for l in order:
        if l and l not in seen:
            seen.add(l)
            out.append(l)
    return out


# ----------------------------------------------------------------------------
# Text
# ----------------------------------------------------------------------------

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-ZÀ-Þ\"'«“‘(])")
_ABBREV = re.compile(r"\b(?:St|Ss|Mr|Mrs|Dr|Prof|ed|vol|cap|n|pp|ca|c|sec|secc|a\.C|d\.C|v\.Chr|n\.Chr|hl|Hl|Bd|Nr|S|Jh|Jhd|approx|cf|vgl|z\.B|u\.a|usw)\.$")


def sentences(text):
    text = re.sub(r"\s+", " ", (text or "")).strip()
    if not text:
        return []
    parts, buf = [], ""
    for piece in _SENTENCE_SPLIT.split(text):
        buf = (buf + " " + piece).strip() if buf else piece
        if _ABBREV.search(buf):
            continue                      # "sec. XV" is not a sentence end
        parts.append(buf)
        buf = ""
    if buf:
        parts.append(buf)
    return parts


def trim(text, limit=MAX_DESC_CHARS):
    text = re.sub(r"\s+", " ", (text or "")).strip()
    if len(text) <= limit:
        return text
    cut = text[:limit - 1]
    # cut at the last sentence end or, failing that, the last word boundary
    m = list(re.finditer(r"[.!?](?=\s)", cut))
    if m and m[-1].end() > limit // 2:
        return cut[:m[-1].end()].strip()
    return cut[:cut.rfind(" ")].rstrip(" ,;:") + "…"


def summary_text(extract):
    return trim(" ".join(sentences(extract)[:2]))


def first_sentence(extract):
    s = sentences(extract)
    return s[0] if s else ""


def birth_year(summary):
    """Birth year of a person from a summary: the first plausible year in the
    'description' field ('Italian novelist (1932–2016)') or the first sentence."""
    for text in ((summary.get("description") or ""), first_sentence(summary.get("extract") or "")):
        m = re.search(r"\b(1[0-9]{3}|20[0-2][0-9])\b", text)
        if m:
            return m.group(1)
    return ""


# ----------------------------------------------------------------------------
# HTTP with disk cache
# ----------------------------------------------------------------------------

class Wiki:
    """Cached, rate-limit-aware client for the REST summary and search endpoints."""

    def __init__(self, cache_dir, workers=MAX_WORKERS, offline=False, verbose=False):
        self.cache_dir = cache_dir
        self.offline = offline
        self.verbose = verbose
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT, "Accept": "application/json"})
        self.lock = threading.Lock()
        self.hold_until = 0.0          # shared pause after a 429 / 5xx
        self.min_gap = 0.05 * workers  # gentle spacing between requests, overall
        self.last_start = 0.0
        self.stats = {"http": 0, "cache_hits": 0, "retries": 0, "gave_up": 0, "elapsed": 0.0}

    # -- cache ---------------------------------------------------------------
    def _cache_path(self, lang, kind, query):
        key = "%s|%s|%s" % (lang, kind, query)
        h = hashlib.sha1(key.encode("utf-8")).hexdigest()
        d = os.path.join(self.cache_dir, lang)
        os.makedirs(d, exist_ok=True)
        return os.path.join(d, "%s-%s.json" % (kind, h))

    def _cache_get(self, path):
        try:
            with open(path, encoding="utf-8") as fh:
                return json.load(fh)
        except (OSError, ValueError):
            return None

    def _cache_put(self, path, obj):
        tmp = "%s.%d.tmp" % (path, threading.get_ident())
        try:
            with open(tmp, "w", encoding="utf-8") as fh:
                json.dump(obj, fh, ensure_ascii=False)
            os.replace(tmp, path)
        except OSError:
            pass

    # -- transport -----------------------------------------------------------
    def _wait_turn(self):
        while True:
            with self.lock:
                now = time.time()
                wait = max(self.hold_until - now, self.last_start + self.min_gap - now)
                if wait <= 0:
                    self.last_start = time.time()
                    return
            time.sleep(min(wait, 5.0))

    def _get(self, url, params, label):
        """(status, json_or_None). status is the HTTP code, or 0 after giving up
        (network error / exhausted retries) -- never cached."""
        delay = 2.0
        for attempt in range(MAX_RETRIES + 1):
            self._wait_turn()
            t0 = time.time()
            try:
                with self.lock:
                    self.stats["http"] += 1
                r = self.session.get(url, params=params, timeout=TIMEOUT, verify=VERIFY)
            except requests.RequestException as e:
                with self.lock:
                    self.stats["elapsed"] += time.time() - t0
                if attempt >= MAX_RETRIES:
                    print("  ! network error for %r: %s" % (label, e), file=sys.stderr)
                    break
                time.sleep(delay)
                delay = min(delay * 2, 60)
                continue
            with self.lock:
                self.stats["elapsed"] += time.time() - t0
            if r.status_code == 429 or 500 <= r.status_code < 600:
                if attempt >= MAX_RETRIES:
                    print("  ! giving up on %r after HTTP %s" % (label, r.status_code), file=sys.stderr)
                    break
                try:
                    wait = float(r.headers.get("Retry-After") or 0)
                except ValueError:
                    wait = 0.0
                wait = min(max(wait, delay), 300.0)
                with self.lock:
                    self.stats["retries"] += 1
                    self.hold_until = max(self.hold_until, time.time() + wait)   # every worker pauses
                    if self.verbose:
                        print("  ~ HTTP %s for %r (Retry-After %s): all workers pause %.0fs"
                              % (r.status_code, label, r.headers.get("Retry-After"), wait), file=sys.stderr)
                delay = min(delay * 2, 60)
                continue
            try:
                return r.status_code, (r.json() if r.content else None)
            except ValueError:
                return r.status_code, None
        with self.lock:
            self.stats["gave_up"] += 1
        return 0, None

    def _cached(self, lang, kind, query, url, params, label):
        path = self._cache_path(lang, kind, query)
        hit = self._cache_get(path)
        if hit is not None:
            with self.lock:
                self.stats["cache_hits"] += 1
            return hit.get("status", 0), hit.get("data")
        if self.offline:
            return 0, None
        status, data = self._get(url, params, label)
        if status:
            self._cache_put(path, {"status": status, "data": data, "url": url, "params": params,
                                   "fetched": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
        return status, data

    # -- endpoints -----------------------------------------------------------
    def summary(self, lang, title):
        """REST summary dict for an article title (redirects followed), or None."""
        title = re.sub(r"\s+", " ", title or "").strip()
        if not title:
            return None
        encoded = urllib.parse.quote(title.replace(" ", "_"), safe="")
        url = SUMMARY_PATH % lang + encoded
        status, data = self._cached(lang, "summary", fold(title) + "|" + title, url,
                                    {"redirect": "true"}, "%s:%s" % (lang, title))
        if status == 200 and isinstance(data, dict):
            return data
        return None

    def search(self, lang, query):
        """List of article titles for a full-text search (may be empty)."""
        query = re.sub(r"\s+", " ", query or "").strip()
        if not query:
            return []
        params = {"action": "query", "list": "search", "srsearch": query, "srlimit": SEARCH_LIMIT,
                  "srnamespace": 0, "format": "json", "utf8": 1}
        status, data = self._cached(lang, "search", fold(query), SEARCH_PATH % lang, params,
                                    "%s:search %s" % (lang, query))
        hits = (((data or {}).get("query") or {}).get("search")) if status == 200 else None
        return [h.get("title", "") for h in (hits or []) if h.get("title")]


# ----------------------------------------------------------------------------
# Matching
# ----------------------------------------------------------------------------

def is_standard(summary):
    return isinstance(summary, dict) and summary.get("type") == "standard" and (summary.get("extract") or "").strip()


def page_url(summary):
    return ((summary.get("content_urls") or {}).get("desktop") or {}).get("page") or ""


def mentions(summary, needle):
    """Does the summary name the author? Exact word for short surnames ('eco'),
    a 5-letter word prefix for longer ones so that 'Cusanus' ~ 'Cusano' and
    'Petrarca' ~ 'Petrarch'."""
    if not needle:
        return False
    hay = " %s " % fold((summary.get("extract") or "") + " " + (summary.get("description") or ""))
    if " %s " % needle in hay:
        return True
    last = needle.split()[-1]
    if len(last) < 5:
        return False
    # Latin / vernacular name forms: 'Cusanus' ~ 'Cusa' / 'Cusano', 'Petrarca' ~ 'Petrarch'
    return any(len(w) >= 4 and (last.startswith(w) or w.startswith(last[:5])) for w in hay.split())


def looks_like_work(summary):
    words = set(fold(summary.get("description") or "").split()) | set(fold(first_sentence(summary.get("extract") or "")).split())
    return bool(words & WORK_HINTS)


def looks_like_person(summary, surname):
    desc = summary.get("description") or ""
    words = set(fold(desc).split()) | set(fold(first_sentence(summary.get("extract") or "")).split())
    if not mentions(summary, surname):
        return False
    return bool(re.search(r"\b1[0-9]{3}\b|\b20[0-2][0-9]\b", desc + " " + first_sentence(summary.get("extract") or ""))) \
        or bool(words & PERSON_HINTS)


def article_ok(summary, surname):
    """Is this summary an article about the book? With a known author the
    extract must name the author; without one the page must describe a work."""
    if not is_standard(summary):
        return False
    if surname:
        return mentions(summary, surname)
    return looks_like_work(summary)


def same_title(page_title, wanted, surname):
    """The page a summary came back with (after redirects) is about the wanted
    title: equal when normalised, or wanted plus a disambiguator / the surname."""
    return title_key(page_title) == title_key(wanted) or search_hit_ok(page_title, wanted, surname)


def search_hit_ok(hit_title, book_title, surname):
    """Accept a search hit only if its title is the whole book title (normalised)
    or the book title plus the author's surname; a parenthetical disambiguator
    is allowed when it names the author or a work-type word."""
    want = title_key(book_title)
    if not want or len(want) < 3:
        return False
    hit = hit_title or ""
    m = re.match(r"^(.*?)\s*\(([^)]*)\)\s*$", hit)
    base, paren = (m.group(1), m.group(2)) if m else (hit, "")
    got = title_key(base)
    if got == want:
        if not paren:
            return True
        pw = set(fold(paren).split())
        return (surname and surname in fold(paren)) or bool(pw & WORK_HINTS) or bool(re.search(r"\b1[0-9]{3}\b", paren))
    if surname and title_key(hit) in (want + " " + surname, surname + " " + want):
        return True
    return False


# ----------------------------------------------------------------------------
# Per-book resolution
# ----------------------------------------------------------------------------

def plan(book, override=None):
    """The lookup plan for one book: editions, title variants, author forms."""
    title = (book.get("title") or "").strip()
    author_clean = clean_author(book.get("author"))
    surname = author_surname(author_clean)
    if author_clean and fold(author_clean) in {"anonimo", "anonymous", "anonyme", "anonym", "aa vv", "aa vv", "autori vari", "various", "s n"}:
        author_clean, surname = "", ""
    return {
        "langs": lang_order(book, override),
        "variants": title_variants(title),
        "cleaned": clean_title(title),
        "author": author_clean,
        "surname": surname,
    }


def none_record():
    return {"description": None, "description_kind": "none", "description_source": None,
            "wikipedia_title": None, "wikipedia_lang": None}


def resolve(wiki, book, override=None):
    p = plan(book, override)
    surname = p["surname"]
    cleaned = p["cleaned"]

    # 1a. direct article, per edition
    for lang in p["langs"]:
        for cand in p["variants"]:
            s = wiki.summary(lang, cand)
            # redirect guard: "De docta ignorantia" on it.wikipedia redirects to
            # "Nicola Cusano" -- the page must still be titled like the book
            if s and same_title(s.get("title") or "", cand, surname) and article_ok(s, surname):
                return {"description": summary_text(s["extract"]), "description_kind": "article",
                        "description_source": page_url(s), "wikipedia_title": s.get("title") or cand,
                        "wikipedia_lang": lang}
    # 1b. search, per edition (strict title match). A quoted-phrase search on a
    # catalogue title of more than MAX_SEARCH_WORDS words (long Latin title pages,
    # often truncated by the catalogue) can never satisfy the exact-title
    # acceptance rule below, so it is not sent: every request counts against
    # Wikimedia's per-address budget.
    if cleaned and len(title_key(cleaned)) >= 3 and len(cleaned.split()) <= MAX_SEARCH_WORDS:
        for lang in p["langs"]:
            query = '"%s"' % cleaned + (" " + p["author"] if p["author"] else "")
            hits = wiki.search(lang, query)
            if not hits and p["author"]:
                hits = wiki.search(lang, '"%s"' % cleaned)
            for hit in hits:
                if not search_hit_ok(hit, cleaned, surname):
                    continue
                s = wiki.summary(lang, hit)
                if not is_standard(s):
                    continue
                # a disambiguated hit that names the author is already checked; a
                # bare one must still mention the author (or describe a work)
                if surname and not (mentions(s, surname) or surname in fold(hit)):
                    continue
                if not surname and not looks_like_work(s):
                    continue
                return {"description": summary_text(s["extract"]), "description_kind": "search",
                        "description_source": page_url(s), "wikipedia_title": s.get("title") or hit,
                        "wikipedia_lang": lang}
    # 2. the author
    if p["author"]:
        for lang in p["langs"]:
            s = wiki.summary(lang, p["author"])
            if s and is_standard(s) and looks_like_person(s, surname):
                year = birth_year(s)
                head = "By %s (b. %s): " % (p["author"], year) if year else "By %s: " % p["author"]
                sent = first_sentence(s["extract"])
                return {"description": trim(head + sent), "description_kind": "author",
                        "description_source": page_url(s), "wikipedia_title": s.get("title") or p["author"],
                        "wikipedia_lang": lang}
    return none_record()


# ----------------------------------------------------------------------------
# Driver
# ----------------------------------------------------------------------------

def load_json(path, default):
    if path and os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as fh:
                return json.load(fh)
        except (OSError, ValueError):
            pass
    return default


def save_json_atomic(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.write("\n")
    os.replace(tmp, path)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", required=True, help="JSON list of books (id, title, author, language, ...)")
    ap.add_argument("--out", default=DEFAULT_OUT, help="output JSON keyed by book id (default descriptions_eco.json)")
    ap.add_argument("--cache-dir", default=DEFAULT_CACHE, help="HTTP cache folder (default cache/ next to this file)")
    ap.add_argument("--limit", type=int, default=0, help="only the first N books")
    ap.add_argument("--dry-run", action="store_true", help="print the lookup plan for each book; no network")
    ap.add_argument("--lang-order", default="", help="comma-separated editions to ask for every book, e.g. it,en (English is always appended)")
    ap.add_argument("--resume", action="store_true", help="keep existing entries in --out and skip those ids")
    ap.add_argument("--workers", type=int, default=MAX_WORKERS)
    ap.add_argument("--offline", action="store_true", help="answer from the cache only (uncached lookups count as 404)")
    ap.add_argument("--verbose", action="store_true", help="one line per book with the result and its wall-clock time")
    args = ap.parse_args()

    books = load_json(args.input, None)
    if not isinstance(books, list):
        sys.exit("input must be a JSON list of books: %s" % args.input)
    override = [normalise_lang(x) or x.strip().lower() for x in args.lang_order.split(",") if x.strip()] or None

    results = load_json(args.out, {}) if args.resume else {}
    todo = [b for b in books if b.get("id") and (not args.resume or b["id"] not in results)]
    if args.limit:
        todo = todo[:args.limit]
    print("books: %d in %s; %d already done; %d to look up; editions override: %s"
          % (len(books), args.input, len(results), len(todo), ",".join(override) if override else "per book"))

    if args.dry_run:
        for b in todo:
            p = plan(b, override)
            print("%-12s %s | %s | %s" % (b["id"], b.get("title", ""), b.get("author", ""), b.get("language", "")))
            print("      editions: %s" % ",".join(p["langs"]))
            for v in p["variants"]:
                print("      summary  -> %s" % v)
            if p["cleaned"]:
                print('      search   -> "%s"%s   (accept only the title%s)'
                      % (p["cleaned"], " " + p["author"] if p["author"] else "",
                         " or title + '%s'" % p["surname"] if p["surname"] else ""))
            if p["author"]:
                print("      author   -> %s" % p["author"])
        return
    if not todo:
        save_json_atomic(args.out, results)
        return

    wiki = Wiki(args.cache_dir, workers=args.workers, offline=args.offline, verbose=args.verbose)
    lock = threading.Lock()
    done, kinds, times = [0], {}, []
    started = time.time()

    def work(book):
        t0 = time.time()
        rec = resolve(wiki, book, override)
        return book, rec, time.time() - t0

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(work, b) for b in todo]
        for fut in as_completed(futures):
            try:
                book, rec, dt = fut.result()
            except Exception as e:  # keep going on unexpected errors
                print("  ! worker error: %s" % e, file=sys.stderr)
                continue
            with lock:
                results[book["id"]] = rec
                done[0] += 1
                times.append(dt)
                kinds[rec["description_kind"]] = kinds.get(rec["description_kind"], 0) + 1
                if args.verbose:
                    print("  %-12s %-7s %5.2fs  %s%s" % (book["id"], rec["description_kind"], dt,
                          ("%s:%s" % (rec["wikipedia_lang"], rec["wikipedia_title"])) if rec["wikipedia_title"] else "-",
                          ("  | " + rec["description"][:90] + ("…" if len(rec["description"]) > 90 else "")) if rec["description"] else ""))
                if done[0] % PROGRESS_EVERY == 0:
                    save_json_atomic(args.out, results)
                    print("  %d/%d done, %s, %.0fs elapsed, %d HTTP requests, %d cache hits, %d retries"
                          % (done[0], len(todo), json.dumps(kinds, sort_keys=True), time.time() - started,
                             wiki.stats["http"], wiki.stats["cache_hits"], wiki.stats["retries"]))
    save_json_atomic(args.out, results)

    elapsed = time.time() - started
    print("finished: %d books in %.1fs (%.2fs per book wall-clock across %d workers, %.2fs mean per lookup); kinds %s"
          % (done[0], elapsed, elapsed / max(done[0], 1), args.workers,
             sum(times) / max(len(times), 1), json.dumps(kinds, sort_keys=True)))
    print("  HTTP: %d requests, %.2fs mean per request, %d cache hits, %d retries (429/5xx), %d given up"
          % (wiki.stats["http"], wiki.stats["elapsed"] / max(wiki.stats["http"], 1),
             wiki.stats["cache_hits"], wiki.stats["retries"], wiki.stats["gave_up"]))
    print("  wrote %s (%d entries)" % (args.out, len(results)))


if __name__ == "__main__":
    main()
