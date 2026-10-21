# CLAUDE.md: George Hospital IM manual (read this first in every session)

## What this project is
Two books for the Internal Medicine department, George Hospital (Western Cape, South Africa), modelled on the
MGH Housestaff Manual ("White Book"), adapted to South African public-sector resources:
- **Acute Handbook**: quick referral, Paarl-style; 1–2 printed pages per topic; what to do in the first hours.
- **Reference Manual**: MGH-style; deeper background, where guidelines differ, linked citations.
Both are built from one source (see README.md for commands, layout and building blocks).

Owner: an internal medicine registrar at George (Tygerberg post). **The owner wants to remain the thinker and
learn from the process.** Claude drafts and speeds things up; clinical decisions go to the owner and section
editors as DECISION markers, not silent choices.

## Approved house style (do not change without asking)
- GRH protocol look: Carlito font (Calibri twin), thin black grid borders, grey header bands, black/white/grey only.
  Only CHECK (amber) and DECISION (red) markers are coloured; they are removed before release.
- Small running header top-left: "GEORGE HOSPITAL: ACUTE HANDBOOK · CARDIOLOGY". Topic in bold caps in the grey
  title band with a version / effective / review row. "Back to contents" top right.
- **Acute Handbook pages have no subtitle.** Reference pages may have an italic subtitle.
- No "first hours at George and when to call" line on acute pages.
- Footer: author, section editor, editors, based on, version, reviewed; "Approved by · Level/rank · Date";
  "Suggest an edit".
- South African context: tertiary options in a side box (`box tert`); a mitigation box (`box mit`) for when
  transfer is delayed or declined; George-specific facts in a "local" box (`box local`) so other hospitals can
  adapt the book.

## House rules (also in README.md)
- No Latin abbreviations: 12hrly, 8hrly, 4hrly; "at night", "orally", "as needed", "now". IV/IM/SC/SL are fine.
- Drug naming: class first, agent in brackets, e.g. "3rd-gen cephalosporin (ceftriaxone)". Alternatives: George
  first-choice agent in full as the first option, others by class only ("alternatives: FQ, carbapenem"). If the George
  first-choice agent is unclear, name the most likely one and add a CHECK.
  Class once per topic (acute and reference pages each), then the agent alone as named on the EML: "LMWH (enoxaparin)",
  later "enoxaparin". A different type of drug as an alternative gets its own class and agent: "ARB (losartan)".
  Omit the class where the agent is alone in its class or the class adds nothing: "thiamine", not "vitamin (thiamine)".
- Abbreviations: standard ones from the start, never spelled out (3rd-gen, LMWH, UFH, DOAC, ACEi, ARB, BB, CCB, FQ,
  PPI, SGLT2i). Only ones any SA registrar would recognise immediately.
- Cross-links: link each cause or related condition to its own topic where the manifest has one (`@acute:<id>`),
  including planned topics. Recommendation classes print in brackets "(I A)" via the stylesheet; don't type them.
- Doctors only. Nursing instructions only when they change the patient's outcome, never routine ward care.
- Base: where a current GRH protocol exists for the topic, build the topic on it. Check and update it against the
  evidence below; every difference becomes a DECISION.
- Evidence order: SA STG/EML (2024/2025 chapters) or another official, current SA guideline → European guideline
  (ESC, ESH, EASL, ERS, etc.; preferred over American ones) where no SA guideline is official or up to date → other
  international guideline. With no current GRH protocol, write from this evidence and use any old GRH protocol only
  for local practice.
  Where they differ, show it and add a DECISION.
- Drugs and doses are handled carefully per topic; every dose box needs a CHECK until a pharmacist has checked it.
- Abbreviations page, who-to-call block, phone/web version, indices and QR codes: later, not now.
- Shared-decisions list is not pre-built; decisions are collected per topic in editor.html.
- Length: 1–2 printed pages per topic in the Acute Handbook and 1–2 in the Reference Manual. Brevity and clarity
  come first. If a topic cannot fit, propose splitting it into separate topics rather than running long.
  Exceptions in "Syllabus architecture" below (one-book topics, one-page poison pages).
