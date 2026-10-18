"""One-off: convert the STEMI / NSTE-ACS / heart-failure sample pages into topic folders.
Run once; afterwards the topic folders are the source of truth."""
import re, sys, pathlib, yaml
from bs4 import BeautifulSoup

ROOT = pathlib.Path(__file__).resolve().parents[1]
SAMPLE = pathlib.Path('/home/claude/sample')
sources = yaml.safe_load((ROOT / 'sources.yaml').read_text())
url2key = {v['url']: k for k, v in sources.items()}

def clean(html, idmap):
    for a, b in [('⁺', '<sup>+</sup>'), ('₂', '<sub>2</sub>'), ('′', "'"), ('▼', '↓')]:
        html = html.replace(a, b)
    def href(m):
        u = m.group(1)
        if u in url2key: return f'href="src:{url2key[u]}"'
        if u.startswith('#') and u[1:] in idmap: return f'href="{idmap[u[1:]]}"'
        return m.group(0)
    html = re.sub(r'href="([^"]+)"', href, html)
    html = html.replace('<p style="margin-top:2mm;color:#475467">', '<p class="note">')
    html = re.sub(r'<div class="bh" style="[^"]*">', '<div class="bh">', html)
    html = re.sub(r'\s*color:#[0-9a-fA-F]{3,6};?', '', html)
    html = re.sub(r' style=""', '', html)
    unknown = sorted(set(re.findall(r'href="(https?://[^"]+)"', html)))
    for u in unknown: print('  WARNING: url not in sources.yaml:', u)
    return html.strip() + '\n'

def inner(sec, editor=False):
    for sel in ['.toc', '.topbar', 'table.hdr', '.runhead', '.foot']:
        for el in sec.select(sel): el.decompose()
    if editor:
        for el in sec.select('h2, p.legend'): el.decompose()
    return sec.decode_contents()

def sheet(content, **attrs):
    a = ''.join(f' data-{k}="{v}"' for k, v in attrs.items() if v)
    return f'<div class="sheet"{a}>\n{content.strip()}\n</div>\n'

def write(topic, files):
    d = ROOT / 'topics' / 'cardiology' / topic
    d.mkdir(parents=True, exist_ok=True)
    for name, text in files.items():
        (d / name).write_text(text, encoding='utf-8')
    print('wrote', d)

def load(fn):
    return BeautifulSoup((SAMPLE / fn).read_text(encoding='utf-8'), 'html.parser')

# ---------------- STEMI ----------------
s = load('stemi-protocol.html')
idmap = {'acute-stemi': '@acute:stemi', 'ref-stemi': '@ref:stemi', 'contents': '#contents'}
write('stemi', {
  'acute.html': clean(sheet(inner(s.find(id='acute-stemi'))), idmap),
  'reference.html': clean(sheet(inner(s.find(id='ref-stemi')),
                                subtitle='Diagnosis, reperfusion at a non-PCI regional hospital, and after'), idmap),
  'editor.html': clean(inner(s.find(id='editor'), editor=True), idmap),
})

# ---------------- NSTE-ACS ----------------
s = load('nste.html')
idmap = {'acute-nste': '@acute:nste-acs', 'ref-nste': '@ref:nste-acs', 'contents': '#contents'}
acute = inner(s.find(id='acute-nste')).replace(
    'manage HF as in the heart failure topic', 'manage HF as in the <a href="@ref:heart-failure">heart failure topic</a>')
write('nste-acs', {
  'acute.html': clean(sheet(acute), idmap),
  'reference.html': clean(sheet(inner(s.find(id='ref-nste')),
                                subtitle='Diagnosis, risk, and invasive timing from a non-PCI regional hospital'), idmap),
  'editor.html': clean(inner(s.find(id='editor'), editor=True), idmap),
})

# ---------------- Heart failure ----------------
s = load('hf.html')
idmap = {'acute-hf': '@acute:heart-failure', 'acute-hf2': '@acute:heart-failure#p2',
         'ref-hf': '@ref:heart-failure', 'ref-hfref': '@ref:heart-failure#hfref',
         'ref-card': '@ref:heart-failure#card', 'ref-hfpef': '@ref:heart-failure#hfpef', 'contents': '#contents'}
a1 = inner(s.find(id='acute-hf')).replace('poor response after the dose has been doubled (page 2)',
                                          'poor response after the dose has been doubled (page 2 of 2)')
a2 = inner(s.find(id='acute-hf2')).replace('(dose box, page 1, for maximum)', '(dose box, page 1 of 2, for maximum)') \
                                  .replace('tertiary box, page 1)', 'tertiary box, page 1 of 2)')
r2 = inner(s.find(id='ref-hfref')).replace(
    '(<a href="#acute-hf2">I NEED HELP</a>, p.&nbsp;<a class="pg" href="#acute-hf2"></a>)',
    '(<a href="#acute-hf2">I NEED HELP: Acute Handbook</a>)').replace(
    '(<a href="#acute-hf2">I NEED HELP</a>, p.\xa0<a class="pg" href="#acute-hf2"></a>)',
    '(<a href="#acute-hf2">I NEED HELP: Acute Handbook</a>)')
write('heart-failure', {
  'acute.html': clean(sheet(a1, part='1 of 2') + sheet(a2, part='2 of 2', anchor='p2'), idmap),
  'reference.html': clean(
      sheet(inner(s.find(id='ref-hf')), subtitle='1 · Definitions, diagnosis and causes') +
      sheet(r2, subtitle='2 · HFrEF: foundational and additional medical therapy', anchor='hfref',
            toc='HFrEF: foundational and additional medical therapy') +
      sheet(inner(s.find(id='ref-card')), title='Clinic up-titration card: HFrEF',
            subtitle='3 · For PHC clinics and MOPD · can be printed on its own', anchor='card', cls='large',
            toc='Clinic up-titration card (PHC clinics and MOPD)') +
      sheet(inner(s.find(id='ref-hfpef')), subtitle='4 · HFpEF, self-care, and where the guidelines differ',
            anchor='hfpef', toc='HFpEF, self-care, and where the guidelines differ'), idmap),
  'editor.html': clean(inner(s.find(id='editor'), editor=True), idmap),
})
