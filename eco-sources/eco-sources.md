# Umberto Eco's Milan library (Piazza Castello 13): public non-video sources

The public sources for Umberto Eco's Milan library: catalogue routes, photographs, visitor
accounts, and the numbers each of them supports. Every claim carries the URL it comes from. The
files that hold the data taken from these sources are listed in `README.md`.

---

## 0. Headline numbers (authoritative sources)

| Figure | Value | Source |
|---|---|---|
| Working ("modern") library, total | c. 44,000 vols = Milan c. 33,000 + Monte Cerignone c. 11,000 | Fondazione U. Eco, "Le biblioteche" (fondazioneumbertoeco.org/lebiblioteche); Unibo Magazine 17 Jun 2021 |
| Milan working library moved to Bologna | "oltre 32.000 volumi", transfer spring 2026; opened 1-2 July 2026 | site.unibo.it/eco/it/chi-siamo; Unibo Magazine "Eco library opens in Bologna"; ANSA 1 Jul 2026 |
| Biblioteca Eco (Bologna) space | 600 linear metres of shelving; c. 200 m2 + walkways; 10 thematic rooms; former custodian's flat, 20th-c. wing of Palazzo Poggi, entrance Piazza Puntoni 2 | Il Resto del Carlino 2 Jul 2026 ("sono 600 i metri lineari"); DIRE 17 Jun 2021 ("oltre 200 metri quadrati ... più i ballatoi"); BolognaToday 1 Jul 2026 ("10 sale tematiche") |
| Biblioteca Eco counts on its own site | "+30.000 documenti, +1.000 fumetti, +300 periodici, +2.200 opere di Eco, +600 opere su Eco, 50 lingue" | eco.sba.unibo.it / site.unibo.it/eco/it |
| Annotated / inscribed copies | c. 2,500 annotated; c. 5,000 with dedications | Unibo Magazine 17 Jun 2021; DIRE 17 Jun 2021 |
| Cataloguing status, Bologna (July 2026) | "Restano due operazioni da compiere prima di aprire decisamente al pubblico, una catalogazione dei volumi e la loro magnetizzazione completa" (F. Citti, president BUB) | Il Resto del Carlino 2 Jul 2026 |
| Already catalogued in SBN-UBO with possessor "Eco, Umberto" at BUB | **3,047 records** | sol.unibo.it query, see 1.2 |
| First tranche catalogued/digitised | 2,500 most-annotated volumes, MiC-funded, from 2021 ("Abulafia" project) | Il Resto del Carlino; DIRE 2021 |
| Rare books ("Bibliotheca semiologica curiosa lunatica magica et pneumatica") | c. 1,200 pre-1900 editions, 36 incunabula, "380 volumi fra '500 e '800"; c. 1,000 not previously at Braidense, c. 300 absent from all Italian public collections; arrived July/Aug 2021 in **73 boxes = 1,328 volumes** | ANSA 1 Feb 2021; MilanoToday; Rivista Studio 8 May 2022 ("73 scatole, per un totale di 1328 volumi"); AIB Studi 62(2022) Nuovo & Coletto |
| Rare books catalogued in Braidense OPAC | **2,105 records with shelfmark ECO.xx** / 1,634 with possessor "Eco, Umberto" | opac.braidense.it, see 1.1 |
| Fondazione's own inventory | "La Fondazione ha inventariato i libri di Umberto Eco (circa 35.000 oltre a 1200 libri rari) ... Gli elenchi sono a disposizione del Ministero della Cultura, dell'Università di Bologna e della Biblioteca Braidense" (not public) | fondazioneumbertoeco.org/progetti |
| Eco's own statements | "I have 50,000 books in my various homes ... I also have 1,200 rare titles" (Carrière/Eco, *This Is Not the End of the Book*); "thirty thousand volumes ... another twenty thousand at his manor" (Paris Review 2008) | see section 3 |
| Wikidata | Q35029860 "Umberto Eco's library": P1436 collection size 30,000 and 20,000; owned by Q12807 (Unibo) / Q1347047 (Braidense) | wikidata.org/wiki/Q35029860 |

---

## 1. Catalogues / inventories

### 1.1 Biblioteca Nazionale Braidense OPAC (rare books): exportable and shelf-ordered

