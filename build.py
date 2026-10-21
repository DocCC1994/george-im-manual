#!/usr/bin/env python3
"""Build the George Hospital IM Acute Handbook and Reference Manual.

    python3 build.py                 all draft outputs (both books, combined, editor report)
    python3 build.py --topic stemi   one-topic preview (both books + editor notes)
    python3 build.py --release       final version: refuses while any CHECK/DECISION or unsigned topic remains
    python3 build.py --zip           also zip the source folder (to keep a copy outside this workspace)

Topic files live in topics/<system>/<topic>/ (topic.yaml, acute.html, reference.html, editor.html).
The page shell (running header, title band, footer, page numbers, watermark, contents) is added here,
so topic files hold content only. See README.md for the authoring conventions.
"""
import argparse, datetime, html, pathlib, re, sys, zipfile
import yaml
from bs4 import BeautifulSoup, NavigableString
from weasyprint import HTML

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / 'out'
PREFIX = {'acute': 'acute', 'reference': 'ref', 'editor': 'editor'}
BOOK_OF_PREFIX = {'acute': 'acute', 'ref': 'reference', 'editor': 'editor'}
DRAFT_WM = 'DRAFT FOR REVIEW · NOT FOR CLINICAL USE'
STATUS_LABEL = {'planned': 'Planned', 'draft': 'Draft', 'review': 'Under review', 'signed-off': 'Signed off'}


class Log:
    def __init__(self): self.warnings, self.errors, self.notes = [], [], []
    def warn(self, m):
        if m not in self.warnings: self.warnings.append(m)
    def error(self, m):
        if m not in self.errors: self.errors.append(m)


LOG = Log()
esc = html.escape


# ---------------------------------------------------------------- loading
def load():
    manifest = yaml.safe_load((ROOT / 'manifest.yaml').read_text(encoding='utf-8'))
    sources = yaml.safe_load((ROOT / 'sources.yaml').read_text(encoding='utf-8'))
    topics = []
    for system in manifest['systems']:
        for entry in system['topics']:
            meta = {'id': entry} if isinstance(entry, str) else dict(entry)
            meta.update(system=system['id'], system_name=system['name'])
            folder = ROOT / 'topics' / system['id'] / meta['id']
            if (folder / 'topic.yaml').exists():
                meta.update(yaml.safe_load((folder / 'topic.yaml').read_text(encoding='utf-8')) or {})
                meta['folder'] = folder
                for f in ('title', 'status', 'author', 'section_editor', 'version'):
                    if not meta.get(f): LOG.error(f"{meta['id']}: topic.yaml is missing '{f}'")
                if meta.get('status') not in ('draft', 'review', 'signed-off'):
                    LOG.error(f"{meta['id']}: status must be draft, review or signed-off")
                meta['sheets'] = {b: read_sheets(meta, b) for b in ('acute', 'reference')}
                ed = folder / 'editor.html'
                meta['editor_html'] = ed.read_text(encoding='utf-8') if ed.exists() else ''
            else:
                meta['status'] = 'planned'
                meta.setdefault('title', meta['id'])
                meta['sheets'] = {'acute': [], 'reference': []}
            topics.append(meta)
    return manifest, sources, topics


def read_sheets(topic, book):
    f = topic['folder'] / f'{book}.html'
    if not f.exists():
        return []
    soup = BeautifulSoup(f.read_text(encoding='utf-8'), 'html.parser')
    divs = [d for d in soup.find_all('div', recursive=False) if 'sheet' in (d.get('class') or [])]
    raw = [({}, str(soup))] if not divs else \
          [({k[5:]: v for k, v in d.attrs.items() if k.startswith('data-')}, d.decode_contents()) for d in divs]
    sheets = []
    for i, (attrs, body) in enumerate(raw):
        anchor = attrs.get('anchor') or (str(i + 1) if i else '')
        sid = f"{PREFIX[book]}-{topic['id']}" + (f'-{anchor}' if anchor else '')
        if book == 'acute' and attrs.get('subtitle'):
            LOG.warn(f"{topic['id']}: subtitle dropped from an Acute Handbook page (house rule: no acute subtitles)")
            attrs.pop('subtitle')
        sheets.append({'id': sid, 'attrs': attrs, 'html': body, 'index': i})
        lint(topic['id'], book, body)
    return sheets


