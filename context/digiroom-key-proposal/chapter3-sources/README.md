# Current document production inputs

The delivered DOCX/PDF in `../drafts/` are the authoritative current artifacts. Read them directly; rebuilding is unnecessary for continuation reading. These sources preserve the production route and supplied inputs rather than relying on old chat attachments or scratch paths.

## Inputs

- `annotated_input.docx`: unchanged author-annotated Chapters I–II input. `accepted_input.docx` is the derived intermediate after accepting insertions/deletions and removing comment anchors; it is not the final artifact.
- `persona.png`, `issue_tree_feedback.png`: supplied artwork and issue-tree feedback.
- `chapter3.txt`: final Chapter III source prose with heading/screenshot directives.
- `build.py`: rebuilds the current document from the annotated input, original starting draft, chapter source, generated figures and the existing prototype screenshot inventory. It also enforces full table borders/10 pt text and removes reader-facing casebook references.
- `finalize.py`: repairs missing appendix anchors and fills TOC page numbers using a fresh PDF. Unlike the original in-session script, it takes `--pdf` explicitly and has no dependency on a deleted `/tmp/` render. The final delivered document is unchanged by this portability fix.
- `final_qa.json`: verified delivery counts and checks. Historical rewrite stages are in `../revision-sources/` and `../current-sources/`; their scratch-path assumptions are historical, not the current entry point.

Required base-repo files include `../drafts/Digiroom_KEY_Chapters_1_and_2.docx` and `context/digiroom-key/prototype/screenshots/screenshot-index.csv` plus its 169 PNGs. The complete new NutriSari reference is `../reference-files/NutriSari_Full_Reference.docx`.

## Rebuild sequence

Use Python with `python-docx`, `lxml`, `matplotlib` and `PyMuPDF` (`fitz`). Use the current document environment’s DOCX renderer and comment-removal tool; their installation paths vary by environment.

1. Preserve a copy of the current delivered DOCX/PDF before rebuilding: `build.py` overwrites the current DOCX.
2. Run `python context/digiroom-key-proposal/chapter3-sources/build.py` from the repo root.
3. Render that DOCX to a fresh PDF. Run `python context/digiroom-key-proposal/chapter3-sources/finalize.py --pdf /absolute/path/to/fresh-proof.pdf`.
4. Strip Word comments and comment-extension parts with the document environment’s clean-delivery tool. The source input remains annotated; final delivery should have no comments or tracked changes.
5. Render the cleaned DOCX again. Update the matching PDF only after checking the final pages, TOC numbers, internal links, table fonts/grids and screenshot captions. No body content should be silently changed to force a page target.
6. Run `verify_document.py`; review its output. Update `final_qa.json` only to record a newly verified delivery, retaining the distinction between structural checks and manual visual review.

The supplied PDF is the49-page proof reviewed in this session. PNG page renders and the managed Python environment are transient production tools and are not necessary to read the document.