- Entry: http://opac.braidense.it/. Software: Inera "opaclib" (Solr backend `db=solr_braidense`), same engine as the old SBN OPAC. Advanced form `/opac_braidense/opac/braidense/avanzata.jsp`. Field list includes `Possessori:2390`, `Collocazione:901` (Braidense shelfmark), `Any:1016`, `BID:1032`, filters for language (`filter:54:Lingua`), country, year range, doc type.
- Landing page for the fund: https://bibliotecabraidense.org/collezione/fondo-umberto-eco/: "circa 1.300 titoli rari ... 36 incunaboli", Studiolo Umberto Eco open since 5 May 2022, Via Brera 28; links OPAC and https://cloud.sbn.it/servizi.

**Queries (all GET):**

1. Possessor search, `Possessori = Eco, Umberto` → **1,634 records**:
   `http://opac.braidense.it/opac_braidense/opaclib?db=solr_braidense&select_db=solr_braidense&nentries=20&from=1&searchForm=opac/braidense/avanzata.jsp&resultForward=opac/braidense/brief.jsp&do_cmd=search_show_cmd&saveparams=true&fieldstruct:1=ricerca.parole_tutte:@and@&fieldaccess:1=Possessori:2390&fieldval:1=Eco,+Umberto`
2. Shelfmark search, `Collocazione (Braidense) = ECO` → **2,105 records** (the larger, better set: every physical copy in the fund, incl. records where the possessor link was not added):
   same URL with `fieldaccess:1=Collocazione:901&fieldval:1=ECO`
3. Paging: `nentries` 10/20/30/50 via the form (`nentries=50` works when combined with `saveparams=true` form params; the `rpnquery` variant with 50 fails). `from=N` pages. Sort: `Rilevanza / Titolo / Autore / Data`.
4. Full record: `...resultForward=opac/braidense/full.jsp&nentries=1&from=N`. Permalinks also exist as `http://opac.braidense.it/bid/<BID>`.
5. **Bulk UNIMARC export** (Content-Type `text/x-marc`, ISO 2709). It needs the JSESSIONID cookie of a prior search in the same session and the Solr RPN query. Batches of 500 work, so the whole fund takes 5 requests:
   ```
   curl -c cj -b cj "http://opac.braidense.it/opac_braidense/opaclib?db=solr_braidense&select_db=solr_braidense&nentries=20&from=1&searchForm=opac/braidense/avanzata.jsp&resultForward=opac/braidense/brief.jsp&do_cmd=search_show_cmd&saveparams=true&fieldstruct:1=ricerca.parole_tutte:@and@&fieldaccess:1=Collocazione:901&fieldval:1=ECO"
   for from in 1 501 1001 1501 2001; do
     curl -c cj -b cj -o eco_$from.mrc "http://opac.braidense.it/opac_braidense/opaclib?db=solr_braidense&select_db=solr_braidense&nentries=500&from=$from&searchForm=opac/braidense/error.jsp&resultForward=opac/braidense/scarico_uni.jsp&do_cmd=search_show_cmd&format=unimarc&rpnlabel=Collocazione&rpnquery=%40attrset+bib-1++%40attr+1%3D901+%40attr+4%3D2+%22ECO%22&totalResult=2105&fname=none"
   done
   ```
   The same export with the *possessor* RPN query fails, and so does `format=xml`. Per-record "Scarico Unimarc" and "Citazioni" links exist on every full record. No SRU or Z39.50 endpoint is advertised; SBN's national Z39.50 covers the same BIDs.

**Record fields** (from the UNIMARC and the HTML full view): BID (001), title/responsibility, edition (205), imprint (210), physical description (215), fingerprint (012, for antiquarian), language (101), country (102), notes (300, 316 binding/ex-libris notes with `$5 IT-MI0185 ECO. xx. xxxx`), 317 provenance note "Possessore: Eco, Umberto", names (700/702/712) incl. `702 Eco, Umberto $4 390` (former owner) and printers/booksellers, holdings 950 with `$d NBECO. xx. xxxx` shelfmark, inventory number, "Sala manoscritti", "Consultazione antichi e di pregio – richiedere in Sala Manoscritti o b-brai.libroantico@cultura.gov.it".