LATIN = re.compile(r'\b(bd|b\.d\.|tds|t\.d\.s\.|qid|q\.i\.d\.|nocte|mane|prn|stat|PO|od|o\.d\.|\d+-hourly)\b')


def lint(topic_id, book, body):
    """House notation: no Latin abbreviations; frequencies written as 12hrly, 8hrly."""
    text = BeautifulSoup(body, 'html.parser').get_text(' ')
    for m in sorted(set(LATIN.findall(text))):
        LOG.warn(f'{topic_id}/{book}: notation "{m}" found; house style is 12hrly / 8hrly / at night / orally / as needed')


def book_title(topic, book):
    return topic.get(f'{book}_title') or topic['title']


# ---------------------------------------------------------------- links
REF_RE = re.compile(r'^@(acute|ref|editor):([\w-]+)(?:#([\w-]+))?$')


def resolve_links(fragment, sources, known_ids, where):
    """src:key -> URL; @book:topic#anchor -> internal link, or plain text if the target isn't in this output."""
    soup = BeautifulSoup(fragment, 'html.parser')
    for a in soup.find_all('a', href=True):
        h = a['href']
        if h.startswith('src:'):
            key = h[4:]
            if key in sources:
                a['href'] = sources[key]['url']
            else:
                LOG.error(f'{where}: unknown source key "{key}" (add it to sources.yaml)')
        elif h.startswith('@'):
            m = REF_RE.match(h)
            if not m:
                LOG.error(f'{where}: bad cross-reference "{h}"'); continue
            target = f'{m[1]}-{m[2]}' + (f'-{m[3]}' if m[3] else '')
            if target in known_ids:
                a['href'] = '#' + target
            else:
                if target not in ALL_IDS:
                    LOG.warn(f'{where}: link to "{h}", which does not exist yet; shown as plain text')
                cls = a.get('class') or []
                if 'pg' in cls:
                    a.replace_with(NavigableString('the other book'))
                else:
                    a.name = 'span'; del a['href']; a['class'] = cls + ['xref-off']
    return str(soup)


# ---------------------------------------------------------------- markers (CHECK / DECISION)
def where_of(el):
    box = el.find_parent(class_=['box', 'card'])
    if box and box.find(class_='bh'):
        return box.find(class_='bh').get_text(' ', strip=True)
    tr = el.find_parent('tr')
    while tr is not None:
        th = tr.find('th', recursive=False)
        if th and tr.find_parent('table', class_='rows'):
            return th.get_text(' ', strip=True).capitalize()
        tr = tr.find_parent('tr')
    h = el.find_previous('h3')
    return h.get_text(' ', strip=True) if h else ''


def harvest(topic):
    found = []
    for book in ('acute', 'reference'):
        for sh in topic['sheets'][book]:
            soup = BeautifulSoup(sh['html'], 'html.parser')
            for el in soup.select('span.chk, span.dec'):
                kind = 'CHECK' if 'chk' in el['class'] else 'DECISION'
                flat = lambda n: re.sub(r'\s+', ' ', n.get_text()).strip()
                text = re.sub(r'^(CHECK|DECISION)\s*:?\s*', '', flat(el))
                parent = el.find_parent(['li', 'td', 'p', 'th']) or el.parent
                ctx = flat(parent).replace(flat(el), '…').strip()
                if parent.name == 'td' and not parent.find_parent('table', class_='rows'):
                    first = parent.find_parent('tr').find(['td', 'th'])
                    if first is not None and first is not parent:
                        ctx = f'{flat(first)}: {ctx}'
                if len(ctx) > 170: ctx = ctx[:167].rsplit(' ', 1)[0] + ' …'
                found.append({'book': 'Acute' if book == 'acute' else 'Reference', 'kind': kind,
                              'text': text or '(no detail)', 'where': where_of(el), 'context': ctx})
    return found


