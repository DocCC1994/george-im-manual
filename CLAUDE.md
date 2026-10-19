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
- Doctors only. Nursing instructions only when they change the patient's outcome, never routine ward care.
- Evidence order: SA STG/EML (2024/2025 chapters) or another official, current SA guideline → European guideline
  (ESC, ESH, EASL, ERS, etc.; preferred over American ones) where no SA guideline is official or up to date → other
  international guideline → old GRH protocol.
  Where they differ, show it and add a DECISION.
- Drugs and doses are handled carefully per topic; every dose box needs a CHECK until a pharmacist has checked it.
- Abbreviations page, who-to-call block, phone/web version, indices and QR codes: later, not now.
- Shared-decisions list is not pre-built; decisions are collected per topic in editor.html.
- Length: 1–2 printed pages per topic in the Acute Handbook and 1–2 in the Reference Manual. Brevity and clarity
  come first. If a topic cannot fit, propose splitting it into separate topics rather than running long.
- Guideline PDFs: before writing a topic, ask the owner in that topic's thread for the PDF of each relevant guideline
  other than the SA STG/EML (European first), giving the full title, issuing body and year so he can fetch it with his university
  access. He uploads it into that topic's thread, so it is read only for that topic. The SA STG/EML 2024 (updated
  Dec 2025) is already in /mnt/project-files/sources/stg-eml-2024/ (index.md maps sections to part and page); never
  request it. Do not draft from secondhand online summaries while waiting.

## Status (18 Oct 2026)
- Built: cardiology/stemi, cardiology/nste-acs, cardiology/heart-failure, endocrine/dka-hhs. Build: 0 errors.
- 49 topics planned in manifest.yaml (valvular heart disease added). ~123 open CHECK/DECISION markers.
- Next topics: cardiology (arrhythmias as a two-page acute topic, hypertensive emergency, pulmonary embolism,
  infective endocarditis, valvular heart disease), then other systems in manifest order.

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

## Scheduled topic runs (one topic per run, 1–2 per night)
1. Pull the repo. Read this file and README.md.
2. Pick the first topic in manifest.yaml with no folder under topics/, no open PR and no thread already waiting
   on guideline PDFs (follow manifest order and priority). If a waiting thread now has its PDFs or a go-ahead,
   write that topic instead.
3. Open the topic's thread and post the guideline request there (full title, issuing body and year of each
   relevant guideline other than the STG/EML; European before American). Start writing once the owner uploads the PDFs or says to go ahead
   without them; until then stop.
4. Research: STG/EML chapter first (from /mnt/project-files/sources/stg-eml-2024/), then the uploaded guideline
   PDFs (European preferred over American), then the GRH protocol from Drive. Use WebSearch/WebFetch only for gaps (the shell cannot reach most
   websites). Add every source to sources.yaml.
5. Write topics/<system>/<topic>/{topic.yaml, acute.html, reference.html, editor.html}, using the existing
   topics as models. Mark uncertain facts CHECK and choices DECISION; list open questions in editor.html.
6. `python3 build.py --topic <id>`, then render the pages (pymupdf) and look at them: each acute sheet must fit
   its page; fix overflow (`data-cls="compact"` or split with `data-part`, within the 1–2 page limit). Then
   `python3 build.py`: 0 errors.
7. Commit and push with a short message; notify the owner with the topic name, page count and number of markers.
8. Stop after the topic is done. Never mark a topic signed-off; never run `--release`.
