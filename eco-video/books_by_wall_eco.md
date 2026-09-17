# Books seen in Umberto Eco's library: consolidated spine readings

Generated 2026-09-09T09:36:29Z by `build_books_by_wall_eco.py` from 30 spine files (2405 frames/photos, 2094 titled sightings). Companion to `books_by_wall_eco.json`. Timestamps are corrected source times (`timestamp_s + timestamp_offset_s`, i.e. +0.96 s for zZEy10fpq3I); links use the rounded second.

## Totals

- Distinct titles: 587 (included 517, excluded 70); author-only entries without a legible title among the included: 78
- Included by confidence: high 217, medium 177, low 123
- Included by language: it 268, la 86, en 49, fr 38, de 30, es 7, ru 7, None 5, nl 4, el 3, pl 3, pt 3, uk 3, bg 2, ca 1, cs 1, da 1, ko 1, lt 1, ro 1, sr 1, sv 1, tr 1
- Included by source (a title seen in several sources counts once per source): zZEy10fpq3I 316, KZfOaug0mM4 87, photo 62, ygvl-_gtAP8 48, bcK8rOkcb3k 31, FeIUY9EhZgI 30, M8IWTOFNlOc 26, iRXEQVTI95k 21, NtPk4irDiM8 16, B-M8V0PcCrw 4, zj1kwT87ne0 3, Hq66X9f-zgc 2
- Included by room: studio 228, antichi 90, salotto 80, bologna 62, unknown 40, corridoio 16, vestibolo 1
- Included by view kind: shelf 408, pile 96, other 13
- Unlabelled spines counted: 34910 in total, 25864 on included walls

## Input files and validation

| file | lines ok | bad |
|---|---:|---:|
| spines_B-M8V0PcCrw.jsonl | 39 | 0 |
| spines_FeIUY9EhZgI.jsonl | 78 | 0 |
| spines_FeIUY9EhZgI_dense.jsonl | 50 | 0 |
| spines_Hq66X9f-zgc.jsonl | 35 | 0 |
| spines_KZfOaug0mM4.jsonl | 44 | 0 |
| spines_KZfOaug0mM4_dense.jsonl | 61 | 0 |
| spines_M8IWTOFNlOc.jsonl | 460 | 0 |
| spines_M8IWTOFNlOc_dense.jsonl | 36 | 0 |
| spines_NtPk4irDiM8.jsonl | 70 | 0 |
| spines_NtPk4irDiM8_dense.jsonl | 65 | 0 |
| spines_bcK8rOkcb3k.jsonl | 81 | 0 |
| spines_bcK8rOkcb3k_dense.jsonl | 54 | 0 |
| spines_iRXEQVTI95k.jsonl | 61 | 0 |
| spines_iRXEQVTI95k_dense.jsonl | 39 | 0 |
| spines_photos.jsonl | 65 | 0 |
| spines_rMSOvDAyH5c.jsonl | 16 | 0 |
| spines_ygvl-_gtAP8.jsonl | 115 | 0 |
| spines_ygvl-_gtAP8_dense.jsonl | 70 | 0 |
| spines_zZEy10fpq3I_dense.jsonl | 741 | 0 |
| spines_zZEy10fpq3I_part0.jsonl | 23 | 0 |
| spines_zZEy10fpq3I_part1.jsonl | 6 | 0 |
| spines_zZEy10fpq3I_part2.jsonl | 7 | 0 |
| spines_zZEy10fpq3I_part3.jsonl | 12 | 0 |
| spines_zZEy10fpq3I_part4.jsonl | 87 | 0 |
| spines_zZEy10fpq3I_part5.jsonl | 3 | 0 |
| spines_zZEy10fpq3I_part6.jsonl | 6 | 0 |
| spines_zZEy10fpq3I_part7.jsonl | 7 | 0 |
| spines_zZEy10fpq3I_piano.jsonl | 29 | 0 |
| spines_zZEy10fpq3I_piano_heavy.jsonl | 12 | 0 |
| spines_zj1kwT87ne0.jsonl | 33 | 0 |

No line was skipped: every line parses and has the required structure.

Schema deviations tolerated (3103, details in `validation.warnings` of the JSON):
- 2773 x row N book N unlabelled but carries spine_text/title (treated as unlabelled)
- 269 x row N book N author-only (no title)
- 26 x row N book N has neither title nor author (counted as unlabelled N)
- 11 x row N book N lacks pos
- 6 x view not in enum
- 6 x room override
- 3 x source_kind='video_frame' (normalised to video)
- 3 x non-standard room_id 'grand_baroque_library_archival' mapped to other
- 3 x row N lacks 'row' key (books,position,row_index)
- 3 x non-standard room_id 'archive_stacks' mapped to other

## Per source: titles read, by confidence

### Hq66X9f-zgc: Umberto Eco, Sulla memoria. Una conversazione in tre parti, 2015. Parte 1. Regia di Davide Ferrario

Files: `spines_Hq66X9f-zgc.jsonl`. Frames: 35, titled sightings: 2, unlabelled spines: 815, distinct included titles: 2.

- **high** (1): Имя розы (Умберто Эко (Umberto Eco))
- **medium** (1): Une image peut en cacher une autre

### zj1kwT87ne0: Umberto Eco, Sulla memoria. Una conversazione in tre parti, 2015. Parte 2. Regia di Davide Ferrario

Files: `spines_zj1kwT87ne0.jsonl`. Frames: 33, titled sightings: 4, unlabelled spines: 995, distinct included titles: 3.

- **high** (3): [no title; author only: Umberto Eco]; Inventing the Enemy (Umberto Eco); Имя розы (Умберто Эко (Umberto Eco))

### B-M8V0PcCrw: Umberto Eco, Sulla memoria. Una conversazione in tre parti, 2015. Parte 3. Regia di Davide Ferrario

Files: `spines_B-M8V0PcCrw.jsonl`. Frames: 39, titled sightings: 5, unlabelled spines: 950, distinct included titles: 4.

- **high** (3): Inventing an Enemy (Umberto Eco); Italia Vostra; Имя розы (Умберто Эко (Umberto Eco))
- **medium** (1): Une image peut en cacher une autre

### iRXEQVTI95k: I libri e lo Studiolo di Umberto Eco, meraviglie alla Braidense

Files: `spines_iRXEQVTI95k.jsonl`, `spines_iRXEQVTI95k_dense.jsonl`. Frames: 100, titled sightings: 41, unlabelled spines: 1201, distinct included titles: 21.

- **high** (12): An Essay Towards a Real Character and a Philosophical Language (John Wilkins); Ars magna (Raymundus Lullus (Ramon Llull)); Ars Magna Lucis et Umbrae (Athanasius Kircher); Atalanta fugiens (Michael Maier); Corriere dei Piccoli; De mysteriis Aegyptiorum (Iamblichus); I misteri di Torino; Il Conte di Montecristo (Alexandre Dumas); Mandrake; Opera omnia (Raymundus Lullus (Ramon Llull)); Topolino giornalista; Vetera Analecta (Jean Mabillon)
- **medium** (4): Argumentum in librum Mercurii Trismegisti (preface) (Marsilio Ficino); Iamblichus De mysteriis Aegyptiorum, Chaldaeorum, Assyriorum (Iamblichus); L'ultimo Ras; Vetera Analecta, sive Collectio veterum aliquot operum & opusculorum omnis generis, carminum, epistolarum, diplomatum, epitaphiorum, &c. Cum itinere Germanico ... Nova editio (Joannes Mabillon (Jean Mabillon))
- **low** (5): [no title; author only: J.A. G[uer?]]; [no title; author only: J.J. Chenau (uncertain reading)]; [no title; author only: Raymundi Lullii]; Atalanta fugiens, hoc est Emblemata nova de secretis naturae chymica (Michael Maier); Le Service de la Beauté ([?.] Magé)

### NtPk4irDiM8: La biblioteca di Umberto Eco: i 32.000 libri disposti come nella casa milanese del semiologo e sc...

Files: `spines_NtPk4irDiM8.jsonl`, `spines_NtPk4irDiM8_dense.jsonl`. Frames: 135, titled sightings: 55, unlabelled spines: 3193, distinct included titles: 16.

