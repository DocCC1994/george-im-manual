# CLAUDE.md: George Hospital IM manual (read this first in every session)

## What this project is
Two books for the Internal Medicine department, George Hospital (Western Cape, South Africa), modelled on the
MGH Housestaff Manual ("White Book"), adapted to South African public-sector resources:
- **Acute Handbook**: quick referral, Paarl-style; 1–2 printed pages per topic; what to do in the first hours.
- **Reference Manual**: MGH-style; deeper background, where guidelines differ, linked citations.
Both are built from one source (see README.md for commands, layout and building blocks).

Owner: an internal medicine registrar at George (Tygerberg post). **The owner wants to remain the thinker and
learn from the process.** Claude drafts and speeds things up; clinical decisions go to the owner (and the
approving consultant) as DECISION markers, not silent choices.

## Approved house style (do not change without asking)
- GRH protocol look: Carlito font (Calibri twin), thin black grid borders, grey header bands, black/white/grey only.
  Only CHECK (amber) and DECISION (red) markers are coloured; they are removed before release.
- Small running header top-left: "GEORGE HOSPITAL: ACUTE HANDBOOK · CARDIOLOGY". Topic in bold caps in the grey
  title band with a version / effective / review row. "Back to contents" top right.
- **Acute Handbook pages have no subtitle.** Reference pages may have an italic subtitle.
- No "first hours at George and when to call" line on acute pages.
- Footer (owner, 21 Oct 2026): author, editors, based on; version, build date and STG/EML edition; the approval
  line "Approved by · Rank · Date" (topic.yaml `approved_by`, `approved_rank`, `approved_date`, left blank until
  approved); "Suggest an edit". There are no section editors, no pharmacist line and no "checked by the editorial
  team" line.
- Non-release builds carry a "DRAFT – not for clinical use" watermark.
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
- Source precedence (owner, 21 Oct 2026): **George local facts decide availability** (what George stocks and can
  do: /mnt/project-files/sources/local-facts/local-facts.md); **the SA STG/EML decides doses**; **SAASP covers
  antimicrobials** (/mnt/project-files/sources/saasp-2026/). International guidelines (ESC, ESH, EASL, ERS, etc.;
  European before American) are used only where these are silent, and every point taken from them is marked
  DECISION.
- Evidence order within that: SA STG/EML (2024/2025 chapters) or another official, current SA guideline → European
  guideline → other international guideline. With no current GRH protocol, write from this evidence and use any old
  GRH protocol only for local practice. Where they differ, show it and add a DECISION.
- Drugs and doses are handled carefully per topic; every dose box keeps a CHECK until its doses have been verified
  against the source and the topic is approved (approval line). If a source is not accessible, never fill a dose or
  fact from memory: mark it CHECK and tell the owner.
- Markers: `[CHECK: …]` and `[DECISION: …]` in instructions mean the `<span class="chk">` / `<span class="dec">`
  markers in the topic files.
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

## Build rules (owner, 21 Oct 2026)
- **Infusion recipes**: every infusion recipe and mL/hr table comes from `recipes.yaml` through a
  `{{recipe:<drug>}}` macro in the topic file. build.py calculates the rates from concentration, dose and weight
  bands; rates are never typed by hand. No hand-written rates for a recipes.yaml drug in topic files (other rate
  lines, such as maintenance fluids, are fine). Potassium: via IVAC (volumetric pump), maximum 20 mmol/hr.
- **[ALLOW]**: a source line that must name a banned term (e.g. "noradrenaline not available") or is a genuine
  exception carries `<!-- [ALLOW] reason -->` on the same line. The checker skips that line; nothing prints.
- `python3 build.py --check`: one line per problem (file:line) and a count; fails on missing topic.yaml fields,
  banned terms or legacy footer text without [ALLOW], an Acute sheet longer than 2 pages, and hand-written rates for
  recipe drugs. `--release` also fails on any open CHECK/DECISION marker or empty approval line. `--status` prints
  one row per topic (acute/reference state, tier, priority, approved, open markers); use it instead of long
  handover summaries.