# ---------------------------------------------------------------- page pieces
def foot(manifest, topic, book_name, sheet_title):
    parts = [f"Author: <b>{esc(topic['author'])}</b>", f"Section editor: <b>{esc(topic['section_editor'])}</b>"]
    if topic.get('editors'): parts.append(f"Editors: <b>{esc(topic['editors'])}</b>")
    if topic.get('co_reviewer'): parts.append(f"Reviewed with: <b>{esc(topic['co_reviewer'])}</b>")
    if topic.get('based_on'): parts.append(f"Based on {esc(topic['based_on'])}")
    parts.append(f"{esc(topic['version'])} · Reviewed {esc(topic.get('reviewed', '[MM/YYYY]'))}")
    approval = (f"Approved by: <b>{esc(topic.get('approved_by') or '[Name]')}</b> · "
                f"Level/rank: <b>{esc(topic.get('approved_rank') or '[Rank]')}</b> · "
                f"Date: <b>{esc(topic.get('approved_date') or '[DD/MM/YYYY]')}</b>")
    subject = f"Suggest an edit: {book_name} – {sheet_title}"
    from urllib.parse import quote
    mail = f"mailto:{manifest['editor_email']}?subject={quote(subject)}"
    return (f'<div class="foot"><div class="who">{" · ".join(parts)}<div class="appr">{approval}</div></div>'
            f'<span><a class="btn" href="{mail}">Suggest an edit</a></span></div>')


def meta_row(topic):
    return (f'<tr><td class="meta"><span>Version: {esc(topic["version"])}</span>'
            f'<span>Effective date: {esc(topic.get("effective", "[MM/YYYY]"))}</span>'
            f'<span>Review date: {esc(topic.get("review", "[MM/YYYY]"))}</span></td></tr>')


def bm(level, label):
    return f'<div class="bm" style="bookmark-level:{level}">{esc(label)}</div>' if level else ''


def render_sheet(manifest, sources, known_ids, topic, book, sh, bm_base, first_in_system):
    a = sh['attrs']
    title = a.get('title') or book_title(topic, book)
    if a.get('part'): title += f" ({a['part']})"
    subtitle = a.get('subtitle', '')
    bname = manifest['books'][book]['name']
    runhead = f"{manifest['books'][book]['runhead']} · {topic['system_name'].upper()}"
    marks = ''
    if first_in_system and sh['index'] == 0: marks += bm(bm_base, topic['system_name'])
    if sh['index'] == 0: marks += bm(bm_base + 1, book_title(topic, book))
    elif a.get('toc'): marks += bm(bm_base + 2, a['toc'])
    body = resolve_links(sh['html'], sources, known_ids, f"{topic['id']}/{book}")
    classes = ' '.join(['sheet', book] + a.get('cls', '').split())
    band = esc(title) + (f'<small>{esc(subtitle)}</small>' if subtitle else '')
    return f'''
<section class="{classes}" id="{sh['id']}">
<div class="runhead">{esc(runhead)}</div>{marks}
<div class="toc-link"><a href="#contents">Back to contents</a></div>
<table class="hdr"><tr><td class="h1">{band}</td></tr>{meta_row(topic)}</table>
{body}
{foot(manifest, topic, bname, title)}
</section>'''


def cover(manifest, label, draft):
    d = f'<div class="draft">{DRAFT_WM}</div>' if draft else ''
    return f'''
<section class="cover">
<div class="frame"><div class="band"><div class="k">{esc(manifest['hospital'].upper())} · {esc(manifest['department'].upper())}</div>
<div class="t">{esc(label.upper())}</div></div>
<div class="meta"><span>{esc(manifest['edition'])}</span><span>Version {esc(manifest['version'])}</span></div></div>
<img class="logo" src="assets/george_im_logo.jpg" alt="George Hospital Internal Medicine">
{d}
<div class="dept">{esc(manifest['hospital'])} · {esc(manifest['department'])}</div>
</section>'''


def front_page(manifest, title, inner, draft, runhead, page_id=None):
    wm = f'<div class="wm">{DRAFT_WM}</div>' if draft else '<div class="wm"> </div>'
    pid = f' id="{page_id}"' if page_id else ''
    return f'''
<section class="sheet front"{pid}>
<div class="runhead">{esc(runhead)}</div>{wm}
<table class="hdr"><tr><td class="h1">{esc(title)}</td></tr>
<tr><td class="meta"><span>{esc(manifest['edition'])} · Version {esc(manifest['version'])}</span>{'<span>Draft for review</span>' if draft else ''}</td></tr></table>
{inner}
</section>'''


