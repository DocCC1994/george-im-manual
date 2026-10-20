# George Hospital IM: Acute Handbook and Reference Manual (build system)

## Commands
```
python3 build.py                 # all draft PDFs: Acute Handbook, Reference Manual, combined, editor report
python3 build.py --topic stemi   # one-topic preview -> out/preview/stemi.pdf
python3 build.py --release       # final version; refused while any CHECK/DECISION or unsigned topic remains
python3 build.py --zip           # also zip the source folder (keep a copy outside the workspace)
```
Needs Python 3 with weasyprint, beautifulsoup4, pyyaml (and the Carlito font). Output goes to `out/`;
`out/build-log.txt` lists errors (broken links, unknown sources, missing fields) and warnings.

## Layout
```
manifest.yaml        order of systems and topics; planned topics (no folder yet) feed the progress table
sources.yaml         every external link, defined once; cite with href="src:<key>"
style/house.css      the house style (GRH protocol look)
templates/howto.html the "How to read this book" page
assets/              logo and images (reference as assets/<file>)
topics/<system>/<topic>/
    topic.yaml       title, status, author, section editor, version, dates, based_on
    acute.html       Acute Handbook page(s)
    reference.html   Reference Manual page(s)
    editor.html      change log and open questions (editor report only)
```

## topic.yaml
`title`, optional `acute_title` / `reference_title`, `short`, `status` (draft | review | signed-off), `version`,
`effective`, `review`, `reviewed`, `author`, `section_editor`, optional `editors`, `co_reviewer`, `based_on`, `note`.

## Writing a topic file
Content only: the build adds the running header, title band, version and dates row, footer, page numbers,
"Back to contents", watermark, bookmarks and contents entries.

One `<div class="sheet">` per printed page (a file with no sheet div is one sheet). Sheet attributes:
`data-part="1 of 2"` (added to the title), `data-subtitle` (Reference Manual only), `data-title` (override),
`data-anchor` (link target for later sheets), `data-toc` (adds a contents sub-entry), `data-cls` (`compact`, `large`).

Building blocks (see the cardiology topics for examples):
- Acute rows: `<table class="rows">` with `<th>RECOGNISE</th>`, INVESTIGATE, IMMEDIATE, ONGOING, REFER …
- Two columns: `<div class="cols"><div class="main">…</div><div class="side">…</div></div>`
- Side boxes: `<div class="box dose|tert|mit|local"><div class="bh">Dose box</div>…</div>` (named by the band)
- Section band `<h3>`; grid table `<table class="t">` (`t sm` = smaller); `.card`; stepped `.flow`;
  2x2 `table.prof`; traffic lights `table.tl` (`g`/`a`/`r` cells)
- Labels: `<span class="cls">I A</span>`, `<span class="avail y|s|n">EML</span>`, `<span class="cite">[…]</span>`
- Draft markers: `<span class="chk">CHECK …</span>`, `<span class="dec">DECISION …</span>` (harvested into the editor report)

Links:
- `href="src:stg-ch3"` → the URL in sources.yaml
- `href="@acute:stemi"`, `href="@ref:heart-failure#card"` → another topic or sheet; becomes plain text when the
  target is in the other book (separate-book PDFs) or not written yet
- `<a class="pg" href="@ref:heart-failure#hfpef"></a>` → that sheet's page number (same book only)

## House rules
- Acute Handbook pages have no subtitle and each sheet fits one page (use `data-part` for a second page).
- Length: 1–2 pages per topic in the Acute Handbook and 1–2 in the Reference Manual. If a topic cannot fit,
  propose splitting it into separate topics rather than running long.
- Only CHECK and DECISION are in colour; everything else is black, white or grey.
- Write K<sup>+</sup>, SpO<sub>2</sub> with `<sup>`/`<sub>`; avoid ▲ ▼ ′ (not in Carlito): use ↓ and '.
- No Latin abbreviations: 12hrly, 8hrly, 4hrly (not bd/tds/12-hourly); "at night" (not nocte); "orally" (not PO);
  "as needed" (not prn); "now" or "immediately" (not stat). IV, IM, SC and SL are fine. The build warns on any it finds.
- Drug naming: lead with the drug class, then the agent in brackets, e.g. "3rd-gen cephalosporin (ceftriaxone)", never
  the agent alone. Where there are alternatives, give the George first-choice agent in full as the first option and
  list the alternatives by class only (e.g. "alternatives: FQ, carbapenem"), so the book transfers to other
  formularies. If the George first-choice agent is not clear from the STG or the old GRH protocol, name the most
  likely agent and add a CHECK.
  Give the class once per topic (once in each of the acute and reference pages); after that, use the agent alone
  (the EML name), e.g. "LMWH (enoxaparin)" first, then "enoxaparin". If an alternative is a different type of drug,
  name it with its own class and agent, e.g. "ARB (losartan)" or "alteplase" vs "streptokinase".
- Abbreviations: use standard ones from the start without spelling them out (3rd-gen, LMWH, UFH, DOAC, ACEi, ARB, BB,
  CCB, FQ, PPI, SGLT2i). Only use ones any SA registrar would recognise immediately.
- The book is for doctors. Include a nursing instruction only when it changes the patient's outcome
  (for example, hourly glucose during an insulin infusion), never routine ward care.
- Every topic carries an approval line (approved_by, approved_rank, approved_date in topic.yaml); the release build
  refuses while any is empty.
- An abbreviations page is added at the end of the project.
- Base: where a current GRH protocol exists for the topic, build on it, then check and update it against the
  evidence order below; flag every difference as a DECISION.
- Evidence order: SA STG/EML or another official, current SA guideline; then European guidelines (ESC, ESH, EASL,
  ERS, etc.), preferred over American ones where no SA guideline is official or up to date; then other international
  guidelines. Without a current GRH protocol, an old one informs local practice only.
- Guideline PDFs: before writing a topic, ask the owner in that topic's thread for the PDF of each relevant
  guideline other than the SA STG/EML, European first (full title, issuing body and year). He uploads it into that
  thread so it is
  read only for that topic. The STG/EML 2024 (updated Dec 2025) is already in
  /mnt/project-files/sources/stg-eml-2024/ and is never requested.

## Workflow
draft → review (section editor has the editor-report pages) → signed-off (all markers resolved).
`--release` builds only when every included topic is signed off and no markers remain; it drops the watermark.
