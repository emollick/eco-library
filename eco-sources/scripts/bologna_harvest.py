#!/usr/bin/env python3
"""Harvest the SBN-UBO SebinaYOU records with possessor 'Eco, Umberto' at BUB.
Public GET/POST only (DWR endpoints the OPAC's own JS uses). One request at a time, with delay.
Resumable: skips ids already in the JSONL; page state in progress log."""
import requests, re, json, random, time, html, sys, os, csv, datetime
from jsun import dwr_html
BASE="https://sol.unibo.it"
QPATH="/SebinaOpac/query/KF_XP:%22eco%20umberto%22%20KF_BIBVIRT:ubobu?context=catalogo"
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36 (EcoLibraryResearch harvester; polite, 1 req/s)"
OUT_DIR="/mnt/project-files/eco-sources"
JSONL=os.path.join(OUT_DIR,"bologna_eco_modern.jsonl")
PROG=os.path.join(OUT_DIR,"bologna_eco_modern.progress.log")
DELAY=float(os.environ.get("DELAY","0.6"))
SORT=os.environ.get("SORT","Titolo")   # stable order
PAGE_SIZE=10

def log(msg):
    line=f"{datetime.datetime.utcnow().isoformat(timespec='seconds')}Z {msg}"
    print(line, flush=True)
    with open(PROG,"a") as f: f.write(line+"\n")

class Opac:
    def __init__(self):
        self.S=requests.Session(); self.S.headers["User-Agent"]=UA; self.jglo=None; self.total=None
    def _sleep(self): time.sleep(DELAY)
    def init_session(self):
        self._sleep()
        r=self.S.get(BASE+QPATH, timeout=120); r.raise_for_status()
        m=re.search(r'JGLO\.init\((\{[^)]*\})\)', r.text)
        if not m: raise RuntimeError("no JGLO in list page")
        self.jglo=m.group(1)
        t=re.search(r'Risultati\s*<span>\d+</span>\s*-\s*<span>\d+</span>\s*di\s*<span>(\d+)</span>', r.text)
        self.total=int(t.group(1)) if t else None
        log(f"session init: total={self.total} jglo={self.jglo}")
        if SORT and SORT!="Ranking":
            h=self.dwr("A","a10m03",[SORT])
            if not h: raise RuntimeError("sort failed")
            log(f"sorted by {SORT}")
        return r.text
    def dwr(self, script, method, params, retries=3):
        body=["callCount=1", f"page={QPATH}", "httpSessionId=", f"scriptSessionId=F06EEE08B86C956A7BD2D48F091F2168{random.randint(100,999)}", f"c0-scriptName={script}", f"c0-methodName={method}", "c0-id=0"]
        for i,p in enumerate(params):
            if p is None: body.append(f"c0-param{i}=null:null")
            elif isinstance(p,int): body.append(f"c0-param{i}=number:{p}")
            else: body.append(f"c0-param{i}=string:{requests.utils.quote(p)}")
        body.append("batchId=0")
        data=("\n".join(body)+"\n").encode()
        for attempt in range(retries):
            self._sleep()
            try:
                r=self.S.post(f"{BASE}/SebinaOpac/dwr/call/plaincall/{script}.{method}.dwr", data=data, headers={"Content-Type":"text/plain","jglo":self.jglo,"Origin":BASE,"Referer":BASE+QPATH}, timeout=120)
            except Exception as e:
                log(f"  net error {script}.{method}{params}: {e}; retry {attempt+1}"); time.sleep(5*(attempt+1)); continue
            if r.status_code!=200:
                log(f"  http {r.status_code} {script}.{method}{params}; retry {attempt+1}"); time.sleep(10*(attempt+1)); continue
            if "_remoteHandleException" in r.text or "_remoteHandleBatchException" in r.text:
                log(f"  DWR exception {script}.{method}{params}: {r.text[-200:].strip()}"); return None
            h=dwr_html(r.text)
            return h if h is not None else ""
        return None

def parse_list(h):
    items=[]
    for m in re.finditer(r'<li[^>]*class="[^"]*documento[^"]*"[^>]*id="listadocumenti_(\d+)"[^>]*data-idopac="([^"]+)"', h):
        items.append((int(m.group(1)), m.group(2)))
    stat=re.search(r'da\s+([\d.]+)\s+a\s+([\d.]+)\s+di\s+([\d.]+)', h)
    return items, (stat.group(0) if stat else None)

def strip(s): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',s))).strip()