def contents_table(manifest, topics, books, draft):
    rows = []
    for book in books:
        if len(books) > 1:
            rows.append(f'<tr class="part"><td colspan="{3 if draft else 2}">{esc(manifest["books"][book]["name"])}</td></tr>')
        for sysid in dict.fromkeys(t['system'] for t in topics):
            ts = [t for t in topics if t['system'] == sysid and t['sheets'][book]]
            if not ts: continue
            rows.append(f'<tr class="sys"><td colspan="{3 if draft else 2}">{esc(ts[0]["system_name"])}</td></tr>')
            for t in ts:
                first = t['sheets'][book][0]
                st = f'<td class="st">{STATUS_LABEL[t["status"]]}</td>' if draft else ''
                rows.append(f'<tr><td class="name"><a href="#{first["id"]}">{esc(book_title(t, book))}</a></td>{st}'
                            f'<td class="pg"><a class="pg" href="#{first["id"]}"></a></td></tr>')
                for sh in t['sheets'][book][1:]:
                    if sh['attrs'].get('toc'):
                        st = '<td class="st"></td>' if draft else ''
                        rows.append(f'<tr class="sub"><td class="name"><a href="#{sh["id"]}">{esc(sh["attrs"]["toc"])}</a></td>{st}'
                                    f'<td class="pg"><a class="pg" href="#{sh["id"]}"></a></td></tr>')
    head = '<tr><td><b>Topic</b></td>' + ('<td class="st"><b>Status</b></td>' if draft else '') + '<td class="pg"><b>Page</b></td></tr>'
    return f'<h3>Contents</h3><table class="toc">{head}{"".join(rows)}</table>'


def divider(label, sub, level):
    return f'''
<section class="divider">{bm(level, label)}<div class="frame"><div class="band">{esc(label)}</div>
<div class="sub">{esc(sub)}</div></div></section>'''


def document(body, title):
    return f'''<!doctype html><html lang="en-ZA"><head><meta charset="utf-8"><title>{esc(title)}</title>
<link rel="stylesheet" href="style/house.css"></head><body>{body}</body></html>'''


# ---------------------------------------------------------------- outputs
ALL_IDS = set()


def build_book(manifest, sources, topics, books, label, draft, with_cover=True):
    known = {sh['id'] for t in topics for b in books for sh in t['sheets'][b]}
    parts = []
    if with_cover: parts.append(cover(manifest, label, draft))
    howto = (ROOT / 'templates' / 'howto.html').read_text(encoding='utf-8')
    runhead = f"{manifest['hospital'].upper()}: {manifest['department'].upper()}"
    parts.append(front_page(manifest, label, contents_table(manifest, topics, books, draft), draft, runhead, 'contents'))
    parts.append(front_page(manifest, 'How to read this book', howto, draft, runhead))
    acks = (ROOT / 'templates' / 'acknowledgements.html').read_text(encoding='utf-8')
    parts.append(front_page(manifest, 'Acknowledgements and authorship', acks, draft, runhead))
    for book in books:
        base = 1
        if len(books) > 1:
            parts.append(divider(manifest['books'][book]['name'], f"{manifest['hospital']} · {manifest['edition']} · Version {manifest['version']}", 1))
            base = 2
        seen = set()
        for t in topics:
            for sh in t['sheets'][book]:
                first_sys = t['system'] not in seen
                seen.add(t['system'])
                parts.append(render_sheet(manifest, sources, known, t, book, sh, base, first_sys))
    return document(''.join(parts), label)