**Do the shelfmarks encode physical order? Yes.** Shelfmark = `ECO.<section>.<running number>[/<vol>]`. Il Foglio 5 May 2022: "arrivati in 73 scatole, sono stati riposizionati secondo la suddivisione originaria (catalogazione ECO.01 e così via)"; AIB Studi 2022: books "disposti nelle scaffalature nello stesso ordine ideato dal professore per la sua abitazione"; Braidense/Scalpendi: "custodito nello stesso ordine in cui si trovava nella casa milanese". Parsed distribution of the 2,105 records (2,103 have a shelfmark):

| Section | records | max running no. | content (from samples) |
|---|---|---|---|
| ECO.01 | 1,570 | 1107 | main "curiosa/lunatica/magica" run: hermetica, Fludd, Kircher, Boaistuau 1560, Rosicrucians ... |
| ECO.02 | 372 | 169 | 19th-c. French sets (Dumas, Sue, Tallemant, Péladan, "fous littéraires") |
| ECO.03 | 51 | 77 | incunabula and earliest books (Alanus de Insulis c.1473, Panormitanus c.1490, Malleus, Albumasar, Hermes Trismegistus) |
| ECO.04 | 110 | 102 | Eco's own works kept in the room (Trattato di semiotica generale 1975, Il Medioevo, Diario minimo ...) |

Language of the 2,105: fre 652, lat 614, ita 511, eng 169, ger 123, grc 12 ... Date (100$a): 15th c. 36, 16th 231, 17th 530, 18th 361, 19th 521, 20th 315, 21st 103. Records with possessor field = 1,633.

**Five sample records (from full.jsp):**
1. VEAE142687: Boaistuau, Pierre. *Histoires prodigieuses ...* Paris: Longis & Le Mangnier, 1560. 4°. FRE. Coll. IT-MI0185 **ECO. 01. 0227**; "Legatura in pergamena. Ex libris sul contropiatto anteriore"; Possessore: Eco, Umberto; Sala manoscritti.
2. MIL1038655: Dumas, Alexandre. *Le bâtard de Mauléon*, vol. 1. Paris: Calmann Lévy, 1887. 282 p.; 19 cm. FRE. Coll. **ECO. 02. 0160/1**, inv. 900028192.
3. MIL1038657: idem, vol. 2. Coll. **ECO. 02. 0160/2**, inv. 900028193.
4. MIL1038851: Tallemant des Réaux, *Les historiettes*, vol. 5, 3rd ed. Paris: Techener, 1856. Coll. **ECO. 02. 0165/5**, inv. 900028212; "Timbro ex libris sul recto della carta di guardia".
5. PUV0675761: Theobald, Bertram G. *Francis Bacon concealed and revealed*. London: Cecil Palmer, 1930. XIII, 389 p. ENG. Coll. **ECO. 01. 0523**, inv. 001417504; "Ex libris sul verso della carta di guardia".

Coverage: the whole rare-book collection (1,328 physical volumes -> 2,105 catalogue records incl. multi-volume parts and some later additions). **This is the authoritative title list for the rare books.**

### 1.2 University of Bologna, SBN-UBO SebinaYOU (sol.unibo.it): 3,047 records so far

- The Biblioteca Eco's own site (https://site.unibo.it/eco/it/cataloghi-e-risorse-online/cataloghi) publishes a ready-made query "**Documenti provenienza Umberto Eco - BUB** – Lista di documenti bibliografici appartenuti a Umberto Eco presenti in Biblioteca Universitaria":
  `https://sol.unibo.it/SebinaOpac/query/KF_XP:%22eco%20umberto%22%20KF_BIBVIRT:ubobu?context=catalogo`
  → "Possessore: eco umberto AND Biblioteca: B. Universitaria — **Risultati 1 - 10 di 3047**". Without the library filter the same possessor key gives 3,050 (3 elsewhere in the Polo).