def parse_unimarc(h):
    fields=[]
    for m in re.finditer(r"<span class=rosso>(\d{3})</span></b>&nbsp;</td><td class=testo align=left>(.*?)</td>", h, re.S):
        tag=m.group(1); raw=html.unescape(m.group(2)).replace('\xa0',' ')
        if tag<"010":
            fields.append({"tag":tag,"ind":"","subfields":[],"value":raw.strip()}); continue
        ind=raw[:3].replace('_',' ') if '$' in raw else ''
        body=raw[raw.find('$'):] if '$' in raw else raw
        subs=[(p[0],p[1:]) for p in body.split('$')[1:] if p]
        fields.append({"tag":tag,"ind":ind.strip(),"subfields":subs})
    guida=re.search(r'<b>Guida:</b>&nbsp;&nbsp;([^<]*)', h)
    return fields, (guida.group(1).strip() if guida else None)

def sf(f, code): return [v for c,v in f["subfields"] if c==code]
def ctrl(fields, tag):
    for f in fields:
        if f["tag"]==tag and f.get("value"): return f["value"]
    return None
def first(fields, tag, code):
    for f in fields:
        if f["tag"]==tag:
            v=sf(f,code)
            if v: return v[0].strip()
    return None

def parse_holdings(h):
    """BUB holdings blocks from the tabloca detail html."""
    out=[]
    for m in re.finditer(r'<div id="([^"]*)" class="inventario"\s*>(.*?)(?=<div id="[^"]*" class="inventario"|<div class="biblioteca">|<div id="fine_localizzazioni"|$)', h, re.S):
        blk=m.group(2); d={"block_id":m.group(1)}
        a=re.search(r'inventario-disponibilita">(.*?)</p>', blk, re.S)
        if a: d["availability"]=strip(a.group(1))
        for tr in re.finditer(r'<td><span class="campo">(.*?)</span></td>\s*<td>(.*?)</td>', blk, re.S):
            d[strip(tr.group(1)).lower()]=strip(tr.group(2))
        for dv in re.finditer(r'<span class="campo">(.*?)</span>\s*<span class="valore">(.*?)</span>', blk, re.S):
            d[strip(dv.group(1)).lower()]=strip(dv.group(2))
        p=re.search(r'<span class="campo">Provenienza</span></div>\s*<div>(.*?)</div>', blk, re.S)
        if p: d["provenienza"]=strip(p.group(1))
        out.append(d)
    return out