- Guideline PDFs: before writing a topic, ask the owner in that topic's thread for the PDF of each relevant guideline
  other than the SA STG/EML (European first), giving the full title, issuing body and year so he can fetch it with his university
  access. He uploads it into that topic's thread, so it is read only for that topic. The SA STG/EML 2024 (updated
  Dec 2025) is already in /mnt/project-files/sources/stg-eml-2024/ (index.md maps sections to part and page); never
  request it. Do not draft from secondhand online summaries while waiting.

## Syllabus architecture (owner, 21 Oct 2026)
**Dual-book philosophy: the two books do NOT need a rigid 1:1 pairing.**
- **Part 1, Acute Handbook** (Paarl emergency guideline style): 1–2 page bedside action sheets for 2 AM
  presentations. Blocks: RECOGNISE / INVESTIGATE / IMMEDIATE / ONGOING / REFER, plus DOSE BOX / TERTIARY / LOCAL
  NOTES. **Every DOSE BOX gives exact ward reconstitution recipes and starting rates in mL/hr** that nurses can
  follow (e.g. number of ampoules in 200 mL sodium chloride 0.9% or dextrose 5%: HIET insulin/dextrose bags,
  inotropes, labetalol, GTN).
- **Part 2, Reference Manual** (MGH Pocket Medicine / White Book style): high-density ward reference for
  post-admission review: structured diagnostic workup (e.g. hyponatraemia, anaemia/thrombocytopenia),
  pathophysiology pearls, chronic disease staging and the "Where the guidelines differ" tables.

manifest.yaml is the master syllabus and table of contents. A topic has both books unless its entry says
`books: [acute]` or `books: [reference]`; write only the file(s) for its book(s). build.py does not read `books:`
yet; a one-book topic simply has no file for the other book.
- **Acute Handbook only** (one page, no reference.html unless the owner asks later):
  - The 13 specific poisons: paracetamol, salicylates, TCAs, carbamazepine and phenytoin, CCBs (full HIET mixing
    recipe), BBs, digoxin, theophylline, isoniazid, organophosphates, methanol and ethylene glycol,
    sympathomimetics/amphetamine derivatives (tik, ecstasy, cocaine), iron/paraquat/paraffin/CO/corrosives.
    `poisoning-general` (General approach to poisoning and toxidromes) keeps both books. Each poison stays its own
    contents entry. **Batching: write the poisons in 3 batched threads of 4–5 pages each (one PR per batch,
    manifest order), never one thread per poison.**
  - Anaphylaxis and angio-oedema; Hypoglycaemia; Intubation, ICU referral and ceiling-of-care decisions.
- **Reference Manual only** (no acute.html): Valvular heart disease (including rheumatic heart disease), for
  post-admission review, ward workup and learning; Approach to ECG interpretation and ABG / acid-base analysis
  (new "Foundations" section at the front).
- **First seizure** is no longer a topic: it is a dedicated sub-block inside Status epilepticus covering the
  first-seizure workup, CT and LP indications (including HIV), and admission vs discharge criteria.
- **Suspected TB in the EC** is removed.
- **Severe malaria** is expanded to "Severe malaria, severe rickettsiosis (tick bite fever) and VHF red flags"
  (id `malaria` unchanged).
- **Added, not started, both books**: Pericardial effusion and cardiac tamponade (TB, uraemic and malignant
  causes; emergency pericardiocentesis); Pneumothorax and acute pleural emergencies (tension and secondary
  pneumothorax, complicated parapneumonic effusion/empyema, ICD and thoracentesis rules); Hypercalcaemic crisis
  and severe hypocalcaemia; Acute spinal cord compression, cauda equina and Guillain-Barré syndrome; Severe
  anaemia, severe thrombocytopenia (including TTP/MAHA) and pancytopenia: acute emergencies and initial workup
  (red flags such as TTP/DIC where platelet transfusion is contraindicated; pre-transfusion bloods to draw on
  admission).