- Record pages: `https://sol.unibo.it/SebinaOpac/resource/<UBO id>` (e.g. UBO04526278 Terrinoni, *James Joyce e la fine del romanzo*, 2015; UBO05644199 Galli, *Hitler e il nazismo magico*, 2015; UBO03806838 Palumbo, *Frontespizi*, 2012; UBO10375041 *The List: the uses and pleasures of cataloguing*, 2024). Fields: title, author, imprint, ISBN, OCLC, series, subjects, Dewey, year. **Holdings/shelfmark for BUB are not in the static HTML** (loaded by JS); "Biblioteca Eco" is not (yet) a separate library code in the Polo list (`/SebinaOpac/article/biblioteche`), the Eco copies sit under "B. Universitaria" (`pb=UBOBU`).
- Access notes: result list is 10 per page; paging and sort are JavaScript POST actions (`page=`, `pag=`, `start=` GET params are ignored, and all return page 1); RSS "salva ricerca" requires login; no CSV/MARC export exposed; OpenSearch descriptor exists (`/SebinaOpac/sebinayou/ext/sebinayou.xml`) but only for simple q=. Enumerating the 3,047 records therefore needs either the JS pagination or per-record lookups.
- AlmaStart (Primo VE) REST API works anonymously: guest JWT `https://almastart.unibo.it/primaws/rest/pub/institution/39UBO_INST/guestJwt?viewId=39UBO_INST:VU&lang=it`, then `https://almastart.unibo.it/primaws/rest/pub/pnxs?...&q=any,contains,<term>&vid=39UBO_INST:VU` (JSON, with `info.total`). It does not index the "possessore" key, and a title held only in Eco's library (the Finnish *Ruusun nimi*) does not appear in it, so the Eco holdings are not yet discoverable there.
- Interpretation: c. 3,000 of the ~32,000 Milan volumes are catalogued today (the 2,500 annotated books of the 2021-22 MiC-funded tranche plus later work); cataloguing continues (Citti, July 2026).

### 1.3 SBN national OPAC (opac.sbn.it): a Liferay front-end rendered in the browser, so plain GET does not reach the results
- Advanced search has field `Possessore_precedente:2390` and library facet (`facet_biblioteca`), but `/o/opac-api/results` answers 404 to GET and the result page `risultati-ricerca-avanzata?item:2390:Possessore_precedente:nocheck=Eco,%20Umberto` is rendered client-side. The Braidense BIDs (MIL..., VEAE..., PUV..., BVEE...) are SBN records, so the same 1,634+ appear there; the SBN Z39.50/SRU service (cloud.sbn.it/servizi) is the machine route.
- Internet Culturale, MANUS, Europeana: nothing relevant (Europeana API `api2demo` query "Umberto Eco" AND Braidense → 1 unrelated hit). The fund contains no manuscripts.

### 1.4 Published lists (print / PDF)
- Nuovo, A. & Coletto, A., "Gli incunaboli di Umberto Eco", *AIB Studi* 62/1 (2022) 9-25, DOI 10.2426/aibstudi-13386. PDF: https://aibstudi.aib.it/article/download/13386/224 (914 KB; the copy here is `aib_224.pdf`). Contains the complete numbered list of the **36 incunabula** with ISTC numbers and Eco's own transcribed catalogue cards ("schede" = A4 computer print-outs glued to card, recording provenance, price, comparanda). Also states the fund was inventoried and pre-catalogued by 2022 and displayed "nello stesso ordine ideato dal professore".
- *L'idea della biblioteca. La collezione di libri antichi di Umberto Eco alla Biblioteca Braidense*, eds. Bradburne, Lorusso, Fedriga, Marmo, Pisanty, Sherman. Milan: Scalpendi, 2022, 176 pp., ISBN 9791259551054 (exhibition catalogue, 5 May–2 Jul 2022; selection only, not a full inventory).
- Braidense press release Feb 2021: https://bibliotecabraidense.org/wp-content/uploads/2021/02/CS_Umberto-Eco-Braidense.pdf (the link resolves to HTML; the ANSA text says the same).
- No public PDF/spreadsheet inventory of the modern library exists; the Fondazione's inventory (c. 35,000 + 1,200) is private ("a disposizione del Ministero, dell'Università di Bologna e della Braidense").
- MOVIO virtual exhibition https://bnbrai-libriantichidiumbertoecoallabibliotecanazionalebraidense.movio.it/it/1/home: not reachable.

---

## 2. Photographs of the shelves

The pictures themselves are not kept in the repository, apart from Andrea Zanni's three CC BY-SA
files. `eco-photos/sources.json` lists every photograph with its url, source, credit, pixel size
and legibility.

### 2.1 Fondazione Umberto Eco: the shelf-by-shelf photographic survey, and the best structural source
https://fondazioneumbertoeco.org/en/lebiblioteche. The page's three "scrollwall" galleries are frontal, rectified photographs of every bookcase of the Milan working library, by Studio Curti Parini (curtiparini.com), each captioned with the bookcase letter and its subject, which makes it a public key to the room and shelf plan:

| file | bookcase | caption |
|---|---|---|
| 01_E | E | Ancient art and art catalogues |
| 02_H | H | Contemporary art, theatre, music |
| 03_G | G | Architecture, design, labyrinths |
| 04_F | F | Aesthetics and photography |
| 05_C | C | Books on books |
| 06_B | B | Jewish thought, magic, Kabbalah, and Joyce |
| 07_D | D | Esotericism, encyclopedism, alchemy |
| 08–11_A (bays 1-6, 7-12, 13-18, 19-25) | A | World literatures: texts, studies, comics (the 25-bay corridor) |
| 12_Q | Q | Books by Eco and translations into 40 languages |
| 13_P | P | Text theory, linguistics, semiotics, philosophy of language and mind, logic |
| 14_L1-4 / 15_L5-7 / 16_L8-12 | L | Encyclopedias and medieval philosophy / History of ideas / Renaissance and modern philosophy, 20th-c. history |
| 17_I | I | Ancient, Late Antique, and Christian philosophy |
| 18_M-A / 19_M-B | M | Continental philosophy, philosophical miscellany / Books by Eco and materials about Eco |
| 20_Na / 21_Nb / 22_Nc | N | Translation, publishing, aesthetics / Dictionaries / Philosophy of science |
| 23_Oa / 24_Ob | O | Encyclopedias, manuals / Semiotics, linguistics, literary studies |
| 25_R | R | Miscellany of psychology and sociology |
| 26_S | S | Psychoanalysis, anthropology, sociology, and publishing |
| antichi 01–04 | Stanza degli antichi | exterior view to Castello, interior, detail, "Rare book library on the right: photographic survey" |
| antichi 05–15 | none | ex libris and 10 highlight books (Schoonhoven 1618, Fludd 1619, Kircher 1667/1679, Maier 1618, Rosenkreuzer 1785, Botero 1618, Bonanni, Worm 1655, Ruysch 1744) |