def build_editor_report(manifest, sources, topics, draft=True):
    today = datetime.date.today().strftime('%d %b %Y')
    built = [t for t in topics if t['status'] != 'planned']
    rows, total_c, total_d = [], 0, 0
    for i, t in enumerate(topics, 1):
        mk = t.get('markers', [])
        c = sum(m['kind'] == 'CHECK' for m in mk); d = len(mk) - c
        total_c += c; total_d += d
        rows.append(f'<tr><td class="n">{i}</td><td>{esc(t["system_name"])}</td><td>{esc(t["title"])}</td>'
                    f'<td>{esc(str(t.get("start", "")))}</td><td>{esc(str(t.get("priority", "")))}</td>'
                    f'<td>{STATUS_LABEL[t["status"]]}</td><td>{c if t["status"] != "planned" else ""}</td>'
                    f'<td>{d if t["status"] != "planned" else ""}</td><td>{esc(t.get("author", ""))}</td>'
                    f'<td>{esc(t.get("section_editor", ""))}</td></tr>')
    signed = sum(t['status'] == 'signed-off' for t in topics)
    summary = (f'<p><b>{len(built)} of {len(topics)}</b> topics drafted · <b>{signed}</b> signed off · '
               f'<b>{total_c}</b> CHECK and <b>{total_d}</b> DECISION markers open.</p>')
    progress = (summary + '<h3>Progress</h3><table class="t sm mk"><tr><th>#</th><th>System</th><th>Topic</th><th>Starting point</th>'
                '<th>Priority</th><th>Status</th><th>CHECK</th><th>DECISION</th><th>Author</th><th>Section editor</th></tr>'
                + ''.join(rows) + '</table>')
    runhead = f"{manifest['hospital'].upper()}: EDITOR REPORT"
    parts = [f'''
<section class="sheet front" id="contents">
<div class="runhead">{runhead}</div><div class="wm">EDITOR REPORT · NOT FOR CLINICAL USE</div>
<table class="hdr"><tr><td class="h1">Editor report: open questions and progress<small>Acute Handbook and Reference Manual · generated {today}</small></td></tr>
<tr><td class="meta"><span>{esc(manifest['edition'])} · Version {esc(manifest['version'])}</span></td></tr></table>
<p><span class="chk">CHECK</span> = a fact to confirm locally · <span class="dec">DECISION</span> = a choice for the section owner and HOD.
Send each consultant the pages for their topics; answers go back into the topic files.</p>
{progress}
</section>''']
    for t in built:
        mk = t['markers']
        def q(m):
            main = m['text'] if m['text'] != '(no detail)' else m['context']
            sub = m['context'] if m['text'] != '(no detail)' else ''
            return (f'<b>{esc(main)}</b><br><span style="font-size:90%">{esc(m["where"])}'
                    + (f': {esc(sub)}' if sub else '') + '</span>')
        trs = ''.join(f'<tr><td class="n">{j}</td><td>{m["book"]}</td><td class="ty">'
                      f'<span class="{"chk" if m["kind"] == "CHECK" else "dec"}">{m["kind"]}</span></td>'
                      f'<td>{q(m)}</td></tr>' for j, m in enumerate(mk, 1))
        ed = resolve_links(t['editor_html'], sources, set(), f"{t['id']}/editor")
        c = sum(m['kind'] == 'CHECK' for m in mk)
        parts.append(f'''
<section class="sheet ed-topic" id="editor-{t['id']}">
<div class="runhead">{runhead} · {esc(t['system_name'].upper())}</div>{bm(1, t['title'])}
<table class="hdr"><tr><td class="h1">{esc(t['title'])}<small>Status: {STATUS_LABEL[t['status']]} · Section editor: {esc(t['section_editor'])}</small></td></tr></table>
{f'<p class="note">{esc(t["note"])}</p>' if t.get('note') else ''}
<h3>Markers on the pages ({c} CHECK · {len(mk) - c} DECISION)</h3>
<table class="t mk"><tr><th>#</th><th>Book</th><th>Type</th><th>Question, and where it sits</th></tr>{trs}</table>
{ed}
</section>''')
    return document(''.join(parts), 'Editor report')


def render(html_text, out_pdf):
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    # static link check on the final HTML
    soup = BeautifulSoup(html_text, 'html.parser')
    ids = {el['id'] for el in soup.find_all(id=True)}
    for a in soup.find_all('a', href=True):
        if a['href'].startswith('#') and a['href'][1:] not in ids:
            LOG.error(f'{out_pdf.name}: broken internal link {a["href"]}')
    (OUT / 'html').mkdir(parents=True, exist_ok=True)
    (OUT / 'html' / (out_pdf.stem + '.html')).write_text(html_text, encoding='utf-8')
    doc = HTML(string=html_text, base_url=str(ROOT)).render()
    doc.write_pdf(out_pdf)
    return len(doc.pages)