- topic.yaml carries `acute`, `reference`, `deferred`, `priority`, `version` and the approval fields; they must
  agree with manifest.yaml.

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

### Phased Reference Manual (owner, 21 Oct 2026)
- **Acute sheet first.** Every topic generates its Acute Handbook sheet before any Reference Manual page.
- **Tier 1, Active Reference** (`reference_tier: 1` in manifest.yaml): the topic thread writes the reference page
  too, after the acute sheet. Topics: STEMI and NSTE-ACS (ACS), heart failure, hypertensive emergencies,
  pericardial effusion and cardiac tamponade, sepsis, meningitis, DKA/HHS, hyponatraemia, AKI, decompensated
  cirrhosis, stroke, status epilepticus (with the first-seizure block), severe cytopenias (`cytopenias`: the
  severe haematology workup).
- **Tier 2, Deferred backlog** (`reference_tier: 2, deferred: true`): every other topic that has both books. The
  topic thread writes topic.yaml, acute.html and editor.html only, no reference.html, unless the owner explicitly
  asks for that topic's Reference section. Reference pages already written for Tier 2 topics stay as they are.
- `deferred: true` applies only to the Reference chapter of a topic that has an Acute sheet. One-book topics carry
  no tier and are never deferred. Reference-only topics are scheduled by priority: Valvular heart disease (PR #19)
  ships now; ECG/ABG is P2.
- Priorities (owner, 21 Oct 2026): every topic is P1 except ECG/ABG and sympathomimetics (P2).
- build.py ignores `reference_tier` and `deferred` (like `books:`).

### Reference Manual architecture (owner, 21 Oct 2026)
Every reference.html follows MGH *Pocket Medicine* style: high-density, scannable bullet hierarchies, pearls and
embedded tables; no narrative paragraphs. House rules still apply (SA evidence order, drug naming, no Latin
abbreviations, local box, CHECK on every dose, 1–2 pages). New Tier 1 topics only (see above); existing reference pages are not
retrofitted unless the owner names one. Seven parts, in this order:
1. **Header and metadata band**: formal title (italic subtitle allowed); sub-headings by syndrome or cause.
2. **Overview and definitions**: formal criteria/staging (e.g. KDIGO, Sepsis-3, Wells/Geneva) with inline
   bracketed guideline/trial citations, e.g. [STG 2024], [ESC 2023], [NEJM 2018] (`class="cite"`, each in
   sources.yaml). Epidemiology/risk factors: high-yield, SA ward and ICU relevant (HIV, TB, RHD where they apply).
3. **Pathophysiology and manifestations**: mechanism as bullets; organ-system sub-bullets (cardiorespiratory,
   renal, neurological, haematological).
4. **Stepwise workup**: Step 1 initial labs (exact tests, timing, interpretation); Step 2 ECG/CXR/CT/POCUS
   indications (what George has, from local facts); Step 3 pitfalls (false positives/negatives, lab artefacts).
5. **Mandatory comparison table** (at least one per chapter, `class="t"`): a clinical grid such as
   differential diagnosis (cause / features / tests), subtype comparison or staging. This is in addition to the
   "Where the guidelines differ" table, which stays wherever sources differ.
6. **Management and trial evidence**: management by cause/subtype as stepwise algorithms; dosing pearls (renal and
   hepatic adjustment, titration targets such as MAP ≥65 mmHg, infusion recipes matching the acute dose box);
   bracketed landmark-trial tags beside major recommendations, e.g. [CRASH-2], [COMPLETE]. Trial tags are typed;
   recommendation classes "(I A)" still come from the stylesheet.
7. **Escalation and ward red flags** (callout box): when to call GRH IM / discuss with the internal medicine
   consultant, when to refer to ICU (per the GRH ICU SOP), absolute contraindications (e.g. no platelet
   transfusion in TTP). Use George terms, never generic "page the fellow".

## Status (18 Oct 2026)
- Built: cardiology/stemi, cardiology/nste-acs, cardiology/heart-failure, endocrine/dka-hhs. Build: 0 errors.
- 54 topics in manifest.yaml after the 21 Oct 2026 restructure (see "Syllabus architecture"). ~123 open
  CHECK/DECISION markers (18 Oct count).
- Next topics (owner, 21 Oct 2026), after the open PRs are cleared: CAP, acute asthma, meningitis, cryptococcal
  meningitis, severe malaria. Severe malaria takes the expanded title (rickettsiosis, VHF red flags) when its
  thread is next opened. Then manifest order by priority.
- ACS aspirin (owner, 21 Oct 2026): GRH practice for STEMI and NSTE-ACS is a 300 mg loading dose, then 75 mg
  daily lifelong. This differs from the STG (150 mg load and 150 mg daily: STG Hospital Level Adults 2024, 3.2.1
  p 3.4; 3.2.2 p 3.10; 3.2.3 p 3.13); show the difference in the "Where the guidelines differ" table.

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
- Answer the local-facts questionnaire; give author and approver names.
- Create the "Suggest an edit" Google Form (fields: book, topic, page, section, current text, suggested change,
  reason/reference link, name/role optional, tick "contains no patient details") and send the pre-filled link;
  then replace the mailto in build.py and set the URL in manifest.yaml (`editor_email` is still a placeholder).
- Governance: approval line, P&T committee sign-off for any deviation from the STG.
- Verify against primary sources: ESC 2026 HF figures (taken from the slide set) and ADA/EASD/JBDS 2024 DKA
  numbers (taken from the CCJM review).

## Writing a topic (one thread per topic)
Each topic is written in its own project thread, opened from the project chat. The nightly scheduled run is paused.
1. Pull the repo. Read this file and README.md.
2. The thread names its topic. If not, take the first topic in manifest.yaml with no folder under topics/, no open
   PR and no thread already open for it (follow manifest order and priority).
3. Post the guideline request (for a Tier 2 topic, only the guidelines the acute sheet needs) in the thread (full title, issuing body and year of each relevant guideline other
   than the STG/EML; European before American). Start writing once the owner uploads the PDFs or says to go ahead
   without them; until then stop.
4. Research: the current GRH protocol from Drive first, if one exists, as the base. Then check it against the
   STG/EML chapter (from /mnt/project-files/sources/stg-eml-2024/) and the uploaded guideline PDFs (European
   preferred over American). Use WebSearch/WebFetch only for gaps (the shell cannot reach most websites). Add
   every source to sources.yaml.
5. Write topics/<system>/<topic>/{topic.yaml, acute.html, reference.html, editor.html}, using the existing
   topics as models: acute.html first; reference.html only for Tier 1 topics (or when the owner asks; see
   "Phased Reference Manual"). Mark uncertain facts CHECK and choices DECISION; list open questions in editor.html.
6. `python3 build.py --topic <id>`, then render the pages (pymupdf) and look at them: each acute sheet must fit
   its page; fix overflow (`data-cls="compact"` or split with `data-part`, within the 1–2 page limit). Then
   `python3 build.py`: 0 errors, and `python3 build.py --check`: passes.
7. Commit and push, open a PR "Topic: <title>"; reply in the thread with the topic name, page count and number of
   markers.
8. Stop after the topic is done. Never mark a topic signed-off; never run `--release`.

## Thread coordination (owner, 21 Oct 2026)
- Work-in-progress cap: one active topic thread and no more than 2 open topic PRs. Don't open a new topic while
  2 topic PRs are open.
- A new global rule is recorded here (or in the style guide) in one commit; it is never broadcast to open threads
  or PRs, and nothing is retrofitted until the owner names a thread to update.
- Threads do not watch main or merge/rebase main into their branches when other PRs merge.
- Merge rule (replaces "sync only if conflict"): right before merging a PR, merge main into its branch, run
  `python3 build.py --check`, and merge only if it passes.