Sizes served: 267–1386 px wide × 650 px high (webp). **Spines are visible but not legible at this size**, and the originals are high-resolution (the Fondazione's "Una biblioteca virtuale" project: "una lista delle liste e una mappa delle mappe, basate sulle immagini fotografiche delle sue librerie originali ... rese navigabili da collegamenti ipertestuali"). URL pattern: `https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/<file>.webp` and `.../scrollwall_antichi/<file>.webp`.

### 2.2 Curti Parini room photographs via CriticaLetteraria (Nov 2022)
https://www.criticaletteraria.org/2022/11/blog-post_813.html. 9 unique images (blogger `s1600` originals = 1000×600 px, plus one 1600×1600 collage): corridor bookcase A in perspective, frontal wall of shelves, the big study (comb/island shelving, black round table, ladder), salotto with vetrine, piano with book piles, Stanza degli antichi with balcony to the Castello. Spines not legible at 1000 px. Credit "Foto © Curti Parini".

### 2.3 Andrea Zanni (Wikimedia Italia), 24 Apr 2010, CC BY-SA
- Commons `File:Umberto_Eco_in_his_house.JPG`: 3225×2398 px, 2.75 MB, https://upload.wikimedia.org/wikipedia/commons/f/f8/Umberto_Eco_in_his_house.JPG. Portrait of Eco with shelves behind; banner derivatives `..._banner.JPG`, `..._2_banner_slim.JPG`, `..._banner_rescaled.JPG`.
- https://aubreymcfato.com/wp-content/uploads/2010/05/umberto_eco_in_his_house_banner.jpg: 3221×1057, the salotto display cases with open antique books, not spines.
- MilanoToday reproduction, 1000×563.
- Zanni's text (aubreymcfato.com/2010/05/13/intervista-a-umberto-eco-per-wmi/) is also a layout witness (see 3).

### 2.4 Flickr, Martin Grüner Larsen, 9 May 2011 (all rights reserved)
- https://www.flickr.com/photos/mglarsen/5772998464 → 1024×683 (`_b`; no larger size offered): Eco in front of the bookcase of his own works and translations (Q); a few spines readable ("Umberto Eco", titles mostly not).
- https://www.flickr.com/photos/mglarsen/5772422901 → 683×1024: study corner with piles; "SAINTE-BEUVE PORT-ROYAL" legible.

### 2.5 Getty Images (watermarked comps only; 612 px free preview, 1024 px comp with signed URL)
- 1998-03-31, Alvaro Canovas / Paris Match: IDs 160862244 (Eco in the Stanza degli antichi showing a "vieille carte solaire"; wooden glazed cases, spine "Alchimie" readable), 160862246, 160862247 (salon with Renate), 160687967, 160687973 (at his desk "dans une pièce remplie de livres", that is the big study, white shelving, 1998). Detail page e.g. https://www.gettyimages.com/detail/news-photo/rendezvous-with-umberto-eco-at-home-in-milan-en-italie-%C3%A0-news-photo/160862244.
- 2011-03-01, Eric Vandeville / Gamma-Rapho: series 953403564–953403614 (13 frames) "chez lui à Milan": study with ladder and round table (953403568 is the 1024 px comp), portraits, piano room.
- Undated (c. 1980s), "at his home in Milan" 526649200/236/382/548/640 (Corbis historical), and 862229290 Gianni Giansanti 1997 (flute in the apartment). Search page https://www.gettyimages.com/photos/umberto-eco-home lists 60 IDs incl. non-relevant.
- Spines not legible at comp size; licensable hi-res exists.

### 2.6 Studiolo (Braidense) and Biblioteca Eco (Bologna) reconstructions
- Artribune 2022 (https://www.artribune.com/editoria/2022/05/biblioteca-braidense-miano-studio-umberto-eco/): Studiolo photos credited Cesare Maiocchi; the image files cannot be retrieved.
- ANSA 4 May 2022 https://www.ansa.it/webimages/large/2022/5/4/dc2932dd6791303530f1076fc2facf39.jpg (460×306).
- Artribune July 2026 https://www.artribune.com/wp-content/uploads/2026/07/la-biblioteca-eco-a-bologna.webp and `-1.webp` (1230×692), `-2.jpeg` (710×472); BolognaToday https://www.bolognatoday.it/~media/horizontal-hi/53192554928988/biblioteca-eco.jpg (1280×720): Bologna rooms with the Milan white shelving order reproduced; partial spine legibility.
- Leonardo Cendamo (the only photographer Eco allowed at home regularly, per Fanpage): his photoshelter site is captcha-gated; Fondazione credits "Photo © Leonardo Cendamo" for its portrait.
- Not found: press photo-essays in Corriere/Repubblica/Guardian/NYT/Le Monde/El País/AD/Vanity Fair with legible shelves; Google Arts & Culture has only Ferrario "On memory" video assets and a "Language is culture" asset (https://artsandculture.google.com/search?q=umberto%20eco); no Matterport/3D tour of the apartment or Studiolo is public (the Unibo "3D navigation app" is announced, not released).

---

## 3. Room layout: concrete facts with citations

**The apartment (Piazza Castello 13, top floor, "turn-of-the-century lift")**
- "un grande appartamento a forma di anello nei cui corridoi, dal pavimento appositamente rinforzato, vennero montate le librerie. Seguendo la strada tracciata dai lunghi scaffali a tutta altezza – letteratura italiana e straniera, poesia, narrativa popolare e di genere, feuilleton, fumetto, storia e critica letteraria, stampa, comunicazione e mass media, arte e iconologia – si giunge al grande studio di Umberto Eco, con biblioteche dalla complessa struttura a pettine e isola che ospitano volumi relativi a filosofia, scienza, storia, filologia, mnemotecniche, enigmistica, editoria, linguistica e semiotica, oltre ai libri di e su Eco." Designed for the books "oltre trent'anni fa". (Fondazione, *Le biblioteche*.)
- "Over thirty years ago Umberto Eco decided to move house in Milan because he was looking for somewhere big enough to hold all his books ... He strengthened the floor and filled the corridors with bookshelves, then set aside a room – the Room of the Ancients – with a balcony overlooking the Castello Sforzesco." (BreraPlus, *The Idea of the Library* documentary page.)
- "The apartment is a labyrinth of corridors lined with bookcases that reach all the way up to extraordinarily high ceilings—thirty thousand volumes, said Eco, with another twenty thousand at his manor. I saw scientific treatises by Ptolemy and novels by Calvino, critical studies of Saussure and Joyce, entire sections devoted to medieval history and arcane manuscripts ... In his study, a maze of shelves contains Eco's own complete works in all their translations (Arabic, Finnish, Japanese ... more than thirty languages)." (Lila Azam Zanganeh, *Paris Review* 185 (2008), Art of Fiction 197, (PDF https://www.lazanganeh.com/pdfs/paris_review_art_of_fiction.pdf).
- Zanni 2010: "La libreria nel lunghissimo corridoio è solo la narrativa, mentre la grande stanza contiene varie cose, fra cui: sulla destra un'intera libreria di libri scritti da lui e tradotti in ogni lingua; sull'estrema destra vari scaffali di libri scritti su di lui; una parte centrale con libri suoi che deve dare via, e scatoloni ovunque; una parte centrale con la sezione dei cretini (io ricordo Dumézil e Zolla…); il 'cimitero', una serie di foto di Eco con Montale, Moravia, Foucault…"; the rare-book room: "stanzino adibito, tutto in legno, un'enorme lente sul tavolo". Eco: "Macché comprati! Me li mandano, è per questo che non si può fermare…". 
- CriticaLetteraria visit (Nov 2022, guided by Carlotta Eco and Mario Andreose): sequence of rooms = **salotto** (art books, "libri da esposizione", encyclopaedias, atlases; the vetrina Eco used to display his current research) → **vestibolo** (a shelf for Joyce; Kabbalah, mystery, magic, Templars, devil, alchemy) → **corridoio** ("una teoria infinita di scaffali", the "bosco narrativo": Italian and French authors at eye level, Dante to contemporaries; comics on the highest and lowest shelves: Topolino, Paperino, Sturmtruppen, Mandrake, Linus, Peanuts, Asterix, L'uomo mascherato, Corriere dei Piccoli) → **studio** (behind the desk the working tools: dictionaries, encyclopaedic/geographical lexica; a corner of travel literature = sources of *L'isola del giorno prima*; one whole wall philosophy from the Presocratics; the opposite side semiotics, linguistics, literary theory; his own works in 60+ languages and books about him). Ordering "per simpatia, per affinità intellettuale" (Carlotta Eco); annotated/dedicated books carry a label with a number (the Fondazione's inventory in progress).
- Stanza degli antichi: "un vero e proprio rifugio, affacciato su Castello Sforzesco, senza telefono, senza computer, con gli spartiti e i flauti che Eco suonava quasi ogni giorno ... i volumi erano posizionati sugli scaffali a fianco di veri e propri mirabilia – testicoli di cane, conchiglie, rami di corallo, modellini di legno" (Fondazione; Renate Ramge quoted in Rivista Studio). "La stanza tutta per sé originale di Eco era di forma ellittica, mentre quella in Braidense è rettangolare" (Rivista Studio 8 May 2022). Bradburne (ANSA 2021): "A casa sua, i libri rari erano privilegiati, e posizionati separatamente rispetto alla sua biblioteca moderna." Volumes kept in four ordered sections = shelfmarks ECO.01–04 (see 1.1).
- Eco's own account of order: "My secretary once wanted to draw up a catalogue of my books so that she knew exactly where each one was. I persuaded her not to. While I was writing *The Search for the Perfect Language* I looked at my library anew, with new criteria, and changed it around ... When I finished writing, some books went back on the linguistics shelf, and some to aesthetics"; "I have 50,000 books in my various homes ... I also have 1,200 rare titles"; "My collection is very focused. It is a Bibliotheca Semiologica Curiosa Lunatica Magica et Pneumatica, or 'a collection dedicated to the occult and mistaken sciences'. For example, I have Ptolemy ... but not Galileo" (Eco & Carrière, *This Is Not the End of the Book*, 2011; text on archive.org, djvu.txt).
- Eco, "Come giustificare una biblioteca privata" (*Il secondo diario minimo*, 1992; text at libriantichionline.com): the visitor's "Quanti libri! Li ha letti tutti?"; "la biblioteca come strumento di lavoro"; the reply "No, questi sono quelli che debbo leggere entro il mese prossimo, gli altri li tengo all'università". No physical description.
- Bologna reconstruction (what it preserves of Milan): "la biblioteca, prima del trasferimento, è stata studiata e rilevata scaffale per scaffale, documentando la posizione dei volumi, le sequenze tematiche e gli accostamenti tra autori e discipline" (Artribune/Unibo press, July 2026); "libri disposti orizzontalmente sono rimasti tali, sopra quelli in verticale" (Il Bo Live); "scaffalature bianche distribuite su due livelli divisi da un ballatoio ... chiaro riferimento alla sede originaria: la casa di Milano con le sue alte, lunghe e bianche librerie" (Unibo Magazine 2021); rooms: literatures (Italian, French, English, German, Mitteleuropean, Slavic, Hispano-American, arranged as time-lines), comics and popular culture (complete *Linus*), works by/about Eco, ancient and medieval philosophy, history of ideas, semiotics, translation and theories of language, avant-gardes, mass communication, Kabbalah/magic/alchemy/occultism/conspiracy (Il Resto del Carlino 2 Jul 2026); principle of the Warburg "buon vicino" (all 2026 press; Bradburne 2022 for the Studiolo).
- Le Monde / Guardian / NYT / El País: only obituaries and the viral 2015 Ferrario long take (video, excluded here); no floor plan published anywhere. The closest thing to a plan is the Fondazione's lettered bookcase key (A–S) + the CriticaLetteraria room sequence.

---

## 4. Virtual tours / 3D / Google Arts & Culture / Europeana
- None public. Announced only: Unibo/Abulafia "applicazione di navigazione 3D" (Unibo Magazine 17 Jun 2021; DIRE; MilanoToday 17 Jun 2021 "riprodotta ... online in 3D"), "Index Humbertinus" search engine, LOD; Fondazione "biblioteca virtuale" based on the Curti Parini shelf photographs (fondazioneumbertoeco.org/progetti). Centro "Umberto Eco" page (centri.unibo.it/cue/it/attivita-progetti) lists no released tool.
- BreraPlus documentary page (video; text useful, see 3). Google Arts & Culture: only Ferrario video assets. Europeana: nothing. Braidense "Studiolo Umberto Eco" page: text only.

---

## 5. Coverage summary and recommendation

| Source | Titles it can account for | Shelf position | Public access |
|---|---|---|---|
| Braidense OPAC, `Collocazione = ECO` | **2,105 records** = the whole rare-book fund (1,328 vols) | yes: ECO.01–04 + running number = Eco's own room order | GET search, HTML full records, UNIMARC bulk export, which is `braidense_eco_all.mrc` and `.csv` |
| AIB Studi 2022 | 36 incunabula with ISTC ids + Eco's cards | via ECO.03 | PDF |
| SBN-UBO SebinaYOU, possessor "eco umberto" + BUB | **3,047 records** (growing; c. 9-10 % of the 32,000) | not in public HTML (shelfmark hidden; Eco order kept physically in Bologna) | GET list, 10/page, JS paging; per-record pages |
| Fondazione shelf-survey galleries (Curti Parini) | c. 30,000 volumes *pictured* across bookcases A–S (25 corridor bays + 18 study/vestibule cases), 650 px, spines not readable; hi-res originals private | yes: bookcase letter + subject caption, plus the Stanza degli antichi | GET webp |
| Press/Flickr/Getty photos | a few dozen legible spines (Flickr 2011, Getty 1998/2011 comps) | contextual only | yes (Getty licensed for hi-res) |
| Visitor accounts (Zanni 2010, Paris Review 2008, Carrière 2011, CriticaLetteraria 2022) | named sections and a handful of titles | room sequence and subject-per-wall | yes |
| Fondazione private inventory (c. 35,000 + 1,200) | all | yes (kept "nell'originale ordine autoriale") | not public; held by MiC, Unibo, Braidense |

**Totals.** Of the c. 33,000 books in the Milan flat: the 1,328 rare volumes are fully accounted for by title *and* shelf position (2,105 Braidense records, exported); c. 3,047 of the c. 32,000 modern volumes are accounted for by title in SBN-UBO (no public shelfmark); the remaining c. 29,000 are visible only as unreadable spines in the Fondazione's bookcase-by-bookcase photographs (which do, however, give the complete subject map of the shelving, A–S). So today public sources yield roughly **4,400 titles (~13 %)**, plus a complete *structural* map of where the other ~29,000 stood.

**Authoritative title lists.** For the rare books: the Braidense OPAC ECO fund (UNIMARC export). For the modern library: the SBN-UBO SebinaYOU "Documenti provenienza Umberto Eco – BUB" query (3,047 and growing as BUB catalogues; the definitive list will be this query once cataloguing completes), backed by the Fondazione's non-public inventory. For the physical arrangement: the Braidense ECO.xx shelfmarks (rare room) and the Fondazione's lettered bookcase photographs (working library), cross-read with the CriticaLetteraria room-by-room account.