- **STEMI**: streptokinase stays first-line from available stock at George and first choice in the dose box.

## Status (18 Oct 2026)
- Built: cardiology/stemi, cardiology/nste-acs, cardiology/heart-failure, endocrine/dka-hhs. Build: 0 errors.
- 54 topics in manifest.yaml after the 21 Oct 2026 restructure (see "Syllabus architecture"). ~123 open
  CHECK/DECISION markers (18 Oct count).
- Next topics: cardiology (arrhythmias as a two-page acute topic, hypertensive emergency, pulmonary embolism,
  infective endocarditis, valvular heart disease (Reference only)), then other systems in manifest order.

## Resources
- Owner's Google Drive (Google Drive connector): **George → Unit protocols** (subfolders Cardiac, Metabolic,
  Neurology, Poisoning, Previous Protocols) holds the old GRH protocols; **2026–2029 FCP** holds the MGH White
  Book 2025–26. Read the relevant GRH protocol for each topic.
- Plan doc (Claude Docs): https://claude.ai/code/artifact/ff16ac81-3304-4c40-9112-c87379c2bb7c (needs updating:
  Reference Manual track, author model, 49 topics, build system, automation).
- Local-facts questionnaire (Claude Docs, awaiting the owner's answers):
  https://claude.ai/code/artifact/f269200d-ebaf-413e-93cc-9517cd0f28c6. When answered, turn it into `local.yaml`
  and fill the local boxes from it.

## Open items for the owner
- Answer the local-facts questionnaire; give author / section editor / approver names.
- Create the "Suggest an edit" Google Form (fields: book, topic, page, section, current text, suggested change,
  reason/reference link, name/role optional, tick "contains no patient details") and send the pre-filled link;
  then replace the mailto in build.py and set the URL in manifest.yaml (`editor_email` is still a placeholder).
- Governance: approval line, pharmacist dose check, P&T committee sign-off for any deviation from the STG.
- Verify against primary sources: ESC 2026 HF figures (taken from the slide set) and ADA/EASD/JBDS 2024 DKA
  numbers (taken from the CCJM review).

## Writing a topic (one thread per topic)
Each topic is written in its own project thread, opened from the project chat. The nightly scheduled run is paused.
1. Pull the repo. Read this file and README.md.
2. The thread names its topic. If not, take the first topic in manifest.yaml with no folder under topics/, no open
   PR and no thread already open for it (follow manifest order and priority).
3. Post the guideline request in the thread (full title, issuing body and year of each relevant guideline other
   than the STG/EML; European before American). Start writing once the owner uploads the PDFs or says to go ahead
   without them; until then stop.
4. Research: the current GRH protocol from Drive first, if one exists, as the base. Then check it against the
   STG/EML chapter (from /mnt/project-files/sources/stg-eml-2024/) and the uploaded guideline PDFs (European
   preferred over American). Use WebSearch/WebFetch only for gaps (the shell cannot reach most websites). Add
   every source to sources.yaml.
5. Write topics/<system>/<topic>/{topic.yaml, acute.html, reference.html, editor.html}, using the existing
   topics as models. Mark uncertain facts CHECK and choices DECISION; list open questions in editor.html.
6. `python3 build.py --topic <id>`, then render the pages (pymupdf) and look at them: each acute sheet must fit
   its page; fix overflow (`data-cls="compact"` or split with `data-part`, within the 1–2 page limit). Then
   `python3 build.py`: 0 errors.
7. Commit and push, open a PR "Topic: <title>"; reply in the thread with the topic name, page count and number of
   markers.
8. Stop after the topic is done. Never mark a topic signed-off; never run `--release`.