def make_zip():
    stamp = datetime.date.today().strftime('%Y-%m-%d')
    z = OUT / f'manual-source-{stamp}.zip'
    with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as zf:
        for p in ROOT.rglob('*'):
            if p.is_file() and OUT not in p.parents and '__pycache__' not in p.parts:
                zf.write(p, p.relative_to(ROOT.parent))
    return z


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--topic'); ap.add_argument('--release', action='store_true'); ap.add_argument('--zip', action='store_true')
    args = ap.parse_args()
    manifest, sources, topics = load()
    for t in topics:
        t['markers'] = harvest(t) if t['status'] != 'planned' else []
        ALL_IDS.update(sh['id'] for b in ('acute', 'reference') for sh in t['sheets'][b])
    built = [t for t in topics if t['status'] != 'planned']
    draft = not args.release
    tag = f"{manifest['edition']} v{manifest['version']}"
    suffix = ' (draft)' if draft else ''

    if args.release:
        for t in built:
            if t['status'] != 'signed-off': LOG.error(f"{t['id']}: status is {t['status']}, not signed-off")
            if t['markers']: LOG.error(f"{t['id']}: {len(t['markers'])} CHECK/DECISION markers still open")
            for f in ('approved_by', 'approved_rank', 'approved_date'):
                if not t.get(f): LOG.error(f"{t['id']}: {f} is empty")
        for f in sorted((ROOT / 'templates').glob('*.html')):
            if re.search(r'class="(chk|dec)"', f.read_text(encoding='utf-8')):
                LOG.error(f'templates/{f.name}: CHECK/DECISION markers still open')
        if 'example.com' in manifest['editor_email']: LOG.error('manifest.yaml: editor_email is still a placeholder')
        if LOG.errors:
            print('RELEASE REFUSED:'); [print('  -', e) for e in LOG.errors]; sys.exit(1)

    results = []
    if args.topic:
        sel = [t for t in built if t['id'] == args.topic]
        if not sel: sys.exit(f'No built topic called {args.topic}')
        t = sel[0]
        out = OUT / 'preview' / f"{t['id']}.pdf"
        n = render(build_book(manifest, sources, sel, ('acute', 'reference'), t['short'] if t.get('short') else t['title'],
                              draft, with_cover=False), out)
        results.append((out, n))
    else:
        jobs = [
            (('acute',), manifest['books']['acute']['name'], f"George IM Acute Handbook {tag}{suffix}.pdf"),
            (('reference',), manifest['books']['reference']['name'], f"George IM Reference Manual {tag}{suffix}.pdf"),
            (('acute', 'reference'), 'Acute Handbook and Reference Manual', f"George IM Acute Handbook and Reference Manual {tag} - combined{suffix}.pdf"),
        ]
        for books, label, fname in jobs:
            out = OUT / fname
            results.append((out, render(build_book(manifest, sources, built, books, label, draft), out)))
        if draft:
            out = OUT / f"George IM Editor report {tag} ({datetime.date.today():%Y-%m-%d}).pdf"
            results.append((out, render(build_editor_report(manifest, sources, topics), out)))

    log = ['Build ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), '']
    log += [f'{p.name}: {n} pages' for p, n in results]
    total = sum(len(t['markers']) for t in built)
    log += ['', f'Topics: {len(built)} built of {len(topics)} planned · open markers: {total}']
    log += ['', f'Errors ({len(LOG.errors)}):'] + [f'  - {e}' for e in LOG.errors]
    log += ['', f'Warnings ({len(LOG.warnings)}):'] + [f'  - {w}' for w in LOG.warnings]
    if args.zip: log += ['', f'Source zip: {make_zip().name}']
    (OUT / 'build-log.txt').write_text('\n'.join(log), encoding='utf-8')
    print('\n'.join(log))
    sys.exit(1 if LOG.errors else 0)


if __name__ == '__main__':
    main()