def build_record(rid, idx, page, fields, guida, holdings, detail_html):
    def all_(tag, code): 
        return [v.strip() for f in fields if f["tag"]==tag for v in sf(f,code)]
    def bub_notes(tag):
        return [ "".join(v for c,v in f["subfields"] if c=="a").strip() for f in fields if f["tag"]==tag and any(c=="5" and "IT-BO0098" in v for c,v in f["subfields"])]
    d100=first(fields,"100","a") or ""
    year=None
    if len(d100)>=13:
        y=d100[9:13].strip()
        if re.fullmatch(r'\d{4}',y): year=int(y)
    if year is None:
        y=re.search(r'(1[5-9]\d\d|20\d\d)', first(fields,"210","d") or ""); year=int(y.group(1)) if y else None
    persons=[]
    for f in fields:
        if f["tag"] in ("700","701","702"):
            name=", ".join(x for x in [first([f],f["tag"],"a"), first([f],f["tag"],"b")] if x)
            persons.append({"tag":f["tag"],"name":name,"dates":first([f],f["tag"],"f"),"role":first([f],f["tag"],"4"),"bub_only":any(c=="5" for c,_ in f["subfields"])})
    corp=[", ".join(x for x in [first([f],f["tag"],"a"), first([f],f["tag"],"b")] if x) for f in fields if f["tag"] in ("710","711","712")]
    bub950=[f for f in fields if f["tag"]=="950" and "UNIVERSITARIA" in (first([f],"950","a") or "")]
    inv=[re.sub(r'\s+',' ',v).strip() for f in bub950 for v in sf(f,"e")]
    shelf=[re.sub(r'\s+',' ',v).strip() for f in bub950 for v in sf(f,"d")]
    hold_shelf=[h.get("collocazione") for h in holdings if h.get("collocazione")]
    hold_inv=[h.get("inventario") for h in holdings if h.get("inventario")]
    series=[]
    for f in fields:
        if f["tag"]=="410":
            t=first([f],"410","a"); v=first([f],"410","v"); series.append((t or "")+(f" ; {v}" if v else ""))
    subjects=[" - ".join([first([f],"606","a") or ""]+sf(f,"x")) for f in fields if f["tag"]=="606"]
    title_h=re.search(r'<h3 class="titololistarisultati">.*?<a[^>]*>(.*?)</a>', detail_html, re.S)
    rec={
        "id":rid, "permalink":f"{BASE}/SebinaOpac/resource/{rid}",
        "list_page":page, "list_index":idx, "sort":SORT,
        "title":first(fields,"200","a"), "title_full":" ".join(v.strip() for f in fields if f["tag"]=="200" for c,v in f["subfields"] if c in "aehi") or None,
        "responsibility":first(fields,"200","f"), "responsibility_other":all_("200","g"),
        "edition":first(fields,"205","a"),
        "place":all_("210","a"), "publisher":all_("210","c"), "date_210":first(fields,"210","d"),
        "year":year, "date_raw_100":d100 or None,
        "language":all_("101","a"), "language_original":all_("101","c"), "country":first(fields,"102","a"),
        "isbn":all_("010","a"), "sbn_bid":first(fields,"017","a") or ctrl(fields,"001"), "oclc":all_("035","a"),
        "physical":" ; ".join([ " ".join(x for x in [first([f],"215","a"),first([f],"215","c"),first([f],"215","d")] if x) for f in fields if f["tag"]=="215"]) or None,
        "series":series, "subjects":subjects, "dewey":all_("676","a"), "dewey_label":all_("676","c"),
        "persons":persons, "corporate":corp,
        "author":next((p["name"] for p in persons if p["tag"]=="700"), None),
        "notes_general":all_("300","a"),
        "bub_copy_note_316":bub_notes("316"), "bub_provenance_317":bub_notes("317"), "bub_annotation_318":bub_notes("318"),
        "bub_inventory":inv or hold_inv, "bub_inventory_numbers":[t.split()[1] for t in inv if len(t.split())>1] or hold_inv, "bub_shelfmark":shelf or hold_shelf,
        "bub_holdings":holdings,
        "holdings_libraries":[first([f],"899","a") for f in fields if f["tag"]=="899"],
        "leader":guida, "unimarc":[{"tag":f["tag"],"ind":f["ind"],"sub":f["subfields"]} if f["subfields"] else {"tag":f["tag"],"value":f.get("value")} for f in fields],
        "harvested":datetime.datetime.utcnow().isoformat(timespec="seconds")+"Z",
    }
    return rec

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    done=set()
    if os.path.exists(JSONL):
        with open(JSONL) as f:
            for line in f:
                try: done.add(json.loads(line)["id"])
                except Exception: pass
    start_page=int(os.environ.get("START_PAGE","1"))
    log(f"start: {len(done)} records already in {JSONL}; start_page={start_page}")
    o=Opac(); first_html=o.init_session()
    total=o.total or 3047; npages=(total+PAGE_SIZE-1)//PAGE_SIZE
    if os.environ.get("MAX_PAGES"): npages=min(npages, start_page-1+int(os.environ["MAX_PAGES"]))
    out=open(JSONL,"a")
    consecutive_fail=0
    page=start_page
    while page<=npages:
        h=o.dwr("A","a10m01",[page])
        if h is None or not h:
            consecutive_fail+=1; log(f"page {page}: list fetch failed ({consecutive_fail}); re-init session")
            if consecutive_fail>5: log("too many failures; abort"); break
            time.sleep(20); o.init_session(); continue
        items,stat=parse_list(h)
        if not items:
            consecutive_fail+=1; log(f"page {page}: no items parsed (stat={stat}); re-init")
            if consecutive_fail>5: break
            time.sleep(20); o.init_session(); continue
        consecutive_fail=0
        todo=[(i,r) for i,r in items if r not in done]
        log(f"page {page}/{npages} [{stat}] items={len(items)} new={len(todo)}")
        for idx,rid in todo:
            det=o.dwr("A","a20m00",[idx,"tabloca","UBOBU"])
            if det is None:
                log(f"  {rid}: detail failed; re-init and retry once"); o.init_session(); o.dwr("A","a10m01",[page]); det=o.dwr("A","a20m00",[idx,"tabloca","UBOBU"])
                if det is None: log(f"  {rid}: detail failed twice; skipping"); continue
            if f'resource/{rid}' not in det:
                log(f"  {rid}: detail does not reference id (index drift?); re-init"); o.init_session(); o.dwr("A","a10m01",[page]); det=o.dwr("A","a20m00",[idx,"tabloca","UBOBU"]) or ""
                if f'resource/{rid}' not in det: log(f"  {rid}: still mismatched; skipping"); continue
            um=o.dwr("A","a20m01b",["tabunimarc",None])
            if not um:
                log(f"  {rid}: unimarc failed; skipping"); continue
            fields,guida=parse_unimarc(um)
            if ctrl(fields,"001")!=rid:
                log(f"  {rid}: unimarc 001 mismatch ({[f.get('value') for f in fields if f['tag']=='001']}); skipping"); continue
            rec=build_record(rid, idx, page, fields, guida, parse_holdings(det), det)
            out.write(json.dumps(rec, ensure_ascii=False)+"\n"); out.flush()
            done.add(rid)
        log(f"page {page} done; total records={len(done)}")
        page+=1
    out.close()
    log(f"finished: {len(done)} records")

if __name__=="__main__":
    main()