- **high** (12): [no title; author only: Umberto Eco]; Bernini (Christian Tümpel); Das Foucaultsche Pendel (Umberto Eco); De Naam van de Roos (Umberto Eco); Dialogo sul papa eretico (Guglielmo di Ockham); Il nome della rosa (Umberto Eco); L'ente e l'essenza (Tommaso d'Aquino); Le Nom de la Rose (Umberto Eco); Ockham's Theory of Propositions (William of Ockham); Ockham's Theory of Terms (William of Ockham); Scritti sul pensiero medievale (Umberto Eco); Имя розы (Умберто Эко (Umberto Eco))
- **medium** (3): Cronica dels temps de Jaume I; Der Name der Rose (Umberto Eco); Les Querelles doctrinales à Paris (Zenon Kałuża)
- **low** (1): …oni sulla prospettiva medievale (G. Federici Vescovini)
- excluded (2, see below): Diario; …crònica en temps de Jaume I

### KZfOaug0mM4: 03/07/26 - I libri di Umberto Eco trovano casa a Bologna. inaugurata la nuova biblioteca

Files: `spines_KZfOaug0mM4_dense.jsonl`, `spines_KZfOaug0mM4.jsonl`. Frames: 105, titled sightings: 175, unlabelled spines: 1413, distinct included titles: 87.

- **high** (41): Alessandro Magnasco 1667-1749; Antonie van Dyck 1599-1641; Aufstieg und Niedergang der römischen Welt, II.12.1; Aufstieg und Niedergang der römischen Welt, II.12.2; Barocco; Bellini; Bernini (Christian Tümpel); Committenti d'età barocca (Maria Beatrice Failla, Clara Goria); Dialogo sul papa eretico (Guglielmo di Ockham); Felice Giani; Fiore / Detto d'Amore (Dante Alighieri (attrib.)); France Baroque; Georges de La Tour; Giorgione; Giulio Romano; Goya; Guido Cagnacci; Here Comes Everybody (Anthony Burgess); Historia del arte colonial Hispanoamericano; I disegni del Codice Resta di Palermo; Il genio di Roma 1592-1623; Il grande Borromeo tra storia e fede; James Joyce (Richard Ellmann); L'ente e l'essenza (Tommaso d'Aquino); La collezione di Franco Maria Ricci; Medieval Beasts (Ann Payne); Museo de Bellas Artes de Bilbao; Ockham's Theory of Propositions (William of Ockham); Ockham's Theory of Terms (William of Ockham); Palazzo Altieri; Paradiso perduto (Milton); Raffaello - I disegni; Rembrandt (Christian Tumpel); Rivedendo Correggio: l'Assunzione del Duomo di Parma; Scottish Art (Duncan Macmillan); Scritti sul pensiero medievale (Umberto Eco); Splendeurs d'Espagne I; Splendeurs d'Espagne II; The Widening Gyre (Frank Kermode); Venezia dei grandi viaggiatori; Vico & Joyce (Donald Phillip Verene)
- **medium** (28): [no title; author only: Ezra Pound]; Arte Indiana; Caravaggio and His Italian Followers; Castel del Monte; Cosmos; Dante Alighieri's Inferno Metaphor... (Dante Alighieri); decodeunicode; El Bodegón español; Europa 1492; I colori del tempo 2; I disegni del Codice Rosso di Palermo; Il Cerano; Il museo di Pechino; Illuminating the Renaissance; Joyce (Ezra Pound); L'Antico Testamento; La Bibbia; La Gioconda che...; Leonardo da Vinci; Leonardo di Vinci; Poesie (Friedrich Hölderlin); Rinascimento; Rolo Banca 1473: la civiltà...; Roma antica; The Idea of Art as Propaganda in France, 1750-1799 (James Leith); The Irish Comic Tradition (Vivian Mercier); Treasures of Islam; Van Dyck
- **low** (18): [no title; author only: Luciano]; [no title; author only: Tommaso [d'Aquino]]; [Tre]asures of Islam; Beniamino Simoni; Das alte Dresden (Fritz Laffer[?]); Giacomo Ceruti; Giovanni [Fede Cervicato?]; Il brigante; Il grande Borromeo: una storia e una fede; La nostra terra; La Rocca Pisana di Vicenza [di Scamozzi] (Barduz[zi]); Leonardo & [Vinci]; Plinio; Progetto umano; Stati Uniti d'Europa (Enrico Letta); Studi sulla prospettiva medievale; Toulouse-Lautrec; Époques de la fleur
- excluded (2, see below): [no title; author only: Jean Starobinski]; Genesis (Liber Bresith / Genesis)

### FeIUY9EhZgI: Umberto Eco: A Library of the World - Official Trailer

Files: `spines_FeIUY9EhZgI.jsonl`, `spines_FeIUY9EhZgI_dense.jsonl`. Frames: 128, titled sightings: 56, unlabelled spines: 2428, distinct included titles: 30.

- **high** (23): Alcifrone ossia il filosofo minuzioso (George Berkeley); Ars Magna Lucis et Umbrae (Athanasius Kircher); Ars Magna Lucis et Umbrae, in decem libros digesta (Athanasius Kircher); Ars Magna Sciendi (Athanasius Kircher); Aufstieg und Niedergang der römischen Welt, II. Principat, Bd. 15; Aufstieg und Niedergang der römischen Welt, II.11.1; Aufstieg und Niedergang der römischen Welt, II.12.1; Aufstieg und Niedergang der römischen Welt, II.12.2; Aufstieg und Niedergang der römischen Welt, II.12.3; Aufstieg und Niedergang der römischen Welt, II.13; Aufstieg und Niedergang der römischen Welt, II.14; China Illustrata (Athanasius Kircher); Critica della ragion pratica (Immanuel Kant); Critica della ragion pura (Immanuel Kant); Dizionario filosofico (Voltaire); Dizionario filosofico: tutte le voci del Dizionario filosofico e delle Domande sull'Enciclopedia (Voltaire); La Scienza Nuova - Le tre edizioni del 1725, 1730 e 1744 (Giambattista Vico); La tradizione signorile nella filosofia americana e altri saggi (George Santayana); Mundus Subterraneus (Athanasius Kircher); Saggio sull'intelletto umano (John Locke); Trattato della natura umana (David Hume); Turris Babel (Athanasius Kircher); Tutte le opere (1721-1754) (Montesquieu)
- **medium** (6): Alciphron, ovvero il filosofo minuto (George Berkeley); Aufstieg und Niedergang der römischen Welt, II.7.1; Aufstieg und Niedergang der römischen Welt, II.7.2; Aufstieg und Niedergang der römischen Welt, II.9.2; Obeliscus [Pamphilius?] (Athanasius Kircher); Obeliscus Pamphilius (Athanasius Kircher)
- **low** (1): Aufstieg und Niedergang der römischen Welt, II.9.1
- excluded (5, see below): Intellectual Property Law of East Asia; La responsabilita amministratori sindaci direttori generali liquidatori di societa; The Economics of Legal R[elationships?], Volume 3; The German Law of Obligations, Volume I: The Law of Contracts and Restitution; The German Law of Obligations, Volume II: The Law of Torts (Third Edition)

### bcK8rOkcb3k: Umberto Eco - La Biblioteca del Mondo (Trailer Ufficiale)

Files: `spines_bcK8rOkcb3k.jsonl`, `spines_bcK8rOkcb3k_dense.jsonl`. Frames: 135, titled sightings: 64, unlabelled spines: 3006, distinct included titles: 31.

- **high** (22): Ars Magna Lucis et Umbrae (Athanasius Kircher); Ars Magna Lucis et Umbrae, in decem libros digesta (Athanasius Kircher); Ars Magna Sciendi (Athanasius Kircher); Aufstieg und Niedergang der römischen Welt, II. Principat, Bd. 15; Aufstieg und Niedergang der römischen Welt, II.11.1; Aufstieg und Niedergang der römischen Welt, II.12.1; Aufstieg und Niedergang der römischen Welt, II.12.2; Aufstieg und Niedergang der römischen Welt, II.12.3; Aufstieg und Niedergang der römischen Welt, II.13; Aufstieg und Niedergang der römischen Welt, II.14; China Illustrata (Athanasius Kircher); Critica della ragion pratica (Immanuel Kant); Critica della ragion pura (Immanuel Kant); Dizionario filosofico (Voltaire); Dizionario filosofico: tutte le voci del Dizionario filosofico e delle Domande sull'Enciclopedia (Voltaire); La Scienza Nuova - Le tre edizioni del 1725, 1730 e 1744 (Giambattista Vico); La tradizione signorile nella filosofia americana e altri saggi (George Santayana); Mundus Subterraneus (Athanasius Kircher); Saggio sull'intelletto umano (John Locke); Trattato della natura umana (David Hume); Turris Babel (Athanasius Kircher); Tutte le opere (1721-1754) (Montesquieu)
- **medium** (7): [no title; author only: Athanasii Kircheri (running head)]; Alciphron, ovvero il filosofo minuto (George Berkeley); Aufstieg und Niedergang der römischen Welt, II.7.1; Aufstieg und Niedergang der römischen Welt, II.7.2; Aufstieg und Niedergang der römischen Welt, II.9.2; Obeliscus [Pamphilius?] (Athanasius Kircher); Obeliscus Pamphilius (Athanasius Kircher)
- **low** (2): [no title; author only: Berkeley]; Aufstieg und Niedergang der römischen Welt, II.9.1
- excluded (4, see below): Intellectual Property Law of East Asia; The Economics of Legal R[elationships?], Volume 3; The German Law of Obligations, Volume I: The Law of Contracts and Restitution; The German Law of Obligations, Volume II: The Law of Torts (Third Edition)

### ygvl-_gtAP8: Clip from Umberto Eco - La biblioteca del mondo (Umberto Eco: A Library of the World, 2022, sub ENG)

Files: `spines_ygvl-_gtAP8.jsonl`, `spines_ygvl-_gtAP8_dense.jsonl`. Frames: 185, titled sightings: 190, unlabelled spines: 3286, distinct included titles: 48.

- **high** (30): [no title; author only: Petrus Galatinus (Pietro Colonna Galatino)]; [no title; author only: R. Fludd]; A Theory of Semiotics (Umberto Eco); Anatomiae Amphitheatrum (Robert Fludd); Ars Magna Lucis et Umbrae (Athanasius Kircher); Artis Cabalisticae (scriptores) (ed. Johann Pistorius); Cmentarz w Pradze (Umberto Eco); De Arcanis Catholicae Veritatis (Petrus Galatinus (Pietro Colonna Galatino)); De begraafplaats van Praag (Umberto Eco); De Macrocosmi Historia (Utriusque Cosmi Historia) (Robert Fludd); Die Bücher und das Paradies (Umberto Eco); Dronning Loanas mystiske flamme (Umberto Eco); Foucault's Pendulum (Umberto Eco); Fukoovo klatno (Umberto Eko); Il Pendolo di Foucault (Umberto Eco); Inventing the Enemy (Umberto Eco); Istoriya urodstva (История уродства) (Умберто Эко (ред.)); Istoriya yevropeiskoyi tsyvilizatsiyi: Rym (Історія європейської цивілізації: Рим) (Umberto Eko (editor)); Kant and the Platypus (Umberto Eco); O Cemitério de Praga (Umberto Eco); On Literature (Umberto Eco); Opus mago-caballisticum (Sallwigt); Opus Mago-Cabbalisticum et Theosophicum (Georg von Welling (pseud. Sallwigt)); Ortaçağ (Umberto Eco); Prahos kapinės (Umberto Eco); Prazkyi tsvyntar (Празький цвинтар) (Умберто Еко); The Mysterious Flame of Queen Loana (Umberto Eco); Tractatus (Robert Fludd); Turris Babel (Athanasius Kircher); Баудолино (Umberto Eco)
- **medium** (8): [no title; author only: Athanasii Kircheri (running head)]; [no title; author only: Athanasius Kircher [running head]]; [no title; author only: Bongo (Pietro Bongo / Bungus)]; De Arcanis Catholicae Veritatis (or another work) (Richard of Saint Victor (Richardus a Sancto Victore)); Dictionarium Scripturae Sacrae (Augustin Calmet); Numerorum Mysteria (Pietro Bongo (Petrus Bungus)); Philosophia Moysaica (Robert Fludd); Тайнственное пламя царицы Лоаны (Umberto Eco)
- **low** (10): [no title; author only: Caramuel]; [no title; author only: Mastriani]; [no title; author only: possibly Augustinus (uncertain)]; [no title; author only: Richar[d] a S. Ulric[i]]; Anatomia Amphitheatrum (David [surname not legible]); Arithmeticum (or similar) (Juan Caramuel y Lobkowitz); Artis Cabalistic[ae]; Coelum Sephiroticum (Kabbala-related treatise); Lexicon Alchemiae (Martin Ruland); Самеliche Werke (Umberto Eco)
- excluded (12, see below): (a work by Mastriani, exact title not legible); (Hebrew-language edition, title not transcribed); (untranslated non-Latin script edition); Dronningen Loanas mystiske flamme; Fukoovo klatno (Foucault's Pendulum); La memoria vegetale [e altri scritti di bibliofilia]; Opera aperta; Sull'immortalità; Superman; История уродства (On Ugliness); Пражское кладбище (The Prague Cemetery); Історія європейської цивілізації

### M8IWTOFNlOc: Writer Umberto Eco: I Was Always Narrating \| Louisiana Channel

Files: `spines_M8IWTOFNlOc.jsonl`, `spines_M8IWTOFNlOc_dense.jsonl`. Frames: 496, titled sightings: 75, unlabelled spines: 589, distinct included titles: 26.

- **high** (13): [no title; author only: Umberto Eco]; A paso de cangrejo (Umberto Eco); A Theory of Semiotics (Umberto Eco); Apocalypse Postponed (Umberto Eco); Baudolino (Umberto Eco); Dando buca a Godot (Bartezzaghi); Il ritorno di Himmelfarb (Michael Kruger); Lavorando anche per il futuro (Mario Andreose); Le cose che ho imparato (Gianni Riotta); The Island of the Day Before (Umberto Eco); The Mysterious Flame of Queen Loana (Umberto Eco); The Prague Cemetery (Umberto Eco); To Koimeterio tes Pragas (Umberto Eco)
- **medium** (4): Ernst Blochs Wirkung; Razza e destino (Walter Benjamin); To Koimitirio tis Pragas (The Prague Cemetery, Greek edition) (Oumperto Eko [Umberto Eco]); Un Segno (Umberto Eco)
- **low** (9): [no title; author only: George Steiner]; [no title; author only: Maria Bellonci]; [no title; author only: Mario Andreose]; [no title; author only: Orhan Pamuk]; [Tra]dizione e rivoluzione (Franc[o Fortini]); Aprendo le casse della mia biblioteca (Walter Benjamin); Nero Wolfe (edition/collection title not fully legible); Quattro modi dell'amore; Spettri [...] dell'amore

### rMSOvDAyH5c: Umberto Eco Interview: Advice to the Young

Files: `spines_rMSOvDAyH5c.jsonl`. Frames: 16, titled sightings: 0, unlabelled spines: 32, distinct included titles: 0.


### zZEy10fpq3I: Umberto Eco: La biblioteca del mundo (2022) 1080p

Files: `spines_zZEy10fpq3I_dense.jsonl`, `spines_zZEy10fpq3I_part0.jsonl`, `spines_zZEy10fpq3I_part1.jsonl`, `spines_zZEy10fpq3I_part2.jsonl`, `spines_zZEy10fpq3I_part3.jsonl`, `spines_zZEy10fpq3I_part4.jsonl`, `spines_zZEy10fpq3I_piano.jsonl`, `spines_zZEy10fpq3I_piano_heavy.jsonl`, `spines_zZEy10fpq3I_part5.jsonl`, `spines_zZEy10fpq3I_part6.jsonl`, `spines_zZEy10fpq3I_part7.jsonl`. Frames: 933, titled sightings: 1359, unlabelled spines: 10948, distinct included titles: 316. Timestamp offset +0.96 s.

- **high** (127): [no title; author only: Gianni Vattimo]; [no title; author only: Gillo Dorfles]; [no title; author only: Petrus Galatinus (Pietro Colonna Galatino)]; [no title; author only: R. Fludd]; [no title; author only: Richardus a Sancto Victore]; [no title; author only: Umberto Eco]; A Passo de Caranguejo (Umberto Eco); A passo di gambero (Umberto Eco); A proposito di niente (Woody Allen); A Theory of Semiotics (Umberto Eco); Alcifrone ossia il filosofo minuzioso (George Berkeley); Anatomiae Amphitheatrum (Robert Fludd); Annuario Filosofico 1993; Annuario Filosofico 1994; Apocalypse Postponed (Umberto Eco); Aristotelis Opera (Aristoteles); Ars Magna Lucis et Umbrae (Athanasius Kircher); Ars Magna Lucis et Umbrae, in decem libros digesta (Athanasius Kircher); Ars Magna Sciendi (Athanasius Kircher); Ars Magna Sciendi, sive Combinatoria (Athanasius Kircher); Artificio di memoria (Fabio Mauri); Artis Cabalisticae (scriptores) (ed. Johann Pistorius); Auf den Schultern von Riesen (Umberto Eco); Aufstieg und Niedergang der römischen Welt, II. Principat, Bd. 15; Aufstieg und Niedergang der römischen Welt, II. Principat, Bd. 16.1; Aufstieg und Niedergang der römischen Welt, II.11.1; Aufstieg und Niedergang der römischen Welt, II.12.1; Aufstieg und Niedergang der römischen Welt, II.12.2; Aufstieg und Niedergang der römischen Welt, II.12.3; Aufstieg und Niedergang der römischen Welt, II.13; Aufstieg und Niedergang der römischen Welt, II.14; Begravningsplatsen i Prag (Umberto Eco); Breve autobiografia (Giuseppe Tornatore); China Illustrata (Athanasius Kircher); Cmentarz w Pradze (Umberto Eco); Critica della ragion pratica (Immanuel Kant); Critica della ragion pura (Immanuel Kant); De begraafplaats van Praag (Umberto Eco); De Macrocosmi Historia (Roberto Fludd); De Macrocosmi Historia (Utriusque Cosmi Historia) (Robert Fludd); Der ewige Faschismus (Umberto Eco); Der Friedhof in Prag (Eco); Die Bücher und das Paradies (Umberto Eco); Die Geschichte der Schönheit (Eco); Dizionario filosofico (Voltaire); Dizionario filosofico: tutte le voci del Dizionario filosofico e delle Domande sull'Enciclopedia (Voltaire); Dronning Loanas mystiske flamme (Umberto Eco); Everyman's Talmud (Abraham Cohen); Filosofia della rivelazione (Schelling); Foucault's Pendulum (Umberto Eco); Fukoovo klatno (Umberto Eko); Giorgio Morandi: une retrospective; Histoire des langues; Hitler; I misteri dell'altare di Isenheim di Grunewald (Giovanni Reale); I mutanti (Sofia Bignamini); Il bambino nascosto (Roberto Ando); Il bene e il male (Giulio Giorello, Vittorio Sgarbi); Il cacciatore celeste (Roberto Calasso); Il Conte di Montecristo (Alexandre Dumas); Il Corsaro delle Tenebre; Il crollo (Lorenzo Pregliasco); Il nome della rosa (Umberto Eco); Il Novecento; Il Pendolo di Foucault (Umberto Eco); Il volto del '900: da Matisse a Bacon, capolavori dal Centre Pompidou; Interviste e colloqui (Luciano Berio); Inventing the Enemy (Umberto Eco); Istoriya urodstva (История уродства) (Умберто Эко (ред.)); Istoriya yevropeiskoyi tsyvilizatsiyi: Rym (Історія європейської цивілізації: Рим) (Umberto Eko (editor)); Joco-seriorum Naturae et Artis, sive Magiae Naturalis (Athanasius Kircherus); Kant and the Platypus (Umberto Eco); Kant und das Schnabeltier (Umberto Eco); Kircheri de Arte Magnetica (Athanasius Kircher); L'anima ciliegia (Lia Levi); L'era della comunicazione (Umberto Eco); La luce oltre il vetro (Lorenzo Puglisi); La Scienza Nuova - Le tre edizioni del 1725, 1730 e 1744 (Giambattista Vico); La tradizione signorile nella filosofia americana e altri saggi (George Santayana); Le Robert; Le Roy Soleil; Lo scaffale infinito (Andrea Kerbaker); Maometto; Medioevo; Mundus Subterraneus (Athanasius Kircher); Note (Giancarlo Iliprandi); O Cemitério de Praga (Umberto Eco); Obeliscus Aegyptiacus (Athanasius Kircher); On Literature (Umberto Eco); Opus mago-caballisticum (Sallwigt); Opus Mago-Cabbalisticum et Theosophicum (Georg von Welling (pseud. Sallwigt)); Ortaçağ (Umberto Eco); Palazzo Altieri; Pinocchio; Prahos kapinės (Umberto Eco); Prazkyi tsvyntar (Празький цвинтар) (Умберто Еко); Questo e Kafka (Reiner Stach); Ricordi di un entomologo I (Jean-Henri Fabre); Rivedendo Correggio: l'Assunzione del Duomo di Parma; Romanino e la 'Sistina dei poveri' a Pisogne; Saggio sull'intelletto umano (John Locke); Saggio sulla disuguaglianza delle razze umane (Arthur de Gobineau); San Juan de la Cruz y el Islam; Scritti a mano (Matteo Motolese); Semiotik des Films; Splendeurs d'Espagne II; Storia del racconto popolare: prima del fumetto; Tela Ignea Satanae, Tom. I (Johann Christoph Wagenseil); The Age of Lamarck; The Mysterious Flame of Queen Loana (Umberto Eco); The Prague Cemetery (Umberto Eco); The Search for the Perfect Language (Umberto Eco); Thesaurus Anatomicus (Frederik Ruysch); Tractatus (Robert Fludd); Trattato della natura umana (David Hume); Turris Babel (Athanasius Kircher); Tutte le opere (1721-1754) (Montesquieu); Umberto Eco e il PCI; Una voce; Versus; Viaggio in Italia (Guido Piovene); Vivere con gli dei (Neil MacGregor); Voglia di libri (Mario Andreose); Баудолино (Umberto Eco); История уродства (Умберто Эко (ed.)); Празький цвинтар (У. Еко (Umberto Eco)); Рим (под редакцией Умберто Еко)
- **medium** (114): [no title; author only: A. Dumas]; [no title; author only: Anna Ottani Cavina]; [no title; author only: Athanasius Kircher [running head]]; [no title; author only: Basil Gray]; [no title; author only: Bongo (Pietro Bongo / Bungus)]; [no title; author only: Bursill-Hall]; [no title; author only: Carducci]; [no title; author only: Diego Fusaro]; [no title; author only: Gaffarel]; [no title; author only: George Santayana]; [no title; author only: Giambattista Vico]; [no title; author only: Giuseppe Tornatore]; [no title; author only: Ivano Dionigi]; [no title; author only: Jean de la Hire]; [no title; author only: Jean-François Champollion (about)]; [no title; author only: Samuel Beckett]; [no title; author only: Ουμπέρτο Έκο]; Annales de chimie et de physique; Aufstieg und Niedergang der römischen Welt — Tafeln/Register volume; Avicenne; Behmen's Works; Bond; Cabala; Carmen (In honorem et gloriam ... Chrisostomi Mathanasii); Cerchi di capire, prof (Giovanna Cosenza); Chi mi ha fatta in testa?; China [Monumentis ...] Illustrata (Athanasius Kircher); Ciarlatani (Fausto Colombo); Clave; Come si agisce (Balestrini); Compagni di scuola; Cum se face o teză de licență (Umberto Eco); Da Hitler a Casablanca via Hollywood (Francesco Carbone); Das Irrenhaus; De Coelo et de Inferno; De Sepulchris Hebraeorum; Dictionarium Scripturae Sacrae (Augustin Calmet); Due sigari in riva al mare (Michael Köhlmeier); Ecolinus; Ernst Blochs Wirkung; Fantomas; Francis Bacon: Concealed and Revealed ([Bertram G.] Theobald); I bambini di Marte (Lazzarato); I Misteri della Jungla Nera (Salgari); I segreti dei fiori; Il bel tacere (Pietro Salabe); Il ceffo di Sir Thomas Browne (Roberto Calasso); Il Cimitero di Praga (Umberto Eco); Il Corsaro Nero (Salgari); Il Giardino delle Camelie; Il giornale di Gian Burrasca; Il Giornalino; Il libro rosso; Il paradiso delle aragoste; Il Revival; Il superuomo di massa. Retorica e ideologia nel romanzo popolare (Umberto Eco); il verri; Illuminating the Renaissance; Imię róży (Umberto Eco); Immagini dell'Italia. 1; Intertesto (Mario Ciampi); Intertexto (Mario Chamie); Iter Exstaticum; Joco-Seriorum Naturae et Artis Diatribe (Athanasius Kircherus); Kant en het vogelbekdier (Umberto Eco); L'attico reclamato; L'autre jour Colin malade dedans son lict; L'eredità di Umberto Eco; L'innominabile attuale (Roberto Calasso); L'Uomo Mascherato; La Gioconda che...; La memoria vegetale e altri scritti di bibliofilia (Umberto Eco); La scienza nuova (Giambattista Vico); La tradizione signorile nella Spagna americana (George Santayana); Le isole (Opera Omnia) (Giorgio de Chirico); Le Tigri di Mompracem (E. Salgari); Leonardo di Vinci; Linus; Livre d'Heures d'Anne de Bretagne; Mersenne ou la naissance du mécanisme; Numero Zero (Umberto Eco); Obeliscus [Pamphilius?] (Athanasius Kircher); Obeliscus Pamphilius (Athanasius Kircher); Old Testament; Opus Mago-Cabbalisticum (Sallwigt); Ordini Equestri; Philosophia Moysaica (Robert Fludd); Philosophia Nova; Physica Curiosa (Gaspar Schott (C. Schotti)); Poëme heureusement découvert & mis au jour, avec des Remarques savantes & recherchées (Chrisostome Matanasius (Docteur)); Pražský hřbitov (Umberto Eco); Puikaantekeningen van 't Pronkjuweel der Aarts-Letter-Helden, Doctor Mathanasius; Sandokan alla Riscossa (E. Salgari); Storia delle terre e dei luoghi leggendari; Storie di percorso (Roberto Campari); Sulle spalle dei giganti (Umberto Eco); Sulle spalle di Umberto; Systema Sephyroticum X Divinorum Nominum; Tabula Kircheriana; Tempo di Libri. Programma 2017; Terre senz'ombra (Anna Ottani Cavina); The Future of the Book; The Plot: The Secret Story of the Protocols of the Elders of Zion; The Templars; Traduction Françoise: Poëme à la louange du très excellent et très subtil docteur Chrisostome Matha[nasius]; Trattato di Semiotica Generale (Umberto Eco); Turris Babel sive Archontologia (Athanasius Kircher); Una passione a Manhattan (Anna Ottani Cavina); Una scrittura sconcertante; Utriusque Cosmi Historia (De Macrocosmi Historia) (Robert Fludd (Roberto Fludd)); Vescovi e Chiesa d'Alessandria, Tomo II (G.A. Chiozzi); Vetera Analecta, sive Collectio veterum aliquot operum & opusculorum omnis generis, carminum, epistolarum, diplomatum, epitaphiorum, &c. Cum itinere Germanico ... Nova editio (Joannes Mabillon (Jean Mabillon)); Пражское кладбище (Умберто Еко); 프라하의 묘지 (The Prague Cemetery)
- **low** (75): [...] la primavera; [...]ca dei Miei Ragazzi; [...]della memoria; [no title; author only: [Stevenson?]]; [no title; author only: Aldo Buzzi]; [no title; author only: Auro Rosa (?)]; [no title; author only: Bacon]; [no title; author only: Beniamino Placido]; [no title; author only: Berkeley]; [no title; author only: C. Huijberts]; [no title; author only: Chrysostomus Mathanasius (fictional 'Doctor')]; [no title; author only: Cletto Arrighi]; [no title; author only: Emilio Salgari (per shelf tag)]; [no title; author only: Enzo Golino]; [no title; author only: Ercole Patti]; [no title; author only: G.[D.] Chio[tti]]; [no title; author only: Giovanna Cosenza]; [no title; author only: Gérard de Nerval]; [no title; author only: I. Pezzini; B. Finocchi (a cura di)]; [no title; author only: John Locke]; [no title; author only: Jurij M. Lotman]; [no title; author only: Lia Levi]; [no title; author only: Luigi Spagnol]; [no title; author only: M. Gatti (?)]; [no title; author only: Mario Baudino]; [no title; author only: Michael Maier (uncertain)]; [no title; author only: Philostrate (Philostratus)]; [no title; author only: Ric[?]]; [no title; author only: Roberto Calasso]; [no title; author only: Roberto Campari]; [no title; author only: Ser[r]agli[o] di G[...]]; [no title; author only: Stella Rizzo]; [Philostrate?]; [Philostrati Opera] (Flavius Philostratus (?)); [Vie d']Anne de Bretagne; Amphitheatrum Sapientiae Socraticae Joco-Seriae; Carducci (Giosuè Carducci); Champollion (Jean Lacouture); Chi muore si rivede; Critique; De Sepulchro[?] Hebraeorum[?]; Dizionario Geografico Italiano, Vol. I; Eco; Eroi del racconto popolare; Fenice; I miei scrittori e altri animali; Il mistero de...; Il primo [...] del mondo; In Signs / TnSigns; Iter Ex[s]tati[cum] cum Kircheria[num] (Athanasius Kircher (ed. Gaspar Schott?)); L'inconsolabile pensiero; L'omicidio di Umberto Eco (Oscar Rimini); La colpa dell'agnello; La Divina Commedia ([Dante Alighieri]); La sindrome del pallone (Marcello Carra); Lanzarote (Michel Houellebecq); Le metamorfosi di Narciso; Les Cahiers Feministes; Lexicon Hermeticum[?]; Marie Curie; Modern Art Nouveau; Monumenti Italiani del '900; Oedipus Aegyptiacus[?] (Athanasius Kircher (Kircheri)); Origin of Langu[age]; Polygraphia nova (Athanasius Kircher (Kircherii)); Prague Cemetery (Russian/Ukrainian ed.) (Умберто Еко); Prodromus Coptus (Athanasius Kircherus); Storia di Alessandria; Tafeln; The [Birth] of the Gods and Giants; The Bacon-Shak[e]spea[re Question / Mystery]; Thesaurus Armamentarii Medico[...]; Un sogno per tutti; Una passione [costante?]; Името на розата
- excluded (51, see below): [no title; author only: J. Chasseguet-Smirgel]; [no title; author only: Léo Taxil]; A New Study of Shakespeare; Annals of the Life and Work of William Shakespeare; Apocalittici e integrati; Bacon, Shakespeare, and the Rosicrucians; Clave: diccionario de uso del español actual; Dagli scritti di Umberto Eco; Dall'Albero al Labirinto; Der Spiegel; Des signes et de l'art de penser considérés dans leurs rapports mutuels, tome 1; Des signes et de l'art de penser considérés dans leurs rapports mutuels, tome 2; Des signes et de l'art de penser considérés dans leurs rapports mutuels, tome 3; Des signes et de l'art de penser considérés dans leurs rapports mutuels, tome 4; Dethroning Shakspere; Encyclopaedia Judaica; Ex libris Umberto Eco; I Misteri della Framassoneria; Il nome de la rosa; L'isola del giorno prima; La memoria vegetale [e altri scritti di bibliofilia]; La misteriosa fiamma della Regina Loana; Le Garzantine: Medioevo; Lo snob; Lois Lane; Nafn Rósarinnar; New Glossary of the Obscure Words in Shakespeare, and the Dramatists of the Seventeenth Century; Opere (Carducci); Qizilgülün Adi; Qizilgülün adı; Rosens namn; Shakespeare Studies; Shakespeare's Beehive; Storia della bruttezza; Superman; Tempus, Aevum, Aeternitas; The Gaelic Etymology of the Languages of Western Europe; The Great Cryptogram: Francis Bacon's Cipher in the So-Called Shakespeare Plays; The Name of the Rose; Tractatus de Venenis; William Shakespeare's Comedies, Histories, Tragedies, and Poems; Το όνομα του ρόδου (To onoma tou rodou); Վարդի անունը (Vardi anunըy); اسم الوردة; اسم الوردة (Ism al-Warda) / Il nome della rosa; สัญญาแห่งดอกกุหลาบ; 中共党史人物传 (Zhonggong Dangshi Renwu Zhuan / Biographies of CPC Party History Figures); 薔薇の名前; 薔薇の名前 (Bara no namae), vol. 下 (2); 장미의 이름; 장미의 이름 (Jangmiui ireum) [하] — The Name of the Rose, vol.2, revised edition

### photo: Photographs (spines_photos.jsonl)

Files: `spines_photos.jsonl`. Frames: 65, titled sightings: 68, unlabelled spines: 6054, distinct included titles: 62.

- **high** (37): [no title; author only: Alessandro di Afrodisia]; [no title; author only: Edmond Jabès]; [no title; author only: Epitteto]; [no title; author only: Eunapio (Eunapius)]; [no title; author only: John Henry Newman]; [no title; author only: Lev Šestov]; [no title; author only: Stendhal]; [no title; author only: Umberto Eco]; Atalanta fugiens (Michael Maier); Berkeley; Bernini (Christian Tümpel); David Hume; De la maladie d'amour; De supernaturali historia (Utriusque cosmi historia) (Robert Fludd); Elephanti descriptio (Georg Christoph Petri von Hartenfels); Emblemata (Florentius Schoonhovius (Florent Schoonhoven)); Filosofia della musica; Fisica (Aristotele); Geheime Figuren der Rosenkreuzer; Giorgione; Gli Eleati; Hitler; La regina delle fate (Edmund Spenser); Le Robert; Locke; Michel de Montaigne; Montesquieu; Museum Wormianum (Ole Worm (Olaus Wormius)); Poetica (Aristotele); Port-Royal (Charles Augustin Sainte-Beuve); Rembrandt (Christian Tumpel); Retorica (Aristotele); Schelling; Schola Salernitana; The Book of Kells; Turris Babel (Athanasius Kircher); Voltaire
- **medium** (21): [no title; author only: Hölderlin]; [no title; author only: Jan Patočka]; [no title; author only: William Shakespeare]; A. Bueno; Agostino; Alchimie; Bertozzi; China monumentis (Athanasius Kircher); Clave: diccionario de uso del español; Gli antichi commentatori; Guglielmo di Ockham; L'Antico Testamento; L'eccellenza di Dio; L'origine delle razze; Le opere logiche (Aristotele); Le relationi universali (Giovanni Botero); Matisse; Mercator; Prophéties (Nostradamus); Puglia; Thesaurus animalium / Thesaurus anatomicus (Frederik Ruysch)
- **low** (4): [no title; author only: Filippo Bonanni]; Die Bilder; Elogio della pazzia; Z

## All included titles

Sorted by first sighting (videos in `videos.json` order, then photographs). The link is the first sighting.

| # | title | author | lang | conf | room | first seen | sightings |
|---:|---|---|---|---|---|---|---:|
| 1 | Имя розы | Умберто Эко (Umberto Eco) | ru | high | salotto | [Hq66X9f-zgc 00:00:34](https://www.youtube.com/watch?v=Hq66X9f-zgc&t=34s) | 6 |
| 2 | Une image peut en cacher une autre |  | fr | medium | salotto | [Hq66X9f-zgc 00:00:34](https://www.youtube.com/watch?v=Hq66X9f-zgc&t=34s) | 2 |
| 3 | Inventing the Enemy | Umberto Eco | en | high | studio | [zj1kwT87ne0 00:00:27](https://www.youtube.com/watch?v=zj1kwT87ne0&t=27s) | 17 |
| 4 | [no title; author only: Umberto Eco] | Umberto Eco | fr | high | studio | [zj1kwT87ne0 00:00:34](https://www.youtube.com/watch?v=zj1kwT87ne0&t=34s) | 59 |
| 5 | [no title; author only: Raymundi Lullii] | Raymundi Lullii | la | low | studio | [iRXEQVTI95k 00:00:22](https://www.youtube.com/watch?v=iRXEQVTI95k&t=22s) | 3 |
| 6 | [no title; author only: J.J. Chenau (uncertain reading)] | J.J. Chenau (uncertain reading) | fr | low | antichi | [iRXEQVTI95k 00:00:53](https://www.youtube.com/watch?v=iRXEQVTI95k&t=53s) | 1 |
| 7 | [no title; author only: J.A. G[uer?]] | J.A. G[uer?] | fr | low | antichi | [iRXEQVTI95k 00:00:53](https://www.youtube.com/watch?v=iRXEQVTI95k&t=53s) | 2 |
| 8 | [no title; author only: Tommaso [d'Aquino]] | Tommaso [d'Aquino] | it | low | bologna | [KZfOaug0mM4 00:00:29](https://www.youtube.com/watch?v=KZfOaug0mM4&t=29s) | 1 |
| 9 | [no title; author only: Ezra Pound] | Ezra Pound | en | medium | corridoio | [KZfOaug0mM4 00:01:41](https://www.youtube.com/watch?v=KZfOaug0mM4&t=101s) | 2 |
| 10 | [no title; author only: Luciano] | Luciano | it | low | bologna | [KZfOaug0mM4 00:02:11](https://www.youtube.com/watch?v=KZfOaug0mM4&t=131s) | 1 |
| 11 | [no title; author only: Berkeley] | Berkeley | it | low | studio | [bcK8rOkcb3k 00:00:39](https://www.youtube.com/watch?v=bcK8rOkcb3k&t=39s) | 3 |
| 12 | [no title; author only: Athanasii Kircheri (running head)] | Athanasii Kircheri (running head) | la | medium | studio | [bcK8rOkcb3k 00:00:40](https://www.youtube.com/watch?v=bcK8rOkcb3k&t=40s) | 6 |
| 13 | [no title; author only: possibly Augustinus (uncertain)] | possibly Augustinus (uncertain) | la | low | unknown | [ygvl-_gtAP8 00:00:03](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=3s) | 1 |
| 14 | [no title; author only: Richar[d] a S. Ulric[i]] | Richar[d] a S. Ulric[i] | la | low | unknown | [ygvl-_gtAP8 00:00:19](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=19s) | 1 |
| 15 | [no title; author only: Athanasius Kircher [running head]] | Athanasius Kircher [running head] | la | medium | vestibolo | [ygvl-_gtAP8 00:00:27](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=27s) | 20 |
| 16 | [no title; author only: Bongo (Pietro Bongo / Bungus)] | Bongo (Pietro Bongo / Bungus) | la | medium | antichi | [ygvl-_gtAP8 00:00:38](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=38s) | 16 |
| 17 | [no title; author only: Petrus Galatinus (Pietro Colonna Galatino)] | Petrus Galatinus (Pietro Colonna Galatino) | la | high | antichi | [ygvl-_gtAP8 00:00:39](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=39s) | 9 |
| 18 | [no title; author only: R. Fludd] | R. Fludd | la | high | antichi | [ygvl-_gtAP8 00:00:41](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=41s) | 19 |
| 19 | [no title; author only: Caramuel] | Caramuel | la | low | antichi | [ygvl-_gtAP8 00:00:43](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=43s) | 2 |
| 20 | [no title; author only: Mastriani] | Mastriani | it | low | bologna | [ygvl-_gtAP8 00:01:06](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=66s) | 2 |
| 21 | [no title; author only: George Steiner] | George Steiner |  | low | studio | [M8IWTOFNlOc 00:01:11](https://www.youtube.com/watch?v=M8IWTOFNlOc&t=71s) | 5 |
| 22 | [no title; author only: Mario Andreose] | Mario Andreose | it | low | studio | [M8IWTOFNlOc 00:23:24](https://www.youtube.com/watch?v=M8IWTOFNlOc&t=1404s) | 5 |
| 23 | [no title; author only: Orhan Pamuk] | Orhan Pamuk | de | low | studio | [M8IWTOFNlOc 00:23:29](https://www.youtube.com/watch?v=M8IWTOFNlOc&t=1409s) | 5 |
| 24 | [no title; author only: Maria Bellonci] | Maria Bellonci | it | low | studio | [M8IWTOFNlOc 00:23:31](https://www.youtube.com/watch?v=M8IWTOFNlOc&t=1411s) | 1 |
| 25 | [no title; author only: Ercole Patti] | Ercole Patti | it | low | bologna | [zZEy10fpq3I 00:05:22](https://www.youtube.com/watch?v=zZEy10fpq3I&t=322s) | 1 |
| 26 | [no title; author only: Aldo Buzzi] | Aldo Buzzi | it | low | bologna | [zZEy10fpq3I 00:05:22](https://www.youtube.com/watch?v=zZEy10fpq3I&t=322s) | 1 |
| 27 | [no title; author only: Jurij M. Lotman] | Jurij M. Lotman | it | low | bologna | [zZEy10fpq3I 00:05:22](https://www.youtube.com/watch?v=zZEy10fpq3I&t=322s) | 1 |
| 28 | [no title; author only: Enzo Golino] | Enzo Golino | it | low | studio | [zZEy10fpq3I 00:05:27](https://www.youtube.com/watch?v=zZEy10fpq3I&t=327s) | 1 |
| 29 | [no title; author only: Mario Baudino] | Mario Baudino | it | low | studio | [zZEy10fpq3I 00:05:27](https://www.youtube.com/watch?v=zZEy10fpq3I&t=327s) | 1 |
| 30 | [no title; author only: Auro Rosa (?)] | Auro Rosa (?) | it | low | studio | [zZEy10fpq3I 00:05:27](https://www.youtube.com/watch?v=zZEy10fpq3I&t=327s) | 1 |
| 31 | [no title; author only: Gaffarel] | Gaffarel | fr | medium | antichi | [zZEy10fpq3I 00:06:03](https://www.youtube.com/watch?v=zZEy10fpq3I&t=363s) | 1 |
| 32 | [no title; author only: Michael Maier (uncertain)] | Michael Maier (uncertain) | la | low | antichi | [zZEy10fpq3I 00:06:07](https://www.youtube.com/watch?v=zZEy10fpq3I&t=367s) | 1 |
| 33 | [no title; author only: Stella Rizzo] | Stella Rizzo | it | low | studio | [zZEy10fpq3I 00:06:52](https://www.youtube.com/watch?v=zZEy10fpq3I&t=412s) | 4 |
| 34 | [no title; author only: Ser[r]agli[o] di G[...]] | Ser[r]agli[o] di G[...] | it | low | bologna | [zZEy10fpq3I 00:07:08](https://www.youtube.com/watch?v=zZEy10fpq3I&t=428s) | 2 |
| 35 | [no title; author only: G.[D.] Chio[tti]] | G.[D.] Chio[tti] | la | low | bologna | [zZEy10fpq3I 00:07:08](https://www.youtube.com/watch?v=zZEy10fpq3I&t=428s) | 1 |
| 36 | [no title; author only: M. Gatti (?)] | M. Gatti (?) | it | low | bologna | [zZEy10fpq3I 00:07:08](https://www.youtube.com/watch?v=zZEy10fpq3I&t=428s) | 1 |
| 37 | [no title; author only: Philostrate (Philostratus)] | Philostrate (Philostratus) | fr | low | antichi | [zZEy10fpq3I 00:07:21](https://www.youtube.com/watch?v=zZEy10fpq3I&t=441s) | 1 |
| 38 | [no title; author only: Ric[?]] | Ric[?] |  | low | unknown | [zZEy10fpq3I 00:08:09](https://www.youtube.com/watch?v=zZEy10fpq3I&t=489s) | 1 |
| 39 | [no title; author only: Richardus a Sancto Victore] | Richardus a Sancto Victore | la | high | unknown | [zZEy10fpq3I 00:08:09](https://www.youtube.com/watch?v=zZEy10fpq3I&t=489s) | 3 |
| 40 | [no title; author only: Ουμπέρτο Έκο] | Ουμπέρτο Έκο | el | medium | studio | [zZEy10fpq3I 00:09:33](https://www.youtube.com/watch?v=zZEy10fpq3I&t=573s) | 1 |
| 41 | [no title; author only: Gérard de Nerval] | Gérard de Nerval | it | low | studio | [zZEy10fpq3I 00:12:48](https://www.youtube.com/watch?v=zZEy10fpq3I&t=768s) | 1 |
| 42 | [no title; author only: Bursill-Hall] | Bursill-Hall | en | medium | studio | [zZEy10fpq3I 00:13:08](https://www.youtube.com/watch?v=zZEy10fpq3I&t=788s) | 1 |
| 43 | [no title; author only: Basil Gray] | Basil Gray | en | medium | studio | [zZEy10fpq3I 00:13:21](https://www.youtube.com/watch?v=zZEy10fpq3I&t=801s) | 2 |
| 44 | [no title; author only: C. Huijberts] | C. Huijberts | la | low | studio | [zZEy10fpq3I 00:15:56](https://www.youtube.com/watch?v=zZEy10fpq3I&t=956s) | 1 |
| 45 | [no title; author only: [Stevenson?]] | [Stevenson?] | it | low | studio | [zZEy10fpq3I 00:18:23](https://www.youtube.com/watch?v=zZEy10fpq3I&t=1103s) | 1 |
| 46 | [no title; author only: Chrysostomus Mathanasius (fictional 'Doctor')] | Chrysostomus Mathanasius (fictional 'Doctor') | la | low | unknown | [zZEy10fpq3I 00:27:48](https://www.youtube.com/watch?v=zZEy10fpq3I&t=1668s) | 1 |
| 47 | [no title; author only: John Locke] | John Locke | it | low | studio | [zZEy10fpq3I 00:35:20](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2120s) | 1 |
| 48 | [no title; author only: Jean-François Champollion (about)] | Jean-François Champollion (about) | it | medium | studio | [zZEy10fpq3I 00:35:20](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2120s) | 3 |
| 49 | [no title; author only: Giambattista Vico] | Giambattista Vico | it | medium | studio | [zZEy10fpq3I 00:35:23](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2123s) | 1 |
| 50 | [no title; author only: George Santayana] | George Santayana | it | medium | studio | [zZEy10fpq3I 00:35:23](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2123s) | 1 |
| 51 | [no title; author only: Cletto Arrighi] | Cletto Arrighi | it | low | antichi | [zZEy10fpq3I 00:40:31](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2431s) | 1 |
| 52 | [no title; author only: Gianni Vattimo] | Gianni Vattimo | it | high | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 4 |
| 53 | [no title; author only: I. Pezzini; B. Finocchi (a cura di)] | I. Pezzini; B. Finocchi (a cura di) | it | low | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 4 |
| 54 | [no title; author only: Gillo Dorfles] | Gillo Dorfles | it | high | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 4 |
| 55 | [no title; author only: Anna Ottani Cavina] | Anna Ottani Cavina | it | medium | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 3 |
| 56 | [no title; author only: Luigi Spagnol] | Luigi Spagnol | it | low | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 3 |
| 57 | [no title; author only: Samuel Beckett] | Samuel Beckett | it | medium | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 3 |
| 58 | [no title; author only: Diego Fusaro] | Diego Fusaro | it | medium | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 3 |
| 59 | [no title; author only: Roberto Calasso] | Roberto Calasso | it | low | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 1 |
| 60 | [no title; author only: Beniamino Placido] | Beniamino Placido | it | low | studio | [zZEy10fpq3I 00:42:59](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2579s) | 1 |
| 61 | [no title; author only: Lia Levi] | Lia Levi | it | low | studio | [zZEy10fpq3I 00:43:03](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2583s) | 2 |
| 62 | [no title; author only: Roberto Campari] | Roberto Campari | it | low | studio | [zZEy10fpq3I 00:43:03](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2583s) | 2 |
| 63 | [no title; author only: Giovanna Cosenza] | Giovanna Cosenza | it | low | studio | [zZEy10fpq3I 00:43:03](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2583s) | 1 |
| 64 | [no title; author only: Ivano Dionigi] | Ivano Dionigi | it | medium | salotto | [zZEy10fpq3I 00:43:03](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2583s) | 2 |
| 65 | [no title; author only: Giuseppe Tornatore] | Giuseppe Tornatore | it | medium | salotto | [zZEy10fpq3I 00:43:03](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2583s) | 1 |
| 66 | [no title; author only: Jean de la Hire] | Jean de la Hire | fr | medium | corridoio | [zZEy10fpq3I 00:43:18](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2598s) | 4 |
| 67 | [no title; author only: A. Dumas] | A. Dumas | fr | medium | corridoio | [zZEy10fpq3I 00:43:23](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2603s) | 4 |
| 68 | [no title; author only: Carducci] | Carducci | it | medium | corridoio | [zZEy10fpq3I 00:43:27](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2607s) | 3 |
| 69 | [no title; author only: Emilio Salgari (per shelf tag)] | Emilio Salgari (per shelf tag) | it | low | corridoio | [zZEy10fpq3I 00:43:48](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2628s) | 1 |
| 70 | [no title; author only: Bacon] | Bacon | en | low | unknown | [zZEy10fpq3I 01:00:14](https://www.youtube.com/watch?v=zZEy10fpq3I&t=3614s) | 1 |
| 71 | [no title; author only: Stendhal] | Stendhal | it | high | studio | [fondazione_25_R](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/25_R.webp) | 1 |
| 72 | [no title; author only: Hölderlin] | Hölderlin | it | medium | studio | [fondazione_08_A-da_1_a_6](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/08_A-da%201%20a%206.webp) | 1 |
| 73 | [no title; author only: Alessandro di Afrodisia] | Alessandro di Afrodisia | it | high | studio | [fondazione_17_I](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/17_I.webp) | 1 |
| 74 | [no title; author only: Epitteto] | Epitteto | it | high | studio | [fondazione_17_I](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/17_I.webp) | 1 |
| 75 | [no title; author only: Jan Patočka] | Jan Patočka | it | medium | studio | [fondazione_18_M-A](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/18_M-A.webp) | 1 |
| 76 | [no title; author only: John Henry Newman] | John Henry Newman | it | high | studio | [fondazione_18_M-A](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/18_M-A.webp) | 1 |
| 77 | [no title; author only: Edmond Jabès] | Edmond Jabès | it | high | studio | [fondazione_25_R](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/25_R.webp) | 1 |
| 78 | [no title; author only: Lev Šestov] | Lev Šestov | it | high | studio | [fondazione_25_R](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/25_R.webp) | 1 |
| 79 | [no title; author only: Eunapio (Eunapius)] | Eunapio (Eunapius) | it | high | studio | [fondazione_25_R](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/25_R.webp) | 1 |
| 80 | [no title; author only: William Shakespeare] | William Shakespeare |  | medium | antichi | [fondazione_04_Libreria_Antichi_DX](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall_antichi/04_Libreria%20Antichi%20DX.webp) | 1 |
| 81 | [no title; author only: Filippo Bonanni] | Filippo Bonanni |  | low | antichi | [fondazione_13_772-19](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall_antichi/13_772-19.webp) | 1 |
| 82 | Inventing an Enemy | Umberto Eco | en | high | salotto | [B-M8V0PcCrw 00:00:25](https://www.youtube.com/watch?v=B-M8V0PcCrw&t=25s) | 1 |
| 83 | Italia Vostra |  | it | high | salotto | [B-M8V0PcCrw 00:04:47](https://www.youtube.com/watch?v=B-M8V0PcCrw&t=287s) | 1 |
| 84 | Opera omnia | Raymundus Lullus (Ramon Llull) | la | high | antichi | [iRXEQVTI95k 00:00:22](https://www.youtube.com/watch?v=iRXEQVTI95k&t=22s) | 2 |
| 85 | Ars Magna Lucis et Umbrae | Athanasius Kircher | la | high | studio | [iRXEQVTI95k 00:00:23](https://www.youtube.com/watch?v=iRXEQVTI95k&t=23s) | 25 |
| 86 | Ars magna | Raymundus Lullus (Ramon Llull) | la | high | antichi | [iRXEQVTI95k 00:00:25](https://www.youtube.com/watch?v=iRXEQVTI95k&t=25s) | 1 |
| 87 | I misteri di Torino |  | it | high | antichi | [iRXEQVTI95k 00:00:51](https://www.youtube.com/watch?v=iRXEQVTI95k&t=51s) | 2 |
| 88 | Le Service de la Beauté | [?.] Magé | fr | low | unknown | [iRXEQVTI95k 00:00:51](https://www.youtube.com/watch?v=iRXEQVTI95k&t=51s) | 1 |
| 89 | Mandrake |  | it | high | antichi | [iRXEQVTI95k 00:00:56](https://www.youtube.com/watch?v=iRXEQVTI95k&t=56s) | 2 |
| 90 | Vetera Analecta | Jean Mabillon | la | high | antichi | [iRXEQVTI95k 00:01:07](https://www.youtube.com/watch?v=iRXEQVTI95k&t=67s) | 1 |
| 91 | Vetera Analecta, sive Collectio veterum aliquot operum & opusculorum omnis generis, carminum, epistolarum, diplomatum, epitaphiorum, &c. Cum itinere Germanico ... Nova editio | Joannes Mabillon (Jean Mabillon) | la | medium | antichi | [iRXEQVTI95k 00:01:07](https://www.youtube.com/watch?v=iRXEQVTI95k&t=67s) | 5 |
| 92 | De mysteriis Aegyptiorum | Iamblichus | la | high | antichi | [iRXEQVTI95k 00:01:10](https://www.youtube.com/watch?v=iRXEQVTI95k&t=70s) | 1 |
| 93 | Argumentum in librum Mercurii Trismegisti (preface) | Marsilio Ficino | la | medium | antichi | [iRXEQVTI95k 00:01:10](https://www.youtube.com/watch?v=iRXEQVTI95k&t=70s) | 2 |
| 94 | Iamblichus De mysteriis Aegyptiorum, Chaldaeorum, Assyriorum | Iamblichus | la | medium | antichi | [iRXEQVTI95k 00:01:10](https://www.youtube.com/watch?v=iRXEQVTI95k&t=70s) | 1 |
| 95 | Atalanta fugiens | Michael Maier | la | high | antichi | [iRXEQVTI95k 00:01:12](https://www.youtube.com/watch?v=iRXEQVTI95k&t=72s) | 2 |
| 96 | Atalanta fugiens, hoc est Emblemata nova de secretis naturae chymica | Michael Maier | la | low | antichi | [iRXEQVTI95k 00:01:12](https://www.youtube.com/watch?v=iRXEQVTI95k&t=72s) | 1 |
| 97 | An Essay Towards a Real Character and a Philosophical Language | John Wilkins | en | high | antichi | [iRXEQVTI95k 00:01:17](https://www.youtube.com/watch?v=iRXEQVTI95k&t=77s) | 2 |
| 98 | Topolino giornalista |  | it | high | antichi | [iRXEQVTI95k 00:01:29](https://www.youtube.com/watch?v=iRXEQVTI95k&t=89s) | 1 |
| 99 | Corriere dei Piccoli |  | it | high | antichi | [iRXEQVTI95k 00:01:29](https://www.youtube.com/watch?v=iRXEQVTI95k&t=89s) | 2 |
| 100 | L'ultimo Ras |  | it | medium | antichi | [iRXEQVTI95k 00:01:29](https://www.youtube.com/watch?v=iRXEQVTI95k&t=89s) | 1 |
| 101 | Il Conte di Montecristo | Alexandre Dumas | it | high | antichi | [iRXEQVTI95k 00:01:33](https://www.youtube.com/watch?v=iRXEQVTI95k&t=93s) | 6 |
| 102 | Ockham's Theory of Terms | William of Ockham | en | high | bologna | [NtPk4irDiM8 00:00:47](https://www.youtube.com/watch?v=NtPk4irDiM8&t=47s) | 5 |
| 103 | Ockham's Theory of Propositions | William of Ockham | en | high | bologna | [NtPk4irDiM8 00:00:47](https://www.youtube.com/watch?v=NtPk4irDiM8&t=47s) | 5 |
| 104 | Les Querelles doctrinales à Paris | Zenon Kałuża | fr | medium | bologna | [NtPk4irDiM8 00:00:47](https://www.youtube.com/watch?v=NtPk4irDiM8&t=47s) | 2 |
| 105 | Scritti sul pensiero medievale | Umberto Eco | it | high | bologna | [NtPk4irDiM8 00:00:47](https://www.youtube.com/watch?v=NtPk4irDiM8&t=47s) | 8 |
| 106 | L'ente e l'essenza | Tommaso d'Aquino | it | high | bologna | [NtPk4irDiM8 00:00:47](https://www.youtube.com/watch?v=NtPk4irDiM8&t=47s) | 8 |
| 107 | …oni sulla prospettiva medievale | G. Federici Vescovini | it | low | studio | [NtPk4irDiM8 00:00:47](https://www.youtube.com/watch?v=NtPk4irDiM8&t=47s) | 2 |
| 108 | Dialogo sul papa eretico | Guglielmo di Ockham | it | high | bologna | [NtPk4irDiM8 00:00:51](https://www.youtube.com/watch?v=NtPk4irDiM8&t=51s) | 7 |
| 109 | Cronica dels temps de Jaume I |  | ca | medium | bologna | [NtPk4irDiM8 00:00:55](https://www.youtube.com/watch?v=NtPk4irDiM8&t=55s) | 1 |
| 110 | Bernini | Christian Tümpel | it | high | bologna | [NtPk4irDiM8 00:01:06](https://www.youtube.com/watch?v=NtPk4irDiM8&t=66s) | 4 |
| 111 | Da Hitler a Casablanca via Hollywood | Francesco Carbone | it | medium | studio | [zZEy10fpq3I 00:05:27](https://www.youtube.com/watch?v=zZEy10fpq3I&t=327s) | 1 |
| 112 | Le Nom de la Rose | Umberto Eco | fr | high | bologna | [NtPk4irDiM8 00:02:22](https://www.youtube.com/watch?v=NtPk4irDiM8&t=142s) | 6 |
| 113 | De Naam van de Roos | Umberto Eco | nl | high | bologna | [NtPk4irDiM8 00:02:22](https://www.youtube.com/watch?v=NtPk4irDiM8&t=142s) | 4 |
| 114 | Der Name der Rose | Umberto Eco | de | medium | bologna | [NtPk4irDiM8 00:02:22](https://www.youtube.com/watch?v=NtPk4irDiM8&t=142s) | 1 |
| 115 | Das Foucaultsche Pendel | Umberto Eco | de | high | bologna | [NtPk4irDiM8 00:02:25](https://www.youtube.com/watch?v=NtPk4irDiM8&t=145s) | 1 |
| 116 | Il nome della rosa | Umberto Eco | pl | high | salotto | [NtPk4irDiM8 00:02:25](https://www.youtube.com/watch?v=NtPk4irDiM8&t=145s) | 13 |
| 117 | Studi sulla prospettiva medievale |  | it | low | bologna | [KZfOaug0mM4 00:00:27](https://www.youtube.com/watch?v=KZfOaug0mM4&t=27s) | 1 |
| 118 | La Bibbia |  | it | medium | studio | [KZfOaug0mM4 00:00:33](https://www.youtube.com/watch?v=KZfOaug0mM4&t=33s) | 3 |
| 119 | L'Antico Testamento |  | it | medium | studio | [KZfOaug0mM4 00:00:33](https://www.youtube.com/watch?v=KZfOaug0mM4&t=33s) | 3 |
| 120 | Progetto umano |  | it | low | studio | [KZfOaug0mM4 00:00:35](https://www.youtube.com/watch?v=KZfOaug0mM4&t=35s) | 1 |
| 121 | Stati Uniti d'Europa | Enrico Letta | it | low | studio | [KZfOaug0mM4 00:00:57](https://www.youtube.com/watch?v=KZfOaug0mM4&t=57s) | 1 |
| 122 | Raffaello - I disegni |  | it | high | bologna | [KZfOaug0mM4 00:01:11](https://www.youtube.com/watch?v=KZfOaug0mM4&t=71s) | 1 |
| 123 | Europa 1492 |  | it | medium | bologna | [KZfOaug0mM4 00:01:11](https://www.youtube.com/watch?v=KZfOaug0mM4&t=71s) | 1 |
| 124 | Roma antica |  | it | medium | bologna | [KZfOaug0mM4 00:01:11](https://www.youtube.com/watch?v=KZfOaug0mM4&t=71s) | 2 |
| 125 | Medieval Beasts | Ann Payne | en | high | bologna | [KZfOaug0mM4 00:01:11](https://www.youtube.com/watch?v=KZfOaug0mM4&t=71s) | 2 |
| 126 | Treasures of Islam |  | en | medium | bologna | [KZfOaug0mM4 00:01:11](https://www.youtube.com/watch?v=KZfOaug0mM4&t=71s) | 1 |
| 127 | Castel del Monte |  | it | medium | bologna | [KZfOaug0mM4 00:01:11](https://www.youtube.com/watch?v=KZfOaug0mM4&t=71s) | 2 |
| 128 | Bellini |  | it | high | bologna | [KZfOaug0mM4 00:01:11](https://www.youtube.com/watch?v=KZfOaug0mM4&t=71s) | 2 |
| 129 | Leonardo da Vinci |  | it | medium | bologna | [KZfOaug0mM4 00:01:11](https://www.youtube.com/watch?v=KZfOaug0mM4&t=71s) | 1 |
| 130 | Giulio Romano |  | it | high | bologna | [KZfOaug0mM4 00:01:11](https://www.youtube.com/watch?v=KZfOaug0mM4&t=71s) | 2 |
| 131 | Rinascimento |  | it | medium | bologna | [KZfOaug0mM4 00:01:11](https://www.youtube.com/watch?v=KZfOaug0mM4&t=71s) | 2 |
| 132 | El Bodegón español |  | es | medium | bologna | [KZfOaug0mM4 00:01:11](https://www.youtube.com/watch?v=KZfOaug0mM4&t=71s) | 2 |
| 133 | Il genio di Roma 1592-1623 |  | it | high | bologna | [KZfOaug0mM4 00:01:11](https://www.youtube.com/watch?v=KZfOaug0mM4&t=71s) | 2 |
| 134 | Il grande Borromeo tra storia e fede |  | it | high | bologna | [KZfOaug0mM4 00:01:11](https://www.youtube.com/watch?v=KZfOaug0mM4&t=71s) | 1 |
| 135 | Palazzo Altieri |  | it | high | studio | [KZfOaug0mM4 00:01:11](https://www.youtube.com/watch?v=KZfOaug0mM4&t=71s) | 6 |
| 136 | La Gioconda che... |  | it | medium | studio | [KZfOaug0mM4 00:01:11](https://www.youtube.com/watch?v=KZfOaug0mM4&t=71s) | 6 |
| 137 | Rivedendo Correggio: l'Assunzione del Duomo di Parma |  | it | high | studio | [KZfOaug0mM4 00:01:11](https://www.youtube.com/watch?v=KZfOaug0mM4&t=71s) | 6 |
| 138 | Scottish Art | Duncan Macmillan | en | high | bologna | [KZfOaug0mM4 00:01:11](https://www.youtube.com/watch?v=KZfOaug0mM4&t=71s) | 2 |
| 139 | Giorgione |  | it | high | studio | [KZfOaug0mM4 00:01:11](https://www.youtube.com/watch?v=KZfOaug0mM4&t=71s) | 4 |
| 140 | Rolo Banca 1473: la civiltà... |  | it | medium | bologna | [KZfOaug0mM4 00:01:11](https://www.youtube.com/watch?v=KZfOaug0mM4&t=71s) | 1 |
| 141 | Museo de Bellas Artes de Bilbao |  | es | high | studio | [KZfOaug0mM4 00:01:11](https://www.youtube.com/watch?v=KZfOaug0mM4&t=71s) | 3 |
| 142 | Splendeurs d'Espagne I |  | fr | high | bologna | [KZfOaug0mM4 00:01:11](https://www.youtube.com/watch?v=KZfOaug0mM4&t=71s) | 1 |
| 143 | Splendeurs d'Espagne II |  | fr | high | studio | [KZfOaug0mM4 00:01:11](https://www.youtube.com/watch?v=KZfOaug0mM4&t=71s) | 13 |
| 144 | Historia del arte colonial Hispanoamericano |  | es | high | bologna | [KZfOaug0mM4 00:01:11](https://www.youtube.com/watch?v=KZfOaug0mM4&t=71s) | 2 |
| 145 | La Rocca Pisana di Vicenza [di Scamozzi] | Barduz[zi] | it | low | studio | [KZfOaug0mM4 00:01:11](https://www.youtube.com/watch?v=KZfOaug0mM4&t=71s) | 1 |
| 146 | Plinio |  | it | low | studio | [KZfOaug0mM4 00:01:11](https://www.youtube.com/watch?v=KZfOaug0mM4&t=71s) | 1 |
| 147 | Leonardo & [Vinci] |  | it | low | studio | [KZfOaug0mM4 00:01:11](https://www.youtube.com/watch?v=KZfOaug0mM4&t=71s) | 1 |
| 148 | Leonardo di Vinci |  | fr | medium | studio | [KZfOaug0mM4 00:01:11](https://www.youtube.com/watch?v=KZfOaug0mM4&t=71s) | 5 |
| 149 | [Tre]asures of Islam |  | en | low | studio | [KZfOaug0mM4 00:01:11](https://www.youtube.com/watch?v=KZfOaug0mM4&t=71s) | 1 |
| 150 | Illuminating the Renaissance |  | en | medium | studio | [KZfOaug0mM4 00:01:11](https://www.youtube.com/watch?v=KZfOaug0mM4&t=71s) | 5 |
| 151 | Guido Cagnacci |  | it | high | bologna | [KZfOaug0mM4 00:01:13](https://www.youtube.com/watch?v=KZfOaug0mM4&t=73s) | 2 |
| 152 | Cosmos |  | it | medium | bologna | [KZfOaug0mM4 00:01:13](https://www.youtube.com/watch?v=KZfOaug0mM4&t=73s) | 2 |
| 153 | La collezione di Franco Maria Ricci |  | it | high | bologna | [KZfOaug0mM4 00:01:13](https://www.youtube.com/watch?v=KZfOaug0mM4&t=73s) | 2 |
| 154 | Époques de la fleur |  | fr | low | studio | [KZfOaug0mM4 00:01:13](https://www.youtube.com/watch?v=KZfOaug0mM4&t=73s) | 1 |
| 155 | Il grande Borromeo: una storia e una fede |  | it | low | studio | [KZfOaug0mM4 00:01:13](https://www.youtube.com/watch?v=KZfOaug0mM4&t=73s) | 1 |
| 156 | La nostra terra |  | it | low | studio | [KZfOaug0mM4 00:01:13](https://www.youtube.com/watch?v=KZfOaug0mM4&t=73s) | 1 |
| 157 | Giovanni [Fede Cervicato?] |  | it | low | studio | [KZfOaug0mM4 00:01:13](https://www.youtube.com/watch?v=KZfOaug0mM4&t=73s) | 1 |
| 158 | Caravaggio and His Italian Followers |  | en | medium | studio | [KZfOaug0mM4 00:01:13](https://www.youtube.com/watch?v=KZfOaug0mM4&t=73s) | 1 |
| 159 | Il Cerano |  | it | medium | studio | [KZfOaug0mM4 00:01:13](https://www.youtube.com/watch?v=KZfOaug0mM4&t=73s) | 1 |
| 160 | I disegni del Codice Rosso di Palermo |  | it | medium | studio | [KZfOaug0mM4 00:01:13](https://www.youtube.com/watch?v=KZfOaug0mM4&t=73s) | 1 |
| 161 | decodeunicode |  | en | medium | studio | [KZfOaug0mM4 00:01:13](https://www.youtube.com/watch?v=KZfOaug0mM4&t=73s) | 2 |
| 162 | I disegni del Codice Resta di Palermo |  | it | high | bologna | [KZfOaug0mM4 00:01:15](https://www.youtube.com/watch?v=KZfOaug0mM4&t=75s) | 1 |
| 163 | Georges de La Tour |  | fr | high | studio | [KZfOaug0mM4 00:01:15](https://www.youtube.com/watch?v=KZfOaug0mM4&t=75s) | 3 |
| 164 | Committenti d'età barocca | Maria Beatrice Failla, Clara Goria | it | high | studio | [KZfOaug0mM4 00:01:15](https://www.youtube.com/watch?v=KZfOaug0mM4&t=75s) | 3 |
| 165 | Alessandro Magnasco 1667-1749 |  | it | high | studio | [KZfOaug0mM4 00:01:15](https://www.youtube.com/watch?v=KZfOaug0mM4&t=75s) | 3 |
| 166 | Venezia dei grandi viaggiatori |  | it | high | studio | [KZfOaug0mM4 00:01:15](https://www.youtube.com/watch?v=KZfOaug0mM4&t=75s) | 3 |
| 167 | France Baroque |  | fr | high | studio | [KZfOaug0mM4 00:01:15](https://www.youtube.com/watch?v=KZfOaug0mM4&t=75s) | 3 |
| 168 | Goya |  | it | high | studio | [KZfOaug0mM4 00:01:15](https://www.youtube.com/watch?v=KZfOaug0mM4&t=75s) | 3 |
| 169 | Antonie van Dyck 1599-1641 |  | en | high | studio | [KZfOaug0mM4 00:01:15](https://www.youtube.com/watch?v=KZfOaug0mM4&t=75s) | 4 |
| 170 | Rembrandt | Christian Tumpel | it | high | studio | [KZfOaug0mM4 00:01:15](https://www.youtube.com/watch?v=KZfOaug0mM4&t=75s) | 4 |
| 171 | Barocco |  | it | high | bologna | [KZfOaug0mM4 00:01:15](https://www.youtube.com/watch?v=KZfOaug0mM4&t=75s) | 2 |
| 172 | Van Dyck |  | it | medium | bologna | [KZfOaug0mM4 00:01:15](https://www.youtube.com/watch?v=KZfOaug0mM4&t=75s) | 1 |
| 173 | Felice Giani |  | it | high | studio | [KZfOaug0mM4 00:01:15](https://www.youtube.com/watch?v=KZfOaug0mM4&t=75s) | 6 |
| 174 | I colori del tempo 2 |  | it | medium | bologna | [KZfOaug0mM4 00:01:15](https://www.youtube.com/watch?v=KZfOaug0mM4&t=75s) | 1 |
| 175 | Arte Indiana |  | it | medium | bologna | [KZfOaug0mM4 00:01:15](https://www.youtube.com/watch?v=KZfOaug0mM4&t=75s) | 2 |
| 176 | Il museo di Pechino |  | it | medium | studio | [KZfOaug0mM4 00:01:15](https://www.youtube.com/watch?v=KZfOaug0mM4&t=75s) | 3 |
| 177 | Giacomo Ceruti |  | it | low | studio | [KZfOaug0mM4 00:01:15](https://www.youtube.com/watch?v=KZfOaug0mM4&t=75s) | 2 |
| 178 | The Idea of Art as Propaganda in France, 1750-1799 | James Leith | en | medium | studio | [KZfOaug0mM4 00:01:15](https://www.youtube.com/watch?v=KZfOaug0mM4&t=75s) | 2 |
| 179 | Das alte Dresden | Fritz Laffer[?] | de | low | studio | [KZfOaug0mM4 00:01:15](https://www.youtube.com/watch?v=KZfOaug0mM4&t=75s) | 1 |
| 180 | Beniamino Simoni |  | it | low | studio | [KZfOaug0mM4 00:01:15](https://www.youtube.com/watch?v=KZfOaug0mM4&t=75s) | 2 |
| 181 | Aufstieg und Niedergang der römischen Welt, II.12.2 |  | de | high | unknown | [KZfOaug0mM4 00:01:15](https://www.youtube.com/watch?v=KZfOaug0mM4&t=75s) | 5 |
| 182 | Toulouse-Lautrec |  | fr | low | studio | [KZfOaug0mM4 00:01:15](https://www.youtube.com/watch?v=KZfOaug0mM4&t=75s) | 1 |
| 183 | Aufstieg und Niedergang der römischen Welt, II.12.1 |  | de | high | studio | [KZfOaug0mM4 00:01:15](https://www.youtube.com/watch?v=KZfOaug0mM4&t=75s) | 10 |
| 184 | Paradiso perduto | Milton | it | high | bologna | [KZfOaug0mM4 00:01:19](https://www.youtube.com/watch?v=KZfOaug0mM4&t=79s) | 1 |
| 185 | Here Comes Everybody | Anthony Burgess | en | high | corridoio | [KZfOaug0mM4 00:01:41](https://www.youtube.com/watch?v=KZfOaug0mM4&t=101s) | 2 |
| 186 | Vico & Joyce | Donald Phillip Verene | en | high | corridoio | [KZfOaug0mM4 00:01:41](https://www.youtube.com/watch?v=KZfOaug0mM4&t=101s) | 3 |
| 187 | The Irish Comic Tradition | Vivian Mercier | en | medium | corridoio | [KZfOaug0mM4 00:01:41](https://www.youtube.com/watch?v=KZfOaug0mM4&t=101s) | 2 |
| 188 | The Widening Gyre | Frank Kermode | en | high | corridoio | [KZfOaug0mM4 00:01:41](https://www.youtube.com/watch?v=KZfOaug0mM4&t=101s) | 2 |
| 189 | James Joyce | Richard Ellmann | it | high | corridoio | [KZfOaug0mM4 00:01:41](https://www.youtube.com/watch?v=KZfOaug0mM4&t=101s) | 3 |
| 190 | Joyce | Ezra Pound | en | medium | bologna | [KZfOaug0mM4 00:01:43](https://www.youtube.com/watch?v=KZfOaug0mM4&t=103s) | 1 |
| 191 | Dante Alighieri's Inferno Metaphor... | Dante Alighieri | en | medium | bologna | [KZfOaug0mM4 00:01:51](https://www.youtube.com/watch?v=KZfOaug0mM4&t=111s) | 1 |
| 192 | Fiore / Detto d'Amore | Dante Alighieri (attrib.) | it | high | bologna | [KZfOaug0mM4 00:01:51](https://www.youtube.com/watch?v=KZfOaug0mM4&t=111s) | 1 |
| 193 | Il brigante |  | it | low | bologna | [KZfOaug0mM4 00:01:54](https://www.youtube.com/watch?v=KZfOaug0mM4&t=114s) | 2 |
| 194 | Poesie | Friedrich Hölderlin | de | medium | bologna | [KZfOaug0mM4 00:01:55](https://www.youtube.com/watch?v=KZfOaug0mM4&t=115s) | 2 |
| 195 | Saggio sull'intelletto umano | John Locke | it | high | studio | [FeIUY9EhZgI 00:00:39](https://www.youtube.com/watch?v=FeIUY9EhZgI&t=39s) | 16 |
| 196 | Trattato della natura umana | David Hume | it | high | studio | [FeIUY9EhZgI 00:00:39](https://www.youtube.com/watch?v=FeIUY9EhZgI&t=39s) | 14 |
| 197 | Alcifrone ossia il filosofo minuzioso | George Berkeley | it | high | studio | [FeIUY9EhZgI 00:00:39](https://www.youtube.com/watch?v=FeIUY9EhZgI&t=39s) | 6 |
| 198 | Critica della ragion pratica | Immanuel Kant | it | high | studio | [FeIUY9EhZgI 00:00:39](https://www.youtube.com/watch?v=FeIUY9EhZgI&t=39s) | 19 |
| 199 | Tutte le opere (1721-1754) | Montesquieu | it | high | studio | [FeIUY9EhZgI 00:00:39](https://www.youtube.com/watch?v=FeIUY9EhZgI&t=39s) | 13 |
| 200 | Dizionario filosofico: tutte le voci del Dizionario filosofico e delle Domande sull'Enciclopedia | Voltaire | it | high | studio | [FeIUY9EhZgI 00:00:39](https://www.youtube.com/watch?v=FeIUY9EhZgI&t=39s) | 9 |
| 201 | La Scienza Nuova - Le tre edizioni del 1725, 1730 e 1744 | Giambattista Vico | it | high | studio | [FeIUY9EhZgI 00:00:39](https://www.youtube.com/watch?v=FeIUY9EhZgI&t=39s) | 12 |
| 202 | La tradizione signorile nella filosofia americana e altri saggi | George Santayana | it | high | studio | [FeIUY9EhZgI 00:00:39](https://www.youtube.com/watch?v=FeIUY9EhZgI&t=39s) | 10 |
| 203 | Alciphron, ovvero il filosofo minuto | George Berkeley | it | medium | studio | [FeIUY9EhZgI 00:00:39](https://www.youtube.com/watch?v=FeIUY9EhZgI&t=39s) | 2 |
| 204 | Critica della ragion pura | Immanuel Kant | it | high | studio | [FeIUY9EhZgI 00:00:39](https://www.youtube.com/watch?v=FeIUY9EhZgI&t=39s) | 3 |
| 205 | Dizionario filosofico | Voltaire | it | high | studio | [FeIUY9EhZgI 00:00:39](https://www.youtube.com/watch?v=FeIUY9EhZgI&t=39s) | 3 |
| 206 | Ars Magna Lucis et Umbrae, in decem libros digesta | Athanasius Kircher | la | high | studio | [FeIUY9EhZgI 00:00:41](https://www.youtube.com/watch?v=FeIUY9EhZgI&t=41s) | 10 |
| 207 | Mundus Subterraneus | Athanasius Kircher | la | high | studio | [FeIUY9EhZgI 00:00:51](https://www.youtube.com/watch?v=FeIUY9EhZgI&t=51s) | 15 |
| 208 | Obeliscus Pamphilius | Athanasius Kircher | la | medium | antichi | [FeIUY9EhZgI 00:00:51](https://www.youtube.com/watch?v=FeIUY9EhZgI&t=51s) | 3 |
| 209 | Turris Babel | Athanasius Kircher | la | high | studio | [FeIUY9EhZgI 00:00:51](https://www.youtube.com/watch?v=FeIUY9EhZgI&t=51s) | 27 |
| 210 | Ars Magna Sciendi | Athanasius Kircher | la | high | antichi | [FeIUY9EhZgI 00:00:51](https://www.youtube.com/watch?v=FeIUY9EhZgI&t=51s) | 7 |
| 211 | China Illustrata | Athanasius Kircher | la | high | unknown | [FeIUY9EhZgI 00:00:51](https://www.youtube.com/watch?v=FeIUY9EhZgI&t=51s) | 9 |
| 212 | Obeliscus [Pamphilius?] | Athanasius Kircher | la | medium | studio | [FeIUY9EhZgI 00:00:51](https://www.youtube.com/watch?v=FeIUY9EhZgI&t=51s) | 15 |
| 213 | Aufstieg und Niedergang der römischen Welt, II.11.1 |  | de | high | antichi | [FeIUY9EhZgI 00:00:57](https://www.youtube.com/watch?v=FeIUY9EhZgI&t=57s) | 59 |
| 214 | Aufstieg und Niedergang der römischen Welt, II.12.3 |  | de | high | unknown | [FeIUY9EhZgI 00:00:57](https://www.youtube.com/watch?v=FeIUY9EhZgI&t=57s) | 3 |
| 215 | Aufstieg und Niedergang der römischen Welt, II.13 |  | de | high | unknown | [FeIUY9EhZgI 00:00:57](https://www.youtube.com/watch?v=FeIUY9EhZgI&t=57s) | 3 |
| 216 | Aufstieg und Niedergang der römischen Welt, II.14 |  | de | high | unknown | [FeIUY9EhZgI 00:00:57](https://www.youtube.com/watch?v=FeIUY9EhZgI&t=57s) | 3 |
| 217 | Aufstieg und Niedergang der römischen Welt, II. Principat, Bd. 15 |  | de | high | unknown | [FeIUY9EhZgI 00:00:57](https://www.youtube.com/watch?v=FeIUY9EhZgI&t=57s) | 3 |
| 218 | Aufstieg und Niedergang der römischen Welt, II.7.1 |  | de | medium | unknown | [FeIUY9EhZgI 00:00:57](https://www.youtube.com/watch?v=FeIUY9EhZgI&t=57s) | 2 |
| 219 | Aufstieg und Niedergang der römischen Welt, II.7.2 |  | de | medium | unknown | [FeIUY9EhZgI 00:00:57](https://www.youtube.com/watch?v=FeIUY9EhZgI&t=57s) | 2 |
| 220 | Aufstieg und Niedergang der römischen Welt, II.9.1 |  | de | low | unknown | [FeIUY9EhZgI 00:00:57](https://www.youtube.com/watch?v=FeIUY9EhZgI&t=57s) | 2 |
| 221 | Aufstieg und Niedergang der römischen Welt, II.9.2 |  | de | medium | unknown | [FeIUY9EhZgI 00:00:57](https://www.youtube.com/watch?v=FeIUY9EhZgI&t=57s) | 2 |
| 222 | Dictionarium Scripturae Sacrae | Augustin Calmet | la | medium | unknown | [ygvl-_gtAP8 00:00:13](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=13s) | 12 |
| 223 | De Arcanis Catholicae Veritatis (or another work) | Richard of Saint Victor (Richardus a Sancto Victore) | la | medium | antichi | [ygvl-_gtAP8 00:00:17](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=17s) | 1 |
| 224 | De Arcanis Catholicae Veritatis | Petrus Galatinus (Pietro Colonna Galatino) | la | high | antichi | [ygvl-_gtAP8 00:00:37](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=37s) | 1 |
| 225 | Philosophia Moysaica | Robert Fludd | la | medium | antichi | [ygvl-_gtAP8 00:00:37](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=37s) | 10 |
| 226 | Opus Mago-Cabbalisticum et Theosophicum | Georg von Welling (pseud. Sallwigt) | la | high | antichi | [ygvl-_gtAP8 00:00:37](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=37s) | 6 |
| 227 | Anatomia Amphitheatrum | David [surname not legible] | la | low | antichi | [ygvl-_gtAP8 00:00:37](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=37s) | 1 |
| 228 | De Macrocosmi Historia (Utriusque Cosmi Historia) | Robert Fludd | la | high | antichi | [ygvl-_gtAP8 00:00:37](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=37s) | 12 |
| 229 | De Macrocosmi Historia | Roberto Fludd | la | high | antichi | [zZEy10fpq3I 00:06:07](https://www.youtube.com/watch?v=zZEy10fpq3I&t=367s) | 1 |
| 230 | Numerorum Mysteria | Pietro Bongo (Petrus Bungus) | la | medium | antichi | [ygvl-_gtAP8 00:00:37](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=37s) | 1 |
| 231 | Lexicon Alchemiae | Martin Ruland | la | low | antichi | [ygvl-_gtAP8 00:00:37](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=37s) | 1 |
| 232 | Tractatus | Robert Fludd | la | high | antichi | [ygvl-_gtAP8 00:00:37](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=37s) | 18 |
| 233 | Artis Cabalisticae (scriptores) | ed. Johann Pistorius | la | high | antichi | [ygvl-_gtAP8 00:00:37](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=37s) | 15 |
| 234 | Coelum Sephiroticum (Kabbala-related treatise) |  | la | low | antichi | [ygvl-_gtAP8 00:00:37](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=37s) | 1 |
| 235 | Arithmeticum (or similar) | Juan Caramuel y Lobkowitz | la | low | antichi | [ygvl-_gtAP8 00:00:37](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=37s) | 1 |
| 236 | Opus mago-caballisticum | Sallwigt | la | high | antichi | [ygvl-_gtAP8 00:00:38](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=38s) | 9 |
| 237 | Anatomiae Amphitheatrum | Robert Fludd | la | high | antichi | [ygvl-_gtAP8 00:00:38](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=38s) | 15 |
| 238 | Artis Cabalistic[ae] |  | la | low | antichi | [ygvl-_gtAP8 00:00:38](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=38s) | 2 |
| 239 | Празький цвинтар | У. Еко (Umberto Eco) | uk | high | studio | [zZEy10fpq3I 00:09:27](https://www.youtube.com/watch?v=zZEy10fpq3I&t=567s) | 1 |
| 240 | История уродства | Умберто Эко (ed.) | ru | high | studio | [zZEy10fpq3I 00:09:27](https://www.youtube.com/watch?v=zZEy10fpq3I&t=567s) | 1 |
| 241 | De begraafplaats van Praag | Umberto Eco | nl | high | studio | [ygvl-_gtAP8 00:01:31](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=91s) | 16 |
| 242 | Fukoovo klatno | Umberto Eko | sr | high | studio | [ygvl-_gtAP8 00:01:31](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=91s) | 17 |
| 243 | On Literature | Umberto Eco | en | high | studio | [ygvl-_gtAP8 00:01:31](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=91s) | 17 |
| 244 | Kant and the Platypus | Umberto Eco | en | high | studio | [ygvl-_gtAP8 00:01:31](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=91s) | 16 |
| 245 | Prahos kapinės | Umberto Eco | lt | high | studio | [ygvl-_gtAP8 00:01:31](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=91s) | 16 |
| 246 | Die Bücher und das Paradies | Umberto Eco | de | high | studio | [ygvl-_gtAP8 00:01:31](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=91s) | 14 |
| 247 | Foucault's Pendulum | Umberto Eco | en | high | studio | [ygvl-_gtAP8 00:01:31](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=91s) | 18 |
| 248 | The Mysterious Flame of Queen Loana | Umberto Eco | en | high | studio | [ygvl-_gtAP8 00:01:29](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=89s) | 22 |
| 249 | Cmentarz w Pradze | Umberto Eco | pl | high | studio | [ygvl-_gtAP8 00:01:31](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=91s) | 18 |
| 250 | Ortaçağ | Umberto Eco | tr | high | studio | [ygvl-_gtAP8 00:01:29](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=89s) | 8 |
| 251 | Пражское кладбище | Умберто Еко | ru | medium | studio | [zZEy10fpq3I 00:09:27](https://www.youtube.com/watch?v=zZEy10fpq3I&t=567s) | 2 |
| 252 | Der Friedhof in Prag | Eco | de | high | studio | [zZEy10fpq3I 00:09:27](https://www.youtube.com/watch?v=zZEy10fpq3I&t=567s) | 3 |
| 253 | Die Geschichte der Schönheit | Eco | de | high | studio | [zZEy10fpq3I 00:09:27](https://www.youtube.com/watch?v=zZEy10fpq3I&t=567s) | 2 |
| 254 | A Passo de Caranguejo | Umberto Eco | pt | high | studio | [zZEy10fpq3I 00:09:27](https://www.youtube.com/watch?v=zZEy10fpq3I&t=567s) | 2 |
| 255 | Баудолино | Umberto Eco | bg | high | studio | [ygvl-_gtAP8 00:01:29](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=89s) | 4 |
| 256 | O Cemitério de Praga | Umberto Eco | pt | high | studio | [ygvl-_gtAP8 00:01:29](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=89s) | 6 |
| 257 | Istoriya urodstva (История уродства) | Умберто Эко (ред.) | ru | high | studio | [ygvl-_gtAP8 00:01:29](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=89s) | 16 |
| 258 | A Theory of Semiotics | Umberto Eco | en | high | studio | [ygvl-_gtAP8 00:01:29](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=89s) | 5 |
| 259 | Il Pendolo di Foucault | Umberto Eco | it | high | unknown | [ygvl-_gtAP8 00:01:29](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=89s) | 6 |
| 260 | Тайнственное пламя царицы Лоаны | Umberto Eco | ru | medium | studio | [ygvl-_gtAP8 00:01:31](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=91s) | 1 |
| 261 | Istoriya yevropeiskoyi tsyvilizatsiyi: Rym (Історія європейської цивілізації: Рим) | Umberto Eko (editor) | uk | high | studio | [ygvl-_gtAP8 00:01:31](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=91s) | 17 |
| 262 | Самеliche Werke | Umberto Eco | de | low | studio | [ygvl-_gtAP8 00:01:35](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=95s) | 1 |
| 263 | Prazkyi tsvyntar (Празький цвинтар) | Умберто Еко | uk | high | studio | [ygvl-_gtAP8 00:01:35](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=95s) | 12 |
| 264 | Dronning Loanas mystiske flamme | Umberto Eco | da | high | studio | [ygvl-_gtAP8 00:01:35](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=95s) | 13 |
| 265 | La memoria vegetale e altri scritti di bibliofilia | Umberto Eco | it | medium | studio | [zZEy10fpq3I 00:44:53](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2693s) | 1 |
| 266 | Nero Wolfe (edition/collection title not fully legible) |  | it | low | studio | [M8IWTOFNlOc 00:01:11](https://www.youtube.com/watch?v=M8IWTOFNlOc&t=71s) | 6 |
| 267 | A paso de cangrejo | Umberto Eco | es | high | studio | [M8IWTOFNlOc 00:23:23](https://www.youtube.com/watch?v=M8IWTOFNlOc&t=1403s) | 2 |
| 268 | Il ritorno di Himmelfarb | Michael Kruger | it | high | studio | [M8IWTOFNlOc 00:23:29](https://www.youtube.com/watch?v=M8IWTOFNlOc&t=1409s) | 5 |
| 269 | Spettri [...] dell'amore |  | it | low | studio | [M8IWTOFNlOc 00:23:29](https://www.youtube.com/watch?v=M8IWTOFNlOc&t=1409s) | 2 |
| 270 | Razza e destino | Walter Benjamin | it | medium | studio | [M8IWTOFNlOc 00:23:29](https://www.youtube.com/watch?v=M8IWTOFNlOc&t=1409s) | 4 |
| 271 | Dando buca a Godot | Bartezzaghi | it | high | studio | [M8IWTOFNlOc 00:23:29](https://www.youtube.com/watch?v=M8IWTOFNlOc&t=1409s) | 5 |
| 272 | Le cose che ho imparato | Gianni Riotta | it | high | studio | [M8IWTOFNlOc 00:23:29](https://www.youtube.com/watch?v=M8IWTOFNlOc&t=1409s) | 5 |
| 273 | [Tra]dizione e rivoluzione | Franc[o Fortini] | it | low | studio | [M8IWTOFNlOc 00:23:29](https://www.youtube.com/watch?v=M8IWTOFNlOc&t=1409s) | 1 |
| 274 | Lavorando anche per il futuro | Mario Andreose | it | high | studio | [M8IWTOFNlOc 00:23:31](https://www.youtube.com/watch?v=M8IWTOFNlOc&t=1411s) | 4 |
| 275 | Quattro modi dell'amore |  | it | low | studio | [M8IWTOFNlOc 00:23:35](https://www.youtube.com/watch?v=M8IWTOFNlOc&t=1415s) | 1 |
| 276 | Aprendo le casse della mia biblioteca | Walter Benjamin | it | low | studio | [M8IWTOFNlOc 00:23:35](https://www.youtube.com/watch?v=M8IWTOFNlOc&t=1415s) | 1 |
| 277 | To Koimitirio tis Pragas (The Prague Cemetery, Greek edition) | Oumperto Eko [Umberto Eco] | el | medium | studio | [M8IWTOFNlOc 00:24:04](https://www.youtube.com/watch?v=M8IWTOFNlOc&t=1444s) | 1 |
| 278 | Apocalypse Postponed | Umberto Eco | en | high | studio | [M8IWTOFNlOc 00:24:04](https://www.youtube.com/watch?v=M8IWTOFNlOc&t=1444s) | 2 |
| 279 | The Island of the Day Before | Umberto Eco | en | high | studio | [M8IWTOFNlOc 00:24:05](https://www.youtube.com/watch?v=M8IWTOFNlOc&t=1445s) | 3 |
| 280 | Baudolino | Umberto Eco | it | high | studio | [M8IWTOFNlOc 00:24:05](https://www.youtube.com/watch?v=M8IWTOFNlOc&t=1445s) | 5 |
| 281 | To Koimeterio tes Pragas | Umberto Eco | el | high | studio | [M8IWTOFNlOc 00:24:05](https://www.youtube.com/watch?v=M8IWTOFNlOc&t=1445s) | 1 |
| 282 | The Prague Cemetery | Umberto Eco | en | high | studio | [M8IWTOFNlOc 00:24:05](https://www.youtube.com/watch?v=M8IWTOFNlOc&t=1445s) | 2 |
| 283 | Prague Cemetery (Russian/Ukrainian ed.) | Умберто Еко | ru | low | studio | [zZEy10fpq3I 00:09:27](https://www.youtube.com/watch?v=zZEy10fpq3I&t=567s) | 1 |
| 284 | Un Segno | Umberto Eco | it | medium | studio | [M8IWTOFNlOc 00:24:07](https://www.youtube.com/watch?v=M8IWTOFNlOc&t=1447s) | 1 |
| 285 | Ernst Blochs Wirkung |  | de | medium | studio | [M8IWTOFNlOc 00:24:15](https://www.youtube.com/watch?v=M8IWTOFNlOc&t=1455s) | 4 |
| 286 | Linus |  | it | medium | salotto | [zZEy10fpq3I 00:03:52](https://www.youtube.com/watch?v=zZEy10fpq3I&t=232s) | 1 |
| 287 | Ecolinus |  | it | medium | salotto | [zZEy10fpq3I 00:03:56](https://www.youtube.com/watch?v=zZEy10fpq3I&t=236s) | 1 |
| 288 | Chi muore si rivede |  | it | low | salotto | [zZEy10fpq3I 00:04:11](https://www.youtube.com/watch?v=zZEy10fpq3I&t=251s) | 1 |
| 289 | Le Robert |  | fr | high | studio | [zZEy10fpq3I 00:05:22](https://www.youtube.com/watch?v=zZEy10fpq3I&t=322s) | 5 |
| 290 | La sindrome del pallone | Marcello Carra | it | low | bologna | [zZEy10fpq3I 00:05:22](https://www.youtube.com/watch?v=zZEy10fpq3I&t=322s) | 1 |
| 291 | I miei scrittori e altri animali |  | it | low | bologna | [zZEy10fpq3I 00:05:22](https://www.youtube.com/watch?v=zZEy10fpq3I&t=322s) | 1 |
| 292 | Lanzarote | Michel Houellebecq | it | low | bologna | [zZEy10fpq3I 00:05:22](https://www.youtube.com/watch?v=zZEy10fpq3I&t=322s) | 1 |
| 293 | Imię róży | Umberto Eco | pl | medium | bologna | [zZEy10fpq3I 00:05:22](https://www.youtube.com/watch?v=zZEy10fpq3I&t=322s) | 1 |
| 294 | Cum se face o teză de licență | Umberto Eco | ro | medium | bologna | [zZEy10fpq3I 00:05:22](https://www.youtube.com/watch?v=zZEy10fpq3I&t=322s) | 1 |
| 295 | Le isole (Opera Omnia) | Giorgio de Chirico | it | medium | studio | [zZEy10fpq3I 00:05:23](https://www.youtube.com/watch?v=zZEy10fpq3I&t=323s) | 1 |
| 296 | [...]ca dei Miei Ragazzi |  | it | low | studio | [zZEy10fpq3I 00:05:27](https://www.youtube.com/watch?v=zZEy10fpq3I&t=327s) | 1 |
| 297 | Una passione [costante?] |  | it | low | studio | [zZEy10fpq3I 00:05:27](https://www.youtube.com/watch?v=zZEy10fpq3I&t=327s) | 1 |
| 298 | Trattato di Semiotica Generale | Umberto Eco | it | medium | unknown | [zZEy10fpq3I 01:02:22](https://www.youtube.com/watch?v=zZEy10fpq3I&t=3742s) | 1 |
| 299 | Tela Ignea Satanae, Tom. I | Johann Christoph Wagenseil | la | high | antichi | [zZEy10fpq3I 00:06:03](https://www.youtube.com/watch?v=zZEy10fpq3I&t=363s) | 3 |
| 300 | Behmen's Works |  | en | medium | antichi | [zZEy10fpq3I 00:06:03](https://www.youtube.com/watch?v=zZEy10fpq3I&t=363s) | 9 |
| 301 | De Sepulchro[?] Hebraeorum[?] |  | la | low | antichi | [zZEy10fpq3I 00:06:03](https://www.youtube.com/watch?v=zZEy10fpq3I&t=363s) | 2 |
| 302 | De Coelo et de Inferno |  | la | medium | antichi | [zZEy10fpq3I 00:06:03](https://www.youtube.com/watch?v=zZEy10fpq3I&t=363s) | 3 |
| 303 | Histoire des langues |  | fr | high | antichi | [zZEy10fpq3I 00:06:03](https://www.youtube.com/watch?v=zZEy10fpq3I&t=363s) | 2 |
| 304 | De Sepulchris Hebraeorum |  | la | medium | antichi | [zZEy10fpq3I 00:06:03](https://www.youtube.com/watch?v=zZEy10fpq3I&t=363s) | 1 |
| 305 | Utriusque Cosmi Historia (De Macrocosmi Historia) | Robert Fludd (Roberto Fludd) | la | medium | antichi | [zZEy10fpq3I 00:06:05](https://www.youtube.com/watch?v=zZEy10fpq3I&t=365s) | 4 |
| 306 | Lexicon Hermeticum[?] |  | la | low | antichi | [zZEy10fpq3I 00:06:05](https://www.youtube.com/watch?v=zZEy10fpq3I&t=365s) | 4 |
| 307 | Opus Mago-Cabbalisticum | Sallwigt | la | medium | antichi | [zZEy10fpq3I 00:06:07](https://www.youtube.com/watch?v=zZEy10fpq3I&t=367s) | 1 |
| 308 | Philosophia Nova |  | la | medium | antichi | [zZEy10fpq3I 00:06:09](https://www.youtube.com/watch?v=zZEy10fpq3I&t=369s) | 1 |
| 309 | Oedipus Aegyptiacus[?] | Athanasius Kircher (Kircheri) | la | low | antichi | [zZEy10fpq3I 00:06:13](https://www.youtube.com/watch?v=zZEy10fpq3I&t=373s) | 3 |
| 310 | Polygraphia nova | Athanasius Kircher (Kircherii) | la | low | antichi | [zZEy10fpq3I 00:06:13](https://www.youtube.com/watch?v=zZEy10fpq3I&t=373s) | 1 |
| 311 | Monumenti Italiani del '900 |  | it | low | studio | [zZEy10fpq3I 00:06:52](https://www.youtube.com/watch?v=zZEy10fpq3I&t=412s) | 4 |
| 312 | Il Revival |  | it | medium | studio | [zZEy10fpq3I 00:06:52](https://www.youtube.com/watch?v=zZEy10fpq3I&t=412s) | 4 |
| 313 | Modern Art Nouveau |  | en | low | studio | [zZEy10fpq3I 00:06:52](https://www.youtube.com/watch?v=zZEy10fpq3I&t=412s) | 4 |
| 314 | Vescovi e Chiesa d'Alessandria, Tomo II | G.A. Chiozzi | it | medium | bologna | [zZEy10fpq3I 00:07:04](https://www.youtube.com/watch?v=zZEy10fpq3I&t=424s) | 3 |
| 315 | Il libro rosso |  | it | medium | bologna | [zZEy10fpq3I 00:07:04](https://www.youtube.com/watch?v=zZEy10fpq3I&t=424s) | 3 |
| 316 | Il Giardino delle Camelie |  | it | medium | bologna | [zZEy10fpq3I 00:07:04](https://www.youtube.com/watch?v=zZEy10fpq3I&t=424s) | 4 |
| 317 | Dizionario Geografico Italiano, Vol. I |  | it | low | bologna | [zZEy10fpq3I 00:07:08](https://www.youtube.com/watch?v=zZEy10fpq3I&t=428s) | 2 |
| 318 | [Philostrati Opera] | Flavius Philostratus (?) | la | low | antichi | [zZEy10fpq3I 00:07:20](https://www.youtube.com/watch?v=zZEy10fpq3I&t=440s) | 1 |
| 319 | [Philostrate?] |  | fr | low | antichi | [zZEy10fpq3I 00:07:20](https://www.youtube.com/watch?v=zZEy10fpq3I&t=440s) | 2 |
| 320 | Storia di Alessandria |  | it | low | antichi | [zZEy10fpq3I 00:07:22](https://www.youtube.com/watch?v=zZEy10fpq3I&t=442s) | 5 |
| 321 | Physica Curiosa | Gaspar Schott (C. Schotti) | la | medium | antichi | [zZEy10fpq3I 00:07:22](https://www.youtube.com/watch?v=zZEy10fpq3I&t=442s) | 5 |
| 322 | Joco-Seriorum Naturae et Artis Diatribe | Athanasius Kircherus | la | medium | antichi | [zZEy10fpq3I 00:07:31](https://www.youtube.com/watch?v=zZEy10fpq3I&t=451s) | 5 |
| 323 | Aristotelis Opera | Aristoteles | la | high | antichi | [zZEy10fpq3I 00:07:45](https://www.youtube.com/watch?v=zZEy10fpq3I&t=465s) | 1 |
| 324 | Come si agisce | Balestrini | it | medium | studio | [zZEy10fpq3I 00:09:13](https://www.youtube.com/watch?v=zZEy10fpq3I&t=553s) | 1 |
| 325 | Begravningsplatsen i Prag | Umberto Eco | sv | high | studio | [zZEy10fpq3I 00:09:20](https://www.youtube.com/watch?v=zZEy10fpq3I&t=560s) | 12 |
| 326 | The Search for the Perfect Language | Umberto Eco | en | high | studio | [zZEy10fpq3I 00:09:20](https://www.youtube.com/watch?v=zZEy10fpq3I&t=560s) | 2 |
| 327 | The Templars |  | en | medium | studio | [zZEy10fpq3I 00:09:20](https://www.youtube.com/watch?v=zZEy10fpq3I&t=560s) | 1 |
| 328 | The Future of the Book |  | en | medium | studio | [zZEy10fpq3I 00:09:20](https://www.youtube.com/watch?v=zZEy10fpq3I&t=560s) | 1 |
| 329 | In Signs / TnSigns |  | en | low | studio | [zZEy10fpq3I 00:09:20](https://www.youtube.com/watch?v=zZEy10fpq3I&t=560s) | 1 |
| 330 | Bond |  | en | medium | studio | [zZEy10fpq3I 00:09:20](https://www.youtube.com/watch?v=zZEy10fpq3I&t=560s) | 1 |
| 331 | Рим | под редакцией Умберто Еко | ru | high | studio | [zZEy10fpq3I 00:09:27](https://www.youtube.com/watch?v=zZEy10fpq3I&t=567s) | 1 |
| 332 | 프라하의 묘지 (The Prague Cemetery) |  | ko | medium | studio | [zZEy10fpq3I 00:09:33](https://www.youtube.com/watch?v=zZEy10fpq3I&t=573s) | 2 |
| 333 | Kant und das Schnabeltier | Umberto Eco | de | high | studio | [zZEy10fpq3I 00:09:33](https://www.youtube.com/watch?v=zZEy10fpq3I&t=573s) | 1 |
| 334 | Pražský hřbitov | Umberto Eco | cs | medium | studio | [zZEy10fpq3I 00:09:33](https://www.youtube.com/watch?v=zZEy10fpq3I&t=573s) | 1 |
| 335 | Medioevo |  | it | high | studio | [zZEy10fpq3I 00:13:03](https://www.youtube.com/watch?v=zZEy10fpq3I&t=783s) | 4 |
| 336 | Hitler |  | it | high | studio | [zZEy10fpq3I 00:13:05](https://www.youtube.com/watch?v=zZEy10fpq3I&t=785s) | 3 |
| 337 | Avicenne |  | fr | medium | studio | [zZEy10fpq3I 00:13:21](https://www.youtube.com/watch?v=zZEy10fpq3I&t=801s) | 1 |
| 338 | Maometto |  | it | high | studio | [zZEy10fpq3I 00:13:21](https://www.youtube.com/watch?v=zZEy10fpq3I&t=801s) | 3 |
| 339 | San Juan de la Cruz y el Islam |  | es | high | studio | [zZEy10fpq3I 00:13:21](https://www.youtube.com/watch?v=zZEy10fpq3I&t=801s) | 2 |
| 340 | Il giornale di Gian Burrasca |  | it | medium | unknown | [zZEy10fpq3I 00:13:47](https://www.youtube.com/watch?v=zZEy10fpq3I&t=827s) | 1 |
| 341 | Il Giornalino |  | it | medium | unknown | [zZEy10fpq3I 00:13:48](https://www.youtube.com/watch?v=zZEy10fpq3I&t=828s) | 1 |
| 342 | Thesaurus Anatomicus | Frederik Ruysch | la | high | studio | [zZEy10fpq3I 00:14:18](https://www.youtube.com/watch?v=zZEy10fpq3I&t=858s) | 9 |
| 343 | Cabala |  | la | medium | unknown | [zZEy10fpq3I 00:16:30](https://www.youtube.com/watch?v=zZEy10fpq3I&t=990s) | 1 |
| 344 | Ars Magna Sciendi, sive Combinatoria | Athanasius Kircher | la | high | studio | [zZEy10fpq3I 00:17:11](https://www.youtube.com/watch?v=zZEy10fpq3I&t=1031s) | 14 |
| 345 | China [Monumentis ...] Illustrata | Athanasius Kircher | la | medium | studio | [zZEy10fpq3I 00:17:21](https://www.youtube.com/watch?v=zZEy10fpq3I&t=1041s) | 6 |
| 346 | Numero Zero | Umberto Eco | it | medium | studio | [zZEy10fpq3I 00:18:23](https://www.youtube.com/watch?v=zZEy10fpq3I&t=1103s) | 1 |
| 347 | Turris Babel sive Archontologia | Athanasius Kircher | la | medium | unknown | [zZEy10fpq3I 00:18:14](https://www.youtube.com/watch?v=zZEy10fpq3I&t=1094s) | 2 |
| 348 | Systema Sephyroticum X Divinorum Nominum |  | la | medium | unknown | [zZEy10fpq3I 00:20:25](https://www.youtube.com/watch?v=zZEy10fpq3I&t=1225s) | 1 |
| 349 | Tafeln |  | de | low | antichi | [zZEy10fpq3I 00:21:00](https://www.youtube.com/watch?v=zZEy10fpq3I&t=1260s) | 4 |
| 350 | Aufstieg und Niedergang der römischen Welt, II. Principat, Bd. 16.1 |  | de | high | unknown | [zZEy10fpq3I 00:21:01](https://www.youtube.com/watch?v=zZEy10fpq3I&t=1261s) | 1 |
| 351 | Aufstieg und Niedergang der römischen Welt — Tafeln/Register volume |  | de | medium | unknown | [zZEy10fpq3I 00:21:01](https://www.youtube.com/watch?v=zZEy10fpq3I&t=1261s) | 1 |
| 352 | Annales de chimie et de physique |  | fr | medium | antichi | [zZEy10fpq3I 00:26:56](https://www.youtube.com/watch?v=zZEy10fpq3I&t=1616s) | 55 |
| 353 | Poëme heureusement découvert & mis au jour, avec des Remarques savantes & recherchées | Chrisostome Matanasius (Docteur) | fr | medium | unknown | [zZEy10fpq3I 00:27:26](https://www.youtube.com/watch?v=zZEy10fpq3I&t=1646s) | 1 |
| 354 | L'autre jour Colin malade dedans son lict |  | fr | medium | unknown | [zZEy10fpq3I 00:28:33](https://www.youtube.com/watch?v=zZEy10fpq3I&t=1713s) | 2 |
| 355 | Carmen (In honorem et gloriam ... Chrisostomi Mathanasii) |  | la | medium | unknown | [zZEy10fpq3I 00:29:03](https://www.youtube.com/watch?v=zZEy10fpq3I&t=1743s) | 1 |
| 356 | Traduction Françoise: Poëme à la louange du très excellent et très subtil docteur Chrisostome Matha[nasius] |  | fr | medium | unknown | [zZEy10fpq3I 00:29:03](https://www.youtube.com/watch?v=zZEy10fpq3I&t=1743s) | 1 |
| 357 | Puikaantekeningen van 't Pronkjuweel der Aarts-Letter-Helden, Doctor Mathanasius |  | nl | medium | unknown | [zZEy10fpq3I 00:29:06](https://www.youtube.com/watch?v=zZEy10fpq3I&t=1746s) | 1 |
| 358 | Amphitheatrum Sapientiae Socraticae Joco-Seriae |  | la | low | unknown | [zZEy10fpq3I 00:30:21](https://www.youtube.com/watch?v=zZEy10fpq3I&t=1821s) | 1 |
| 359 | Chi mi ha fatta in testa? |  | it | medium | salotto | [zZEy10fpq3I 00:32:54](https://www.youtube.com/watch?v=zZEy10fpq3I&t=1974s) | 4 |
| 360 | L'Uomo Mascherato |  | it | medium | unknown | [zZEy10fpq3I 00:34:02](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2042s) | 1 |
| 361 | Sandokan alla Riscossa | E. Salgari | it | medium | salotto | [zZEy10fpq3I 00:34:13](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2053s) | 1 |
| 362 | I Misteri della Jungla Nera | Salgari | it | medium | salotto | [zZEy10fpq3I 00:34:13](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2053s) | 1 |
| 363 | Le Tigri di Mompracem | E. Salgari | it | medium | salotto | [zZEy10fpq3I 00:34:13](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2053s) | 1 |
| 364 | Il Corsaro Nero | Salgari | it | medium | salotto | [zZEy10fpq3I 00:34:13](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2053s) | 1 |
| 365 | Fantomas |  | fr | medium | salotto | [zZEy10fpq3I 00:34:17](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2057s) | 1 |
| 366 | Thesaurus Armamentarii Medico[...] |  | la | low | antichi | [zZEy10fpq3I 00:34:41](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2081s) | 1 |
| 367 | La scienza nuova | Giambattista Vico | it | medium | studio | [zZEy10fpq3I 00:35:20](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2120s) | 1 |
| 368 | La tradizione signorile nella Spagna americana | George Santayana | it | medium | studio | [zZEy10fpq3I 00:35:20](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2120s) | 1 |
| 369 | Champollion | Jean Lacouture | it | low | studio | [zZEy10fpq3I 00:35:21](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2121s) | 2 |
| 370 | Origin of Langu[age] |  | en | low | studio | [zZEy10fpq3I 00:35:23](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2123s) | 1 |
| 371 | Filosofia della rivelazione | Schelling | it | high | studio | [zZEy10fpq3I 00:35:23](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2123s) | 1 |
| 372 | [Vie d']Anne de Bretagne |  | fr | low | antichi | [zZEy10fpq3I 00:40:31](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2431s) | 1 |
| 373 | Livre d'Heures d'Anne de Bretagne |  | fr | medium | antichi | [zZEy10fpq3I 00:40:31](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2431s) | 1 |
| 374 | Ordini Equestri |  | it | medium | antichi | [zZEy10fpq3I 00:40:31](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2431s) | 1 |
| 375 | Old Testament |  | en | medium | antichi | [zZEy10fpq3I 00:40:35](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2435s) | 1 |
| 376 | Marie Curie |  | it | low | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 4 |
| 377 | Vivere con gli dei | Neil MacGregor | it | high | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 4 |
| 378 | Interviste e colloqui | Luciano Berio | it | high | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 4 |
| 379 | Versus |  | it | high | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 6 |
| 380 | Artificio di memoria | Fabio Mauri | it | high | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 4 |
| 381 | I misteri dell'altare di Isenheim di Grunewald | Giovanni Reale | it | high | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 4 |
| 382 | Romanino e la 'Sistina dei poveri' a Pisogne |  | it | high | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 4 |
| 383 | Voglia di libri | Mario Andreose | it | high | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 4 |
| 384 | L'era della comunicazione | Umberto Eco | it | high | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 8 |
| 385 | Il ceffo di Sir Thomas Browne | Roberto Calasso | it | medium | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 4 |
| 386 | Il bambino nascosto | Roberto Ando | it | high | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 4 |
| 387 | Das Irrenhaus |  | de | medium | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 4 |
| 388 | Der ewige Faschismus | Umberto Eco | de | high | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 11 |
| 389 | Note | Giancarlo Iliprandi | it | high | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 4 |
| 390 | Il volto del '900: da Matisse a Bacon, capolavori dal Centre Pompidou |  | it | high | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 4 |
| 391 | Giorgio Morandi: une retrospective |  | fr | high | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 4 |
| 392 | Viaggio in Italia | Guido Piovene | it | high | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 4 |
| 393 | Ricordi di un entomologo I | Jean-Henri Fabre | it | high | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 4 |
| 394 | Il cacciatore celeste | Roberto Calasso | it | high | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 4 |
| 395 | I mutanti | Sofia Bignamini | it | high | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 4 |
| 396 | I bambini di Marte | Lazzarato | it | medium | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 4 |
| 397 | Il crollo | Lorenzo Pregliasco | it | high | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 4 |
| 398 | A proposito di niente | Woody Allen | it | high | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 4 |
| 399 | Una scrittura sconcertante |  | it | medium | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 3 |
| 400 | il verri |  | it | medium | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 8 |
| 401 | Il bene e il male | Giulio Giorello, Vittorio Sgarbi | it | high | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 3 |
| 402 | [...]della memoria |  | it | low | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 1 |
| 403 | Due sigari in riva al mare | Michael Köhlmeier | it | medium | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 1 |
| 404 | Critique |  | fr | low | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 1 |
| 405 | Un sogno per tutti |  | it | low | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 1 |
| 406 | Una passione a Manhattan | Anna Ottani Cavina | it | medium | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 1 |
| 407 | Il primo [...] del mondo |  | it | low | salotto | [zZEy10fpq3I 00:42:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2571s) | 1 |
| 408 | Immagini dell'Italia. 1 |  | it | medium | salotto | [zZEy10fpq3I 00:42:59](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2579s) | 3 |
| 409 | Il Novecento |  | it | high | salotto | [zZEy10fpq3I 00:42:59](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2579s) | 6 |
| 410 | Lo scaffale infinito | Andrea Kerbaker | it | high | salotto | [zZEy10fpq3I 00:42:59](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2579s) | 3 |
| 411 | L'inconsolabile pensiero |  | it | low | studio | [zZEy10fpq3I 00:42:59](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2579s) | 1 |
| 412 | Il paradiso delle aragoste |  | it | medium | salotto | [zZEy10fpq3I 00:42:59](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2579s) | 3 |
| 413 | Scritti a mano | Matteo Motolese | it | high | salotto | [zZEy10fpq3I 00:42:59](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2579s) | 3 |
| 414 | Breve autobiografia | Giuseppe Tornatore | it | high | studio | [zZEy10fpq3I 00:42:59](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2579s) | 2 |
| 415 | L'omicidio di Umberto Eco | Oscar Rimini | it | low | studio | [zZEy10fpq3I 00:42:59](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2579s) | 1 |
| 416 | A passo di gambero | Umberto Eco | it | high | salotto | [zZEy10fpq3I 00:42:59](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2579s) | 3 |
| 417 | Questo e Kafka | Reiner Stach | it | high | salotto | [zZEy10fpq3I 00:42:59](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2579s) | 3 |
| 418 | Sulle spalle dei giganti | Umberto Eco | it | medium | studio | [zZEy10fpq3I 00:43:03](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2583s) | 1 |
| 419 | Il bel tacere | Pietro Salabe | it | medium | salotto | [zZEy10fpq3I 00:43:03](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2583s) | 3 |
| 420 | Umberto Eco e il PCI |  | it | high | salotto | [zZEy10fpq3I 00:43:03](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2583s) | 3 |
| 421 | La luce oltre il vetro | Lorenzo Puglisi | it | high | salotto | [zZEy10fpq3I 00:43:03](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2583s) | 3 |
| 422 | La colpa dell'agnello |  | it | low | studio | [zZEy10fpq3I 00:43:03](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2583s) | 2 |
| 423 | Compagni di scuola |  | it | medium | studio | [zZEy10fpq3I 00:43:03](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2583s) | 2 |
| 424 | I segreti dei fiori |  | it | medium | studio | [zZEy10fpq3I 00:43:03](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2583s) | 2 |
| 425 | Sulle spalle di Umberto |  | it | medium | salotto | [zZEy10fpq3I 00:43:03](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2583s) | 2 |
| 426 | Terre senz'ombra | Anna Ottani Cavina | it | medium | salotto | [zZEy10fpq3I 00:43:03](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2583s) | 2 |
| 427 | Tempo di Libri. Programma 2017 |  | it | medium | salotto | [zZEy10fpq3I 00:43:03](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2583s) | 2 |
| 428 | L'innominabile attuale | Roberto Calasso | it | medium | salotto | [zZEy10fpq3I 00:43:03](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2583s) | 2 |
| 429 | L'eredità di Umberto Eco |  | it | medium | salotto | [zZEy10fpq3I 00:43:03](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2583s) | 2 |
| 430 | Eco |  | it | low | salotto | [zZEy10fpq3I 00:43:03](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2583s) | 1 |
| 431 | Cerchi di capire, prof | Giovanna Cosenza | it | medium | salotto | [zZEy10fpq3I 00:43:03](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2583s) | 1 |
| 432 | L'anima ciliegia | Lia Levi | it | high | salotto | [zZEy10fpq3I 00:43:03](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2583s) | 1 |
| 433 | Il mistero de... |  | it | low | salotto | [zZEy10fpq3I 00:43:03](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2583s) | 1 |
| 434 | Fenice |  | it | low | salotto | [zZEy10fpq3I 00:43:03](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2583s) | 1 |
| 435 | [...] la primavera |  | it | low | salotto | [zZEy10fpq3I 00:43:03](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2583s) | 1 |
| 436 | Ciarlatani | Fausto Colombo | it | medium | salotto | [zZEy10fpq3I 00:43:03](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2583s) | 1 |
| 437 | Storie di percorso | Roberto Campari | it | medium | salotto | [zZEy10fpq3I 00:43:03](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2583s) | 1 |
| 438 | Auf den Schultern von Riesen | Umberto Eco | de | high | salotto | [zZEy10fpq3I 00:43:03](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2583s) | 1 |
| 439 | Pinocchio |  | it | high | corridoio | [zZEy10fpq3I 00:43:13](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2593s) | 10 |
| 440 | Il Corsaro delle Tenebre |  | it | high | corridoio | [zZEy10fpq3I 00:43:17](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2597s) | 9 |
| 441 | Storia del racconto popolare: prima del fumetto |  | it | high | corridoio | [zZEy10fpq3I 00:43:19](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2599s) | 2 |
| 442 | Eroi del racconto popolare |  | it | low | corridoio | [zZEy10fpq3I 00:44:04](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2644s) | 1 |
| 443 | Carducci | Giosuè Carducci | it | low | corridoio | [zZEy10fpq3I 00:44:04](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2644s) | 1 |
| 444 | Saggio sulla disuguaglianza delle razze umane | Arthur de Gobineau | it | high | studio | [zZEy10fpq3I 00:45:17](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2717s) | 1 |
| 445 | Mersenne ou la naissance du mécanisme |  | fr | medium | studio | [zZEy10fpq3I 00:45:17](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2717s) | 1 |
| 446 | The [Birth] of the Gods and Giants |  | en | low | studio | [zZEy10fpq3I 00:45:17](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2717s) | 1 |
| 447 | The Age of Lamarck |  | en | high | studio | [zZEy10fpq3I 00:45:17](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2717s) | 1 |
| 448 | Semiotik des Films |  | de | high | studio | [zZEy10fpq3I 00:46:19](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2779s) | 2 |
| 449 | Kant en het vogelbekdier | Umberto Eco | nl | medium | studio | [zZEy10fpq3I 00:46:41](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2801s) | 1 |
| 450 | Il superuomo di massa. Retorica e ideologia nel romanzo popolare | Umberto Eco | it | medium | unknown | [zZEy10fpq3I 00:47:09](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2829s) | 1 |
| 451 | Името на розата |  | bg | low | studio | [zZEy10fpq3I 01:14:27](https://www.youtube.com/watch?v=zZEy10fpq3I&t=4467s) | 2 |
| 452 | Una voce |  | it | high | studio | [zZEy10fpq3I 00:48:13](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2893s) | 1 |
| 453 | La Divina Commedia | [Dante Alighieri] | it | low | studio | [zZEy10fpq3I 00:48:15](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2895s) | 7 |
| 454 | Les Cahiers Feministes |  | fr | low | studio | [zZEy10fpq3I 00:50:59](https://www.youtube.com/watch?v=zZEy10fpq3I&t=3059s) | 1 |
| 455 | Everyman's Talmud | Abraham Cohen | en | high | studio | [zZEy10fpq3I 00:50:59](https://www.youtube.com/watch?v=zZEy10fpq3I&t=3059s) | 2 |
| 456 | Annuario Filosofico 1993 |  | it | high | studio | [zZEy10fpq3I 00:53:13](https://www.youtube.com/watch?v=zZEy10fpq3I&t=3193s) | 1 |
| 457 | Annuario Filosofico 1994 |  | it | high | studio | [zZEy10fpq3I 00:53:13](https://www.youtube.com/watch?v=zZEy10fpq3I&t=3193s) | 1 |
| 458 | L'attico reclamato |  | it | medium | studio | [zZEy10fpq3I 00:53:13](https://www.youtube.com/watch?v=zZEy10fpq3I&t=3193s) | 1 |
| 459 | Storia delle terre e dei luoghi leggendari |  | it | medium | unknown | [zZEy10fpq3I 00:54:54](https://www.youtube.com/watch?v=zZEy10fpq3I&t=3294s) | 1 |
| 460 | Le Roy Soleil |  | fr | high | antichi | [zZEy10fpq3I 00:57:05](https://www.youtube.com/watch?v=zZEy10fpq3I&t=3425s) | 1 |
| 461 | Francis Bacon: Concealed and Revealed | [Bertram G.] Theobald | en | medium | unknown | [zZEy10fpq3I 01:00:11](https://www.youtube.com/watch?v=zZEy10fpq3I&t=3611s) | 2 |
| 462 | The Bacon-Shak[e]spea[re Question / Mystery] |  | en | low | unknown | [zZEy10fpq3I 01:00:11](https://www.youtube.com/watch?v=zZEy10fpq3I&t=3611s) | 2 |
| 463 | Il Cimitero di Praga | Umberto Eco | it | medium | unknown | [zZEy10fpq3I 01:04:16](https://www.youtube.com/watch?v=zZEy10fpq3I&t=3856s) | 1 |
| 464 | The Plot: The Secret Story of the Protocols of the Elders of Zion |  | en | medium | unknown | [zZEy10fpq3I 01:05:31](https://www.youtube.com/watch?v=zZEy10fpq3I&t=3931s) | 2 |
| 465 | Intertexto | Mario Chamie | pt | medium | studio | [zZEy10fpq3I 01:14:27](https://www.youtube.com/watch?v=zZEy10fpq3I&t=4467s) | 2 |
| 466 | Le metamorfosi di Narciso |  | it | low | studio | [zZEy10fpq3I 01:14:27](https://www.youtube.com/watch?v=zZEy10fpq3I&t=4467s) | 2 |
| 467 | Intertesto | Mario Ciampi | it | medium | corridoio | [zZEy10fpq3I 01:14:27](https://www.youtube.com/watch?v=zZEy10fpq3I&t=4467s) | 1 |
| 468 | Clave |  | es | medium | studio | [zZEy10fpq3I 01:14:32](https://www.youtube.com/watch?v=zZEy10fpq3I&t=4472s) | 2 |
| 469 | Kircheri de Arte Magnetica | Athanasius Kircher | la | high | antichi | [zZEy10fpq3I 01:15:14](https://www.youtube.com/watch?v=zZEy10fpq3I&t=4514s) | 2 |
| 470 | Joco-seriorum Naturae et Artis, sive Magiae Naturalis | Athanasius Kircherus | la | high | antichi | [zZEy10fpq3I 01:15:14](https://www.youtube.com/watch?v=zZEy10fpq3I&t=4514s) | 1 |
| 471 | Iter Exstaticum |  | la | medium | antichi | [zZEy10fpq3I 01:15:14](https://www.youtube.com/watch?v=zZEy10fpq3I&t=4514s) | 1 |
| 472 | Tabula Kircheriana |  | la | medium | antichi | [zZEy10fpq3I 01:15:14](https://www.youtube.com/watch?v=zZEy10fpq3I&t=4514s) | 1 |
| 473 | Obeliscus Aegyptiacus | Athanasius Kircher | la | high | antichi | [zZEy10fpq3I 01:15:14](https://www.youtube.com/watch?v=zZEy10fpq3I&t=4514s) | 2 |
| 474 | Iter Ex[s]tati[cum] cum Kircheria[num] | Athanasius Kircher (ed. Gaspar Schott?) | la | low | antichi | [zZEy10fpq3I 01:15:17](https://www.youtube.com/watch?v=zZEy10fpq3I&t=4517s) | 3 |
| 475 | Prodromus Coptus | Athanasius Kircherus | la | low | antichi | [zZEy10fpq3I 01:15:17](https://www.youtube.com/watch?v=zZEy10fpq3I&t=4517s) | 3 |
| 476 | Puglia |  | it | medium | studio | [fondazione_01_E](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/01_E.webp) | 1 |
| 477 | Elogio della pazzia |  | it | low | studio | [fondazione_01_E](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/01_E.webp) | 1 |
| 478 | Bertozzi |  | it | medium | studio | [fondazione_02_H](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/02_H.webp) | 1 |
| 479 | A. Bueno |  | it | medium | studio | [fondazione_02_H](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/02_H.webp) | 1 |
| 480 | Matisse |  | it | medium | studio | [fondazione_02_H](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/02_H.webp) | 1 |
| 481 | Die Bilder |  | de | low | studio | [fondazione_04_F](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/04_F.webp) | 1 |
| 482 | The Book of Kells |  | en | high | studio | [fondazione_05_C](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/05_C.webp) | 1 |
| 483 | Prophéties | Nostradamus | fr | medium | studio | [fondazione_05_C](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/05_C.webp) | 1 |
| 484 | Alchimie |  | fr | medium | studio | [fondazione_07_D](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/07_D.webp) | 1 |
| 485 | Mercator |  | en | medium | studio | [fondazione_07_D](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/07_D.webp) | 1 |
| 486 | La regina delle fate | Edmund Spenser | it | high | studio | [fondazione_08_A-da_1_a_6](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/08_A-da%201%20a%206.webp) | 1 |
| 487 | Z |  |  | low | studio | [fondazione_09_A-da_7_a_12](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/09_A-da%207%20a%2012.webp) | 2 |
| 488 | Filosofia della musica |  | it | high | studio | [fondazione_14_L1-4](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/14_L1-4.webp) | 1 |
| 489 | Guglielmo di Ockham |  | it | medium | studio | [fondazione_14_L1-4](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/14_L1-4.webp) | 1 |
| 490 | Agostino |  | it | medium | studio | [fondazione_16_L8-12](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/16_L8-12.webp) | 1 |
| 491 | Berkeley |  | it | high | studio | [fondazione_16_L8-12](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/16_L8-12.webp) | 1 |
| 492 | Locke |  | it | high | studio | [fondazione_16_L8-12](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/16_L8-12.webp) | 1 |
| 493 | David Hume |  | it | high | studio | [fondazione_16_L8-12](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/16_L8-12.webp) | 1 |
| 494 | Michel de Montaigne |  | it | high | studio | [fondazione_16_L8-12](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/16_L8-12.webp) | 1 |
| 495 | Montesquieu |  | it | high | studio | [fondazione_16_L8-12](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/16_L8-12.webp) | 1 |
| 496 | Voltaire |  | it | high | studio | [fondazione_16_L8-12](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/16_L8-12.webp) | 1 |
| 497 | Schelling |  | it | high | studio | [fondazione_16_L8-12](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/16_L8-12.webp) | 1 |
| 498 | Gli Eleati |  | it | high | studio | [fondazione_17_I](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/17_I.webp) | 1 |
| 499 | Poetica | Aristotele | it | high | studio | [fondazione_17_I](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/17_I.webp) | 1 |
| 500 | Retorica | Aristotele | it | high | studio | [fondazione_17_I](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/17_I.webp) | 1 |
| 501 | Fisica | Aristotele | it | high | studio | [fondazione_17_I](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/17_I.webp) | 1 |
| 502 | Le opere logiche | Aristotele | it | medium | studio | [fondazione_17_I](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/17_I.webp) | 1 |
| 503 | Gli antichi commentatori |  | it | medium | studio | [fondazione_17_I](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/17_I.webp) | 1 |
| 504 | L'eccellenza di Dio |  | it | medium | studio | [fondazione_19_M-B](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/19_M-B.webp) | 1 |
| 505 | Clave: diccionario de uso del español |  | es | medium | studio | [fondazione_21_Nb](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/21_Nb.webp) | 1 |
| 506 | L'origine delle razze |  | it | medium | studio | [fondazione_26_S](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/26_S.webp) | 1 |
| 507 | Elephanti descriptio | Georg Christoph Petri von Hartenfels | la | high | antichi | [fondazione_03_ANTICHI-24](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall_antichi/03_ANTICHI-24.webp) | 1 |
| 508 | De la maladie d'amour |  | fr | high | antichi | [fondazione_03_ANTICHI-24](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall_antichi/03_ANTICHI-24.webp) | 1 |
| 509 | Schola Salernitana |  | la | high | antichi | [fondazione_03_ANTICHI-24](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall_antichi/03_ANTICHI-24.webp) | 1 |
| 510 | Emblemata | Florentius Schoonhovius (Florent Schoonhoven) | la | high | antichi | [fondazione_06_157-08-2](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall_antichi/06_157-08-2.webp) | 1 |
| 511 | De supernaturali historia (Utriusque cosmi historia) | Robert Fludd | la | high | antichi | [fondazione_07_357-03](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall_antichi/07_357-03.webp) | 1 |
| 512 | China monumentis | Athanasius Kircher | la | medium | antichi | [fondazione_08_399-11](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall_antichi/08_399-11.webp) | 1 |
| 513 | Geheime Figuren der Rosenkreuzer |  | la | high | antichi | [fondazione_11_452-05](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall_antichi/11_452-05.webp) | 1 |
| 514 | Le relationi universali | Giovanni Botero | it | medium | antichi | [fondazione_12_770-11](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall_antichi/12_770-11.webp) | 1 |
| 515 | Museum Wormianum | Ole Worm (Olaus Wormius) | la | high | antichi | [fondazione_14_778-03](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall_antichi/14_778-03.webp) | 1 |
| 516 | Thesaurus animalium / Thesaurus anatomicus | Frederik Ruysch | la | medium | antichi | [fondazione_15_926-12](https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall_antichi/15_926-12.webp) | 1 |
| 517 | Port-Royal | Charles Augustin Sainte-Beuve | fr | high | studio | [flickr_5772422901_b](https://www.flickr.com/photos/mglarsen/5772422901) | 1 |

## Excluded entries

Kept in `books_by_wall_eco.json` with `excluded: true` so the exclusion is auditable. A title is excluded only when every one of its sightings is on a frame with room `other` (or whose notes say the shelf is not Eco's); included titles seen additionally on such frames keep only their Eco-room sightings (132 sightings dropped that way).

| # | title | author | conf | reason | first seen |
|---:|---|---|---|---|---|
| 1 | [no title; author only: Jean Starobinski] | Jean Starobinski | low | room_id other (other): Other library / insert, dense pass 2026-09-09 shot t0009 at 01:54 (not Eco's she; room_id other (other): Other library / insert, dense pass 2026-09-09 shot t0010 at 02:01 (not Eco's she | [KZfOaug0mM4 00:01:54](https://www.youtube.com/watch?v=KZfOaug0mM4&t=114s) |
| 2 | [no title; author only: J. Chasseguet-Smirgel] | J. Chasseguet-Smirgel | low | room_id other (other): Other library / insert, dense pass 2026-09-09 shot d287 at 50:56 (not Eco's shel | [zZEy10fpq3I 00:50:56](https://www.youtube.com/watch?v=zZEy10fpq3I&t=3056s) |
| 3 | [no title; author only: Léo Taxil] | Léo Taxil | low | room_id other (other): Other library / insert, dense pass 2026-09-09 shot d371 at 66:37 (not Eco's shel | [zZEy10fpq3I 01:06:38](https://www.youtube.com/watch?v=zZEy10fpq3I&t=3998s) |
| 4 | …crònica en temps de Jaume I | Carles Vigueras (?) | low | room_id other (other): Other library / insert, dense pass 2026-09-09 shot t0004 at 00:55 (not Eco's she | [NtPk4irDiM8 00:00:55](https://www.youtube.com/watch?v=NtPk4irDiM8&t=55s) |
| 5 | Diario |  | low | notes say shelf is not Eco's: "not Eco's" | [NtPk4irDiM8 00:01:47](https://www.youtube.com/watch?v=NtPk4irDiM8&t=107s) |
| 6 | Genesis (Liber Bresith / Genesis) |  | medium | room_id other (other): Other library / insert, dense pass 2026-09-09 shot t0005 at 01:01 (not Eco's she | [KZfOaug0mM4 00:01:04](https://www.youtube.com/watch?v=KZfOaug0mM4&t=64s) |
| 7 | La responsabilita amministratori sindaci direttori generali liquidatori di societa | Bartolomeo Quatraro; Luca G. Picone | high | notes say shelf is not Eco's: "not part of Eco's home" | [FeIUY9EhZgI 00:00:37](https://www.youtube.com/watch?v=FeIUY9EhZgI&t=37s) |
| 8 | Intellectual Property Law of East Asia |  | high | notes say shelf is not Eco's: "not Eco's apartment"; notes say shelf is not Eco's: "not part of Eco's home" | [FeIUY9EhZgI 00:00:37](https://www.youtube.com/watch?v=FeIUY9EhZgI&t=37s) |
| 9 | The German Law of Obligations, Volume II: The Law of Torts (Third Edition) | Markesinis | high | notes say shelf is not Eco's: "not Eco's apartment"; notes say shelf is not Eco's: "not part of Eco's home" | [FeIUY9EhZgI 00:00:37](https://www.youtube.com/watch?v=FeIUY9EhZgI&t=37s) |
| 10 | The German Law of Obligations, Volume I: The Law of Contracts and Restitution | Markesinis, Lorenz, Dannemann | high | notes say shelf is not Eco's: "not Eco's apartment"; notes say shelf is not Eco's: "not part of Eco's home" | [FeIUY9EhZgI 00:00:37](https://www.youtube.com/watch?v=FeIUY9EhZgI&t=37s) |
| 11 | The Economics of Legal R[elationships?], Volume 3 | [Buracc]hi?; Ratliff; Cooter | low | notes say shelf is not Eco's: "not Eco's apartment"; notes say shelf is not Eco's: "not part of Eco's home" | [FeIUY9EhZgI 00:00:37](https://www.youtube.com/watch?v=FeIUY9EhZgI&t=37s) |
| 12 | Superman |  | high | room_id other (other): Other library / insert, dense pass 2026-09-09 shot t0043 at 08:39 (not Eco's she; room_id other (other): archival b&w photo, young Eco reading Superman and other comics | [ygvl-_gtAP8 00:00:53](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=53s) |
| 13 | Opera aperta | Umberto Eco | high | room_id other (other): archival b&w photo, young Eco holding up his book "Opera Aperta" | [ygvl-_gtAP8 00:00:55](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=55s) |
| 14 | (a work by Mastriani, exact title not legible) | Francesco Mastriani (probable) | low | room_id other (other): institutional archive shelving, deep oblique tracking shot | [ygvl-_gtAP8 00:01:06](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=66s) |
| 15 | Sull'immortalità | Umberto Eco | low | room_id other (other): institutional archive shelf of Umberto Eco's own works in translation ("Fondo Um | [ygvl-_gtAP8 00:01:29](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=89s) |
| 16 | (untranslated non-Latin script edition) | Umberto Eco | low | room_id other (other): institutional archive shelf of Umberto Eco's own works in translation ("Fondo Um | [ygvl-_gtAP8 00:01:29](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=89s) |
| 17 | Dronningen Loanas mystiske flamme | Umberto Eco | high | room_id other (other): institutional archive shelf of Umberto Eco's own works in translation ("Fondo Um | [ygvl-_gtAP8 00:01:29](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=89s) |
| 18 | История уродства (On Ugliness) | ed. Umberto Eco | high | room_id other (other): institutional archive shelf of Umberto Eco's own works in translation ("Fondo Um | [ygvl-_gtAP8 00:01:29](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=89s) |
| 19 | Fukoovo klatno (Foucault's Pendulum) | Umberto Eco | high | room_id other (other): institutional archive shelf of Umberto Eco's own works in translation ("Fondo Um | [ygvl-_gtAP8 00:01:29](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=89s) |
| 20 | Історія європейської цивілізації | ed. Umberto Eco | medium | room_id other (other): institutional archive shelf of Umberto Eco's own works in translation ("Fondo Um | [ygvl-_gtAP8 00:01:29](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=89s) |
| 21 | (Hebrew-language edition, title not transcribed) | Umberto Eco | low | room_id other (other): institutional archive shelf of Umberto Eco's own works in translation ("Fondo Um | [ygvl-_gtAP8 00:01:29](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=89s) |
| 22 | Пражское кладбище (The Prague Cemetery) | Umberto Eco | high | room_id other (other): institutional archive shelf of Umberto Eco's own works in translation ("Fondo Um | [ygvl-_gtAP8 00:01:29](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=89s) |
| 23 | La memoria vegetale [e altri scritti di bibliofilia] | Umberto Eco | medium | room_id other (other): Other library / insert, dense pass 2026-09-09 shot d073 at 10:00 (not Eco's shel; room_id other (other): Other library / insert, dense pass 2026-09-09 shot t0010 at 02:09 (not Eco's she; room_id other (other): Other library / insert, dense pass 2026-09-09 shot t0011 at 02:13 (not Eco's she | [ygvl-_gtAP8 00:02:11](https://www.youtube.com/watch?v=ygvl-_gtAP8&t=131s) |
| 24 | Dall'Albero al Labirinto | Umberto Eco | medium | room_id other (other): Other library / insert, dense pass 2026-09-09 shot d043 at 05:29 (not Eco's shel | [zZEy10fpq3I 00:05:29](https://www.youtube.com/watch?v=zZEy10fpq3I&t=329s) |
| 25 | Der Spiegel |  | low | room_id other (other): Other library / insert, dense pass 2026-09-09 shot t0043 at 08:39 (not Eco's she | [zZEy10fpq3I 00:08:39](https://www.youtube.com/watch?v=zZEy10fpq3I&t=519s) |
| 26 | Lois Lane |  | low | room_id other (other): Other library / insert, dense pass 2026-09-09 shot t0043 at 08:39 (not Eco's she | [zZEy10fpq3I 00:08:45](https://www.youtube.com/watch?v=zZEy10fpq3I&t=525s) |
| 27 | Le Garzantine: Medioevo |  | high | room_id other (other): Fondazione Umberto Eco archive room, modular shelving (visible unit label partly | [zZEy10fpq3I 00:13:07](https://www.youtube.com/watch?v=zZEy10fpq3I&t=787s) |
| 28 | Tempus, Aevum, Aeternitas |  | medium | room_id other (other): Fondazione Umberto Eco archive room, modular shelving | [zZEy10fpq3I 00:13:09](https://www.youtube.com/watch?v=zZEy10fpq3I&t=789s) |
| 29 | L'isola del giorno prima | Umberto Eco | high | room_id other (other): Modern office/interview-room shelving with paperback stacks (not the private apa; room_id other (other): Other library / insert, dense pass 2026-09-09 shot t0088 at 17:48 (not Eco's she; room_id other (other): Other library / insert, dense pass 2026-09-09 shot t0089 at 17:54 (not Eco's she | [zZEy10fpq3I 00:17:47](https://www.youtube.com/watch?v=zZEy10fpq3I&t=1067s) |
| 30 | Dagli scritti di Umberto Eco | Umberto Eco | medium | room_id other (other): Book endpaper insert with Eco ex-libris bookplate; room_id other (other): Other library / insert, dense pass 2026-09-09 shot d136 at 18:51 (not Eco's shel | [zZEy10fpq3I 00:18:51](https://www.youtube.com/watch?v=zZEy10fpq3I&t=1131s) |
| 31 | Des signes et de l'art de penser considérés dans leurs rapports mutuels, tome 1 | Joseph-Marie Degérando | high | room_id other (grand_baroque_library_archival): antique shelf row, rack-focus close-up (archival/establishing-shot library, not  | [zZEy10fpq3I 00:30:13](https://www.youtube.com/watch?v=zZEy10fpq3I&t=1813s) |
| 32 | Des signes et de l'art de penser considérés dans leurs rapports mutuels, tome 2 | Joseph-Marie Degérando | high | room_id other (grand_baroque_library_archival): antique shelf row, rack-focus close-up (archival/establishing-shot library, not  | [zZEy10fpq3I 00:30:13](https://www.youtube.com/watch?v=zZEy10fpq3I&t=1813s) |
| 33 | Des signes et de l'art de penser considérés dans leurs rapports mutuels, tome 3 | Joseph-Marie Degérando | high | room_id other (grand_baroque_library_archival): antique shelf row, rack-focus close-up (archival/establishing-shot library, not  | [zZEy10fpq3I 00:30:13](https://www.youtube.com/watch?v=zZEy10fpq3I&t=1813s) |
| 34 | Des signes et de l'art de penser considérés dans leurs rapports mutuels, tome 4 | Joseph-Marie Degérando | high | room_id other (grand_baroque_library_archival): antique shelf row, rack-focus close-up (archival/establishing-shot library, not  | [zZEy10fpq3I 00:30:13](https://www.youtube.com/watch?v=zZEy10fpq3I&t=1813s) |
| 35 | La misteriosa fiamma della Regina Loana | Umberto Eco | high | room_id other (other): printed book cover (held by narrator) | [zZEy10fpq3I 00:34:21](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2061s) |
| 36 | Apocalittici e integrati | Umberto Eco | high | room_id other (other): book cover / title card insert | [zZEy10fpq3I 00:34:37](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2077s) |
| 37 | Opere (Carducci) | Giosuè Carducci | high | room_id other (archive_stacks): archive stacks, woman browsing open shelving (Sonzogno/classics section); room_id other (other): empty leather chair, white modern bookshelf clearly visible, catalog tags 'L11.8 | [zZEy10fpq3I 00:43:29](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2609s) |
| 38 | Lo snob |  | medium | room_id other (archive_stacks): archive stacks, shelf edge tag 'A' labelled BAUDELAIRE / HUYSMANS | [zZEy10fpq3I 00:44:35](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2675s) |
| 39 | Storia della bruttezza | Umberto Eco | high | room_id other (other): shelf of foreign-language editions of Umberto Eco's 'Storia della bruttezza'; room_id other (other): shelf of foreign-language editions of Umberto Eco's own books, dark blue/black u | [zZEy10fpq3I 00:45:17](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2717s) |
| 40 | The Name of the Rose | Umberto Eco | high | room_id other (other): graphic montage of foreign-language covers of Eco's 'Il nome della rosa' / The N | [zZEy10fpq3I 00:47:35](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2855s) |
| 41 | Nafn Rósarinnar | Umberto Eco | high | room_id other (other): Other library / insert, dense pass 2026-09-09 shot t0238 at 47:42 (not Eco's she; room_id other (other): graphic montage of 'Il nome della rosa' covers, grid growing to 6 | [zZEy10fpq3I 00:47:37](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2857s) |
| 42 | Il nome de la rosa | Umberto Eco | medium | room_id other (other): Other library / insert, dense pass 2026-09-09 shot t0238 at 47:42 (not Eco's she; room_id other (other): graphic montage of 'Il nome della rosa' covers, grid growing to 6 | [zZEy10fpq3I 00:47:37](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2857s) |
| 43 | 장미의 이름 | Umberto Eco | high | room_id other (other): graphic montage of 'Il nome della rosa' covers, grid grown to 10 | [zZEy10fpq3I 00:47:39](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2859s) |
| 44 | สัญญาแห่งดอกกุหลาบ | Umberto Eco | high | room_id other (other): Other library / insert, dense pass 2026-09-09 shot t0238 at 47:42 (not Eco's she; room_id other (other): graphic montage of 'Il nome della rosa' covers, grid grown to 10 | [zZEy10fpq3I 00:47:39](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2859s) |
| 45 | Qizilgülün adı | Umberto Eco | high | room_id other (other): graphic montage of 'Il nome della rosa' covers, grid grown to 10, different set | [zZEy10fpq3I 00:47:41](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2861s) |
| 46 | اسم الوردة | Umberto Eco | high | room_id other (other): graphic montage of 'Il nome della rosa' covers, grid grown to 10, different set | [zZEy10fpq3I 00:47:41](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2861s) |
| 47 | 薔薇の名前 | Umberto Eco | high | room_id other (other): graphic montage of 'Il nome della rosa' covers, grid grown to 10, different set | [zZEy10fpq3I 00:47:41](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2861s) |
| 48 | 장미의 이름 (Jangmiui ireum) [하] — The Name of the Rose, vol.2, revised edition | 움베르토 에코 (Umberto Eco), tr. 이윤기 | medium | room_id other (other): Other library / insert, dense pass 2026-09-09 shot t0238 at 47:42 (not Eco's she | [zZEy10fpq3I 00:47:42](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2862s) |
| 49 | Το όνομα του ρόδου (To onoma tou rodou) | Ουμπέρτο Έκο (Umberto Eco) | medium | room_id other (other): Other library / insert, dense pass 2026-09-09 shot t0238 at 47:42 (not Eco's she | [zZEy10fpq3I 00:47:42](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2862s) |
| 50 | Վարդի անունը (Vardi anunըy) | Ումբերտո Էկո (Umberto Eco) | medium | room_id other (other): Other library / insert, dense pass 2026-09-09 shot t0238 at 47:42 (not Eco's she | [zZEy10fpq3I 00:47:42](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2862s) |
| 51 | Rosens namn | Umberto Eco | medium | room_id other (other): Other library / insert, dense pass 2026-09-09 shot t0238 at 47:42 (not Eco's she | [zZEy10fpq3I 00:47:42](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2862s) |
| 52 | Qizilgülün Adi | Umberto Eco | medium | room_id other (other): Other library / insert, dense pass 2026-09-09 shot t0238 at 47:42 (not Eco's she | [zZEy10fpq3I 00:47:45](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2865s) |
| 53 | اسم الوردة (Ism al-Warda) / Il nome della rosa | أمبرتو إيكو (Umberto Eco), tr. أحمد الصمعي | medium | room_id other (other): Other library / insert, dense pass 2026-09-09 shot t0238 at 47:42 (not Eco's she | [zZEy10fpq3I 00:47:45](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2865s) |
| 54 | 薔薇の名前 (Bara no namae), vol. 下 (2) | ウンベルト・エーコ (Umberto Eco), tr. 河島英昭 | medium | room_id other (other): Other library / insert, dense pass 2026-09-09 shot t0238 at 47:42 (not Eco's she | [zZEy10fpq3I 00:47:45](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2865s) |
| 55 | Tractatus de Venenis |  | high | room_id other (other): same manuscript, title line visible | [zZEy10fpq3I 00:48:45](https://www.youtube.com/watch?v=zZEy10fpq3I&t=2925s) |
| 56 | Ex libris Umberto Eco |  | medium | room_id other (other): Other library / insert, dense pass 2026-09-09 shot d319 at 57:09 (not Eco's shel | [zZEy10fpq3I 00:57:10](https://www.youtube.com/watch?v=zZEy10fpq3I&t=3430s) |
| 57 | William Shakespeare's Comedies, Histories, Tragedies, and Poems | R. Grant White | medium | room_id other (other): Other library / insert, dense pass 2026-09-09 shot t0289 at 57:53 (not Eco's she | [zZEy10fpq3I 00:57:53](https://www.youtube.com/watch?v=zZEy10fpq3I&t=3473s) |
| 58 | Shakespeare Studies | R. Grant White | medium | room_id other (other): Other library / insert, dense pass 2026-09-09 shot t0289 at 57:53 (not Eco's she | [zZEy10fpq3I 00:57:53](https://www.youtube.com/watch?v=zZEy10fpq3I&t=3473s) |
| 59 | New Glossary of the Obscure Words in Shakespeare, and the Dramatists of the Seventeenth Century | Charles Mackay, LL.D., F.S.A. | medium | room_id other (other): Other library / insert, dense pass 2026-09-09 shot t0289 at 57:53 (not Eco's she | [zZEy10fpq3I 00:57:53](https://www.youtube.com/watch?v=zZEy10fpq3I&t=3473s) |
| 60 | Annals of the Life and Work of William Shakespeare | Joseph Cundall | medium | room_id other (other): Other library / insert, dense pass 2026-09-09 shot t0289 at 57:53 (not Eco's she | [zZEy10fpq3I 00:57:53](https://www.youtube.com/watch?v=zZEy10fpq3I&t=3473s) |
| 61 | The Gaelic Etymology of the Languages of Western Europe | Charles Mackay | medium | room_id other (other): Other library / insert, dense pass 2026-09-09 shot t0289 at 57:53 (not Eco's she | [zZEy10fpq3I 00:57:56](https://www.youtube.com/watch?v=zZEy10fpq3I&t=3476s) |
| 62 | Dethroning Shakspere | edited by R. M. Theobald, M.A. | medium | room_id other (other): Other library / insert, dense pass 2026-09-09 shot t0289 at 57:53 (not Eco's she | [zZEy10fpq3I 00:57:56](https://www.youtube.com/watch?v=zZEy10fpq3I&t=3476s) |
| 63 | Bacon, Shakespeare, and the Rosicrucians |  | medium | room_id other (other): Other library / insert, dense pass 2026-09-09 shot t0290 at 58:07 (not Eco's she | [zZEy10fpq3I 00:58:07](https://www.youtube.com/watch?v=zZEy10fpq3I&t=3487s) |
| 64 | A New Study of Shakespeare |  | low | room_id other (other): Other library / insert, dense pass 2026-09-09 shot t0290 at 58:07 (not Eco's she | [zZEy10fpq3I 00:58:07](https://www.youtube.com/watch?v=zZEy10fpq3I&t=3487s) |
| 65 | The Great Cryptogram: Francis Bacon's Cipher in the So-Called Shakespeare Plays |  | medium | room_id other (other): Other library / insert, dense pass 2026-09-09 shot t0291 at 58:20 (not Eco's she | [zZEy10fpq3I 00:58:20](https://www.youtube.com/watch?v=zZEy10fpq3I&t=3500s) |
| 66 | Shakespeare's Beehive |  | medium | room_id other (other): Archival bookshelf insert illustrating the Shakespeare/Bacon authorship dispute | [zZEy10fpq3I 01:00:08](https://www.youtube.com/watch?v=zZEy10fpq3I&t=3608s) |
| 67 | I Misteri della Framassoneria | Léo Taxil | medium | room_id other (other): Other library / insert, dense pass 2026-09-09 shot d371 at 66:37 (not Eco's shel | [zZEy10fpq3I 01:06:41](https://www.youtube.com/watch?v=zZEy10fpq3I&t=4001s) |
| 68 | Encyclopaedia Judaica |  | high | room_id other (other): Stock/B-roll library footage (not Eco's apartment) - mixed English technical/ref | [zZEy10fpq3I 01:13:09](https://www.youtube.com/watch?v=zZEy10fpq3I&t=4389s) |
| 69 | 中共党史人物传 (Zhonggong Dangshi Renwu Zhuan / Biographies of CPC Party History Figures) |  | medium | room_id other (other): Stock/B-roll library footage (not Eco's apartment) | [zZEy10fpq3I 01:13:11](https://www.youtube.com/watch?v=zZEy10fpq3I&t=4391s) |
| 70 | Clave: diccionario de uso del español actual |  | medium | room_id other (other): Real Milan apartment, exterior courtyard shot through two open windows with flow | [zZEy10fpq3I 01:14:32](https://www.youtube.com/watch?v=zZEy10fpq3I&t=4472s) |

Frames excluded because their notes say the shelf is not Eco's (in addition to every frame with room_id `other`):
- spines_iRXEQVTI95k_dense.jsonl:17 t_000041.jpg (room other, wall dense-other-t0003): "(not Eco's"
- spines_iRXEQVTI95k_dense.jsonl:21 t_000055.jpg (room other, wall dense-other-t0004): "(not Eco's"
- spines_iRXEQVTI95k_dense.jsonl:22 s_000055_60.jpg (room other, wall dense-other-t0004): "(not Eco's"
- spines_iRXEQVTI95k_dense.jsonl:23 s_000101_36.jpg (room other, wall dense-other-t0005): "(not Eco's"
- spines_iRXEQVTI95k_dense.jsonl:24 t_000103.jpg (room other, wall dense-other-t0005): "(not Eco's"
- spines_iRXEQVTI95k_dense.jsonl:29 s_000119_40.jpg (room other, wall dense-other-t0006): "(not Eco's"
- spines_iRXEQVTI95k_dense.jsonl:30 t_000129.jpg (room other, wall dense-other-t0007): "(not Eco's"
- spines_iRXEQVTI95k_dense.jsonl:31 s_000130_12.jpg (room other, wall dense-other-t0007): "(not Eco's"
- spines_iRXEQVTI95k_dense.jsonl:32 t_000131.jpg (room other, wall dense-other-t0007): "(not Eco's"
- spines_iRXEQVTI95k_dense.jsonl:35 s_000142_44.jpg (room other, wall dense-other-t0008): "(not Eco's"
- spines_iRXEQVTI95k_dense.jsonl:36 t_000143.jpg (room other, wall dense-other-t0008): "(not Eco's"
- spines_iRXEQVTI95k_dense.jsonl:37 s_000144_52.jpg (room other, wall dense-other-t0008): "(not Eco's"
- spines_iRXEQVTI95k_dense.jsonl:38 t_000145.jpg (room other, wall dense-other-t0008): "(not Eco's"
- spines_NtPk4irDiM8_dense.jsonl:7 t_000055.jpg (room other, wall dense-other-t0004): "not Eco's own library"
- spines_NtPk4irDiM8_dense.jsonl:8 t_000057.jpg (room other, wall dense-other-t0004): "(not Eco's"
- spines_NtPk4irDiM8_dense.jsonl:10 t_000059.jpg (room other, wall dense-other-t0004): "(not Eco's"
- spines_NtPk4irDiM8_dense.jsonl:11 s_000059_72.jpg (room other, wall dense-other-t0004): "(not Eco's"
- spines_NtPk4irDiM8_dense.jsonl:12 s_000100_24.jpg (room other, wall dense-other-t0005): "(not Eco's"
- spines_NtPk4irDiM8_dense.jsonl:13 s_000100_48.jpg (room other, wall dense-other-t0005): "(not Eco's"
- spines_NtPk4irDiM8_dense.jsonl:14 t_000101.jpg (room other, wall dense-other-t0005): "(not Eco's"
- spines_NtPk4irDiM8_dense.jsonl:15 s_000101_28.jpg (room other, wall dense-other-t0005): "(not Eco's"
- spines_NtPk4irDiM8_dense.jsonl:16 s_000101_52.jpg (room other, wall dense-other-t0005): "(not Eco's"
- spines_NtPk4irDiM8_dense.jsonl:36 t_000121.jpg (room other, wall dense-other-t0006): "(not Eco's"
- spines_NtPk4irDiM8_dense.jsonl:37 s_000122_72.jpg (room other, wall dense-other-t0006): "(not Eco's"
- spines_NtPk4irDiM8_dense.jsonl:38 t_000123.jpg (room other, wall dense-other-t0006): "(not Eco's"
- spines_NtPk4irDiM8_dense.jsonl:39 s_000124_32.jpg (room other, wall dense-other-t0007): "(not Eco's"
- spines_NtPk4irDiM8_dense.jsonl:40 t_000125.jpg (room other, wall dense-other-t0007): "(not Eco's"
- spines_NtPk4irDiM8_dense.jsonl:41 t_000127.jpg (room other, wall dense-other-t0007): "(not Eco's"
- spines_NtPk4irDiM8_dense.jsonl:42 t_000129.jpg (room other, wall dense-other-t0007): "(not Eco's"
- spines_NtPk4irDiM8_dense.jsonl:43 t_000131.jpg (room other, wall dense-other-t0007): "(not Eco's"
- spines_NtPk4irDiM8_dense.jsonl:44 t_000147.jpg (room study, wall dense-studio-t0008): "not Eco's"
- spines_NtPk4irDiM8_dense.jsonl:45 s_000147_96.jpg (room other, wall dense-other-t0008): "(not Eco's"
- spines_NtPk4irDiM8_dense.jsonl:47 t_000151.jpg (room other, wall dense-other-t0009): "(not Eco's"
- spines_NtPk4irDiM8_dense.jsonl:48 t_000153.jpg (room other, wall dense-other-t0009): "(not Eco's"
- spines_NtPk4irDiM8_dense.jsonl:49 t_000155.jpg (room other, wall dense-other-t0009): "(not Eco's"
- spines_KZfOaug0mM4_dense.jsonl:24 t_000041.jpg (room other, wall dense-other-t0003): "(not Eco's"
- spines_KZfOaug0mM4_dense.jsonl:25 t_000043.jpg (room other, wall dense-other-t0003): "(not Eco's"
- spines_KZfOaug0mM4_dense.jsonl:26 t_000045.jpg (room other, wall dense-other-t0003): "(not Eco's"
- spines_KZfOaug0mM4_dense.jsonl:35 t_000101.jpg (room other, wall dense-other-t0005): "not Eco's home"
- spines_KZfOaug0mM4_dense.jsonl:36 t_000103.jpg (room other, wall dense-other-t0005): "(not Eco's"
- spines_KZfOaug0mM4_dense.jsonl:37 s_000103_52.jpg (room other, wall dense-other-t0005): "(not Eco's"
- spines_KZfOaug0mM4_dense.jsonl:38 t_000105.jpg (room other, wall dense-other-t0005): "(not Eco's"
- spines_KZfOaug0mM4_dense.jsonl:39 t_000107.jpg (room other, wall dense-other-t0005): "(not Eco's"
- spines_KZfOaug0mM4_dense.jsonl:40 t_000109.jpg (room other, wall dense-other-t0005): "(not Eco's"
- spines_KZfOaug0mM4_dense.jsonl:55 s_000154_28.jpg (room other, wall dense-other-t0009): "not Eco's flat"
- spines_KZfOaug0mM4_dense.jsonl:56 t_000201.jpg (room other, wall dense-other-t0010): "(not Eco's"
- spines_KZfOaug0mM4_dense.jsonl:57 t_000203.jpg (room other, wall dense-other-t0010): "(not Eco's"
- spines_KZfOaug0mM4_dense.jsonl:58 s_000203_04.jpg (room other, wall dense-other-t0010): "(not Eco's"
- spines_FeIUY9EhZgI_dense.jsonl:15 s_000037_08.jpg (room study, wall W4): "not part of Eco's home"
- spines_FeIUY9EhZgI_dense.jsonl:27 t_000101.jpg (room corridor, wall dense-corridoio-t0005): "not Eco's home"
- spines_FeIUY9EhZgI_dense.jsonl:35 t_000125.jpg (room other, wall dense-other-t0007): "(not Eco's"
- spines_FeIUY9EhZgI_dense.jsonl:38 t_000131.jpg (room other, wall dense-other-t0007): "not Eco's private flat"
- spines_FeIUY9EhZgI_dense.jsonl:39 t_000133.jpg (room other, wall dense-other-t0007): "(not Eco's"
- spines_FeIUY9EhZgI_dense.jsonl:40 t_000135.jpg (room other, wall dense-other-t0007): "(not Eco's"
- spines_FeIUY9EhZgI_dense.jsonl:41 s_000135_96.jpg (room other, wall dense-other-t0007): "(not Eco's"
- spines_FeIUY9EhZgI_dense.jsonl:42 t_000137.jpg (room other, wall dense-other-t0008): "(not Eco's"
- spines_FeIUY9EhZgI_dense.jsonl:43 t_000139.jpg (room other, wall dense-other-t0008): "not Eco's flat"
- spines_FeIUY9EhZgI_dense.jsonl:44 s_000139_25.jpg (room other, wall dense-other-t0008): "not Eco's flat"
- spines_FeIUY9EhZgI_dense.jsonl:45 t_000141.jpg (room other, wall dense-other-t0008): "not Eco's flat"
- spines_FeIUY9EhZgI_dense.jsonl:46 t_000143.jpg (room other, wall dense-other-t0008): "not Eco's flat"
- spines_FeIUY9EhZgI_dense.jsonl:47 t_000145.jpg (room other, wall dense-other-t0008): "not Eco's flat"
- spines_FeIUY9EhZgI_dense.jsonl:48 s_000145_54.jpg (room other, wall dense-other-t0008): "not Eco's flat"
- spines_FeIUY9EhZgI_dense.jsonl:49 t_000147.jpg (room other, wall dense-other-t0008): "not Eco's private library"
- spines_FeIUY9EhZgI_dense.jsonl:50 s_000147_25.jpg (room other, wall dense-other-t0008): "not Eco's private library"
- spines_bcK8rOkcb3k_dense.jsonl:15 t_000037.jpg (room study, wall W5): "not Eco's apartment"
- spines_bcK8rOkcb3k_dense.jsonl:41 t_000131.jpg (room other, wall dense-other-t0007): "not Eco's private apartment"
- spines_bcK8rOkcb3k_dense.jsonl:42 t_000133.jpg (room other, wall dense-other-t0007): "(not Eco's"
- spines_bcK8rOkcb3k_dense.jsonl:43 s_000133_25.jpg (room other, wall dense-other-t0007): "not Eco's private apartment"
- spines_bcK8rOkcb3k_dense.jsonl:44 t_000135.jpg (room other, wall dense-other-t0007): "(not Eco's"
- spines_bcK8rOkcb3k_dense.jsonl:45 s_000135_42.jpg (room other, wall dense-other-t0007): "not Eco's private apartment"
- spines_bcK8rOkcb3k_dense.jsonl:46 t_000137.jpg (room other, wall dense-other-t0008): "not Eco's private apartment"
- spines_bcK8rOkcb3k_dense.jsonl:47 t_000139.jpg (room other, wall dense-other-t0008): "not Eco's private flat"
- spines_bcK8rOkcb3k_dense.jsonl:48 t_000141.jpg (room other, wall dense-other-t0008): "Not Eco's flat"
- spines_bcK8rOkcb3k_dense.jsonl:49 s_000141_54.jpg (room other, wall dense-other-t0008): "(not Eco's"
- spines_bcK8rOkcb3k_dense.jsonl:50 t_000143.jpg (room other, wall dense-other-t0008): "(not Eco's"
- spines_bcK8rOkcb3k_dense.jsonl:51 s_000143_50.jpg (room other, wall dense-other-t0008): "(not Eco's"
- spines_bcK8rOkcb3k_dense.jsonl:52 s_000145_00.jpg (room other, wall dense-other-t0008): "(not Eco's"
- spines_bcK8rOkcb3k_dense.jsonl:53 t_000147.jpg (room other, wall dense-other-t0008): "(not Eco's"
- spines_bcK8rOkcb3k_dense.jsonl:54 t_000149.jpg (room other, wall dense-other-t0009): "(not Eco's"
- spines_ygvl-_gtAP8_dense.jsonl:49 t_000209.jpg (room other, wall dense-other-t0010): "(not Eco's"
- spines_ygvl-_gtAP8_dense.jsonl:50 t_000211.jpg (room other, wall dense-other-t0010): "(not Eco's"
- spines_ygvl-_gtAP8_dense.jsonl:51 t_000213.jpg (room other, wall dense-other-t0011): "(not Eco's"
- spines_ygvl-_gtAP8.jsonl:58 t_000237.jpg (room other, wall W5): "not Eco's flat"
- spines_ygvl-_gtAP8.jsonl:59 t_000239.jpg (room other, wall W5): "not Eco's flat"
- spines_ygvl-_gtAP8.jsonl:60 t_000241.jpg (room other, wall W5): "not Eco's flat"
- spines_ygvl-_gtAP8.jsonl:61 t_000243.jpg (room other, wall W5): "not Eco's flat"
- spines_ygvl-_gtAP8.jsonl:62 t_000245.jpg (room other, wall W5): "not Eco's flat"
- spines_ygvl-_gtAP8_dense.jsonl:53 t_000251.jpg (room other, wall dense-other-t0014): "(not Eco's"
- spines_ygvl-_gtAP8_dense.jsonl:55 t_000309.jpg (room other, wall dense-other-t0015): "(not Eco's"
- spines_ygvl-_gtAP8_dense.jsonl:56 t_000311.jpg (room other, wall dense-other-t0015): "(not Eco's"
- spines_ygvl-_gtAP8_dense.jsonl:57 t_000313.jpg (room other, wall dense-other-t0016): "(not Eco's"
- spines_ygvl-_gtAP8_dense.jsonl:58 t_000315.jpg (room other, wall dense-other-t0016): "(not Eco's"
- spines_ygvl-_gtAP8_dense.jsonl:59 s_000325_88.jpg (room other, wall dense-other-t0017): "(not Eco's"
- spines_ygvl-_gtAP8_dense.jsonl:60 t_000327.jpg (room other, wall dense-other-t0017): "(not Eco's"
- spines_ygvl-_gtAP8_dense.jsonl:61 t_000329.jpg (room other, wall dense-other-t0017): "(not Eco's"
- spines_ygvl-_gtAP8_dense.jsonl:62 t_000331.jpg (room other, wall dense-other-t0017): "(not Eco's"
- spines_ygvl-_gtAP8_dense.jsonl:63 t_000333.jpg (room other, wall dense-other-t0017): "(not Eco's"
- spines_ygvl-_gtAP8_dense.jsonl:64 t_000335.jpg (room other, wall dense-other-t0017): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:14 d_004_85.jpg (room other, wall dense-other-d004): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:15 d_004_91.jpg (room other, wall dense-other-d004): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:27 d_043_03.jpg (room other, wall dense-other-d043): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:31 f_000342.jpg (room other, wall dense-other-t0028): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:32 f_000349.jpg (room other, wall dense-other-t0029): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:34 d_046_03.jpg (room other, wall dense-other-d046): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:48 f_000407.jpg (room other, wall dense-other-t0033): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:49 f_000411.jpg (room other, wall dense-other-t0034): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:101 d_058_08.jpg (room other, wall dense-other-d058): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:102 d_058_09.jpg (room other, wall dense-other-d058): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:105 d_059_01.jpg (room other, wall dense-other-d059): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:107 d_060_01.jpg (room other, wall dense-other-d060): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:108 d_059_03.jpg (room other, wall dense-other-d059): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:157 f_000519.jpg (room other, wall dense-other-t0043): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:158 f_000525.jpg (room other, wall dense-other-t0043): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:159 d_066_01.jpg (room other, wall dense-other-d066): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:160 d_066_02.jpg (room other, wall dense-other-d066): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:161 d_066_04.jpg (room other, wall dense-other-d066): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:162 d_066_05.jpg (room other, wall dense-other-d066): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:163 d_066_07.jpg (room other, wall dense-other-d066): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:164 d_066_08.jpg (room other, wall dense-other-d066): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:165 d_066_10.jpg (room other, wall dense-other-d066): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:194 d_072_03.jpg (room other, wall dense-other-d072): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:195 d_072_04.jpg (room other, wall dense-other-d072): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:196 d_072_05.jpg (room other, wall dense-other-d072): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:197 d_072_06.jpg (room other, wall dense-other-d072): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:198 d_072_07.jpg (room other, wall dense-other-d072): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:199 d_072_08.jpg (room other, wall dense-other-d072): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:201 d_072_10.jpg (room other, wall dense-other-d072): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:202 d_073_01.jpg (room other, wall dense-other-d073): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:203 d_072_11.jpg (room other, wall dense-other-d072): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:204 d_073_02.jpg (room other, wall dense-other-d073): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:205 d_073_03.jpg (room other, wall dense-other-d073): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:206 d_073_04.jpg (room other, wall dense-other-d073): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:207 d_073_05.jpg (room other, wall dense-other-d073): "(not Eco's"
- spines_zZEy10fpq3I_part1.jsonl:6 t_001746.jpg (room other, wall office-shelf-1): "not the private apartment"
- spines_zZEy10fpq3I_dense.jsonl:353 f_001068.jpg (room other, wall dense-other-t0088): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:354 f_001074.jpg (room other, wall dense-other-t0089): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:366 d_136_03.jpg (room other, wall dense-other-d136): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:371 d_138_11.jpg (room other, wall dense-other-d138): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:372 d_138_14.jpg (room other, wall dense-other-d138): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:373 d_138_17.jpg (room other, wall dense-other-d138): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:374 d_138_19.jpg (room other, wall dense-other-d138): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:375 d_138_22.jpg (room other, wall dense-other-d138): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:377 d_138_27.jpg (room other, wall dense-other-d138): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:378 d_138_30.jpg (room other, wall dense-other-d138): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:395 d_141_10.jpg (room other, wall dense-other-d141): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:396 d_141_11.jpg (room other, wall dense-other-d141): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:411 d_143_03.jpg (room other, wall dense-other-d143): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:412 d_143_05.jpg (room other, wall dense-other-d143): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:413 d_143_06.jpg (room other, wall dense-other-d143): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:414 d_143_07.jpg (room other, wall dense-other-d143): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:415 d_143_09.jpg (room other, wall dense-other-d143): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:416 d_143_10.jpg (room other, wall dense-other-d143): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:417 d_143_11.jpg (room other, wall dense-other-d143): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:419 d_143_14.jpg (room other, wall dense-other-d143): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:421 d_143_17.jpg (room other, wall dense-other-d143): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:423 d_143_19.jpg (room other, wall dense-other-d143): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:424 d_163_01.jpg (room other, wall dense-other-d163): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:425 d_163_02.jpg (room other, wall dense-other-d163): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:426 d_163_03.jpg (room other, wall dense-other-d163): "(not Eco's"
- spines_zZEy10fpq3I_part2.jsonl:7 t_002658.jpg (room other, wall library-ladder-wall-of-volumes): "not Eco's apartment"
- spines_zZEy10fpq3I_part3.jsonl:11 t_003012.jpg (room grand_baroque_library_archival, wall unknown): "not Eco's apartment"
- spines_zZEy10fpq3I_part3.jsonl:12 t_003020.jpg (room grand_baroque_library_archival, wall unknown): "not Eco's apartment"
- spines_zZEy10fpq3I_part3.jsonl:10 s_003020_12.jpg (room grand_baroque_library_archival, wall unknown): "not part of Eco's home"
- spines_zZEy10fpq3I_dense.jsonl:455 d_183_07.jpg (room other, wall dense-other-d183): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:456 d_183_08.jpg (room other, wall dense-other-d183): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:457 d_183_09.jpg (room other, wall dense-other-d183): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:458 d_183_10.jpg (room other, wall dense-other-d183): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:472 d_192_01.jpg (room living, wall dense-salotto-d192): "not Eco's library"
- spines_zZEy10fpq3I_dense.jsonl:491 d_196_13.jpg (room other, wall dense-other-d196): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:512 f_002405.jpg (room other, wall dense-other-t0200): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:514 d_240_02.jpg (room other, wall dense-other-d240): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:515 d_240_03.jpg (room other, wall dense-other-d240): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:516 d_240_04.jpg (room other, wall dense-other-d240): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:517 d_240_05.jpg (room other, wall dense-other-d240): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:518 d_240_06.jpg (room other, wall dense-other-d240): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:519 d_240_07.jpg (room other, wall dense-other-d240): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:520 d_240_08.jpg (room other, wall dense-other-d240): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:522 f_002514.jpg (room bologna-reinstalled, wall dense-bologna-t0209): "not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:523 d_251_01.jpg (room other, wall dense-other-d251): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:524 d_251_02.jpg (room other, wall dense-other-d251): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:525 d_251_03.jpg (room other, wall dense-other-d251): "(not Eco's"
- spines_zZEy10fpq3I_part4.jsonl:85 t_004328.jpg (room archive_stacks, wall stacks_shelf_sonzogno): "distinct from Eco apartment"
- spines_zZEy10fpq3I_dense.jsonl:561 f_002862.jpg (room other, wall dense-other-t0238): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:562 f_002865.jpg (room other, wall dense-other-t0238): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:574 d_276_01.jpg (room other, wall dense-other-d276): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:575 d_276_02.jpg (room other, wall dense-other-d276): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:576 d_276_03.jpg (room other, wall dense-other-d276): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:587 d_287_01.jpg (room other, wall dense-other-d287): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:589 f_003060.jpg (room other, wall dense-other-t0254): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:590 f_003100.jpg (room other, wall dense-other-t0258): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:591 f_003103.jpg (room other, wall dense-other-t0258): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:592 d_295_01.jpg (room other, wall dense-other-d295): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:593 d_295_03.jpg (room other, wall dense-other-d295): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:608 d_300_02.jpg (room other, wall dense-other-d300): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:609 d_300_03.jpg (room other, wall dense-other-d300): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:615 f_003363.jpg (room other, wall dense-other-t0280): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:616 f_003366.jpg (room other, wall dense-other-t0280): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:619 d_319_03.jpg (room other, wall dense-other-d319): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:620 d_319_04.jpg (room other, wall dense-other-d319): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:621 f_003473.jpg (room other, wall dense-other-t0289): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:622 f_003476.jpg (room other, wall dense-other-t0289): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:623 f_003487.jpg (room other, wall dense-other-t0290): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:624 f_003500.jpg (room other, wall dense-other-t0291): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:625 f_003504.jpg (room other, wall dense-other-t0291): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:627 f_003571.jpg (room other, wall dense-other-t0297): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:635 d_348_05.jpg (room other, wall dense-other-d348): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:636 d_348_06.jpg (room other, wall dense-other-d348): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:637 d_348_07.jpg (room other, wall dense-other-d348): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:638 d_348_08.jpg (room other, wall dense-other-d348): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:639 d_348_09.jpg (room other, wall dense-other-d348): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:658 d_352_04.jpg (room corridor, wall dense-corridoio-d352): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:661 d_355_01.jpg (room other, wall dense-other-d355): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:702 d_371_02.jpg (room other, wall dense-other-d371): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:703 d_371_03.jpg (room other, wall dense-other-d371): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:704 d_371_04.jpg (room other, wall dense-other-d371): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:705 d_371_05.jpg (room other, wall dense-other-d371): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:706 d_371_06.jpg (room other, wall dense-other-d371): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:707 d_371_07.jpg (room other, wall dense-other-d371): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:708 d_371_08.jpg (room other, wall dense-other-d371): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:709 d_371_09.jpg (room other, wall dense-other-d371): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:710 f_004012.jpg (room other, wall dense-other-t0334): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:711 f_004033.jpg (room other, wall dense-other-t0336): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:712 f_004036.jpg (room other, wall dense-other-t0336): "(not Eco's"
- spines_zZEy10fpq3I_part7.jsonl:1 t_011308.jpg (room other, wall world-libraries-stock-1): "not Eco's Milan apartment"
- spines_zZEy10fpq3I_part7.jsonl:2 t_011310.jpg (room other, wall world-libraries-stock-1): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:713 f_004397.jpg (room other, wall dense-other-t0366): "not part of Eco's home"
- spines_zZEy10fpq3I_dense.jsonl:714 d_413_01.jpg (room other, wall dense-other-d413): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:715 d_413_02.jpg (room other, wall dense-other-d413): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:716 d_413_03.jpg (room other, wall dense-other-d413): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:717 d_413_04.jpg (room other, wall dense-other-d413): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:718 d_413_05.jpg (room other, wall dense-other-d413): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:719 d_413_06.jpg (room other, wall dense-other-d413): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:720 d_413_07.jpg (room other, wall dense-other-d413): "(not Eco's"
- spines_zZEy10fpq3I_dense.jsonl:721 d_413_08.jpg (room other, wall dense-other-d413): "(not Eco's"

## Walls

| wall_id | room | name | frames | time | titles | unlabelled | excluded |
|---|---|---|---:|---|---:|---:|---|
| Hq66X9f-zgc:living-coffee-table-1 | salotto | Coffee table, living room | 1 | 00:00:34-00:00:34 | 2 | 0 |  |
| Hq66X9f-zgc:corridor-1 | corridoio | Entrance hallway shelf (far) | 3 | 00:04:55-00:04:59 | 0 | 35 |  |
| Hq66X9f-zgc:corridor-2 | corridoio | Corridor shelving, statue/print wall | 2 | 00:05:01-00:05:05 | 0 | 55 |  |
| Hq66X9f-zgc:corridor-3 | corridoio | Corridor shelving | 4 | 00:05:07-00:05:13 | 0 | 115 |  |
| Hq66X9f-zgc:corridor-4 | corridoio | Corridor shelving | 3 | 00:05:15-00:05:19 | 0 | 85 |  |
| Hq66X9f-zgc:corridor-5 | corridoio | Corridor shelving near window | 3 | 00:05:21-00:05:25 | 0 | 75 |  |
| Hq66X9f-zgc:corridor-6 | corridoio | Corridor shelving, doorway ahead | 1 | 00:05:27-00:05:27 | 0 | 30 |  |
| Hq66X9f-zgc:study-entry-1 | studio | Entrance to book-lined room | 1 | 00:05:29-00:05:29 | 0 | 25 |  |
| Hq66X9f-zgc:study-room-1 | studio | Book-lined room, table with piled books | 3 | 00:05:31-00:05:35 | 0 | 100 |  |
| Hq66X9f-zgc:study-room-2 | studio | Shelving beside table stacks | 3 | 00:05:37-00:05:41 | 0 | 60 |  |
| Hq66X9f-zgc:study-room-3 | studio | Shelving, window at corridor end | 2 | 00:05:43-00:05:45 | 0 | 40 |  |
| Hq66X9f-zgc:study-room-4 | studio | Shelving Eco is browsing | 6 | 00:05:47-00:05:57 | 0 | 95 |  |
| Hq66X9f-zgc:study-room-5 | studio | Shelving beside desk area | 1 | 00:05:59-00:05:59 | 0 | 20 |  |
| Hq66X9f-zgc:study-main-1 | studio | Long study, shelving both sides | 2 | 00:06:01-00:06:03 | 0 | 80 |  |
| zj1kwT87ne0:living-coffeetable-1 | salotto | coffee table, stack of Eco books (English editions) | 2 | 00:00:27-00:00:34 | 3 | 0 |  |
| zj1kwT87ne0:corridor-entry-1 | corridoio | corridor entrance shelving, near coat rack and green/red abstract pain | 2 | 00:04:57-00:04:59 | 0 | 66 |  |
| zj1kwT87ne0:corridor-1 | corridoio | corridor shelving, both sides, wide shot | 1 | 00:05:01-00:05:01 | 0 | 50 |  |
| zj1kwT87ne0:corridor-2 | corridoio | corridor shelving, right-hand bay | 7 | 00:05:09-00:05:23 | 0 | 256 |  |
| zj1kwT87ne0:corridor-3 | corridoio | corridor shelving near end window, embossed shelf end-panel | 3 | 00:05:25-00:05:29 | 0 | 91 |  |
| zj1kwT87ne0:rare-room-1 | antichi | large library room, entrance view, floor-to-ceiling shelving on 3 wall | 2 | 00:05:31-00:05:33 | 0 | 99 |  |
| zj1kwT87ne0:rare-room-2 | antichi | large library room, right-hand wall shelving | 3 | 00:05:35-00:05:39 | 0 | 106 |  |
| zj1kwT87ne0:rare-room-3 | antichi | large library room, corridor between shelving units toward window | 5 | 00:05:41-00:05:49 | 0 | 112 |  |
| zj1kwT87ne0:rare-room-4 | antichi | shelving unit Eco approaches directly, near door | 5 | 00:05:51-00:05:59 | 0 | 89 |  |
| zj1kwT87ne0:rare-room-5 | antichi | library room, Eco walking past a long central desk with shelving both  | 1 | 00:06:01-00:06:01 | 0 | 33 |  |
| zj1kwT87ne0:rare-room-6 | antichi | library room, wide view toward far window, shelving all sides | 2 | 00:06:03-00:06:05 | 0 | 93 |  |
| B-M8V0PcCrw:table-closeup-1 | salotto | Coffee table, book held to camera | 1 | 00:00:25-00:00:25 | 1 | 0 |  |
| B-M8V0PcCrw:table-closeup-2 | salotto | Coffee table with coffee cups and books | 2 | 00:00:35-00:00:37 | 2 | 0 |  |
| B-M8V0PcCrw:living-glass-cabinet-1 | antichi | Glass curio cabinet with open manuscript facsimiles | 1 | 00:03:16-00:03:16 | 0 | 2 |  |
| B-M8V0PcCrw:living-desk-stack-1 | salotto | Desk / low table stacked with books, glass cabinet behind | 1 | 00:04:47-00:04:47 | 1 | 6 |  |
| B-M8V0PcCrw:corridor-entry | corridoio | Low shelving units at corridor entrance, waist-height | 2 | 00:05:09-00:05:11 | 0 | 40 |  |
| B-M8V0PcCrw:corridor-gallery-wall | corridoio | Gallery wall of framed prints; coat/hat rack; bookshelf edge at far le | 2 | 00:05:13-00:05:15 | 0 | 12 |  |
| B-M8V0PcCrw:corridor-main-shelf | corridoio | Dense white floor-to-ceiling shelving, main corridor stretch | 7 | 00:05:17-00:05:29 | 0 | 250 |  |
| B-M8V0PcCrw:corridor-main-shelf-2 | corridoio | Shelving, corridor bends toward a window | 6 | 00:05:31-00:05:41 | 0 | 150 |  |
| B-M8V0PcCrw:office-wide-1 | corridoio | Wide shot: office/study room, shelving on both walls, desk with monito | 3 | 00:05:43-00:05:47 | 0 | 115 |  |
| B-M8V0PcCrw:corridor-to-office-1 | corridoio | Shelving continues past a bright window | 6 | 00:05:49-00:05:59 | 0 | 125 |  |
| B-M8V0PcCrw:office-shelf-2 | studio | Study/office room, floor-to-ceiling shelving; some volumes carry a rou | 5 | 00:06:01-00:06:09 | 0 | 145 |  |
| B-M8V0PcCrw:office-shelf-3 | studio | Shelving beside a bright window, mixed pamphlets and bound volumes | 3 | 00:06:11-00:06:15 | 0 | 105 |  |
| iRXEQVTI95k:w1 | antichi | Studiolo cabinet, antique vellum/leather bindings | 24 | 00:00:01-00:01:47 | 2 | 432 |  |
| iRXEQVTI95k:dense-studio-t0000 | studio | Study shelf (dense pass 2026-09-09), shot t0000 at 00:07, no call tag  | 3 | 00:00:07-00:00:11 | 0 | 172 |  |
| iRXEQVTI95k:dense-studio-t0001 | studio | Study shelf (dense pass 2026-09-09), shot t0001 at 00:13, no call tag  | 6 | 00:00:13-00:00:23 | 2 | 118 |  |
| iRXEQVTI95k:dense-vestibolo-t0001 | vestibolo | Vestibule shelf (dense pass 2026-09-09), shot t0001 at 00:15, no call  | 1 | 00:00:15-00:00:15 | 0 | 22 |  |
| iRXEQVTI95k:dense-studio-t0002 | studio | Study shelf (dense pass 2026-09-09), shot t0002 at 00:25, no call tag  | 1 | 00:00:25-00:00:25 | 2 | 6 |  |
| iRXEQVTI95k:w2 | antichi | Studiolo interior, reading desk | 1 | 00:00:26-00:00:26 | 0 | 40 |  |
| iRXEQVTI95k:w3 | antichi | Interview backdrop: 'Sala Lalla Romano' cabinet wall | 18 | 00:00:28-00:01:39 | 0 | 0 |  |
| iRXEQVTI95k:w4 | antichi | Display case: open manuscripts on the reading desk | 15 | 00:00:37-00:01:19 | 8 | 6 |  |
| iRXEQVTI95k:dense-other-t0003 | other | Other library / insert, dense pass 2026-09-09 shot t0003 at 00:41 (not | 1 | 00:00:41-00:00:41 | 0 | 4 | yes |
| iRXEQVTI95k:dense-bologna-t0003 | bologna | Bologna reinstallation 2026 shelf (dense pass 2026-09-09), shot t0003  | 1 | 00:00:42-00:00:42 | 0 | 16 |  |
| iRXEQVTI95k:w5 | antichi | Shelf close-up: 19th-c. novels/history bindings | 4 | 00:00:51-00:00:55 | 3 | 31 |  |
| iRXEQVTI95k:dense-unidentified-t0004 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0004 at 00:51,  | 1 | 00:00:51-00:00:51 | 2 | 5 |  |
| iRXEQVTI95k:dense-other-t0004 | other | Other library / insert, dense pass 2026-09-09 shot t0004 at 00:55 (not | 2 | 00:00:55-00:00:56 | 2 | 13 | yes |
| iRXEQVTI95k:w6 | antichi | Table display: comics and pipes | 1 | 00:00:56-00:00:56 | 1 | 0 |  |
| iRXEQVTI95k:dense-other-t0005 | other | Other library / insert, dense pass 2026-09-09 shot t0005 at 01:01 (not | 2 | 00:01:01-00:01:03 | 0 | 16 | yes |
| iRXEQVTI95k:w8 | antichi | Display-case gallery, wide shot | 2 | 00:01:05-00:01:22 | 0 | 100 |  |
| iRXEQVTI95k:dense-other-t0006 | other | Other library / insert, dense pass 2026-09-09 shot t0006 at 01:19 (not | 1 | 00:01:19-00:01:19 | 0 | 0 | yes |
| iRXEQVTI95k:w9 | antichi | Table display: children's comics and adventure novels | 7 | 00:01:29-00:01:35 | 4 | 9 |  |
| iRXEQVTI95k:dense-other-t0007 | other | Other library / insert, dense pass 2026-09-09 shot t0007 at 01:29 (not | 3 | 00:01:29-00:01:31 | 2 | 15 | yes |
| iRXEQVTI95k:w10 | antichi | Gallery wide shot, visitors among display cases | 1 | 00:01:40-00:01:40 | 0 | 40 |  |
| iRXEQVTI95k:dense-other-t0008 | other | Other library / insert, dense pass 2026-09-09 shot t0008 at 01:42 (not | 4 | 00:01:42-00:01:45 | 0 | 68 | yes |
| iRXEQVTI95k:dense-studio-t0008 | studio | Study shelf (dense pass 2026-09-09), shot t0008 at 01:47, no call tag  | 1 | 00:01:47-00:01:47 | 0 | 88 |  |
| NtPk4irDiM8:w2 | bologna | General stacks (pans/wide shots, 360p; spines not legible) | 64 | 00:00:43-00:02:21 | 0 | 1678 |  |
| NtPk4irDiM8:dense-unidentified-t0003 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0003 at 00:43,  | 2 | 00:00:43-00:00:45 | 0 | 16 |  |
| NtPk4irDiM8:w1 | bologna | Medieval-philosophy shelf (Eco/Ockham/Aquinas) | 6 | 00:00:47-00:00:57 | 7 | 14 |  |
| NtPk4irDiM8:dense-studio-t0003 | studio | Study shelf (dense pass 2026-09-09), shot t0003 at 00:47, no call tag  | 1 | 00:00:47-00:00:47 | 4 | 0 |  |
| NtPk4irDiM8:dense-studio-t0004 | studio | Study shelf (dense pass 2026-09-09), shot t0004 at 00:49, no call tag  | 4 | 00:00:49-00:00:58 | 7 | 61 |  |
| NtPk4irDiM8:dense-other-t0004 | other | Other library / insert, dense pass 2026-09-09 shot t0004 at 00:55 (not | 4 | 00:00:55-00:01:00 | 2 | 104 | yes |
| NtPk4irDiM8:dense-other-t0005 | other | Other library / insert, dense pass 2026-09-09 shot t0005 at 01:00 (not | 5 | 00:01:00-00:01:02 | 0 | 143 | yes |
| NtPk4irDiM8:dense-corridoio-t0005 | corridoio | Corridor shelf (dense pass 2026-09-09), shot t0005 at 01:04, no call t | 1 | 00:01:04-00:01:04 | 0 | 30 |  |
| NtPk4irDiM8:w3 | bologna | Art-book shelf close-up (partial) | 6 | 00:01:04-00:01:07 | 1 | 70 |  |
| NtPk4irDiM8:dense-studio-t0005 | studio | Study shelf (dense pass 2026-09-09), shot t0005 at 01:04, no call tag  | 8 | 00:01:04-00:01:09 | 0 | 184 |  |
| NtPk4irDiM8:dense-unidentified-t0006 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0006 at 01:17,  | 1 | 00:01:17-00:01:17 | 0 | 37 |  |
| NtPk4irDiM8:dense-corridoio-t0006 | corridoio | Corridor shelf (dense pass 2026-09-09), shot t0006 at 01:19, no call t | 2 | 00:01:19-00:01:20 | 0 | 70 |  |
| NtPk4irDiM8:dense-studio-t0006 | studio | Study shelf (dense pass 2026-09-09), shot t0006 at 01:20, no call tag  | 1 | 00:01:20-00:01:20 | 0 | 38 |  |
| NtPk4irDiM8:dense-other-t0006 | other | Other library / insert, dense pass 2026-09-09 shot t0006 at 01:21 (not | 3 | 00:01:21-00:01:23 | 0 | 92 | yes |
| NtPk4irDiM8:dense-other-t0007 | other | Other library / insert, dense pass 2026-09-09 shot t0007 at 01:24 (not | 5 | 00:01:24-00:01:31 | 0 | 149 | yes |
| NtPk4irDiM8:w4 | bologna | Librarian showing an illustrated book (title page/woodcut) | 5 | 00:01:33-00:01:39 | 0 | 75 |  |
| NtPk4irDiM8:dense-studio-t0008 | studio | Study shelf (dense pass 2026-09-09), shot t0008 at 01:47, no call tag  | 1 | 00:01:47-00:01:47 | 1 | 19 | yes |
| NtPk4irDiM8:dense-other-t0008 | other | Other library / insert, dense pass 2026-09-09 shot t0008 at 01:48 (not | 1 | 00:01:48-00:01:48 | 0 | 45 | yes |
| NtPk4irDiM8:dense-corridoio-t0009 | corridoio | Corridor shelf (dense pass 2026-09-09), shot t0009 at 01:49, no call t | 2 | 00:01:49-00:02:00 | 0 | 67 |  |
| NtPk4irDiM8:dense-other-t0009 | other | Other library / insert, dense pass 2026-09-09 shot t0009 at 01:51 (not | 3 | 00:01:51-00:01:55 | 1 | 130 | yes |
| NtPk4irDiM8:dense-corridoio-t0010 | corridoio | Corridor shelf (dense pass 2026-09-09), shot t0010 at 02:01, no call t | 1 | 00:02:01-00:02:01 | 0 | 37 |  |
| NtPk4irDiM8:w5 | bologna | Umberto Eco's own works, foreign editions | 8 | 00:02:04-00:02:27 | 7 | 110 |  |
| NtPk4irDiM8:dense-corridoio-t0011 | corridoio | Corridor shelf (dense pass 2026-09-09), shot t0011 at 02:21, no call t | 1 | 00:02:21-00:02:21 | 0 | 24 |  |
| KZfOaug0mM4:dense-bologna-t0000 | bologna | Bologna reinstallation 2026 shelf (dense pass 2026-09-09), shot t0000  | 7 | 00:00:01-00:00:11 | 0 | 0 |  |
| KZfOaug0mM4:w1 | bologna | Entrance shelf: Eco/medieval-philosophy section | 13 | 00:00:13-00:00:29 | 7 | 67 |  |
| KZfOaug0mM4:dense-vestibolo-t0002 | vestibolo | Vestibule shelf (dense pass 2026-09-09), shot t0002 at 00:31, no call  | 1 | 00:00:31-00:00:31 | 0 | 0 |  |
| KZfOaug0mM4:w2 | bologna | Corridor shelving (Bible/general, orange tags) | 11 | 00:00:33-00:00:49 | 2 | 148 |  |
| KZfOaug0mM4:dense-studio-t0002 | studio | Study shelf (dense pass 2026-09-09), shot t0002 at 00:33, no call tag  | 2 | 00:00:33-00:00:35 | 3 | 83 |  |
| KZfOaug0mM4:dense-studio-t0003 | studio | Study shelf (dense pass 2026-09-09), shot t0003 at 00:37, no call tag  | 3 | 00:00:37-00:00:39 | 0 | 125 |  |
| KZfOaug0mM4:dense-other-t0003 | other | Other library / insert, dense pass 2026-09-09 shot t0003 at 00:41 (not | 3 | 00:00:41-00:00:45 | 0 | 100 | yes |
| KZfOaug0mM4:dense-corridoio-t0004 | corridoio | Corridor shelf (dense pass 2026-09-09), shot t0004 at 00:49, no call t | 1 | 00:00:49-00:00:49 | 0 | 14 |  |
| KZfOaug0mM4:w3 | bologna | Two-story mezzanine hall (wide establishing shots) | 5 | 00:00:51-00:01:49 | 0 | 200 |  |
| KZfOaug0mM4:dense-studio-t0004 | studio | Study shelf (dense pass 2026-09-09), shot t0004 at 00:51, no call tag  | 4 | 00:00:51-00:00:57 | 1 | 151 |  |
| KZfOaug0mM4:dense-antichi-t0004 | antichi | Rare-book room shelf (dense pass 2026-09-09), shot t0004 at 00:58, no  | 2 | 00:00:58-00:00:59 | 0 | 2 |  |
| KZfOaug0mM4:dense-other-t0005 | other | Other library / insert, dense pass 2026-09-09 shot t0005 at 01:01 (not | 6 | 00:01:01-00:01:09 | 1 | 2 | yes |
| KZfOaug0mM4:w4 | bologna | Art-history monograph shelving | 3 | 00:01:11-00:01:15 | 42 | 25 |  |
| KZfOaug0mM4:dense-studio-t0005 | studio | Study shelf (dense pass 2026-09-09), shot t0005 at 01:11, no call tag  | 1 | 00:01:11-00:01:11 | 19 | 29 |  |
| KZfOaug0mM4:dense-studio-t0006 | studio | Study shelf (dense pass 2026-09-09), shot t0006 at 01:13, no call tag  | 3 | 00:01:13-00:01:17 | 36 | 36 |  |
| KZfOaug0mM4:w5 | bologna | Rector's reception-room shelf (Milton/Dante/Hölderlin) | 14 | 00:01:19-00:02:13 | 4 | 10 |  |
| KZfOaug0mM4:dense-corridor-02 | corridoio | Bookcase 'A', bays 2-2 (dense pass 2026-09-09, placed by shelf tag in  | 10 | 00:01:29-00:01:49 | 6 | 254 |  |
| KZfOaug0mM4:w6 | bologna | Literary-studies shelf: James Joyce section | 2 | 00:01:43-00:01:45 | 6 | 18 |  |
| KZfOaug0mM4:w7 | bologna | Shelf location-tag close-ups (Armadio A) | 7 | 00:01:54-00:02:11 | 2 | 25 |  |
| KZfOaug0mM4:dense-other-t0009 | other | Other library / insert, dense pass 2026-09-09 shot t0009 at 01:54 (not | 1 | 00:01:54-00:01:54 | 2 | 34 | yes |
| KZfOaug0mM4:dense-other-t0010 | other | Other library / insert, dense pass 2026-09-09 shot t0010 at 02:01 (not | 3 | 00:02:01-00:02:03 | 2 | 71 | yes |
| KZfOaug0mM4:dense-unidentified-t0010 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0010 at 02:07,  | 3 | 00:02:07-00:02:11 | 0 | 19 |  |
| FeIUY9EhZgI:unlabelled | other | Cinema Guild distributor logo card | 56 | 00:00:01-00:02:07 | 0 | 35 | yes |
| FeIUY9EhZgI:W1 | corridoio | corridor, both sides, Eco walking away from camera (B&W archival shot) | 7 | 00:00:03-00:00:09 | 0 | 146 |  |
| FeIUY9EhZgI:dense-unidentified-t0000 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0000 at 00:03,  | 1 | 00:00:03-00:00:03 | 0 | 0 |  |
| FeIUY9EhZgI:W2 | studio | study, floor-to-ceiling shelves with rolling ladder (B&W archival shot | 11 | 00:00:07-00:00:23 | 0 | 240 |  |
| FeIUY9EhZgI:dense-antichi-t0000 | antichi | Rare-book room shelf (dense pass 2026-09-09), shot t0000 at 00:10, no  | 1 | 00:00:10-00:00:10 | 0 | 69 |  |
| FeIUY9EhZgI:dense-pile-t0000 | antichi | Pile of books (dense pass 2026-09-09), Rare-book room, shot t0000 at 0 | 1 | 00:00:11-00:00:11 | 0 | 29 |  |
| FeIUY9EhZgI:dense-antichi-t0001 | antichi | Rare-book room shelf (dense pass 2026-09-09), shot t0001 at 00:13, no  | 2 | 00:00:13-00:00:24 | 0 | 94 |  |
| FeIUY9EhZgI:W3 | other | institutional archive shelving with alphabetical range tags (title-seq | 4 | 00:00:18-00:00:23 | 0 | 30 | yes |
| FeIUY9EhZgI:W4 | studio | Eco's study, Bompiani "Il Pensiero Occidentale" philosophy shelf with  | 18 | 00:00:37-00:01:11 | 23 | 154 |  |
| FeIUY9EhZgI:W5 | antichi | rare-book shelf, Athanasius Kircher volumes (archive/vault setting) | 4 | 00:00:51-00:00:54 | 7 | 47 |  |
| FeIUY9EhZgI:W6 | unknown | archive shelf, German legal reference set (Aufstieg und Niedergang der | 1 | 00:00:57-00:00:57 | 2 | 2 |  |
| FeIUY9EhZgI:dense-corridoio-t0005 | corridoio | Corridor shelf (dense pass 2026-09-09), shot t0005 at 01:01, no call t | 3 | 00:01:01-00:01:05 | 0 | 180 |  |
| FeIUY9EhZgI:W7 | salotto | convex mirror reflecting a wood-paneled room with glass-fronted bookca | 1 | 00:01:11-00:01:11 | 0 | 0 |  |
| FeIUY9EhZgI:dense-unidentified-t0005 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0005 at 01:11,  | 1 | 00:01:11-00:01:11 | 0 | 0 |  |
| FeIUY9EhZgI:dense-unidentified-t0006 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0006 at 01:22,  | 1 | 00:01:22-00:01:22 | 0 | 0 |  |
| FeIUY9EhZgI:dense-other-t0007 | other | Other library / insert, dense pass 2026-09-09 shot t0007 at 01:25 (not | 5 | 00:01:25-00:01:36 | 0 | 258 | yes |
| FeIUY9EhZgI:dense-corridoio-t0007 | corridoio | Corridor shelf (dense pass 2026-09-09), shot t0007 at 01:27, no call t | 2 | 00:01:27-00:01:29 | 0 | 54 |  |
| FeIUY9EhZgI:dense-other-t0008 | other | Other library / insert, dense pass 2026-09-09 shot t0008 at 01:37 (not | 9 | 00:01:37-00:01:47 | 0 | 1090 | yes |
| bcK8rOkcb3k:unlabelled | other | Festa del Cinema di Roma 2022 logo card | 56 | 00:00:01-00:02:07 | 0 | 35 | yes |
| bcK8rOkcb3k:W1 | vestibolo | vestibule, Eco walking away from camera past framed art and shelves (B | 3 | 00:00:03-00:00:05 | 0 | 25 |  |
| bcK8rOkcb3k:dense-unidentified-t0000 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0000 at 00:03,  | 1 | 00:00:03-00:00:03 | 0 | 0 |  |
| bcK8rOkcb3k:W3 | studio | study, floor-to-ceiling shelves with rolling ladder (B&W archival shot | 18 | 00:00:04-00:01:09 | 0 | 399 |  |
| bcK8rOkcb3k:W2 | corridoio | corridor, shelves both sides (B&W archival shot) | 2 | 00:00:07-00:00:09 | 0 | 92 |  |
| bcK8rOkcb3k:W4 | other | institutional archive shelving (title-sequence shot) | 4 | 00:00:18-00:00:23 | 0 | 30 | yes |
| bcK8rOkcb3k:dense-unidentified-t0001 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0001 at 00:19,  | 2 | 00:00:19-00:00:21 | 0 | 40 |  |
| bcK8rOkcb3k:dense-antichi-t0001 | antichi | Rare-book room shelf (dense pass 2026-09-09), shot t0001 at 00:23, no  | 1 | 00:00:23-00:00:23 | 0 | 55 |  |
| bcK8rOkcb3k:W5 | studio | Eco's study, Bompiani "Il Pensiero Occidentale" philosophy shelf with  | 14 | 00:00:37-00:00:51 | 22 | 117 |  |
| bcK8rOkcb3k:W6 | antichi | rare-book shelf, Athanasius Kircher volumes (archive/vault setting) | 2 | 00:00:51-00:00:53 | 6 | 0 |  |
| bcK8rOkcb3k:dense-corridor2-G | corridoio | Bookcase 'G' (dense pass 2026-09-09, placed by shelf tag in the same s | 11 | 00:00:53-00:01:15 | 5 | 360 |  |
| bcK8rOkcb3k:W7 | unknown | archive shelf, German legal reference set (Aufstieg und Niedergang der | 1 | 00:00:57-00:00:57 | 2 | 2 |  |
| bcK8rOkcb3k:W8 | antichi | convex mirror reflecting a wood-paneled room with a glass-fronted book | 2 | 00:01:15-00:01:17 | 0 | 0 |  |
| bcK8rOkcb3k:dense-salotto-t0006 | salotto | Living room shelf (dense pass 2026-09-09), shot t0006 at 01:17, no cal | 1 | 00:01:17-00:01:17 | 0 | 10 |  |
| bcK8rOkcb3k:dense-corridoio-t0007 | corridoio | Corridor shelf (dense pass 2026-09-09), shot t0007 at 01:25, no call t | 3 | 00:01:25-00:01:29 | 0 | 301 |  |
| bcK8rOkcb3k:dense-other-t0007 | other | Other library / insert, dense pass 2026-09-09 shot t0007 at 01:31 (not | 5 | 00:01:31-00:01:35 | 0 | 470 | yes |
| bcK8rOkcb3k:dense-other-t0008 | other | Other library / insert, dense pass 2026-09-09 shot t0008 at 01:37 (not | 8 | 00:01:37-00:01:47 | 0 | 910 | yes |
| bcK8rOkcb3k:dense-other-t0009 | other | Other library / insert, dense pass 2026-09-09 shot t0009 at 01:49 (not | 1 | 00:01:49-00:01:49 | 0 | 160 | yes |
| ygvl-_gtAP8:W0 | other | extreme macro of aged vellum book spine (title sequence) | 8 | 00:00:01-00:00:13 | 0 | 0 | yes |
| ygvl-_gtAP8:dense-unidentified-t0000 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0000 at 00:01,  | 7 | 00:00:01-00:00:11 | 1 | 17 |  |
| ygvl-_gtAP8:dense-unidentified-t0001 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0001 at 00:13,  | 5 | 00:00:13-00:00:19 | 2 | 3 |  |
| ygvl-_gtAP8:W1 | antichi | rare-book shelf, handwritten ink spine labels on vellum bindings | 4 | 00:00:13-00:00:19 | 2 | 0 |  |
| ygvl-_gtAP8:unlabelled | other | open book, Kircher's Ars Magna Lucis et Umbrae title page and plates | 52 | 00:00:20-00:03:51 | 3 | 89 |  |
| ygvl-_gtAP8:dense-pile-t0001 | studio | Pile of books (dense pass 2026-09-09), Study, shot t0001 at 00:20 | 3 | 00:00:20-00:00:23 | 2 | 3 |  |
| ygvl-_gtAP8:dense-pile-t0002 | unknown | Pile of books (dense pass 2026-09-09), Unidentified room, shot t0002 a | 1 | 00:00:25-00:00:25 | 1 | 2 |  |
| ygvl-_gtAP8:W2 | antichi | rare-book shelf, Fludd / Kircher / Kabbalah esoterica | 19 | 00:00:27-00:00:45 | 20 | 42 |  |
| ygvl-_gtAP8:dense-bologna-t0005 | bologna | Bologna reinstallation 2026 shelf (dense pass 2026-09-09), shot t0005  | 4 | 00:01:02-00:01:09 | 1 | 114 |  |
| ygvl-_gtAP8:dense-studio-t0005 | studio | Study shelf (dense pass 2026-09-09), shot t0005 at 01:05, no call tag  | 1 | 00:01:05-00:01:05 | 0 | 10 |  |
| ygvl-_gtAP8:W3b | other | institutional archive shelving, deep oblique tracking shot | 11 | 00:01:06-00:01:25 | 1 | 30 | yes |
| ygvl-_gtAP8:dense-unidentified-t0005 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0005 at 01:11,  | 1 | 00:01:11-00:01:11 | 0 | 44 |  |
| ygvl-_gtAP8:dense-unidentified-t0006 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0006 at 01:13,  | 3 | 00:01:13-00:01:17 | 0 | 126 |  |
| ygvl-_gtAP8:dense-study-Q | studio | Bookcase 'Q' (dense pass 2026-09-09, placed by shelf tag in the same s | 12 | 00:01:19-00:01:45 | 21 | 291 |  |
| ygvl-_gtAP8:W3 | other | institutional archive shelf of Umberto Eco's own works in translation  | 6 | 00:01:29-00:01:39 | 23 | 14 | yes |
| ygvl-_gtAP8:W4 | other | archive shelf, Eco's hand reaching for a book | 2 | 00:01:45-00:01:45 | 0 | 2 | yes |
| ygvl-_gtAP8:dense-other-t0010 | other | Other library / insert, dense pass 2026-09-09 shot t0010 at 02:09 (not | 2 | 00:02:09-00:02:11 | 1 | 1 | yes |
| ygvl-_gtAP8:dense-other-t0011 | other | Other library / insert, dense pass 2026-09-09 shot t0011 at 02:13 (not | 1 | 00:02:13-00:02:13 | 1 | 0 | yes |
| ygvl-_gtAP8:W5 | other | grand historic library, wood-panelled corridor with checkerboard marbl | 7 | 00:02:37-00:02:51 | 0 | 0 | yes |
| ygvl-_gtAP8:dense-corridoio-t0014 | corridoio | Corridor shelf (dense pass 2026-09-09), shot t0014 at 02:49, no call t | 1 | 00:02:49-00:02:49 | 0 | 150 |  |
| ygvl-_gtAP8:dense-other-t0014 | other | Other library / insert, dense pass 2026-09-09 shot t0014 at 02:51 (not | 1 | 00:02:51-00:02:51 | 0 | 150 | yes |
| ygvl-_gtAP8:W6 | other | grand historic library reading room, reading stands and glass-fronted  | 17 | 00:03:07-00:03:47 | 0 | 0 | yes |
| ygvl-_gtAP8:dense-corridoio-t0015 | corridoio | Corridor shelf (dense pass 2026-09-09), shot t0015 at 03:07, no call t | 1 | 00:03:07-00:03:07 | 0 | 150 |  |
| ygvl-_gtAP8:dense-other-t0015 | other | Other library / insert, dense pass 2026-09-09 shot t0015 at 03:09 (not | 2 | 00:03:09-00:03:11 | 0 | 300 | yes |
| ygvl-_gtAP8:dense-other-t0016 | other | Other library / insert, dense pass 2026-09-09 shot t0016 at 03:13 (not | 2 | 00:03:13-00:03:15 | 0 | 400 | yes |
| ygvl-_gtAP8:dense-other-t0017 | other | Other library / insert, dense pass 2026-09-09 shot t0017 at 03:26 (not | 6 | 00:03:26-00:03:35 | 0 | 438 | yes |
| ygvl-_gtAP8:dense-bologna-t0018 | bologna | Bologna reinstallation 2026 shelf (dense pass 2026-09-09), shot t0018  | 6 | 00:03:37-00:03:47 | 0 | 910 |  |
| M8IWTOFNlOc:M8IWTOFNlOc_W2 | studio | Writing desk with pigeonhole/grid shelving | 21 | 00:00:10-00:01:25 | 0 | 115 |  |
| M8IWTOFNlOc:dense-unidentified-t0001 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0001 at 00:15,  | 1 | 00:00:15-00:00:15 | 0 | 0 |  |
| M8IWTOFNlOc:M8IWTOFNlOc_W1 | antichi | Glass display cabinet with illuminated manuscripts (main interview bac | 424 | 00:00:17-00:23:45 | 2 | 6 |  |
| M8IWTOFNlOc:dense-pile-t0005 | studio | Pile of books (dense pass 2026-09-09), Study, shot t0005 at 01:11 | 6 | 00:01:11-00:01:23 | 2 | 71 |  |
| M8IWTOFNlOc:M8IWTOFNlOc_W5 | studio | Bookshelf close-up and desk book-stack ('my books' segment) | 19 | 00:23:23-00:23:35 | 14 | 88 |  |
| M8IWTOFNlOc:M8IWTOFNlOc_W4 | studio | Own-works library wall with rolling ladder | 23 | 00:24:02-00:24:21 | 11 | 264 |  |
| M8IWTOFNlOc:dense-unidentified-t0120 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0120 at 24:02,  | 2 | 00:24:02-00:24:03 | 0 | 45 |  |
| rMSOvDAyH5c:rMSOvDAyH5c_W1 | antichi | Glass display cabinet with illuminated manuscripts | 16 | 00:00:05-00:01:17 | 0 | 32 |  |
| zZEy10fpq3I:dense-unidentified-d004 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot d004 at 00:24, n | 1 | 00:00:24-00:00:24 | 0 | 0 |  |
| zZEy10fpq3I:dense-corridoio-d004 | corridoio | Corridor shelf (dense pass 2026-09-09), shot d004 at 00:54, no call ta | 6 | 00:00:54-00:01:36 | 0 | 90 |  |
| zZEy10fpq3I:dense-studio-d004 | studio | Study shelf (dense pass 2026-09-09), shot d004 at 01:29, no call tag p | 4 | 00:01:29-00:01:54 | 0 | 106 |  |
| zZEy10fpq3I:dense-antichi-d004 | antichi | Rare-book room shelf (dense pass 2026-09-09), shot d004 at 02:09, no c | 2 | 00:02:09-00:02:28 | 0 | 0 |  |
| zZEy10fpq3I:dense-other-d004 | other | Other library / insert, dense pass 2026-09-09 shot d004 at 02:40 (not  | 2 | 00:02:40-00:02:45 | 0 | 0 | yes |
| zZEy10fpq3I:dense-salotto-t0019 | salotto | Living room shelf (dense pass 2026-09-09), shot t0019 at 03:52, no cal | 2 | 00:03:52-00:03:56 | 2 | 0 |  |
| zZEy10fpq3I:dense-salotto-t0020 | salotto | Living room shelf (dense pass 2026-09-09), shot t0020 at 04:05, no cal | 3 | 00:04:05-00:04:12 | 1 | 28 |  |
| zZEy10fpq3I:dense-salotto-t0022 | salotto | Living room shelf (dense pass 2026-09-09), shot t0022 at 04:28, no cal | 2 | 00:04:28-00:04:33 | 0 | 14 |  |
| zZEy10fpq3I:dense-salotto-t0023 | salotto | Living room shelf (dense pass 2026-09-09), shot t0023 at 04:38, no cal | 1 | 00:04:38-00:04:38 | 0 | 0 |  |
| zZEy10fpq3I:dense-corridoio-t0026 | corridoio | Corridor shelf (dense pass 2026-09-09), shot t0026 at 05:22, no call t | 1 | 00:05:22-00:05:22 | 1 | 42 |  |
| zZEy10fpq3I:dense-bologna-d043 | bologna | Bologna reinstallation 2026 shelf (dense pass 2026-09-09), shot d043 a | 1 | 00:05:22-00:05:22 | 8 | 102 |  |
| zZEy10fpq3I:study-labeled-sections | studio | modern white shelving, sections labelled by author/category (Eco's wor | 6 | 00:05:23-00:05:39 | 8 | 51 |  |
| zZEy10fpq3I:dense-other-d043 | other | Other library / insert, dense pass 2026-09-09 shot d043 at 05:29 (not  | 1 | 00:05:29-00:05:29 | 5 | 28 | yes |
| zZEy10fpq3I:dense-other-t0028 | other | Other library / insert, dense pass 2026-09-09 shot t0028 at 05:42 (not | 1 | 00:05:42-00:05:42 | 0 | 29 | yes |
| zZEy10fpq3I:dense-other-t0029 | other | Other library / insert, dense pass 2026-09-09 shot t0029 at 05:49 (not | 1 | 00:05:49-00:05:49 | 0 | 6 | yes |
| zZEy10fpq3I:dense-bologna-d046 | bologna | Bologna reinstallation 2026 shelf (dense pass 2026-09-09), shot d046 a | 1 | 00:05:52-00:05:52 | 0 | 6 |  |
| zZEy10fpq3I:dense-other-d046 | other | Other library / insert, dense pass 2026-09-09 shot d046 at 05:55 (not  | 1 | 00:05:55-00:05:55 | 0 | 5 | yes |
| zZEy10fpq3I:rare-hermetica-shelf | antichi | open wooden shelving, 17th-18th c. leather/vellum-bound occult & antiq | 23 | 00:05:58-00:08:35 | 27 | 162 |  |
| zZEy10fpq3I:dense-salotto-d046 | salotto | Living room shelf (dense pass 2026-09-09), shot d046 at 06:00, no call | 1 | 00:06:00-00:06:00 | 0 | 8 |  |
| zZEy10fpq3I:dense-unidentified-d046 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot d046 at 06:15, n | 3 | 00:06:15-00:06:18 | 0 | 18 |  |
| zZEy10fpq3I:dense-studio-d046 | studio | Study shelf (dense pass 2026-09-09), shot d046 at 06:21, no call tag p | 2 | 00:06:21-00:06:36 | 0 | 112 |  |
| zZEy10fpq3I:dense-other-t0033 | other | Other library / insert, dense pass 2026-09-09 shot t0033 at 06:47 (not | 1 | 00:06:47-00:06:47 | 0 | 1 | yes |
| zZEy10fpq3I:dense-other-t0034 | other | Other library / insert, dense pass 2026-09-09 shot t0034 at 06:51 (not | 1 | 00:06:51-00:06:51 | 0 | 1 | yes |
| zZEy10fpq3I:dense-studio-d048 | studio | Study shelf (dense pass 2026-09-09), shot d048 at 06:52, no call tag p | 4 | 00:06:52-00:06:57 | 11 | 124 |  |
| zZEy10fpq3I:dense-corridoio-d048 | corridoio | Corridor shelf (dense pass 2026-09-09), shot d048 at 06:59, no call ta | 2 | 00:06:59-00:06:59 | 0 | 17 |  |
| zZEy10fpq3I:dense-corridoio-t0034 | corridoio | Corridor shelf (dense pass 2026-09-09), shot t0034 at 06:59, no call t | 1 | 00:06:59-00:06:59 | 0 | 10 |  |
| zZEy10fpq3I:dense-bologna-d050 | bologna | Bologna reinstallation 2026 shelf (dense pass 2026-09-09), shot d050 a | 4 | 00:07:03-00:07:08 | 7 | 85 |  |
| zZEy10fpq3I:rare-glass-cabinet-table | antichi | glass-fronted wooden bookcase and adjoining table, rare/antiquarian ro | 5 | 00:07:04-00:07:12 | 2 | 29 |  |
| zZEy10fpq3I:dense-studio-d050 | studio | Study shelf (dense pass 2026-09-09), shot d050 at 07:10, no call tag p | 1 | 00:07:10-00:07:10 | 0 | 3 |  |
| zZEy10fpq3I:dense-unidentified-d050 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot d050 at 07:11, n | 1 | 00:07:11-00:07:11 | 0 | 3 |  |
| zZEy10fpq3I:dense-unidentified-d051 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot d051 at 07:13, n | 2 | 00:07:13-00:07:13 | 0 | 0 |  |
| zZEy10fpq3I:dense-unidentified-d052 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot d052 at 07:13, n | 4 | 00:07:13-00:07:19 | 0 | 0 |  |
| zZEy10fpq3I:dense-unidentified-d053 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot d053 at 07:19, n | 1 | 00:07:19-00:07:19 | 0 | 0 |  |
| zZEy10fpq3I:dense-antichi-d053 | antichi | Rare-book room shelf (dense pass 2026-09-09), shot d053 at 07:20, no c | 2 | 00:07:20-00:07:21 | 3 | 19 |  |
| zZEy10fpq3I:dense-antichi-d054 | antichi | Rare-book room shelf (dense pass 2026-09-09), shot d054 at 07:20, no c | 5 | 00:07:20-00:07:25 | 4 | 38 |  |
| zZEy10fpq3I:dense-studio-d054 | studio | Study shelf (dense pass 2026-09-09), shot d054 at 07:28, no call tag p | 1 | 00:07:28-00:07:28 | 0 | 0 |  |
| zZEy10fpq3I:dense-unidentified-d055 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot d055 at 07:28, n | 3 | 00:07:28-00:07:31 | 0 | 0 |  |
| zZEy10fpq3I:dense-antichi-d055 | antichi | Rare-book room shelf (dense pass 2026-09-09), shot d055 at 07:31, no c | 2 | 00:07:31-00:07:32 | 2 | 17 |  |
| zZEy10fpq3I:dense-antichi-d056 | antichi | Rare-book room shelf (dense pass 2026-09-09), shot d056 at 07:31, no c | 1 | 00:07:31-00:07:31 | 2 | 14 |  |
| zZEy10fpq3I:dense-unidentified-d056 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot d056 at 07:32, n | 1 | 00:07:32-00:07:32 | 0 | 0 |  |
| zZEy10fpq3I:dense-studio-d056 | studio | Study shelf (dense pass 2026-09-09), shot d056 at 07:34, no call tag p | 3 | 00:07:34-00:07:35 | 0 | 19 |  |
| zZEy10fpq3I:dense-studio-d057 | studio | Study shelf (dense pass 2026-09-09), shot d057 at 07:35, no call tag p | 3 | 00:07:35-00:07:36 | 0 | 14 |  |
| zZEy10fpq3I:dense-studio-d058 | studio | Study shelf (dense pass 2026-09-09), shot d058 at 07:36, no call tag p | 4 | 00:07:36-00:07:39 | 0 | 16 |  |
| zZEy10fpq3I:dense-pile-d058 | studio | Pile of books (dense pass 2026-09-09), Study, shot d058 at 07:40 | 5 | 00:07:40-00:07:46 | 0 | 62 |  |
| zZEy10fpq3I:dense-other-d058 | other | Other library / insert, dense pass 2026-09-09 shot d058 at 07:42 (not  | 2 | 00:07:42-00:07:43 | 0 | 0 | yes |
| zZEy10fpq3I:rare-manuscript-table | antichi | table with a row of vellum-bound folios, rare/antiquarian room | 6 | 00:07:45-00:08:09 | 2 | 16 |  |
| zZEy10fpq3I:dense-other-d059 | other | Other library / insert, dense pass 2026-09-09 shot d059 at 07:46 (not  | 2 | 00:07:46-00:07:48 | 0 | 1 | yes |
| zZEy10fpq3I:dense-unidentified-d059 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot d059 at 07:47, n | 1 | 00:07:47-00:07:47 | 0 | 0 |  |
| zZEy10fpq3I:dense-other-d060 | other | Other library / insert, dense pass 2026-09-09 shot d060 at 07:47 (not  | 1 | 00:07:47-00:07:47 | 0 | 0 | yes |
| zZEy10fpq3I:dense-unidentified-d061 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot d061 at 07:49, n | 15 | 00:07:49-00:08:04 | 1 | 32 |  |
| zZEy10fpq3I:dense-unidentified-d062 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot d062 at 08:04, n | 7 | 00:08:04-00:08:11 | 3 | 5 |  |
| zZEy10fpq3I:dense-vest-B | vestibolo | Bookcase 'B' (dense pass 2026-09-09, placed by shelf tag in the same s | 17 | 00:08:11-00:08:36 | 3 | 55 |  |
| zZEy10fpq3I:rare-kircher-book | antichi | open folio on a desk/table, rare/antiquarian room | 1 | 00:08:13-00:08:13 | 1 | 0 |  |
| zZEy10fpq3I:dense-other-t0043 | other | Other library / insert, dense pass 2026-09-09 shot t0043 at 08:39 (not | 2 | 00:08:39-00:08:45 | 3 | 24 | yes |
| zZEy10fpq3I:dense-other-d066 | other | Other library / insert, dense pass 2026-09-09 shot d066 at 08:57 (not  | 7 | 00:08:57-00:09:07 | 1 | 147 | yes |
| zZEy10fpq3I:study-general-shelves | studio | modern white shelving, mixed Italian paperbacks/hardbacks | 4 | 00:09:05-00:09:13 | 0 | 59 |  |
| zZEy10fpq3I:dense-study-Q | studio | Bookcase 'Q' (dense pass 2026-09-09, placed by shelf tag in the same s | 8 | 00:09:09-00:09:19 | 1 | 161 |  |
| zZEy10fpq3I:study-eco-translations-wall | studio | shelf bay Q4/Q5, foreign-language editions of Umberto Eco's own books | 18 | 00:09:20-00:09:40 | 39 | 162 |  |
| zZEy10fpq3I:dense-antichi-d071 | antichi | Rare-book room shelf (dense pass 2026-09-09), shot d071 at 09:43, no c | 1 | 00:09:43-00:09:43 | 0 | 0 |  |
| zZEy10fpq3I:dense-antichi-d072 | antichi | Rare-book room shelf (dense pass 2026-09-09), shot d072 at 09:43, no c | 2 | 00:09:43-00:09:46 | 0 | 0 |  |
| zZEy10fpq3I:dense-other-d072 | other | Other library / insert, dense pass 2026-09-09 shot d072 at 09:50 (not  | 8 | 00:09:50-00:10:01 | 0 | 0 | yes |
| zZEy10fpq3I:dense-unidentified-d072 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot d072 at 10:00, n | 1 | 00:10:00-00:10:00 | 0 | 0 |  |
| zZEy10fpq3I:dense-other-d073 | other | Other library / insert, dense pass 2026-09-09 shot d073 at 10:00 (not  | 5 | 00:10:00-00:10:05 | 1 | 0 | yes |
| zZEy10fpq3I:dense-studio-d074 | studio | Study shelf (dense pass 2026-09-09), shot d074 at 10:06, no call tag p | 7 | 00:10:06-00:10:26 | 0 | 3 |  |
| zZEy10fpq3I:dense-studio-d073 | studio | Study shelf (dense pass 2026-09-09), shot d073 at 10:07, no call tag p | 1 | 00:10:07-00:10:07 | 0 | 5 |  |
| zZEy10fpq3I:dense-corridoio-d074 | corridoio | Corridor shelf (dense pass 2026-09-09), shot d074 at 10:28, no call ta | 2 | 00:10:28-00:10:29 | 0 | 20 |  |
| zZEy10fpq3I:dense-salotto-t0056 | salotto | Living room shelf (dense pass 2026-09-09), shot t0056 at 11:14, no cal | 1 | 00:11:14-00:11:14 | 0 | 0 |  |
| zZEy10fpq3I:dense-studio-t0063 | studio | Study shelf (dense pass 2026-09-09), shot t0063 at 12:41, no call tag  | 2 | 00:12:41-00:12:48 | 1 | 1 |  |
| zZEy10fpq3I:dense-study-L1-4 | studio | Bookcase 'L', bays 1-4 (dense pass 2026-09-09, placed by shelf tag in  | 7 | 00:13:03-00:13:15 | 3 | 192 |  |
| zZEy10fpq3I:fondazione-archive-1 | other | Fondazione Umberto Eco archive room, modular shelving (visible unit la | 2 | 00:13:07-00:13:09 | 2 | 15 | yes |
| zZEy10fpq3I:dense-study-Oa | studio | Bookcase 'Oa' (dense pass 2026-09-09, placed by shelf tag in the same  | 6 | 00:13:21-00:13:36 | 4 | 42 |  |
| zZEy10fpq3I:dense-unidentified-d091 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot d091 at 13:47, n | 2 | 00:13:47-00:13:47 | 1 | 0 |  |
| zZEy10fpq3I:dense-unidentified-t0068 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0068 at 13:48,  | 1 | 00:13:48-00:13:48 | 1 | 0 |  |
| zZEy10fpq3I:dense-salotto-d093 | salotto | Living room shelf (dense pass 2026-09-09), shot d093 at 13:50, no call | 1 | 00:13:50-00:13:50 | 0 | 17 |  |
| zZEy10fpq3I:dense-studio-d093 | studio | Study shelf (dense pass 2026-09-09), shot d093 at 13:55, no call tag p | 2 | 00:13:55-00:13:56 | 0 | 26 |  |
| zZEy10fpq3I:dense-antichi-d094 | antichi | Rare-book room shelf (dense pass 2026-09-09), shot d094 at 13:56, no c | 4 | 00:13:56-00:13:59 | 0 | 67 |  |
| zZEy10fpq3I:dense-studio-d094 | studio | Study shelf (dense pass 2026-09-09), shot d094 at 14:00, no call tag p | 3 | 00:14:00-00:14:02 | 0 | 23 |  |
| zZEy10fpq3I:dense-studio-d096 | studio | Study shelf (dense pass 2026-09-09), shot d096 at 14:04, no call tag p | 1 | 00:14:04-00:14:04 | 0 | 1 |  |
| zZEy10fpq3I:dense-salotto-d096 | salotto | Living room shelf (dense pass 2026-09-09), shot d096 at 14:06, no call | 2 | 00:14:06-00:14:06 | 0 | 6 |  |
| zZEy10fpq3I:dense-antichi-d096 | antichi | Rare-book room shelf (dense pass 2026-09-09), shot d096 at 14:07, no c | 2 | 00:14:07-00:14:08 | 0 | 8 |  |
| zZEy10fpq3I:dense-antichi-d097 | antichi | Rare-book room shelf (dense pass 2026-09-09), shot d097 at 14:07, no c | 2 | 00:14:07-00:14:08 | 0 | 8 |  |
| zZEy10fpq3I:dense-unidentified-d097 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot d097 at 14:10, n | 2 | 00:14:10-00:14:12 | 0 | 2 |  |
| zZEy10fpq3I:dense-studio-d097 | studio | Study shelf (dense pass 2026-09-09), shot d097 at 14:13, no call tag p | 5 | 00:14:13-00:14:17 | 0 | 48 |  |
| zZEy10fpq3I:dense-studio-d098 | studio | Study shelf (dense pass 2026-09-09), shot d098 at 14:17, no call tag p | 2 | 00:14:17-00:14:18 | 1 | 19 |  |
| zZEy10fpq3I:dense-antichi-d098 | antichi | Rare-book room shelf (dense pass 2026-09-09), shot d098 at 14:18, no c | 1 | 00:14:18-00:14:18 | 1 | 15 |  |
| zZEy10fpq3I:dense-studio-d099 | studio | Study shelf (dense pass 2026-09-09), shot d099 at 14:18, no call tag p | 12 | 00:14:18-00:14:35 | 1 | 103 |  |
| zZEy10fpq3I:dense-corridoio-d099 | corridoio | Corridor shelf (dense pass 2026-09-09), shot d099 at 14:23, no call ta | 1 | 00:14:23-00:14:23 | 0 | 5 |  |
| zZEy10fpq3I:rare-01 | antichi | Rare-book room (Stanza degli antichi), table close-up of an open volum | 1 | 00:14:35-00:14:35 | 1 | 0 |  |
| zZEy10fpq3I:dense-studio-t0073 | studio | Study shelf (dense pass 2026-09-09), shot t0073 at 14:39, no call tag  | 1 | 00:14:39-00:14:39 | 0 | 3 |  |
| zZEy10fpq3I:dense-studio-d101 | studio | Study shelf (dense pass 2026-09-09), shot d101 at 14:42, no call tag p | 3 | 00:14:42-00:14:46 | 0 | 36 |  |
| zZEy10fpq3I:dense-studio-d102 | studio | Study shelf (dense pass 2026-09-09), shot d102 at 14:47, no call tag p | 2 | 00:14:47-00:14:49 | 0 | 18 |  |
| zZEy10fpq3I:dense-studio-d103 | studio | Study shelf (dense pass 2026-09-09), shot d103 at 14:49, no call tag p | 3 | 00:14:49-00:14:50 | 0 | 40 |  |
| zZEy10fpq3I:dense-studio-d104 | studio | Study shelf (dense pass 2026-09-09), shot d104 at 14:50, no call tag p | 3 | 00:14:50-00:14:51 | 0 | 60 |  |
| zZEy10fpq3I:dense-unidentified-d104 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot d104 at 14:53, n | 2 | 00:14:53-00:14:54 | 0 | 2 |  |
| zZEy10fpq3I:dense-unidentified-t0074 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0074 at 14:54,  | 1 | 00:14:54-00:14:54 | 0 | 1 |  |
| zZEy10fpq3I:dense-studio-d106 | studio | Study shelf (dense pass 2026-09-09), shot d106 at 14:59, no call tag p | 5 | 00:14:59-00:15:05 | 0 | 40 |  |
| zZEy10fpq3I:dense-studio-d107 | studio | Study shelf (dense pass 2026-09-09), shot d107 at 15:04, no call tag p | 3 | 00:15:04-00:15:08 | 0 | 9 |  |
| zZEy10fpq3I:dense-antichi-d108 | antichi | Rare-book room shelf (dense pass 2026-09-09), shot d108 at 15:08, no c | 3 | 00:15:08-00:15:10 | 0 | 1 |  |
| zZEy10fpq3I:dense-antichi-d109 | antichi | Rare-book room shelf (dense pass 2026-09-09), shot d109 at 15:10, no c | 4 | 00:15:10-00:15:13 | 0 | 7 |  |
| zZEy10fpq3I:dense-unidentified-t0076 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0076 at 15:15,  | 2 | 00:15:15-00:15:18 | 0 | 2 |  |
| zZEy10fpq3I:dense-antichi-d111 | antichi | Rare-book room shelf (dense pass 2026-09-09), shot d111 at 15:24, no c | 1 | 00:15:24-00:15:24 | 0 | 10 |  |
| zZEy10fpq3I:dense-unidentified-d111 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot d111 at 15:26, n | 1 | 00:15:26-00:15:26 | 0 | 0 |  |
| zZEy10fpq3I:dense-unidentified-t0077 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0077 at 15:27,  | 2 | 00:15:27-00:15:30 | 0 | 2 |  |
| zZEy10fpq3I:dense-studio-d113 | studio | Study shelf (dense pass 2026-09-09), shot d113 at 15:40, no call tag p | 7 | 00:15:40-00:15:56 | 1 | 49 |  |
| zZEy10fpq3I:dense-antichi-d113 | antichi | Rare-book room shelf (dense pass 2026-09-09), shot d113 at 15:57, no c | 2 | 00:15:57-00:15:57 | 0 | 2 |  |
| zZEy10fpq3I:dense-unidentified-t0079 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0079 at 15:59,  | 1 | 00:15:59-00:15:59 | 0 | 0 |  |
| zZEy10fpq3I:dense-unidentified-t0080 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0080 at 16:04,  | 1 | 00:16:04-00:16:04 | 0 | 0 |  |
| zZEy10fpq3I:dense-unidentified-t0082 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0082 at 16:27,  | 4 | 00:16:27-00:16:34 | 1 | 2 |  |
| zZEy10fpq3I:dense-unidentified-t0083 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0083 at 16:40,  | 2 | 00:16:40-00:16:43 | 0 | 2 |  |
| zZEy10fpq3I:dense-study-M-A | studio | Bookcase 'M-A' (dense pass 2026-09-09, placed by shelf tag in the same | 22 | 00:17:11-00:17:42 | 7 | 20 |  |
| zZEy10fpq3I:rare-kircher-shelf | antichi | Rare-book room shelf, run of Athanasius Kircher volumes | 2 | 00:17:21-00:17:33 | 6 | 0 |  |
| zZEy10fpq3I:dense-unidentified-t0088 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0088 at 17:43,  | 1 | 00:17:43-00:17:43 | 1 | 1 |  |
| zZEy10fpq3I:office-shelf-1 | other | Modern office/interview-room shelving with paperback stacks (not the p | 1 | 00:17:47-00:17:47 | 2 | 0 | yes |
| zZEy10fpq3I:dense-other-t0088 | other | Other library / insert, dense pass 2026-09-09 shot t0088 at 17:48 (not | 1 | 00:17:48-00:17:48 | 2 | 33 | yes |
| zZEy10fpq3I:dense-other-t0089 | other | Other library / insert, dense pass 2026-09-09 shot t0089 at 17:54 (not | 1 | 00:17:54-00:17:54 | 2 | 33 | yes |
| zZEy10fpq3I:dense-unidentified-t0089 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0089 at 17:59,  | 1 | 00:17:59-00:17:59 | 1 | 0 |  |
| zZEy10fpq3I:dense-unidentified-t0090 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0090 at 18:09,  | 1 | 00:18:09-00:18:09 | 0 | 1 |  |
| zZEy10fpq3I:dense-studio-t0090 | studio | Study shelf (dense pass 2026-09-09), shot t0090 at 18:12, no call tag  | 1 | 00:18:12-00:18:12 | 0 | 0 |  |
| zZEy10fpq3I:dense-unidentified-t0091 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0091 at 18:14,  | 2 | 00:18:14-00:18:21 | 1 | 0 |  |
| zZEy10fpq3I:dense-studio-t0091 | studio | Study shelf (dense pass 2026-09-09), shot t0091 at 18:23, no call tag  | 1 | 00:18:23-00:18:23 | 3 | 14 |  |
| zZEy10fpq3I:dense-unidentified-t0092 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0092 at 18:30,  | 2 | 00:18:30-00:18:33 | 0 | 2 |  |
| zZEy10fpq3I:dense-unidentified-t0093 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0093 at 18:42,  | 1 | 00:18:42-00:18:42 | 0 | 1 |  |
| zZEy10fpq3I:dense-pile-d136 | studio | Pile of books (dense pass 2026-09-09), Study, shot d136 at 18:47 | 2 | 00:18:47-00:18:50 | 0 | 14 |  |
| zZEy10fpq3I:dense-other-d136 | other | Other library / insert, dense pass 2026-09-09 shot d136 at 18:51 (not  | 1 | 00:18:51-00:18:51 | 1 | 0 | yes |
| zZEy10fpq3I:dense-bologna-d138 | bologna | Bologna reinstallation 2026 shelf (dense pass 2026-09-09), shot d138 a | 4 | 00:18:58-00:19:22 | 0 | 200 |  |
| zZEy10fpq3I:dense-other-d138 | other | Other library / insert, dense pass 2026-09-09 shot d138 at 19:26 (not  | 7 | 00:19:26-00:19:50 | 0 | 60 | yes |
| zZEy10fpq3I:dense-antichi-d138 | antichi | Rare-book room shelf (dense pass 2026-09-09), shot d138 at 19:44, no c | 1 | 00:19:44-00:19:44 | 0 | 20 |  |
| zZEy10fpq3I:dense-studio-d138 | studio | Study shelf (dense pass 2026-09-09), shot d138 at 19:54, no call tag p | 2 | 00:19:54-00:19:58 | 0 | 74 |  |
| zZEy10fpq3I:dense-unidentified-d138 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot d138 at 20:03, n | 1 | 00:20:03-00:20:03 | 0 | 0 |  |
| zZEy10fpq3I:dense-unidentified-d139 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot d139 at 20:04, n | 3 | 00:20:04-00:20:06 | 0 | 0 |  |
| zZEy10fpq3I:dense-studio-d139 | studio | Study shelf (dense pass 2026-09-09), shot d139 at 20:07, no call tag p | 1 | 00:20:07-00:20:07 | 0 | 55 |  |
| zZEy10fpq3I:dense-unidentified-d141 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot d141 at 20:25, n | 9 | 00:20:25-00:20:32 | 1 | 0 |  |
| zZEy10fpq3I:dense-other-d141 | other | Other library / insert, dense pass 2026-09-09 shot d141 at 20:33 (not  | 2 | 00:20:33-00:20:34 | 0 | 0 | yes |
| zZEy10fpq3I:dense-studio-d141 | studio | Study shelf (dense pass 2026-09-09), shot d141 at 20:37, no call tag p | 1 | 00:20:37-00:20:37 | 0 | 15 |  |
| zZEy10fpq3I:dense-studio-d142 | studio | Study shelf (dense pass 2026-09-09), shot d142 at 20:37, no call tag p | 5 | 00:20:37-00:20:45 | 0 | 75 |  |
| zZEy10fpq3I:dense-bologna-d142 | bologna | Bologna reinstallation 2026 shelf (dense pass 2026-09-09), shot d142 a | 1 | 00:20:49-00:20:49 | 0 | 1 |  |
| zZEy10fpq3I:dense-antichi-d142 | antichi | Rare-book room shelf (dense pass 2026-09-09), shot d142 at 20:54, no c | 5 | 00:20:54-00:21:00 | 2 | 369 |  |
| zZEy10fpq3I:dense-antichi-d143 | antichi | Rare-book room shelf (dense pass 2026-09-09), shot d143 at 21:00, no c | 2 | 00:21:00-00:21:00 | 2 | 0 |  |
| zZEy10fpq3I:anrw-reference-shelf | unknown | Shelf of the ANRW classics reference set | 5 | 00:21:01-00:21:09 | 3 | 0 |  |
| zZEy10fpq3I:dense-other-d143 | other | Other library / insert, dense pass 2026-09-09 shot d143 at 21:01 (not  | 10 | 00:21:01-00:21:19 | 1 | 802 | yes |
| zZEy10fpq3I:dense-corridoio-d143 | corridoio | Corridor shelf (dense pass 2026-09-09), shot d143 at 21:13, no call ta | 3 | 00:21:13-00:21:18 | 0 | 845 |  |
| zZEy10fpq3I:dense-other-d163 | other | Other library / insert, dense pass 2026-09-09 shot d163 at 26:49 (not  | 3 | 00:26:49-00:26:54 | 1 | 31 | yes |
| zZEy10fpq3I:hora-clave-interview-shelf | studio | Dark wood shelf behind armchair interview (archival 'Hora Clave 9' TV  | 1 | 00:26:50-00:26:50 | 0 | 14 |  |
| zZEy10fpq3I:dense-antichi-d163 | antichi | Rare-book room shelf (dense pass 2026-09-09), shot d163 at 26:56, no c | 8 | 00:26:56-00:27:06 | 1 | 498 |  |
| zZEy10fpq3I:library-ladder-wall-of-volumes | other | Wood-panelled wall of uniform bound volumes, library-ladder scene | 1 | 00:26:59-00:26:59 | 0 | 24 | yes |
| zZEy10fpq3I:dense-studio-d163 | studio | Study shelf (dense pass 2026-09-09), shot d163 at 27:07, no call tag p | 4 | 00:27:07-00:27:11 | 0 | 54 |  |
| zZEy10fpq3I:dense-unidentified-t0136 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0136 at 27:23,  | 1 | 00:27:23-00:27:23 | 0 | 1 |  |
| zZEy10fpq3I:dense-unidentified-t0137 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0137 at 27:26,  | 1 | 00:27:26-00:27:26 | 1 | 0 |  |
| zZEy10fpq3I:dense-unidentified-t0138 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0138 at 27:48,  | 1 | 00:27:48-00:27:48 | 1 | 0 |  |
| zZEy10fpq3I:dense-unidentified-t0142 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0142 at 28:33,  | 2 | 00:28:33-00:28:36 | 1 | 0 |  |
| zZEy10fpq3I:dense-unidentified-t0145 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0145 at 29:03,  | 2 | 00:29:03-00:29:06 | 3 | 1 |  |
| zZEy10fpq3I:dense-unidentified-t0146 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0146 at 29:21,  | 2 | 00:29:21-00:29:22 | 0 | 2 |  |
| zZEy10fpq3I:unknown | other | antique shelf row, rack-focus close-up (archival/establishing-shot lib | 3 | 00:30:13-00:30:21 | 2 | 6 | yes |
| zZEy10fpq3I:dense-unidentified-t0151 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0151 at 30:21,  | 1 | 00:30:21-00:30:21 | 1 | 0 |  |
| zZEy10fpq3I:dense-bologna-d183 | bologna | Bologna reinstallation 2026 shelf (dense pass 2026-09-09), shot d183 a | 1 | 00:31:09-00:31:09 | 0 | 0 |  |
| zZEy10fpq3I:dense-unidentified-d183 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot d183 at 31:10, n | 7 | 00:31:10-00:31:29 | 0 | 0 |  |
| zZEy10fpq3I:dense-other-d183 | other | Other library / insert, dense pass 2026-09-09 shot d183 at 31:19 (not  | 4 | 00:31:19-00:31:27 | 0 | 0 | yes |
| zZEy10fpq3I:dense-studio-d186 | studio | Study shelf (dense pass 2026-09-09), shot d186 at 31:59, no call tag p | 3 | 00:31:59-00:32:07 | 0 | 0 |  |
| zZEy10fpq3I:dense-antichi-d186 | antichi | Rare-book room shelf (dense pass 2026-09-09), shot d186 at 32:08, no c | 2 | 00:32:08-00:32:09 | 0 | 2 |  |
| zZEy10fpq3I:dense-studio-t0160 | studio | Study shelf (dense pass 2026-09-09), shot t0160 at 32:12, no call tag  | 1 | 00:32:12-00:32:12 | 0 | 1 |  |
| zZEy10fpq3I:dense-studio-t0161 | studio | Study shelf (dense pass 2026-09-09), shot t0161 at 32:22, no call tag  | 1 | 00:32:22-00:32:22 | 0 | 1 |  |
| zZEy10fpq3I:dense-unidentified-t0162 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0162 at 32:33,  | 2 | 00:32:33-00:32:36 | 1 | 0 |  |
| zZEy10fpq3I:dense-unidentified-t0163 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0163 at 32:41,  | 1 | 00:32:41-00:32:41 | 1 | 0 |  |
| zZEy10fpq3I:dense-salotto-t0163 | salotto | Living room shelf (dense pass 2026-09-09), shot t0163 at 32:47, no cal | 1 | 00:32:47-00:32:47 | 0 | 1 |  |
| zZEy10fpq3I:dense-salotto-d192 | salotto | Living room shelf (dense pass 2026-09-09), shot d192 at 32:50, no call | 4 | 00:32:50-00:32:59 | 1 | 21 |  |
| zZEy10fpq3I:dense-salotto-t0165 | salotto | Living room shelf (dense pass 2026-09-09), shot t0165 at 33:02, no cal | 1 | 00:33:02-00:33:02 | 0 | 1 |  |
| zZEy10fpq3I:dense-salotto-d194 | salotto | Living room shelf (dense pass 2026-09-09), shot d194 at 33:04, no call | 1 | 00:33:04-00:33:04 | 1 | 7 |  |
| zZEy10fpq3I:dense-unidentified-d194 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot d194 at 33:09, n | 1 | 00:33:09-00:33:09 | 0 | 0 |  |
| zZEy10fpq3I:dense-unidentified-d196 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot d196 at 33:13, n | 12 | 00:33:13-00:33:40 | 0 | 0 |  |
| zZEy10fpq3I:dense-other-d196 | other | Other library / insert, dense pass 2026-09-09 shot d196 at 33:42 (not  | 1 | 00:33:42-00:33:42 | 0 | 0 | yes |
| zZEy10fpq3I:dense-unidentified-t0169 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0169 at 33:59,  | 1 | 00:33:59-00:33:59 | 0 | 1 |  |
| zZEy10fpq3I:dense-unidentified-t0170 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0170 at 34:02,  | 1 | 00:34:02-00:34:02 | 1 | 0 |  |
| zZEy10fpq3I:salgari-book-insert | other | printed book page (Salgari cover gallery, reproduced within a paperbac | 2 | 00:34:11-00:34:13 | 4 | 0 | yes |
| zZEy10fpq3I:dense-salotto-t0171 | salotto | Living room shelf (dense pass 2026-09-09), shot t0171 at 34:13, no cal | 2 | 00:34:13-00:34:17 | 5 | 0 |  |
| zZEy10fpq3I:eco-novel-cover | other | printed book cover (held by narrator) | 2 | 00:34:19-00:34:21 | 1 | 0 | yes |
| zZEy10fpq3I:dense-unidentified-t0172 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0172 at 34:30,  | 1 | 00:34:30-00:34:30 | 0 | 1 |  |
| zZEy10fpq3I:eco-book-title-card | other | book cover / title card insert | 1 | 00:34:37-00:34:37 | 1 | 0 | yes |
| zZEy10fpq3I:dense-antichi-t0173 | antichi | Rare-book room shelf (dense pass 2026-09-09), shot t0173 at 34:41, no  | 1 | 00:34:41-00:34:41 | 1 | 6 |  |
| zZEy10fpq3I:dense-studio-t0175 | studio | Study shelf (dense pass 2026-09-09), shot t0175 at 35:04, no call tag  | 1 | 00:35:04-00:35:04 | 0 | 3 |  |
| zZEy10fpq3I:philosophy-shelf-L11-L12 | studio | Bompiani 'Il Pensiero Occidentale' philosophy shelving (hand-labelled  | 17 | 00:35:07-00:35:23 | 20 | 196 |  |
| zZEy10fpq3I:dense-other-t0200 | other | Other library / insert, dense pass 2026-09-09 shot t0200 at 40:05 (not | 1 | 00:40:05-00:40:05 | 0 | 0 | yes |
| zZEy10fpq3I:rare-glass-cabinet-1 | antichi | glass-fronted antiquarian cabinet, leather-bound volumes | 3 | 00:40:31-00:40:33 | 4 | 42 |  |
| zZEy10fpq3I:dense-other-d240 | other | Other library / insert, dense pass 2026-09-09 shot d240 at 40:32 (not  | 7 | 00:40:32-00:40:37 | 1 | 180 | yes |
| zZEy10fpq3I:rare-glass-cabinet-2 | antichi | second antiquarian cabinet, near rolling library ladder | 2 | 00:40:35-00:40:37 | 1 | 42 |  |
| zZEy10fpq3I:dense-corridoio-d240 | corridoio | Corridor shelf (dense pass 2026-09-09), shot d240 at 40:38, no call ta | 1 | 00:40:38-00:40:38 | 0 | 200 |  |
| zZEy10fpq3I:dense-bologna-t0209 | bologna | Bologna reinstallation 2026 shelf (dense pass 2026-09-09), shot t0209  | 1 | 00:41:54-00:41:54 | 0 | 81 | yes |
| zZEy10fpq3I:dense-other-d251 | other | Other library / insert, dense pass 2026-09-09 shot d251 at 42:42 (not  | 3 | 00:42:42-00:42:46 | 0 | 0 | yes |
| zZEy10fpq3I:study-desk-piles-1 | studio | piles of contemporary books stacked on a dark wood credenza/desk | 7 | 00:42:51-00:43:03 | 52 | 27 |  |
| zZEy10fpq3I:salotto-piano-pile-07 | salotto | salotto upright piano, keyboard shelf (closed fallboard / music shelf) | 4 | 00:42:51-00:43:03 | 7 | 18 |  |
| zZEy10fpq3I:salotto-piano-pile-08 | salotto | salotto upright piano, keyboard shelf (closed fallboard / music shelf) | 4 | 00:42:51-00:43:03 | 14 | 13 |  |
| zZEy10fpq3I:salotto-piano-pile-09 | salotto | salotto upright piano, keyboard shelf (closed fallboard / music shelf) | 4 | 00:42:51-00:43:03 | 9 | 20 |  |
| zZEy10fpq3I:salotto-piano-pile-10 | salotto | salotto upright piano, keyboard shelf (closed fallboard / music shelf) | 4 | 00:42:51-00:43:03 | 5 | 4 |  |
| zZEy10fpq3I:salotto-piano-pile-11 | salotto | salotto upright piano, keyboard shelf (closed fallboard / music shelf) | 4 | 00:42:51-00:43:03 | 8 | 16 |  |
| zZEy10fpq3I:salotto-piano-pile-12 | salotto | salotto upright piano, keyboard shelf (closed fallboard / music shelf) | 3 | 00:42:51-00:43:03 | 4 | 14 |  |
| zZEy10fpq3I:salotto-piano-pile-01 | salotto | salotto upright piano, piano lid (top), pile 1 of 6 (leftmost, about 0 | 3 | 00:42:59-00:43:03 | 5 | 3 |  |
| zZEy10fpq3I:salotto-piano-pile-02 | salotto | salotto upright piano, piano lid (top), pile 2 of 6 (second from the l | 3 | 00:42:59-00:43:03 | 6 | 7 |  |
| zZEy10fpq3I:salotto-piano-pile-03 | salotto | salotto upright piano, piano lid (top), pile 3 of 6 (third from the le | 3 | 00:42:59-00:43:03 | 3 | 19 |  |
| zZEy10fpq3I:salotto-piano-pile-04 | salotto | salotto upright piano, piano lid (top), pile 4 of 6 (fourth from the l | 3 | 00:42:59-00:43:03 | 7 | 14 |  |
| zZEy10fpq3I:salotto-piano-pile-05 | salotto | salotto upright piano, piano lid (top), pile 5 of 6 (fifth from the le | 3 | 00:42:59-00:43:03 | 6 | 4 |  |
| zZEy10fpq3I:salotto-piano-pile-06 | salotto | salotto upright piano, piano lid (top), pile 6 of 6 (rightmost, about  | 3 | 00:42:59-00:43:03 | 3 | 13 |  |
| zZEy10fpq3I:corridor-shelf-A | corridoio | modern white shelving unit, section tagged 'A', bay of 19th-century ad | 8 | 00:43:13-00:43:31 | 6 | 34 |  |
| zZEy10fpq3I:dense-corridor-10 | corridoio | Bookcase 'A', bays 10-10 (dense pass 2026-09-09, placed by shelf tag i | 5 | 00:43:15-00:43:30 | 7 | 46 |  |
| zZEy10fpq3I:stacks_shelf_sonzogno | other | archive stacks, woman browsing open shelving (Sonzogno/classics sectio | 1 | 00:43:29-00:43:29 | 3 | 11 | yes |
| zZEy10fpq3I:dense-studio-d254 | studio | Study shelf (dense pass 2026-09-09), shot d254 at 43:32, no call tag p | 1 | 00:43:32-00:43:32 | 0 | 1 |  |
| zZEy10fpq3I:dense-bologna-d254 | bologna | Bologna reinstallation 2026 shelf (dense pass 2026-09-09), shot d254 a | 2 | 00:43:36-00:43:41 | 1 | 1 |  |
| zZEy10fpq3I:dense-corridoio-d254 | corridoio | Corridor shelf (dense pass 2026-09-09), shot d254 at 43:43, no call ta | 6 | 00:43:43-00:44:04 | 6 | 67 |  |
| zZEy10fpq3I:dense-studio-t0221 | studio | Study shelf (dense pass 2026-09-09), shot t0221 at 44:19, no call tag  | 1 | 00:44:19-00:44:19 | 0 | 8 |  |
| zZEy10fpq3I:dense-studio-t0222 | studio | Study shelf (dense pass 2026-09-09), shot t0222 at 44:27, no call tag  | 1 | 00:44:27-00:44:27 | 0 | 8 |  |
| zZEy10fpq3I:stacks_shelf_A_baudelaire | other | archive stacks, shelf edge tag 'A' labelled BAUDELAIRE / HUYSMANS | 2 | 00:44:35-00:44:37 | 1 | 8 | yes |
| zZEy10fpq3I:held-book-memoria-vegetale | other | book held to camera by an interviewee (editor/bookseller), blurred she | 2 | 00:44:51-00:44:57 | 1 | 0 | yes |
| zZEy10fpq3I:dense-studio-t0224 | studio | Study shelf (dense pass 2026-09-09), shot t0224 at 44:53, no call tag  | 1 | 00:44:53-00:44:53 | 1 | 0 |  |
| zZEy10fpq3I:interview-graybeard-1 | other | new interviewee (grey curly hair, black glasses, dark sweater, black l | 8 | 00:44:59-00:45:15 | 2 | 16 | yes |
| zZEy10fpq3I:dense-study-L8-12 | studio | Bookcase 'L', bays 8-12 (dense pass 2026-09-09, placed by shelf tag in | 1 | 00:45:17-00:45:17 | 5 | 50 |  |
| zZEy10fpq3I:eco-foreign-editions-1 | other | shelf of foreign-language editions of Umberto Eco's own books, dark bl | 5 | 00:45:17-00:45:39 | 2 | 7 | yes |
| zZEy10fpq3I:dense-unidentified-d262 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot d262 at 45:49, n | 8 | 00:45:49-00:46:03 | 0 | 0 |  |
| zZEy10fpq3I:scholarly-shelf-Q49 | studio | man sitting down on a black leather sofa in front of a large white she | 12 | 00:46:07-00:46:41 | 3 | 212 |  |
| zZEy10fpq3I:book-cover-superuomo | other | extreme close-up of a single book cover held/shown to camera | 3 | 00:47:03-00:47:05 | 1 | 0 | yes |
| zZEy10fpq3I:dense-unidentified-t0235 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0235 at 47:09,  | 1 | 00:47:09-00:47:09 | 1 | 0 |  |
| zZEy10fpq3I:montage-name-of-the-rose | other | graphic montage of foreign-language covers of Eco's 'Il nome della ros | 6 | 00:47:35-00:47:45 | 11 | 2 | yes |
| zZEy10fpq3I:dense-other-t0238 | other | Other library / insert, dense pass 2026-09-09 shot t0238 at 47:42 (not | 2 | 00:47:42-00:47:45 | 12 | 0 | yes |
| zZEy10fpq3I:unlabelled | other |  | 1 | 00:47:47-00:47:47 | 0 | 0 | yes |
| zZEy10fpq3I:eco-archival-red-chair | other | archival footage of Umberto Eco himself (red velvet vest, wire-rim gla | 17 | 00:47:49-00:48:59 | 0 | 0 | yes |
| zZEy10fpq3I:dense-antichi-t0239 | antichi | Rare-book room shelf (dense pass 2026-09-09), shot t0239 at 47:56, no  | 1 | 00:47:56-00:47:56 | 0 | 1 |  |
| zZEy10fpq3I:eco-archival-white-sofa | other | archival Eco footage, white sofa, glass display case with an open manu | 2 | 00:48:07-00:48:39 | 0 | 0 | yes |
| zZEy10fpq3I:interview-mustache-wooden-shelf | studio | new interviewee (moustache, glasses, olive-green shirt) against a wood | 13 | 00:48:13-00:48:30 | 2 | 110 |  |
| zZEy10fpq3I:dense-antichi-t0241 | antichi | Rare-book room shelf (dense pass 2026-09-09), shot t0241 at 48:13, no  | 1 | 00:48:13-00:48:13 | 0 | 1 |  |
| zZEy10fpq3I:dense-unidentified-d275 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot d275 at 48:32, n | 1 | 00:48:32-00:48:32 | 0 | 1 |  |
| zZEy10fpq3I:dense-other-d276 | other | Other library / insert, dense pass 2026-09-09 shot d276 at 48:32 (not  | 3 | 00:48:32-00:48:39 | 0 | 0 | yes |
| zZEy10fpq3I:dense-antichi-d276 | antichi | Rare-book room shelf (dense pass 2026-09-09), shot d276 at 48:41, no c | 1 | 00:48:41-00:48:41 | 0 | 1 |  |
| zZEy10fpq3I:manuscript-tractatus-venenis | other | extreme close-up of an open medieval/early-print manuscript page shown | 3 | 00:48:41-00:48:45 | 1 | 2 | yes |
| zZEy10fpq3I:dense-antichi-t0243 | antichi | Rare-book room shelf (dense pass 2026-09-09), shot t0243 at 48:44, no  | 1 | 00:48:44-00:48:44 | 0 | 6 |  |
| zZEy10fpq3I:dense-salotto-t0244 | salotto | Living room shelf (dense pass 2026-09-09), shot t0244 at 48:57, no cal | 1 | 00:48:57-00:48:57 | 0 | 0 |  |
| zZEy10fpq3I:dense-antichi-t0244 | antichi | Rare-book room shelf (dense pass 2026-09-09), shot t0244 at 49:00, no  | 1 | 00:49:00-00:49:00 | 0 | 1 |  |
| zZEy10fpq3I:eco-archival-lecture | other | archival Eco footage, lecture/panel setting with dark background and p | 9 | 00:49:01-00:49:25 | 0 | 0 | yes |
| zZEy10fpq3I:dense-unidentified-t0246 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0246 at 49:15,  | 2 | 00:49:15-00:49:21 | 0 | 0 |  |
| zZEy10fpq3I:dense-salotto-t0249 | salotto | Living room shelf (dense pass 2026-09-09), shot t0249 at 49:51, no cal | 2 | 00:49:51-00:49:57 | 0 | 0 |  |
| zZEy10fpq3I:dense-salotto-t0251 | salotto | Living room shelf (dense pass 2026-09-09), shot t0251 at 50:20, no cal | 1 | 00:50:20-00:50:20 | 0 | 0 |  |
| zZEy10fpq3I:dense-corridoio-t0254 | corridoio | Corridor shelf (dense pass 2026-09-09), shot t0254 at 50:55, no call t | 1 | 00:50:55-00:50:55 | 0 | 2 |  |
| zZEy10fpq3I:dense-other-d287 | other | Other library / insert, dense pass 2026-09-09 shot d287 at 50:56 (not  | 1 | 00:50:56-00:50:56 | 1 | 0 | yes |
| zZEy10fpq3I:dense-studio-d287 | studio | Study shelf (dense pass 2026-09-09), shot d287 at 50:59, no call tag p | 1 | 00:50:59-00:50:59 | 2 | 7 |  |
| zZEy10fpq3I:living-gosh-shelf | salotto | Living room shelf beside framed GOSH! print | 1 | 00:50:59-00:50:59 | 1 | 18 |  |
| zZEy10fpq3I:dense-other-t0254 | other | Other library / insert, dense pass 2026-09-09 shot t0254 at 51:00 (not | 1 | 00:51:00-00:51:00 | 1 | 11 | yes |
| zZEy10fpq3I:dense-other-t0258 | other | Other library / insert, dense pass 2026-09-09 shot t0258 at 51:40 (not | 2 | 00:51:40-00:51:43 | 0 | 0 | yes |
| zZEy10fpq3I:dense-other-d295 | other | Other library / insert, dense pass 2026-09-09 shot d295 at 52:32 (not  | 2 | 00:52:32-00:52:33 | 0 | 0 | yes |
| zZEy10fpq3I:dense-unidentified-d295 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot d295 at 52:36, n | 13 | 00:52:36-00:53:07 | 0 | 0 |  |
| zZEy10fpq3I:study-francoforte-deleuze | studio | Study shelving with subject tab labels 'FRANCOFORTE' and 'DELEUZE' | 1 | 00:53:13-00:53:13 | 4 | 37 |  |
| zZEy10fpq3I:dense-studio-d300 | studio | Study shelf (dense pass 2026-09-09), shot d300 at 53:59, no call tag p | 1 | 00:53:59-00:53:59 | 0 | 20 |  |
| zZEy10fpq3I:dense-other-d300 | other | Other library / insert, dense pass 2026-09-09 shot d300 at 54:03 (not  | 2 | 00:54:03-00:54:04 | 0 | 0 | yes |
| zZEy10fpq3I:dense-unidentified-t0274 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0274 at 54:54,  | 1 | 00:54:54-00:54:54 | 1 | 0 |  |
| zZEy10fpq3I:dense-unidentified-t0276 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0276 at 55:16,  | 2 | 00:55:16-00:55:19 | 0 | 2 |  |
| zZEy10fpq3I:dense-unidentified-t0277 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0277 at 55:31,  | 2 | 00:55:31-00:55:35 | 0 | 2 |  |
| zZEy10fpq3I:dense-other-t0280 | other | Other library / insert, dense pass 2026-09-09 shot t0280 at 56:03 (not | 2 | 00:56:03-00:56:06 | 0 | 1 | yes |
| zZEy10fpq3I:dense-studio-d319 | studio | Study shelf (dense pass 2026-09-09), shot d319 at 57:00, no call tag p | 2 | 00:57:00-00:57:08 | 0 | 110 |  |
| zZEy10fpq3I:rare-leather-shelf-eco | antichi | Antiquarian leather-bound shelf behind Eco's interview seat | 1 | 00:57:05-00:57:05 | 1 | 22 |  |
| zZEy10fpq3I:dense-other-d319 | other | Other library / insert, dense pass 2026-09-09 shot d319 at 57:09 (not  | 2 | 00:57:09-00:57:10 | 1 | 8 | yes |
| zZEy10fpq3I:dense-other-t0289 | other | Other library / insert, dense pass 2026-09-09 shot t0289 at 57:53 (not | 2 | 00:57:53-00:57:56 | 6 | 1 | yes |
| zZEy10fpq3I:dense-other-t0290 | other | Other library / insert, dense pass 2026-09-09 shot t0290 at 58:07 (not | 1 | 00:58:07-00:58:07 | 2 | 0 | yes |
| zZEy10fpq3I:dense-other-t0291 | other | Other library / insert, dense pass 2026-09-09 shot t0291 at 58:20 (not | 2 | 00:58:20-00:58:24 | 1 | 0 | yes |
| zZEy10fpq3I:dense-studio-t0297 | studio | Study shelf (dense pass 2026-09-09), shot t0297 at 59:28, no call tag  | 1 | 00:59:28-00:59:28 | 0 | 0 |  |
| zZEy10fpq3I:dense-other-t0297 | other | Other library / insert, dense pass 2026-09-09 shot t0297 at 59:31 (not | 1 | 00:59:31-00:59:31 | 0 | 0 | yes |
| zZEy10fpq3I:archival-shakespeare-bacon-shelf | other | Archival bookshelf insert illustrating the Shakespeare/Bacon authorshi | 1 | 01:00:08-01:00:08 | 2 | 1 | yes |
| zZEy10fpq3I:dense-unidentified-t0300 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0300 at 60:11,  | 1 | 01:00:11-01:00:11 | 2 | 0 |  |
| zZEy10fpq3I:dense-unidentified-t0301 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0301 at 60:14,  | 1 | 01:00:14-01:00:14 | 3 | 0 |  |
| zZEy10fpq3I:dense-unidentified-t0311 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0311 at 62:22,  | 1 | 01:02:22-01:02:22 | 1 | 0 |  |
| zZEy10fpq3I:dense-bologna-d348 | bologna | Bologna reinstallation 2026 shelf (dense pass 2026-09-09), shot d348 a | 4 | 01:02:23-01:02:41 | 0 | 13 |  |
| zZEy10fpq3I:dense-other-d348 | other | Other library / insert, dense pass 2026-09-09 shot d348 at 62:43 (not  | 5 | 01:02:43-01:02:51 | 0 | 0 | yes |
| zZEy10fpq3I:insert-trattato-semiotica | other | Book-cover insert: Trattato di semiotica generale | 1 | 01:02:49-01:02:49 | 1 | 0 | yes |
| zZEy10fpq3I:dense-studio-d350 | studio | Study shelf (dense pass 2026-09-09), shot d350 at 63:02, no call tag p | 3 | 01:03:02-01:03:10 | 0 | 12 |  |
| zZEy10fpq3I:dense-salotto-d350 | salotto | Living room shelf (dense pass 2026-09-09), shot d350 at 63:12, no call | 8 | 01:03:12-01:03:25 | 0 | 16 |  |
| zZEy10fpq3I:dense-unidentified-d350 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot d350 at 63:25, n | 2 | 01:03:25-01:03:26 | 0 | 2 |  |
| zZEy10fpq3I:dense-unidentified-t0317 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0317 at 63:26,  | 2 | 01:03:26-01:03:34 | 0 | 2 |  |
| zZEy10fpq3I:dense-studio-d352 | studio | Study shelf (dense pass 2026-09-09), shot d352 at 63:45, no call tag p | 3 | 01:03:45-01:04:06 | 0 | 4 |  |
| zZEy10fpq3I:dense-corridoio-d352 | corridoio | Corridor shelf (dense pass 2026-09-09), shot d352 at 64:11, no call ta | 2 | 01:04:11-01:04:11 | 0 | 0 |  |
| zZEy10fpq3I:dense-unidentified-t0321 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0321 at 64:16,  | 1 | 01:04:16-01:04:16 | 1 | 0 |  |
| zZEy10fpq3I:dense-other-d355 | other | Other library / insert, dense pass 2026-09-09 shot d355 at 64:24 (not  | 1 | 01:04:24-01:04:24 | 0 | 0 | yes |
| zZEy10fpq3I:dense-unidentified-d355 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot d355 at 64:25, n | 2 | 01:04:25-01:04:27 | 0 | 0 |  |
| zZEy10fpq3I:dense-studio-d355 | studio | Study shelf (dense pass 2026-09-09), shot d355 at 64:29, no call tag p | 3 | 01:04:29-01:04:31 | 0 | 0 |  |
| zZEy10fpq3I:insert-cimitero-praga | other | Book-cover insert: Il cimitero di Praga | 1 | 01:04:29-01:04:29 | 1 | 0 | yes |
| zZEy10fpq3I:dense-unidentified-t0325 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0325 at 65:06,  | 2 | 01:05:06-01:05:11 | 0 | 2 |  |
| zZEy10fpq3I:dense-unidentified-t0326 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0326 at 65:17,  | 3 | 01:05:17-01:05:22 | 0 | 1 |  |
| zZEy10fpq3I:dense-antichi-d363 | antichi | Rare-book room shelf (dense pass 2026-09-09), shot d363 at 65:26, no c | 3 | 01:05:26-01:05:28 | 0 | 3 |  |
| zZEy10fpq3I:dense-unidentified-d363 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot d363 at 65:31, n | 2 | 01:05:31-01:05:32 | 1 | 0 |  |
| zZEy10fpq3I:insert-the-plot-eisner | other | Book-cover insert: The Plot (Will Eisner) | 1 | 01:05:39-01:05:39 | 1 | 0 | yes |
| zZEy10fpq3I:dense-studio-t0329 | studio | Study shelf (dense pass 2026-09-09), shot t0329 at 65:57, no call tag  | 1 | 01:05:57-01:05:57 | 0 | 10 |  |
| zZEy10fpq3I:dense-unidentified-d367 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot d367 at 65:57, n | 5 | 01:05:57-01:06:02 | 1 | 0 |  |
| zZEy10fpq3I:insert-pendolo-foucault | other | Book-cover insert: Il pendolo di Foucault | 1 | 01:05:58-01:05:58 | 1 | 0 | yes |
| zZEy10fpq3I:dense-studio-d367 | studio | Study shelf (dense pass 2026-09-09), shot d367 at 66:03, no call tag p | 1 | 01:06:03-01:06:03 | 0 | 12 |  |
| zZEy10fpq3I:dense-salotto-t0330 | salotto | Living room shelf (dense pass 2026-09-09), shot t0330 at 66:05, no cal | 2 | 01:06:05-01:06:10 | 0 | 20 |  |
| zZEy10fpq3I:dense-unidentified-d369 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot d369 at 66:10, n | 15 | 01:06:10-01:06:30 | 0 | 0 |  |
| zZEy10fpq3I:dense-unidentified-d371 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot d371 at 66:36, n | 1 | 01:06:36-01:06:36 | 0 | 0 |  |
| zZEy10fpq3I:dense-other-d371 | other | Other library / insert, dense pass 2026-09-09 shot d371 at 66:37 (not  | 8 | 01:06:37-01:06:45 | 2 | 1 | yes |
| zZEy10fpq3I:dense-other-t0334 | other | Other library / insert, dense pass 2026-09-09 shot t0334 at 66:52 (not | 1 | 01:06:52-01:06:52 | 0 | 0 | yes |
| zZEy10fpq3I:dense-other-t0336 | other | Other library / insert, dense pass 2026-09-09 shot t0336 at 67:13 (not | 2 | 01:07:13-01:07:16 | 0 | 0 | yes |
| zZEy10fpq3I:insert-exlibris-scritti | other | Book endpaper insert with Eco ex-libris bookplate | 1 | 01:07:37-01:07:37 | 1 | 0 | yes |
| zZEy10fpq3I:world-libraries-stock-1 | other | Stock/B-roll library footage (not Eco's apartment) - mixed English tec | 2 | 01:13:09-01:13:11 | 2 | 25 | yes |
| zZEy10fpq3I:dense-other-t0366 | other | Other library / insert, dense pass 2026-09-09 shot t0366 at 73:17 (not | 1 | 01:13:17-01:13:17 | 0 | 2000 | yes |
| zZEy10fpq3I:epilogue-diorama-miniature | other | Artistic miniature diorama (shadow-box) of a library/study with firepl | 1 | 01:13:37-01:13:37 | 1 | 34 | yes |
| zZEy10fpq3I:dense-other-d413 | other | Other library / insert, dense pass 2026-09-09 shot d413 at 74:13 (not  | 8 | 01:14:13-01:14:22 | 0 | 0 | yes |
| zZEy10fpq3I:dense-antichi-d413 | antichi | Rare-book room shelf (dense pass 2026-09-09), shot d413 at 74:24, no c | 1 | 01:14:24-01:14:24 | 0 | 1 |  |
| zZEy10fpq3I:dense-studio-d413 | studio | Study shelf (dense pass 2026-09-09), shot d413 at 74:27, no call tag p | 3 | 01:14:27-01:14:32 | 5 | 233 |  |
| zZEy10fpq3I:corridor-shelving-main | corridoio | Real Milan apartment - long white Billy-style shelving corridor (a chi | 1 | 01:14:27-01:14:27 | 1 | 60 |  |
| zZEy10fpq3I:exterior-window-view-1 | other | Real Milan apartment, exterior courtyard shot through two open windows | 1 | 01:14:32-01:14:32 | 2 | 53 | yes |
| zZEy10fpq3I:dense-studio-d414 | studio | Study shelf (dense pass 2026-09-09), shot d414 at 74:32, no call tag p | 6 | 01:14:32-01:15:12 | 2 | 343 |  |
| zZEy10fpq3I:dense-corridoio-d414 | corridoio | Corridor shelf (dense pass 2026-09-09), shot d414 at 74:44, no call ta | 4 | 01:14:44-01:15:00 | 0 | 115 |  |
| zZEy10fpq3I:dense-vestibolo-d414 | vestibolo | Vestibule shelf (dense pass 2026-09-09), shot d414 at 75:03, no call t | 2 | 01:15:03-01:15:06 | 0 | 14 |  |
| zZEy10fpq3I:rare-books-table | antichi | Rare-book room, dark wood table with antique volumes | 1 | 01:15:13-01:15:13 | 1 | 1 |  |
| zZEy10fpq3I:rare-books-kircher-cabinet | antichi | Rare-book room glass-fronted cabinet - a shelf of 17th-century Athanas | 4 | 01:15:14-01:15:25 | 8 | 49 |  |
| zZEy10fpq3I:dense-unidentified-t0377 | unknown | Unidentified room shelf (dense pass 2026-09-09), shot t0377 at 75:34,  | 1 | 01:15:34-01:15:34 | 0 | 9 |  |
| photo:fondazione_01_E | studio | Bookcase 'E' (Fondazione lettering), Milan apartment working library:  | 1 | - | 5 | 157 |  |
| photo:fondazione_02_H | studio | Bookcase 'H' (Fondazione lettering), Milan apartment working library:  | 1 | - | 3 | 509 |  |
| photo:fondazione_03_G | studio | Bookcase 'G' (Fondazione lettering), Milan apartment working library:  | 1 | - | 0 | 130 |  |
| photo:fondazione_04_F | studio | Bookcase 'F' (Fondazione lettering), Milan apartment working library:  | 1 | - | 1 | 122 |  |
| photo:fondazione_05_C | studio | Bookcase 'C' (Fondazione lettering), Milan apartment working library:  | 1 | - | 2 | 99 |  |
| photo:fondazione_06_B | studio | Bookcase 'B' (Fondazione lettering), Milan apartment working library:  | 1 | - | 0 | 156 |  |
| photo:fondazione_07_D | studio | Bookcase 'D' (Fondazione lettering), Milan apartment working library,  | 1 | - | 2 | 140 |  |
| photo:fondazione_08_A-da_1_a_6 | studio | Bookcase 'A', shelves 1-6 (Fondazione lettering), Milan apartment work | 1 | - | 2 | 231 |  |
| photo:fondazione_09_A-da_7_a_12 | studio | Bookcase 'A', shelves 7-12 (Fondazione lettering), Milan apartment wor | 1 | - | 1 | 225 |  |
| photo:fondazione_12_Q | studio | Bookcase 'Q' (Fondazione lettering), Milan apartment working library:  | 1 | - | 1 | 254 |  |
| photo:fondazione_10_A-da_13_a_18 | studio | Bookcase 'A', shelves 13-18 (Fondazione lettering), Milan apartment wo | 1 | - | 0 | 224 |  |
| photo:fondazione_11_A-da_19_a_25 | studio | Bookcase 'A', shelves 19-25 (Fondazione lettering), Milan apartment wo | 1 | - | 0 | 204 |  |
| photo:fondazione_13_P | studio | Bookcase 'P' (Fondazione lettering), Milan apartment working library,  | 1 | - | 0 | 530 |  |
| photo:fondazione_14_L1-4 | studio | Bookcase 'L', shelves 1-4 (Fondazione lettering), Milan apartment work | 1 | - | 2 | 94 |  |
| photo:fondazione_15_L5-7 | studio | Bookcase 'L', shelves 5-7 (Fondazione lettering), Milan apartment work | 1 | - | 0 | 81 |  |
| photo:fondazione_16_L8-12 | studio | Bookcase 'L', shelves 8-12 (Fondazione lettering), Milan apartment wor | 1 | - | 9 | 192 |  |
| photo:fondazione_17_I | studio | Bookcase 'I' (Fondazione lettering), Milan apartment working library,  | 1 | - | 8 | 136 |  |
| photo:fondazione_18_M-A | studio | Bookcase 'M-A' (Fondazione lettering), Milan apartment working library | 1 | - | 2 | 130 |  |
| photo:fondazione_19_M-B | studio | Bookcase 'M-B' (Fondazione lettering), Milan apartment working library | 1 | - | 2 | 126 |  |
| photo:fondazione_20_Na | studio | Bookcase 'Na' (Fondazione lettering), Milan apartment working library, | 1 | - | 0 | 72 |  |
| photo:fondazione_21_Nb | studio | Bookcase 'Nb' (Fondazione lettering), Milan apartment working library, | 1 | - | 2 | 52 |  |
| photo:fondazione_22_Nc | studio | Bookcase 'Nc' (Fondazione lettering), Milan apartment working library, | 1 | - | 0 | 54 |  |
| photo:fondazione_23_Oa | studio | Bookcase 'Oa' (Fondazione lettering), Milan apartment working library, | 1 | - | 0 | 66 |  |
| photo:fondazione_24_Ob | studio | Bookcase 'Ob' (Fondazione lettering), Milan apartment working library, | 1 | - | 0 | 62 |  |
| photo:fondazione_25_R | studio | Bookcase 'R' (Fondazione lettering), Milan apartment working library:  | 1 | - | 4 | 102 |  |
| photo:fondazione_26_S | studio | Bookcase 'S' (Fondazione lettering), Milan apartment working library:  | 1 | - | 1 | 112 |  |
| photo:fondazione_01_Studio_antichi_milano_foto_curtiparini | antichi | Stanza degli antichi (rare-book room), Milan apartment, Piazza Castell | 1 | - | 0 | 0 |  |
| photo:fondazione_02_Studio_antichi_milano_foto_curtiparini_MG_9923 | antichi | Stanza degli antichi (rare-book room), Milan apartment, Piazza Castell | 1 | - | 0 | 0 |  |
| photo:fondazione_03_ANTICHI-24 | antichi | Stanza degli antichi (rare-book room), Milan apartment: single-shelf c | 1 | - | 3 | 2 |  |
| photo:fondazione_04_Libreria_Antichi_DX | antichi | Stanza degli antichi (rare-book room), Milan apartment: the right-hand | 1 | - | 1 | 74 |  |
| photo:fondazione_05_102-01 | antichi | Stanza degli antichi (rare-book room), Milan apartment: single antique | 1 | - | 0 | 1 |  |
| photo:fondazione_06_157-08-2 | antichi | Stanza degli antichi (rare-book room), Milan apartment: single antique | 1 | - | 1 | 0 |  |
| photo:fondazione_07_357-03 | antichi | Stanza degli antichi (rare-book room), Milan apartment: single antique | 1 | - | 1 | 0 |  |
| photo:fondazione_08_399-11 | antichi | Stanza degli antichi (rare-book room), Milan apartment: single antique | 1 | - | 1 | 0 |  |
| photo:fondazione_09_402-04 | antichi | Stanza degli antichi (rare-book room), Milan apartment: single antique | 1 | - | 1 | 0 |  |
| photo:fondazione_10_424-07 | antichi | Stanza degli antichi (rare-book room), Milan apartment: single antique | 1 | - | 1 | 0 |  |
| photo:fondazione_11_452-05 | antichi | Stanza degli antichi (rare-book room), Milan apartment: single antique | 1 | - | 1 | 0 |  |
| photo:fondazione_12_770-11 | antichi | Stanza degli antichi (rare-book room), Milan apartment: single antique | 1 | - | 1 | 0 |  |
| photo:fondazione_13_772-19 | antichi | Stanza degli antichi (rare-book room), Milan apartment: single antique | 1 | - | 1 | 0 |  |
| photo:fondazione_14_778-03 | antichi | Stanza degli antichi (rare-book room), Milan apartment: single antique | 1 | - | 1 | 0 |  |
| photo:fondazione_15_926-12 | antichi | Stanza degli antichi (rare-book room), Milan apartment: single antique | 1 | - | 1 | 0 |  |
| photo:fondazione_FUE_Le_Biblioteche_ExLibris_00 | antichi | Ex-libris gallery (Fondazione website), studio photograph of the bookp | 1 | - | 0 | 1 |  |
| photo:fondazione_FUE_Le_Biblioteche_ExLibris_01 | antichi | Ex-libris gallery (Fondazione website), studio photograph of the bookp | 1 | - | 0 | 1 |  |
| photo:fondazione_FUE_Le_Biblioteche_ExLibris_02 | antichi | Ex-libris gallery (Fondazione website), studio photograph of the bookp | 1 | - | 0 | 1 |  |
| photo:fondazione_FUE_Le_Biblioteche_ExLibris_03 | antichi | Ex-libris gallery (Fondazione website), studio photograph of the bookp | 1 | - | 0 | 1 |  |
| photo:fondazione_FUE_Le_Biblioteche_ExLibris_04 | antichi | Ex-libris gallery (Fondazione website), studio photograph of the bookp | 1 | - | 0 | 1 |  |
| photo:fondazione_FUE_Le_Biblioteche_ExLibris_05 | antichi | Ex-libris gallery (Fondazione website), studio photograph of the bookp | 1 | - | 0 | 1 |  |
| photo:artribune2026_bologna | unknown | Biblioteca Eco, Palazzo Poggi, Bologna (2026 reconstruction, not the M | 1 | - | 1 | 196 |  |
| photo:artribune2026_bologna_1 | unknown | Biblioteca Eco, Palazzo Poggi, Bologna (2026 reconstruction) -- corner | 1 | - | 1 | 86 |  |
| photo:artribune2026_bologna_2 | unknown | Biblioteca Eco, Palazzo Poggi, Bologna (2026 reconstruction) -- recept | 1 | - | 0 | 48 |  |
| photo:bolognatoday_biblioteca_eco | unknown | Biblioteca Eco, Palazzo Poggi, Bologna (2026 reconstruction) -- two-pa | 1 | - | 0 | 134 |  |
| photo:criticaletteraria_2022_1 | salotto | Salotto (living room), Milan apartment: free-standing glass display ca | 1 | - | 0 | 0 |  |
| photo:criticaletteraria_2022_3 | corridoio | Two-panel composite: left, the long book-lined corridor of the Milan a | 1 | - | 0 | 224 |  |
| photo:criticaletteraria_2022_5 | studio | Working study/office, Milan apartment: open-plan room with a central d | 1 | - | 1 | 158 |  |
| photo:criticaletteraria_2022_7 | salotto | Two-panel composite: left, a glass-fronted walnut curio cabinet in the | 1 | - | 1 | 49 |  |
| photo:criticaletteraria_2022_10 | unknown | Not a library image | 1 | - | 0 | 0 |  |
| photo:criticaletteraria_2022_11 | studio | Working study/office, Milan apartment: wide view of the same open-plan | 1 | - | 0 | 170 |  |
| photo:criticaletteraria_2022_13 | studio | Working study/office, Milan apartment: same room as criticaletteraria_ | 1 | - | 0 | 158 |  |
| photo:criticaletteraria_2022_16 | antichi | Stanza degli antichi (rare-book room), Milan apartment: same room and  | 1 | - | 0 | 0 |  |
| photo:flickr_5772422901_b | studio | Working study, Milan apartment, 9 May 2011: Eco seated in front of a m | 1 | - | 1 | 118 |  |
| photo:flickr_5772998464_b | studio | Working study, Milan apartment, 9 May 2011: Eco standing beside a roll | 1 | - | 1 | 178 |  |
| photo:getty_953403568_1024 | studio | Working study, Milan apartment, 1 March 2011: Eco on a rolling ladder  | 1 | - | 0 | 104 |  |
| photo:milanotoday_zanni | studio | Working study, Milan apartment, 24 April 2010: Eco standing in the for | 1 | - | 0 | 78 |  |
| photo:zanni_banner_orig | salotto | Salotto (living room), Milan apartment, 24 April 2010: close portrait  | 1 | - | 0 | 0 |  |
| photo:salotto-E | salotto | Display wall | 1 | - | 0 | 10 |  |
