# Rights notice

This repository holds the 3D map of Umberto Eco's Milan library and what was made to build
it. The MIT licence in `LICENSE` covers the work done for this project. It does not cover the
material the map was built from, which belongs to other people and institutions and comes
with terms of its own. This notice says which is which, file by file where it matters.

## What the MIT licence covers

Everything written for this project: the page (`eco-map/index_eco.html`), the generator and
the build and test scripts, the description pipeline and the harvest scripts, the staging and
deploy kit, the room and bookcase layout, the spine readings and the consolidated book lists,
the inventory of objects, the mapping tables, the fourteen tours and their captions, the
English titles and the translations made for the map, the descriptions written here for books
that have no article, the READMEs and the notes. Copyright in that work belongs to Ethan
Mollick, and the MIT licence lets anyone use it, change it and pass it on, with the copyright
line kept.

## What it does not cover

### Catalogue records

**Biblioteca Nazionale Braidense, Milan.** The 2,105 records of the fondo Umberto Eco,
shelfmarks ECO.01 to ECO.04, were exported in UNIMARC from the library's online catalogue
(opac.braidense.it). The Braidense publishes its general online catalogue as open data under
the Creative Commons CC0 1.0 Universal Public Domain Dedication, as its page of licences says
(https://bibliotecabraidense.org/info-utili/#licenze, "Catalogo generale online ... Licenza:
Creative Commons CC0 1.0 Universal Public Domain Dedication"). The export is
`eco-sources/braidense_eco_all.mrc` and `.csv`; the converted records are
`eco-map/books_braidense.json` and `braidense_id_map.json`; every Braidense entry in
`books.json` and in the built pages carries the record's fields, and every card names the
library and links the record. The records are the library's work, used here under CC0.

**Biblioteca Universitaria di Bologna, University of Bologna.** The 3,047 records with the
possessor note "Eco, Umberto" were harvested from the catalogue of the Polo bolognese, SBN UBO
(sol.unibo.it), together with the notes the Biblioteca Universitaria added to Eco's copies: the
inventory number, the provenance, the dedications with the inscriptions transcribed, the
underlinings, marginalia, dog-ears and inserts, and the ex-libris stamp. The catalogue states no
licence for its records. The University's legal notes
(https://www.unibo.it/it/ateneo/privacy-e-note-legali/note-legali) say that the contents of
its portal may be reproduced with the consent of the rights holders, except for contents
released under a Creative Commons licence, and that the source must be cited. The records are
reproduced here as the public record of a public collection, with the catalogue named as the
source on every card and in this notice; they remain the University's and the library's, and
the MIT licence does not extend to them. The export is `eco-sources/bologna_eco_modern.jsonl`
and `.csv`; the converted records are `eco-map/books_bologna.json` and `bologna_id_map.json`;
the Bologna entries in `books.json` and in the built pages, and the index of Eco's copies on
the page, carry the fields and the copy notes.

Both catalogues take part in the Servizio Bibliotecario Nazionale, the Italian union catalogue
run by the ICCU, whose record identifiers the files keep.

**Incunabula Short Title Catalogue.** The cards of the 36 incunabula link to the ISTC
(data.cerl.org/istc), the international database of fifteenth-century printing hosted by the
Consortium of European Research Libraries, and sixteen entries in
`eco-map/descriptions_eco_overrides.json` are short descriptions taken from its records, each
with the record linked. No licence statement for the ISTC data was found on its site.

### Book descriptions from Wikipedia

Of the 2,264 descriptions the page shows, 2,222 are the opening sentences of Wikipedia articles
in the Italian, French, English, Spanish, German, Swedish and Hungarian editions: the article on
the book where one exists, otherwise a sentence from the article on its author, marked as such.
The English versions in `eco-map/descriptions_en_eco.json` marked "translated here" are
translations of those sentences. Wikipedia's text is licensed under the Creative Commons
Attribution-ShareAlike 4.0 International licence (https://creativecommons.org/licenses/by-sa/4.0/),
as the Wikimedia Foundation's terms of use provide
(https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use). Every description carries the
address of its article, which is the attribution the terms ask for, and these texts and their
translations stay under CC BY-SA 4.0 wherever they appear: `eco-map/descriptions_bologna.json`,
`descriptions_braidense.json`, `descriptions_eco_bologna.json`,
`descriptions_eco_braidense.json`, the Wikipedia entries of `descriptions_eco_overrides.json`
and `descriptions_eco_seen.json`, `descriptions_en_eco.json`, the description fields of
`books.json`, and the built pages in `dist/`. The remaining 42 descriptions were written here
from the film, from the ISTC or from a library record, and say so.

### Pictures from Wikimedia Commons

Forty-seven tour stops show a picture of the book from Wikimedia Commons. The files are in
`eco-map/tour-images/`, and the generator embeds a 200-pixel copy in `books.json` and in the
built pages, credited on the card. Forty-four are in the public domain, one is a CC0 release by
the Rijksmuseum, and two are photographs under Creative Commons licences that ask for the
photographer's name: the Wellcome Collection's photograph of Ruysch's *Thesaurus anatomicus*
(CC BY 4.0) and Sailko's photograph of Aldrovandi's *Monstrorum historia* (CC BY 3.0). Each
picture keeps its own licence, as its Commons page states it.

| file | Commons file | author or source, as the card credits it | licence |
|---|---|---|---|
| `agrippa.jpg` | [Theban alphabet from De Occulta Philosophia 1533.png](https://commons.wikimedia.org/wiki/File:Theban_alphabet_from_De_Occulta_Philosophia_1533.png) | Heinrich Cornelius Agrippa, 1533 | public domain |
| `aldrovandi.jpg` | [Ulisse aldrovandi, monstrorum historia, per nicola tebaldini, bologna 1642, 104 acefali.jpg](https://commons.wikimedia.org/wiki/File:Ulisse_aldrovandi,_monstrorum_historia,_per_nicola_tebaldini,_bologna_1642,_104_acefali.jpg) | Ulisse Aldrovandi, Monstrorum historia (1642); photograph by Sailko, CC BY 3.0 | CC BY 3.0 (photograph by Sailko) |
| `bordone.jpg` | [1528 - Bordone - Title page.jpg](https://commons.wikimedia.org/wiki/File:1528_-_Bordone_-_Title_page.jpg) | Benedetto Bordone, 1528 | public domain |
| `bruno.jpg` | [Bruno De Umbris ombre.JPG](https://commons.wikimedia.org/wiki/File:Bruno_De_Umbris_ombre.JPG) | Giordano Bruno, 1582 | public domain |
| `burnet.jpg` | [Christ standing above views of the earth showing its formation and predicting a final conflagration LCCN92517753.jpg](https://commons.wikimedia.org/wiki/File:Christ_standing_above_views_of_the_earth_showing_its_formation_and_predicting_a_final_conflagration_LCCN92517753.jpg) | Thomas Burnet, 1681; Library of Congress | public domain |
| `chemical_wedding.jpg` | [Chymische Hochzeit Christiani Rosencreutz anno 1459.png](https://commons.wikimedia.org/wiki/File:Chymische_Hochzeit_Christiani_Rosencreutz_anno_1459.png) | Johann Valentin Andreae, 1616 | public domain |
| `corriere.jpg` | [Corriere dei Piccoli prima edizione.jpg](https://commons.wikimedia.org/wiki/File:Corriere_dei_Piccoli_prima_edizione.jpg) | Corriere dei Piccoli, 27 December 1908 | public domain |
| `cosmas.jpg` | [WorldMapCosmasIndicopleustes.jpg](https://commons.wikimedia.org/wiki/File:WorldMapCosmasIndicopleustes.jpg) | Cosmas Indicopleustes, 6th century (later manuscript copy) | public domain |
| `dee.jpg` | [Monas Hieroglyphica.jpg](https://commons.wikimedia.org/wiki/File:Monas_Hieroglyphica.jpg) | John Dee, 1564 | public domain |
| `donnelly.jpg` | [Atlantis map 1882.jpg](https://commons.wikimedia.org/wiki/File:Atlantis_map_1882.jpg) | Ignatius Donnelly, 1882 | public domain |
| `fama.jpg` | [Fama fraternitatis.jpg](https://commons.wikimedia.org/wiki/File:Fama_fraternitatis.jpg) | Anonymous (attributed circle of Johann Valentin Andreae), 1614 | public domain |
| `fantomas.jpg` | [Fantomas 1911.jpg](https://commons.wikimedia.org/wiki/File:Fantomas_1911.jpg) | Unknown/anonymous illustrator, Fayard edition, Paris, 1911 | public domain |
| `fludd.jpg` | [Robert Fludd Utriusque Cosmi Tract1 Lib1 p26.jpg](https://commons.wikimedia.org/wiki/File:Robert_Fludd_Utriusque_Cosmi_Tract1_Lib1_p26.jpg) | Robert Fludd, 1617 (Tractatus I, Liber I, p.26) | public domain |
| `fontenelle.jpg` | [Conversations on the Plurality of Worlds frontpiece.jpg](https://commons.wikimedia.org/wiki/File:Conversations_on_the_Plurality_of_Worlds_frontpiece.jpg) | Bernard le Bovier de Fontenelle, 1686 | public domain |
| `godwin.jpg` | [Houghton STC 11943.5 - The Man in the Moone, title.jpg](https://commons.wikimedia.org/wiki/File:Houghton_STC_11943.5_-_The_Man_in_the_Moone,_title.jpg) | Francis Godwin, 1638; Houghton Library, Harvard | public domain |
| `huysmans.jpg` | [Martin van Maële - Là-bas - Sur une table servant d'autel.jpg](https://commons.wikimedia.org/wiki/File:Martin_van_Ma%C3%ABle_-_L%C3%A0-bas_-_Sur_une_table_servant_d%27autel.jpg) | Martin van Maele, illustration for Huysmans's La-bas, before 1926 | public domain |
| `hypnerotomachia.jpg` | [Hypnerotomachia Polifili 00042.jpg](https://commons.wikimedia.org/wiki/File:Hypnerotomachia_Polifili_00042.jpg) | Aldus Manutius / Francesco Colonna, 1499; scan via Herzog August Bibliothek Wolfenbuttel | public domain |
| `khunrath.jpg` | [Amphitheatrum sapientiae aeternae - Alchemist's Laboratory.jpg](https://commons.wikimedia.org/wiki/File:Amphitheatrum_sapientiae_aeternae_-_Alchemist%27s_Laboratory.jpg) | Hans Vredeman de Vries, for Khunrath's Amphitheatrum sapientiae aeternae (1595) | public domain |
| `kircher_atlantis.jpg` | [Atlantis Kircher Mundus subterraneus 1678.jpg](https://commons.wikimedia.org/wiki/File:Atlantis_Kircher_Mundus_subterraneus_1678.jpg) | Athanasius Kircher, 1665 (1678 edition shown) | public domain |
| `kircher_babel.jpg` | [Athanasius Kircher - Turris Babel - 1679 (page 5 crop).jpg](https://commons.wikimedia.org/wiki/File:Athanasius_Kircher_-_Turris_Babel_-_1679_(page_5_crop).jpg) | Athanasius Kircher, 1679 | public domain |
| `kircher_china.jpg` | [Frontispiece to China illustrated by Athanasius Kircher..JPG](https://commons.wikimedia.org/wiki/File:Frontispiece_to_China_illustrated_by_Athanasius_Kircher..JPG) | Athanasius Kircher, 1667 | public domain |
| `kircher_fire.jpg` | [Kircher Mundus Subterraneus fire canals.jpg](https://commons.wikimedia.org/wiki/File:Kircher_Mundus_Subterraneus_fire_canals.jpg) | Athanasius Kircher, 1665 | public domain |
| `kircher_lucis.jpg` | [Kirchner, Athanasius - Ars Magna Lucis et Umbrae (frontispiece).jpg](https://commons.wikimedia.org/wiki/File:Kirchner,_Athanasius_-_Ars_Magna_Lucis_et_Umbrae_(frontispiece).jpg) | Athanasius Kircher, 1646 | public domain |
| `kircher_mithras.jpg` | [Kircher oedipus aegyptiacus 23 mithras tauroctony.png](https://commons.wikimedia.org/wiki/File:Kircher_oedipus_aegyptiacus_23_mithras_tauroctony.png) | Athanasius Kircher, 1652-1654 | public domain |
| `kircher_musurgia.jpg` | [Frontispiece,volume one of "Musurgia Universalis" by Athanasius Kircher, 1650.png](https://commons.wikimedia.org/wiki/File:Frontispiece,volume_one_of_%22Musurgia_Universalis%22_by_Athanasius_Kircher,_1650.png) | Athanasius Kircher, 1650 | public domain |
| `kircher_oedipus.jpg` | [Oedipus lost het raadsel op Titelpagina voor A. Kircher, Oedipus Aegyptiacus, Rome 1652-1654, RP-P-BI-1459.jpg](https://commons.wikimedia.org/wiki/File:Oedipus_lost_het_raadsel_op_Titelpagina_voor_A._Kircher,_Oedipus_Aegyptiacus,_Rome_1652-1654,_RP-P-BI-1459.jpg) | Athanasius Kircher, 1652-1654; Rijksmuseum Amsterdam (RP-P-BI-1459) | CC0 1.0 (Rijksmuseum) |
| `lull.jpg` | [Title page with illustration showing the tree of knowledge LCCN2006681057.jpg](https://commons.wikimedia.org/wiki/File:Title_page_with_illustration_showing_the_tree_of_knowledge_LCCN2006681057.jpg) | Ramon Llull; Library of Congress digitization | public domain |
| `maier.jpg` | [Michael Maier Atalanta Fugiens Emblem 21.jpeg](https://commons.wikimedia.org/wiki/File:Michael_Maier_Atalanta_Fugiens_Emblem_21.jpeg) | Michael Maier, engraved by Matthaeus Merian, 1617 | public domain |
| `malleus.jpg` | [Malleus maleficarum, Köln 1520, Titelseite.jpg](https://commons.wikimedia.org/wiki/File:Malleus_maleficarum,_K%C3%B6ln_1520,_Titelseite.jpg) | Heinrich Kramer (Institoris), Cologne, 1520 | public domain |
| `ortelius.jpg` | [Theatrum Orbis Terrarum, by Abraham Ortelius, World, 1572.jpg](https://commons.wikimedia.org/wiki/File:Theatrum_Orbis_Terrarum,_by_Abraham_Ortelius,_World,_1572.jpg) | Abraham Ortelius, 1570/1572 | public domain |
| `paget.jpg` | [Sherlock Holmes & Watson - The Adventure of the Empty House - Sidney Paget.jpg](https://commons.wikimedia.org/wiki/File:Sherlock_Holmes_%26_Watson_-_The_Adventure_of_the_Empty_House_-_Sidney_Paget.jpg) | Sidney Paget (1860-1908), 1903, for The Strand Magazine | public domain |
| `piazzi_smyth.jpg` | [Piazzi-plate 13.jpg](https://commons.wikimedia.org/wiki/File:Piazzi-plate_13.jpg) | Charles Piazzi Smyth, 1864 | public domain |
| `pinocchio.jpg` | [Pinocchio visto da Enrico Mazzanti (1883).jpg](https://commons.wikimedia.org/wiki/File:Pinocchio_visto_da_Enrico_Mazzanti_(1883).jpg) | Enrico Mazzanti (1852-1910), 1883 | public domain |
| `pliny.jpg` | [Plinius, Naturalis historia, incunable, 1469.jpg](https://commons.wikimedia.org/wiki/File:Plinius,_Naturalis_historia,_incunable,_1469.jpg) | Pliny the Elder (text), printed by Johannes de Spira, Venice, 1469 | public domain |
| `popeye.jpg` | [The Thimble Theatre (January 17, 1929) "'Gobs'" of Work).jpg](https://commons.wikimedia.org/wiki/File:The_Thimble_Theatre_(January_17,_1929)_%22%27Gobs%27%22_of_Work).jpg) | E. C. Segar (1894-1938), 17 January 1929 | public domain |
| `protocols.jpg` | [1905 Velikoe v malom - Serge Nilus - Title page - Facsimile - 1920.jpg](https://commons.wikimedia.org/wiki/File:1905_Velikoe_v_malom_-_Serge_Nilus_-_Title_page_-_Facsimile_-_1920.jpg) | Sergei Nilus, 1905 (facsimile reproduced 1920) | public domain |
| `rabelais.jpg` | [Prologue of Gargantua and Pantagruel by Gustav Dore (55219036).jpg](https://commons.wikimedia.org/wiki/File:Prologue_of_Gargantua_and_Pantagruel_by_Gustav_Dore_(55219036).jpg) | Gustave Dore, illustration for Rabelais's Gargantua et Pantagruel (19th-century illustrated edition) | public domain |
| `rosenroth.jpg` | [Kabbala denudata sefirot.jpg](https://commons.wikimedia.org/wiki/File:Kabbala_denudata_sefirot.jpg) | Christian Knorr von Rosenroth, 1677-1684 | public domain |
| `ruysch.jpg` | [Ruysch "Thesaurus anatomicus", 1701-16; foetal skeletons Wellcome L0019778.jpg](https://commons.wikimedia.org/wiki/File:Ruysch_%22Thesaurus_anatomicus%22,_1701-16;_foetal_skeletons_Wellcome_L0019778.jpg) | Cornelis Huyberts (engraver) after Frederik Ruysch, 1701-1716; Wellcome Collection (CC BY 4.0) | CC BY 4.0 (Wellcome Collection) |
| `schedel_city.jpg` | [Hartmann Schedel - Nuremberg Chronicle, Page 100 - View of the city of Nuremberg - WGA20964.jpg](https://commons.wikimedia.org/wiki/File:Hartmann_Schedel_-_Nuremberg_Chronicle,_Page_100_-_View_of_the_city_of_Nuremberg_-_WGA20964.jpg) | Michael Wolgemut workshop (woodcut), Hartmann Schedel text, 1493 | public domain |
| `schedel_map.jpg` | [1493 map of the world by Hartmann Schedel.jpg](https://commons.wikimedia.org/wiki/File:1493_map_of_the_world_by_Hartmann_Schedel.jpg) | Hartmann Schedel, 1493 (Liber Chronicarum / Nuremberg Chronicle) | public domain |
| `sue.jpg` | [Le Juif errant Gavarni.jpg](https://commons.wikimedia.org/wiki/File:Le_Juif_errant_Gavarni.jpg) | Paul Gavarni, 1844-45 | public domain |
| `taxil.jpg` | [Taxil, Hacks, Le Diable au XIXe siècle, p601.jpg](https://commons.wikimedia.org/wiki/File:Taxil,_Hacks,_Le_Diable_au_XIXe_si%C3%A8cle,_p601.jpg) | Leo Taxil / Karl Hacks (Dr. Bataille), 1892 | public domain |
| `tigri.jpg` | [Tigri 1900.jpg](https://commons.wikimedia.org/wiki/File:Tigri_1900.jpg) | Alberto della Valle (1851-1928), cover for the 1906 edition | public domain |
| `valeriano.jpg` | [Hieroglyphica 1556 (67921011).jpg](https://commons.wikimedia.org/wiki/File:Hieroglyphica_1556_(67921011).jpg) | Pierio Valeriano, 1556 | public domain |
| `wilkins.jpg` | [An Essay towards a Real Character, and a Philosophical Language - title.png](https://commons.wikimedia.org/wiki/File:An_Essay_towards_a_Real_Character,_and_a_Philosophical_Language_-_title.png) | John Wilkins, 1668 | public domain |
| `yellow_kid.jpg` | [The Yellow Kid Well here's to happy days, see - - R.F. Outcault. LCCN00650391.jpg](https://commons.wikimedia.org/wiki/File:The_Yellow_Kid_Well_here's_to_happy_days,_see_-_-_R.F._Outcault._LCCN00650391.jpg) | Richard Felton Outcault (1863-1928), 1897 | public domain |

### The article on Eco's incunabula

`eco-sources/aib_224.pdf` is Angela Nuovo and Aldo Coletto, "Gli incunaboli di Umberto Eco",
*AIB studi* 62, no. 1 (2022), https://doi.org/10.2426/aibstudi-13386, copyright 2022 Angela
Nuovo and Aldo Coletto, published under the Creative Commons Attribution-ShareAlike 4.0
licence. The list of the 36 incunabula in `eco-sources/experience/incunabula.json`, whose
binding and provenance notes are the article's, the notes on it in
`eco-sources/experience/incunabula-notes.md`, and the incunabula cards on the page derive from
it, cite its pages, and stay under CC BY-SA 4.0.

### Quotations

The tour cards, the room panels and the notes quote Umberto Eco and his family in short
passages, each attributed and linked: the *Paris Review* interview with Lila Azam Zanganeh
(2008), *This Is Not the End of the Book* by Eco and Jean-Claude Carrière (2011), the lecture
*De Bibliotheca* (1981), the Tanner and Borges lectures, "Come giustificare una biblioteca
privata" and other essays and columns, the *Der Spiegel* interview on lists (2009), the
Louisiana Channel interviews (2015), the words of Eco's family in the 2022 film and at the
Braidense, and the press reports on the two libraries. `eco-sources/experience/quotes.json`
holds the passages with their sources. Copyright in these texts remains with their authors,
publishers and heirs; they are quoted with attribution and are not licensed under MIT. The
full texts of the *Paris Review* interview and of Eco and Carrière's book are not in the
repository.

### The films

The identifications rest on footage of the flat: Davide Ferrario's documentary *Umberto Eco.
La biblioteca del mondo* (Rossofuoco and Fandango, 2022), his video conversation *Umberto Eco.
Sulla memoria* (Codice Italia, Venice Art Biennale, 2015), the Louisiana Channel's two
interviews (Louisiana Museum of Modern Art, 2015), the trailers released by Fandango and The
Cinema Guild, and news reports by Corriere della Sera, askanews and Telecity News 24: twelve
videos, listed in `eco-video/videos.json`. The page links to each of them on YouTube at the
second a book or an object appears, and 132 objects carry a small crop of the frame that shows
them, embedded in `books.json` and in the built pages, so that a visitor can see what the map
drew. The films themselves, the frames cut from them, the crops made while reading them, their
subtitles and their page metadata are not in the repository: the spine readings and the object
inventory record what was read, frame by frame, and each entry names its video and its second.
The films' images and their words remain the property of their producers and are not licensed
here.

### Photographs of the rooms

The layout was read from published photographs: the Fondazione Umberto Eco's photographic
survey of the bookcases and of the Stanza degli antichi, photographed by Studio Curti Parini,
with the captions of its galleries in `eco-sources/fondazione_galleries.json`; the room
photographs by Curti Parini published by CriticaLetteraria in 2022; two photographs by Martin
Gruner Larsen (Flickr, 2011, all rights reserved); two photographs distributed by Getty Images
(Alvaro Canovas for Paris Match, Eric Vandeville for Gamma-Rapho); and press images from ANSA,
Artribune and BolognaToday of the Braidense's studiolo and of the Biblioteca Eco in Bologna.
`eco-sources/eco-photos/sources.json` lists every one of them with its address, its source and
its credit, and the spine readings in `eco-video/spines_photos.jsonl` say what was read in
each. The photographs themselves are not in the repository, and no licence to reuse them is
given or implied; they remain the property of their photographers, their agencies and the
Fondazione. The exception is Andrea Zanni, who photographed Eco in his flat in 2010 for
Wikimedia Italia and released the pictures under CC BY-SA: three of his files stay in
`eco-sources/eco-photos/` (`zanni_2010_umberto_eco_in_his_house_orig.jpg`,
`zanni_banner_orig.jpg` and `milanotoday_zanni.jpg`, the last a reproduction of his photograph
by MilanoToday), with a crop in `eco-video/salotto/crops/photo_zanni_2010.jpg`; they may be
reused with his name under the same licence.

### Third-party code

`eco-map/vendor/` carries three.js release 160 (`three.module.min.js`) with its OrbitControls
and PointerLockControls modules, copyright 2010-2023 Three.js Authors, under the MIT licence:

> Permission is hereby granted, free of charge, to any person obtaining a copy of this software
> and associated documentation files (the "Software"), to deal in the Software without
> restriction, including without limitation the rights to use, copy, modify, merge, publish,
> distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
> Software is furnished to do so, subject to the following conditions: The above copyright
> notice and this permission notice shall be included in all copies or substantial portions of
> the Software. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
> PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
> LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
> OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
> DEALINGS IN THE SOFTWARE.

Nothing else in the repository comes from a software library, and the page uses the reader's
own fonts.

### Not in the repository

The videos and the frames cut from them, the crops and the subtitles of the films, the room
photographs other than Zanni's, the Wikipedia lookup cache, and the full texts of the two
copyrighted works named above are not in the repository.
