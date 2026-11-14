"""Build the user's detailed, current research context without new retrieval.

Only authored/curated project evidence is embedded. Private source bodies, current
review text, account links, installation caches and unrelated user context are not.
The original friend context is preserved as a marked historical appendix, with its
six private storage URLs replaced by named source-reference anchors.
"""
from pathlib import Path
import argparse
import csv
import datetime as dt
import hashlib
import json
import re
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ORIGINAL = ROOT.parent / 'upload' / 'IBSC_2026_Auto2000_Digiroom_Master_AI_Context (2).md'
DEFAULT_OUTPUT = ROOT / 'context' / 'Auto2000_Master_AI_Context_Updated.md'
NOW = dt.datetime.now(dt.timezone.utc).isoformat()
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
used_inputs = {}
missing_inputs = []
sections = []
embedded_report_hashes = {}
report_aliases = []

def remember(path):
    path = Path(path)
    data = path.read_bytes()
    try:
        name = path.relative_to(ROOT).as_posix()
    except ValueError:
        name = path.name
    used_inputs[name] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
    return data

def jread(rel, default=None):
    path = ROOT / rel
    if not path.exists():
        return default
    return json.loads(remember(path))

def clean_private_links(text):
    text = re.sub(r'https?://(?:www\.)?chatgpt\.com/library[^\s)>\]]*', '[private storage URL redacted]', text)
    text = re.sub(r'(?:oai-library|library-file|mcp-resource)://[^\s)>\]]*', '[private storage URI redacted]', text)
    text = re.sub(r'(?:file-inline-)?libfile_[A-Za-z0-9_-]+', '[private file ID redacted]', text)
    text = re.sub(r'(?i)account_id=[^\s&)>\]]+', '[private account parameter redacted]', text)
    text = text.replace(str(ROOT) + '/', '')
    return text

def prose(value):
    if value is None:
        return 'Not reported.'
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if isinstance(value, list):
        if all(not isinstance(x, (list, dict)) for x in value):
            return '; '.join(prose(x) for x in value) or 'None listed.'
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False)
    return clean_private_links(str(value)).replace('\r', '').strip()

def add(title, body):
    sections.append((title, clean_private_links(body).strip()))

def relative_links(text, source):
    """Resolve local links from the original source location into context/ output."""
    source = Path(source)
    def replace(match):
        label, dest = match.group(1), match.group(2)
        if dest.startswith(('http:', 'https:', '#', 'mailto:', 'data:')):
            return match.group(0)
        if dest.startswith('sandbox:'):
            dest = dest[len('sandbox:'):]
        if ' ' in dest or '"' in dest:
            return match.group(0)
        target = (source.parent / dest).resolve()
        try:
            rel = target.relative_to(ROOT)
        except ValueError:
            return match.group(0)
        return f'[{label}](../{rel.as_posix()})'
    return re.sub(r'\[([^\]]*)\]\(([^)]+)\)', replace, text)

def report(title, rel, note='', required=False):
    path = ROOT / rel
    if not path.exists():
        missing_inputs.append(rel)
        if required:
            add(title, f'**PENDING / NOT AVAILABLE AT THIS BUILD.** Expected file: `{rel}`. No results are inferred from its planned existence. {note}')
        return
    text = remember(path).decode('utf-8')
    content_hash = hashlib.sha256(text.strip().encode()).hexdigest()
    if content_hash in embedded_report_hashes:
        original_rel = embedded_report_hashes[content_hash]
        report_aliases.append({'alias': rel, 'same_content_as': original_rel, 'sha256_trimmed_text': content_hash})
        add(title, f'**Source alias:** `{rel}` contains the same authored report text as `{original_rel}`, which is already included above. It is not another study, source observation or separate finding. Input provenance still records both file paths. {note}')
        return
    embedded_report_hashes[content_hash] = rel
    text = relative_links(text, path)
    add(title, f'**Curated source:** `{rel}`. {note}\n\n{text}')

def docx_to_markdown(rel):
    path = ROOT / rel
    if not path.exists():
        missing_inputs.append(rel)
        return f'Pending: `{rel}`.'
    remember(path)
    with zipfile.ZipFile(path) as archive:
        root = ET.fromstring(archive.read('word/document.xml'))
    body = root.find('w:body', NS)
    out = []
    for element in body:
        tag = element.tag.rsplit('}', 1)[-1]
        if tag == 'p':
            text = ''.join(x.text or '' for x in element.findall('.//w:t', NS)).strip()
            if not text:
                continue
            style = element.find('w:pPr/w:pStyle', NS)
            name = style.attrib.get('{'+NS['w']+'}val', '') if style is not None else ''
            if name.startswith('Heading'):
                level = re.sub(r'\D', '', name)
                out.append('#' * min(6, int(level or 2) + 1) + ' ' + text)
            else:
                out.append(text)
        elif tag == 'tbl':
            rows = []
            for tr in element.findall('w:tr', NS):
                rows.append([' '.join(''.join(t.text or '' for t in p.findall('.//w:t', NS)) for p in cell.findall('w:p', NS)).strip().replace('|', '\\|') for cell in tr.findall('w:tc', NS)])
            if rows:
                width = max(map(len, rows))
                rows = [r + [''] * (width - len(r)) for r in rows]
                out.extend(['| ' + ' | '.join(rows[0]) + ' |', '| ' + ' | '.join(['---'] * width) + ' |'])
                out.extend('| ' + ' | '.join(r) + ' |' for r in rows[1:])
        out.append('')
    return clean_private_links('\n'.join(out))

def capsules(title, rel, id_field, fields, list_key=None, note=''):
    data = jread(rel)
    if data is None:
        missing_inputs.append(rel)
        add(title, f'Pending source register: `{rel}`. {note}')
        return
    if list_key:
        data = data[list_key]
    if isinstance(data, dict):
        add(title, f'Input `{rel}` has a dictionary schema; its readable report, rather than an invented row interpretation, remains authoritative.\n\n```json\n{json.dumps(data, ensure_ascii=False, indent=2)}\n```')
        return
    out = [f'**Register:** `{rel}`. {len(data)} curated records. {note}', '']
    for row in data:
        out += [f"### {title.split(':')[0]} record {prose(row.get(id_field, 'unlabeled'))}", '']
        for field, label in fields:
            if field in row:
                out += [f'**{label}.** {prose(row[field])}', '']
    add(title, '\n'.join(out))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--original', type=Path, default=DEFAULT_ORIGINAL)
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument('--backup-status', type=Path)
    parser.add_argument('--final-pdf', type=Path, help='Explicit final visual memo, only after its visual QA is complete.')
    args = parser.parse_args()
    original_bytes = remember(args.original)
    original_hash = hashlib.sha256(original_bytes).hexdigest()
    original = original_bytes.decode('utf-8')

    # Names, not private IDs, remain sufficient to identify the historical inputs.
    historical_references = {
        'cb': '#source-reference-casebook',
        'ar': '#source-reference-astra-annual-report',
        'statista-ev': '#source-reference-statista-ev',
        'statista-auto': '#source-reference-statista-automotive',
        'strategic-md': '#source-reference-prior-analysis-markdown',
        'strategic-pdf': '#source-reference-prior-analysis-pdf',
    }
    replacements = 0
    historical = original
    for key, replacement in historical_references.items():
        pattern = rf'(?m)^(\[{re.escape(key)}\]:\s*)https?://(?:www\.)?chatgpt\.com/library[^\r\n]*$'
        historical, count = re.subn(pattern, lambda m: m.group(1) + replacement, historical)
        replacements += count
    if replacements != 6:
        raise RuntimeError(f'Expected six historical private-storage definitions; found {replacements}. Inspect source safely before publishing.')
    # Preserve everything else in the user's historical source exactly.
    redacted_lines = [(a, b) for a, b in zip(original.splitlines(), historical.splitlines()) if a != b]
    assert len(original.splitlines()) == len(historical.splitlines()) and len(redacted_lines) == 6

    reviews = jread('workstreams/extension_reviews/analysis_summary.json', {})
    old_reviews = jread('workstreams/reviews/review_summary.json', {})
    narratives = jread('workstreams/narratives/combined_metrics.json', {})
    site = jread('workstreams/site/summary.json', {})
    battery = jread('workstreams/extension_battery/INITIAL_SIGNAL_AUDIT.json', [])
    sign = jread('workstreams/extension_battery/SIGN_ENDPOINT_AUDIT.json', [])
    bmanifest = jread('workstreams/extension_battery/SOURCE_FILE_MANIFEST.json', [])
    journeys = jread('workstreams/extension_journeys/summary.json', {})
    stakeholders = jread('workstreams/extension_stakeholders/summary.json', {})
    claims = jread('workstreams/friend_challenge/claims_summary.json', {})
    econ = jread('workstreams/extension_economics/summary.json', {})
    actual_values = sum(r.get('actual_signal_values', 0) for r in battery)
    raw_mats = list((ROOT / 'raw_licensed_data').rglob('*.mat'))
    battery_reports = sorted((ROOT / 'workstreams/extension_battery').glob('*REPORT*.md'))
    battery_status = 'Readable report present; inspect its final QA/manifest limits.' if battery_reports else 'PENDING readable battery report at this build; downloaded-file and signal audits are available. No completed final audit is inferred.'
    mobile_n = journeys.get('mobile_journeys', 0)
    mobile_status = f'{mobile_n} recorded mobile journeys in the current summary.' if mobile_n else 'No completed mobile journey in the current summary. Device capability/launch restrictions are recorded; desktop results do not validate mobile.'
    backup_status = 'PENDING: no completed new-release upload receipt supplied to this build.'
    if args.backup_status and args.backup_status.exists():
        backup_status = 'Receipt supplied; review the explicitly recorded success/failure states:\n\n' + clean_private_links(remember(args.backup_status).decode('utf-8'))
    visual_reference = ROOT.parent / 'upload' / 'Audit_Kesesuaian_Umpan_Balik_Juri (2).pdf'
    visual_reference_meta = None
    if visual_reference.exists():
        reference_bytes = remember(visual_reference)
        visual_reference_meta = {'filename': visual_reference.name, 'sha256': hashlib.sha256(reference_bytes).hexdigest(), 'role': 'visual reference only, not IBSC evidence'}
    final_pdf_meta = None
    if args.final_pdf:
        final_path = args.final_pdf if args.final_pdf.is_absolute() else ROOT / args.final_pdf
        if not final_path.exists():
            raise RuntimeError('Explicit final PDF not found: ' + str(final_path))
        final_bytes = remember(final_path)
        final_pdf_meta = {'filename': final_path.name, 'bytes': len(final_bytes), 'sha256': hashlib.sha256(final_bytes).hexdigest()}
        try:
            import fitz
            with fitz.open(final_path) as pdf:
                final_pdf_meta['pages'] = len(pdf)
                final_pdf_meta['pdf_text_words_whitespace'] = sum(len(page.get_text().split()) for page in pdf)
        except ImportError:
            final_pdf_meta['pages'] = 'Not computed: optional PyMuPDF unavailable.'
    pdf_presentation_state = 'The current primary reading PDF is the shorter visual memo.' if final_pdf_meta else 'The primary reading PDF is being replaced by a shorter visual memo.'
    story_qa_receipts = []
    for qa_path in sorted((ROOT / 'reports').glob('STORY*QA*.json')):
        qa = jread(qa_path.relative_to(ROOT).as_posix(), {})
        if not isinstance(qa, dict):
            continue
        checked_hash = qa.get('pdf_sha256') or qa.get('reviewed_pdf_sha256') or qa.get('sha256')
        blocking_count = qa.get('blocking_issue_count', qa.get('blocking_issues'))
        if blocking_count is None:
            for field in ['blocking_defects', 'blocking_defects_observed', 'blocking_findings']:
                if isinstance(qa.get(field), list):
                    blocking_count = len(qa[field])
                    break
        story_qa_receipts.append({
            'file': qa_path.relative_to(ROOT).as_posix(),
            'checked_pdf_sha256': checked_hash,
            'matches_explicit_final_pdf': checked_hash == final_pdf_meta['sha256'] if final_pdf_meta and checked_hash else None,
            'scope': qa.get('scope', qa.get('method', qa.get('review_type', qa.get('reviewer', 'see original receipt')))),
            'status': qa.get('status', qa.get('overall', 'see original receipt')),
            'passed': qa.get('passed'), 'failed': qa.get('failed'),
            'blocking_issue_count': blocking_count,
            'visual_review_pending': qa.get('visual_review_pending'),
        })
    final_visual_receipts = [r for r in story_qa_receipts if Path(r['file']).name.startswith('STORY_FINAL_VISUAL_QA_') and r['matches_explicit_final_pdf']]
    final_visual_qa_state = 'PENDING matching final-version visual QA receipts.'
    if len(final_visual_receipts) == 3 and all('pass' in r['status'].lower() and r['blocking_issue_count'] == 0 for r in final_visual_receipts):
        final_visual_qa_state = 'Three matching final-version AI visual QA receipts pass their assigned page ranges (1–16,17–28,29–41), with zero blocking defects. Changed pages were rechecked and unchanged coverage retained only as described in the receipts. Any nonblocking notes are limited to those explicitly recorded in the final receipts. This is visual/readability QA, not human or causal validation.'

    add('Current mandate, precedence and how to use this context', f'''
This is the current, detailed English master context for the Auto2000 Digiroom research project. It updates the supplied friend context with completed research, counterevidence, methodological limits, evidence registers, original figures and the deeper follow-up. Build time: **{NOW}**. It is a reusable record of this research task, not a claim to reproduce every message in a conversation transcript.

**Current instructions take precedence over the historical appendix.** The current endpoint is research diagnosis, critical evidence, hypotheses, distinctive insight cards and broad solution alternatives for the user to choose. Do not choose a winner, build an Auto2000 product, select a pilot, prescribe implementation or allocate the investment budget. Earlier historical suggestions about pilots, rollout, preferred channels or writing language are preserved as history and are not current authorization. The current requested language is English. The Indonesian historical document remains in its original language so its nuance is not silently rewritten.

The user asked for a much larger, sustained, parallel research effort, including datasets, social-media possibilities, GitHub discovery, hypotheses, new insights and stakeholder perspectives. They also asked to retain the earlier ZIPs and make a backup later. Their request for scale does not authorize fabricated customer rows, artificial duplication or counting features as people. The project uses actual acquired data and explicitly distinguishes observations from derived calculations and external study sizes.

The first-wave files remain an audit trail. Extension reports refine their interpretation rather than silently upgrading every old claim. The original 25 hypotheses remain unresolved as causal business mechanisms. The 40 friend analytical groups and 148 scoped clauses are coverage, not confirmed findings. The 16 insight cards and27-concept menu are preserved; a later independent candidate is separate, not retroactively selected or added to a frozen menu without a new label.

Public operator publications establish what the operator represents. They do not establish every branch's execution, user comprehension, authorized data access or incremental profit. Self-reports remain unverified. Evaluator browser observations are not recruited-customer tests. Statistical results from foreign studies remain tied to their samples, designs, dates and endpoints. Synthetic risk examples expose the meaning of a promise; they are not sales forecasts or actuarial data.

All source-grounded coding and project crosschecks were done by AI researchers. A second-AI review is useful error checking, not human validation, a blinded reliability experiment or independent verification of customer truth. Upstream published research retains its own methods. This project did not recruit human participants, conduct dealer fieldwork, access private customer records or observe verified Auto2000 deliveries or completed repair contributions.

Do not import unrelated user profile, memories, account identifiers or private source bodies into this context. No private ChatGPT Library links or IDs are included. The original user-supplied context remains unchanged outside the pack; this derivative changes only six private-storage URLs in its marked historical appendix. Original source SHA256: `{original_hash}`. This hash identifies bytes, not a source document's truth or a person's identity.

Use the current report and extension chapters together. A repeated figure in two chapters is one finding discussed twice, not another observation. A study abstract, a survey instrument, a source file, a derived table, a chart and a source-check row have different units. Read their evidence boundaries before reusing a number.
''')

    add('Decision history and scope changes preserved from this task', '''
The task began with a request to examine a research plan before execution. It expanded into a very large public-source Auto2000 research request, with datasets, social-media and GitHub discovery, hypothesis generation and challenge, strategic directions, stakeholder lenses and a large downloadable archive. Planning and execution were separated. The research endpoint was then clarified to exclude an Auto2000 implementation or rollout plan and a final winning strategy. The user chooses among possible solutions.

The run used a lead and six specialist slots, with work rotated across acquisition, customer narratives, market evidence, competitor/operator terms, datasets, live journeys, economics, independent checking and synthesis. Parallelism is an execution method, not seven independent confirmations of the same source. A configured eight-hour proposal and large crawl ceilings are not evidence that eight hours of active work or all planned collection occurred. The actual interrupted site queue and source-access limits remain explicit.

The user had not downloaded an earlier ZIP and asked for it inside the later archive. Both historical releases are preserved unchanged under previous_releases. They contain earlier plans, methods and initial outputs. Those inherited inventories or rows do not count as newly acquired observations merely because they are copied into a new archive.

The later friend-context upload became a new substantive challenge source. The team extracted its nuanced claims instead of rejecting a stronger strawman. R1 concerns driving/charging fit and ownership economics; an existing installment calculator does not settle it. R2 concerns model/job capability and credible fulfillment; an existing booking screen does not settle that either. M2 concerns useful evidence in appraisal; a certificate route alone does not prove acceptance or value, and its existence rules out a first-certificate novelty claim. Insurance, capped top-up, full floor and residual-risk transfer retain distinct counterparties and obligations.

The first release introduced16cross-source insights and 27 consolidated alternatives from 45 draft cards. The next user request authorized a deeper follow-up, with prespecified questions after substantial discovery. This is a disclosed extension, not blind preregistration before any evidence existed. Additional app reviews, geographic sensitivity, BEV journey controls, program/event comparisons, stakeholder lifecycle checks, foreign mechanism studies and battery signal data were collected/analyzed where accessible. New evidence changed or narrowed some interpretations without establishing causal Auto2000 commercial effects.

The latest request is for this long, detailed, updated master context, carrying every substantive new finding and decision boundary. The builder is dynamic: it reads current reports and registers, records input hashes and exposes missing final artifacts. Rerun it after final telemetry, mobile, QA or backup status changes. Earlier source text remains historical; current mandates and the latest scoped evidence control future use.
''')

    add('Latest PDF preference: a clear visual memo with full research retained', f'''
The user supplied **Audit_Kesesuaian_Umpan_Balik_Juri (2).pdf**, a four-page unrelated audit document, as a **visual reference only**. It supplies no IBSC case fact, business finding, judge feedback about this Auto2000 work, new study, sample or validation. Its relevance is presentation: short clear paragraphs, a prominent analytical point, large useful charts and evidence placed near the claim. Do not import its subject matter into the Auto2000 evidence base.

{pdf_presentation_state} Approximately 38 pages was the design target; the explicit final-PDF metadata below records the actual count when supplied. The intended pattern is one main finding per page, roughly 100–200 words where appropriate, readable figures and seven family pages for the 27 solution concepts. Full analysis remains in the archive, Markdown, evidence registers and this detailed context. This changes presentation density, not the scope of research or the unresolved causal status.

The mechanism page briefs in `story_assets/mechanism_story.json` and `.md` express three distinctions in plain English: completed jobs and their contribution; stated preference versus observed purchase; and the five analytical links between a battery measurement and a changed transaction. Their diagrams are conceptual or evidence-state displays, not invented effect-size charts. They contain no implementation choice or winner.

**Explicit final visual PDF supplied to this build:** {json.dumps(final_pdf_meta, ensure_ascii=False) if final_pdf_meta else 'PENDING final-PDF handoff/QA. File existence alone is not treated as approved visual QA.'}

**Current final-version visual QA:** {final_visual_qa_state}

**Visual-reference metadata:** {json.dumps(visual_reference_meta, ensure_ascii=False) if visual_reference_meta else 'Reference filename recorded; source not present at this local build.'}

The supplied original friend context remains a historical appendix. Its earlier delivery style does not override the latest English visual-memo preference. The final PDF can be read first, then this master context and the archive provide the depth and exact source boundaries.

### Visual-memo QA version receipt

The following entries describe the exact PDF versions inspected, not new research observations or human validation. Some frozen receipts can precede a later layout patch. Compare their hashes with the explicit final PDF; a mismatched old receipt does not automatically validate or invalidate a newer version. The original JSON retains page-specific scope and findings. A render-stage visual_review_pending flag records that stage; matching final page-range receipts supersede it once those inspections are complete.

```json
{json.dumps(story_qa_receipts, ensure_ascii=False, indent=2)}
```
''')

    add('Current evidence ledger and freeze-sensitive status', f'''
| Family | Captured unit/count at this build | Meaning and limit |
|---|---|---|
| Initial public automotive reviews | {old_reviews.get('total_unique_reviews', 210)} platform review IDs; six apps; twelve first-wave cohorts | Public-listing convenience evidence, not representative customers or completed jobs. |
| Follow-up reviews | {reviews.get('new_rows', 'PENDING')} new unique IDs; {reviews.get('combined_unique_review_ids', 'PENDING')} combined IDs across {reviews.get('cohorts', 'PENDING')} cohorts | Original and new waves overlap only as documented; metadata/coding views add no reviews. Vehicle context, app role, source language, date and version differ. |
| Narrative discovery/follow-up | {narratives.get('total_annotation_units', 95)} annotations, {narratives.get('unique_source_urls', 38)} URLs | Not95independent people or incidents. Includes questions, advice, employee accounts and study findings. |
| Site sample | {site.get('fetched_urls', 345)} requested records, {site.get('successful_raw_html', 281)} successful raw-HTML responses | Frozen interrupted queue, not completed crawl. Extracted structure is not rendered task success or SEO performance. |
| IGAR auxiliary raw | 617,722 rows in each of two label views; 617,703 composite keys; 19 duplicate excess rows per view | Same government-app corpus, not 1,235,444 independent reviews or Auto2000 data. |
| IGAR storage shape | Eight plus twelve raw column positions, including source index; 12,354,440 row×column slots | About 12.35 million cells, including repeated/shared/missing fields, not independent facts or people. |
| SPKLU | 2,454 station rows; 3,767 charger-box rows | Hierarchical source units, not customer visits, live uptime or usable capacity. |
| Derived geography | 6,019,662 directed pair distances | Computations; full matrix discarded, summary results retained. |
| BPS stock | 1,285 numerical province/year/type cells across seven yearly tables | All registered vehicles under changing boundaries; not Auto2000/BEV exposure. |
| Battery subset |{len(bmanifest)} downloaded MAT bundles;{actual_values:,} stored Curr/Volt/SoC/Temp values, excluding clocks/epoch | Purposeful windows from one Audi e-tron in California, not Toyota/Indonesia owners or independent physical measurements. |
| Battery public staging |{len(raw_mats)} MAT files presently staged under raw_licensed_data | Downloaded source files and public-release staging are different states; final privacy/license checks remain with their receipts. |
| Friend challenge |{claims.get('claim_groups', 40)} groups;{claims.get('subclaims', 148)} scoped clauses | Analytical coverage, not independent studies or proven effects. |
| Lifecycle extension |{stakeholders.get('canonical_jobs', 'PENDING')} analytical job units;{stakeholders.get('owner_matrix_cells', 'PENDING')} owner-matrix cells | Includes institutional risk layer; not additive unmet needs or profit pools. |
| Economics extension |{econ.get('commercial_mechanisms', 'PENDING')} mechanism records;{econ.get('constructed_unit_state_rows', 'PENDING')} constructed unit states | Illustrations/identity checks, zero forecast or causal uplift. |

**Battery completion status:** {battery_status}

**Mobile status:** {mobile_status} No mobile/native success is inferred from desktop observations. Check the latest journey report and capability receipt below; a failed launch is an environment limit, not a customer defect.

**Backup status:** {backup_status}

The expanded sample is larger than the first wave, but no unit is silently recounted as another person. External studies' 3,181, 2,170, 1,490, 1,167 or 9 million figures describe those studies; their raw respondents/listings were not thereby acquired by this project. Their findings remain external mechanism evidence.
''')

    add('Release variants, rights, backup and source privacy', '''
The intended primary user archive is **Auto2000_Research_Project_Full.zip**. It includes the two exact licensed IGAR text CSVs requested as raw data, separately attributed SPKLU/BPS material, project code, derived tables, reports, figures, context and earlier releases. Newly staged licensed telemetry requires its own recorded checks and manifest. Inclusion of licensed raw text does not turn it into current Auto2000 evidence or certify that every self-disclosure is absent.

The intended public backup variant is **Auto2000_Research_Public_Backup.zip**, which omits the two IGAR full-text CSVs. If a host's 100 MB limit requires split delivery, the intended **Auto2000_Public_Backup_Core.zip** excludes the five MAT binaries and the additional **Auto2000_Telemetry_Volume_01.zip** through **Auto2000_Telemetry_Volume_05.zip** each carry a whole telemetry source file in the common extraction layout. This is an explicit multi-archive distribution of complete files, not arbitrary binary truncation or a byte-for-byte mirror of the primary ZIP. Final receipts determine which variants were actually built and uploaded; names here do not assert successful upload.

Private caches are **always excluded**. There is no claimed authorization to bulk publish private_cache, captured current-review text, unlicensed publisher HTML/PDF bodies, source image archives, browser sessions, cookies, credentials, account receipts or installation dependencies. Current automotive reviews appear as derived/nontext source records and conservative paraphrase codes. The full private casebook and Statista dossiers are excluded. Only the user-provided context text and our own summaries of relevant source facts are included. A separately licensed dataset README, including the telemetry source README, has its own explicit source-manifest treatment; this exception does not include the full research paper. Private Library identifiers and account links are redacted even from the historical appendix.

The primary licensed raw appendix retains different rights: IGAR CC BY 4.0; SPKLU CC BY-NC 3.0; telemetry source CC BY-NC 3.0 as recorded; attributed factual BPS table payloads with no blanket unrestricted license claim. A source license applies to its material and conditions, not automatically to every report or web page in this project. Noncommercial restrictions are not commercial deployment permission. Data-set source manifests distinguish exact source bytes from transformed table objects and derived analysis.

Filebin and alternative-host backup success must be established by actual upload receipts. Earlier failure or 507 does not prove the later release is backed up. A backend Library receipt, if used to preserve deliverables, remains private; its IDs do not belong in this context. Final human-facing backup links may be recorded outside the exact archive to avoid checksum self-reference. A backup smaller than the primary archive must disclose omitted files and where licensed volumes can be obtained.

The unchanged earlier archives are `previous_releases/Auto2000_Public_Research_Initial_2026.zip` and `previous_releases/Auto2000_Expanded_Research_Plan_v2.zip`. They are retained for the user's continuity, not used to imply that all their plan ceilings were achieved. The newest source registers, actual request counts and release-status receipts control claims about work completed.
''')

    add('Corrections that must survive every later summary', '''
1. Existing functionality is a baseline: the observed hybrid and BEV finance simulations work before contact; optional income can remain blank. HEV/ICE comparison, broad branch filtering, guest qualification, digital HHC certificate retrieval, BEV trade-in model selection and dated program-specific service estimates exist. This does not prove ideal comprehension or fulfillment, but it defeats universal absence claims.
2. Current versus historical evidence matters. Review dates, installed build, source capture, model year, estimate basis and entitlement cohort are different. Many first-wave selected reviews predate the relaunch. A March 2024 service estimate is not a 2026 personal invoice. New current records do not erase old records; they change the valid inference.
3. The first five-branch coordinate check exposed a material conflict; it did not certify corrected national charger locations. Extension candidate filters show broad 5 km proximity can survive while close 1 km convenience is sensitive. Name/provider proxies are not verified access, road travel, compatibility or uptime.
4. Toyota/Lexus portfolio xEV volume and mix are different quantities, and neither is Auto2000's installed service base. A decomposition is an identity with an ordering choice, not the causal contribution of market weakness or Digiroom.
5. Published service intervals, jobs, included benefits, customer cash and dealer GP must remain separate. Equal visit cadence can coexist with different work. More headline program years can coexist with fewer covered recommended events. A zero customer payment is not zero resource use or necessarily zero reimbursement.
6. A rating is not task completion, a lexical mention is not a validated complaint, and a weak sentiment label is not a root cause. Platform language changes source-selected review cohorts. Foreign/storefront language does not verify residence. Suzuki motorcycle contexts cannot silently become passenger-car evidence.
7. Motor insurance, OEM warranty, normal capacity wear, accident damage, a capped trade-in incentive, an unconditional minimum value and B2B insurer recovery have different triggers, promise owners and retained risk. Policy limits do not cap a separate unconditional customer promise. Product listings do not establish signed Auto2000 routing, fees or local syariah RVI underwriting.
8. Battery telemetry has **not** revealed a reversed charging-sign convention. Folder1/Folder7 current samples are approximately 99.85%/99.91% negative, consistent with the charging documentation. Tiny positive exceptions qualify an “always” statement narrowly. Early concern inferred from a positive maximum was a question, not a finding. The meaningful limits are asynchronous clocks, long gaps, source-side reduction and a confidential/proprietary capacity reference.
9. The telemetry count 56,507,201 covers stored current/voltage/SoC/temperature values before clocks and epoch fields. They are not that many independent synchronized physical measurements, vehicles, owners, charging sessions or capacity labels. Five folder windows can contain many segments from one car.
10. Information experiments, perceived usefulness, proposed instruments and actual purchases remain different endpoints. The Irish showroom trial detected no overall treatment effect; it did not prove a universally zero effect. NIST DCI 008 is an instrument, not a completed price-premium estimate. TN 2328's 1,490 respondents must not be substituted with another analysis's 1,443 or pooled as independent samples.
11. The updated GP ledger assigns recognized direct costs, discounts, benefits, recoveries and obligations once. Below-GP operating cost remains separate. Displacement/cannibalization already represented in all-channel counterfactual volumes is not subtracted again. Primary accounting tags 4/18/1/2 are not independent causes, additive profit pools or measures of commercial importance.
12. The solution menu remains a user choice. Generic coordination/evidence facets can recur across lifecycle jobs; they do not create separate revenue pools. Recall completion, delivery closure, adverse-decision review and ownership/account exit are scope leads, not demonstrated missing Auto2000 capabilities. Safety action is not justified as discretionary paid upsell.
''')

    # The final execution record distinguishes completed release work from old freezes.
    report('Current execution record and release boundaries', 'EXECUTION_RECORD.md')
    # Detailed current first-wave records; these are authored project outputs.
    report('Main research report: complete current narrative', 'reports/RESEARCH_REPORT.md', 'The first-wave report is retained; the extension chapters below refine it.')
    add('Friend-context challenge report: complete readable text', '**Authored source:** `reports/FRIEND_RESEARCH_CHALLENGE.docx`. Tables below are extracted from our Word report, not the private casebook or dossier.\n\n' + docx_to_markdown('reports/FRIEND_RESEARCH_CHALLENGE.docx'))
    report('Sixteen cross-source insight cards', 'reports/INSIGHT_BOOK.md', 'Frozen first-wave cards; later extension counterevidence remains applicable.')
    report('Twenty-seven consolidated solution alternatives', 'reports/SOLUTION_MENU.md', 'User chooses; no rank, winner, implementation or additive profit-pool claim.')
    report('Independent review of all forty-five draft concepts', 'reports/option_review.md')
    report('Original twenty-five hypothesis assessment', 'reports/HYPOTHESIS_ASSESSMENT_NOTES.md')
    report('Numerical and economic audit', 'reports/NUMERICAL_QA.md', 'Read the structured current QA receipt when a later rerun changes the prose freeze.')

    for title, rel in [
        ('First-wave market evidence and competing interpretations', 'workstreams/market/REPORT.md'),
        ('First-wave owner narratives and fresh-source challenge', 'workstreams/narratives/FINDINGS.md'),
        ('First-wave app review findings', 'workstreams/reviews/FINDINGS.md'),
        ('First-wave external datasets and original calculations', 'workstreams/datasets/DATASETS_REPORT.md'),
        ('First-wave evaluator journeys', 'workstreams/journeys/RESEARCH_FINDINGS.md'),
        ('Focused friend-context journey checks', 'workstreams/journeys/FRIEND_CONTEXT_CHALLENGE.md'),
        ('Corporate capability checks', 'workstreams/friend_capabilities/REPORT.md'),
        ('Survey denominator and source audit', 'workstreams/friend_surveys/SURVEY_CLAIM_AUDIT.md'),
        ('Insurance source interpretation', 'workstreams/friend_insurance/README.md'),
    ]:
        report(title, rel)

    report('Deeper follow-up: current integrated synthesis', 'reports/EXTENSION_SYNTHESIS.md', required=True)
    report('Visual memo mechanism briefs: presentation, not additional evidence', 'story_assets/mechanism_story.md', 'The unrelated four-page audit reference informs layout only.')
    for path in sorted((ROOT / 'story_assets').glob('*.md')):
        if path.name == 'mechanism_story.md':
            continue
        report('Visual memo page briefs: ' + path.stem, path.relative_to(ROOT).as_posix(), 'These are readable presentations of the recorded research, not additional studies, customer records or effects.')
    for title, rel in [
        ('Deeper follow-up: automotive review counterexamples', 'workstreams/extension_reviews/EXTENSION_REVIEW_REPORT.md'),
        ('Deeper follow-up: geographic robustness', 'workstreams/extension_geography/GEOGRAPHY_ROBUSTNESS_REPORT.md'),
        ('Deeper follow-up: independent geography challenge', 'workstreams/extension_geography/INDEPENDENT_CHALLENGE.md'),
        ('Deeper follow-up: live website journeys', 'workstreams/extension_journeys/REPORT.md'),
        ('Deeper follow-up: economic mechanisms and obligations', 'workstreams/extension_economics/EXTENSION_ECONOMICS_REPORT.md'),
        ('Deeper follow-up: external mechanisms and accounting coverage', 'workstreams/extension_hypotheses/REPORT.md'),
        ('Deeper follow-up: independent source and accounting review', 'workstreams/extension_hypotheses/INDEPENDENT_REVIEW.md'),
        ('Deeper follow-up: independent lifecycle and menu challenge', 'workstreams/extension_stakeholders/independent_mece_challenge.md'),
    ]:
        report(title, rel, required=True)
    # Capture every additional readable extension report without guessing filenames.
    already = set(used_inputs)
    for directory in ['extension_battery', 'extension_stakeholders', 'extension_journeys']:
        for path in sorted((ROOT / 'workstreams' / directory).glob('*.md')):
            rel = path.relative_to(ROOT).as_posix()
            if rel in already or path.name in ['ANALYSIS_SPECIFICATION.md', 'PREREGISTRATION.md']:
                continue
            if any(word in path.name.lower() for word in ['report', 'finding', 'challenge', 'audit', 'summary', 'readme']):
                report('Additional current extension record: ' + directory + '/' + path.stem, rel)
    if not battery_reports:
        add('Battery extension: final readable report pending', battery_status + '\n\nThe current audit provides the source counts and corrected sign interpretation above. A missing final report is not replaced by fabricated capacity estimates. The final builder rerun will include any readable battery report once present.')

    # Exact structured capsules preserve nuances not necessarily quoted in prose reports.
    capsules('Friend challenge: all forty analytical groups', 'workstreams/friend_challenge/claims.json', 'claim_id', [
        ('friend_section','Original section'),('short_paraphrase','Scoped claim'),('type','Claim type'),('subclaims','Distinct scoped clauses'),('mapped_original_hypotheses','Original hypothesis links'),('current_evidence_refs','Evidence references'),('initial_evidenceability','What can be observed'),('strongest_rival','Strongest rival'),('falsifier_or_scope_limiter','Falsifier or boundary'),('current_status','Current status'),('completed_crosschecks','Completed source checks'),('pending_crosschecks','Pending checks'),('causal_effect_established','Causal effect established')
    ], note='FC IDs here belong to the friend_challenge namespace. Source examination is not confirmation of a business mechanism.')
    capsules('Capability register: entity-specific checks', 'workstreams/friend_capabilities/claim_matrix.json', 'claim_id', [
        ('subject','Subject'),('supplied_claim_or_inference','Claim examined'),('status','Status'),('verified_finding','Verified source statement'),('entity_and_time_scope','Entity and period'),('source_ids','Sources'),('printed_pages','Printed pages'),('pdf_pages_1based','PDF pages'),('limitation','Limit'),('research_implication','Implication'),('causal_effect_established','Causal effect established')
    ], note='FC IDs here belong to capabilities, not the preceding friend groups. Public architecture is not access permission or adoption.')
    capsules('Insurance register: coverage, contracts and risk boundaries', 'workstreams/friend_insurance/claim_matrix.json', 'claim_id', [
        ('friend_claim_tested','Question examined'),('scoped_finding','Scoped source finding'),('verification_status','Verification state'),('source_type','Source type'),('source_date_scope','Date scope'),('document_locator','Locator'),('source_url','Primary source'),('research_implication','Implication'),('financial_role_note','Financial role'),('raw_content_note','Access qualification'),('causal_or_commercial_effect','Commercial evidence')
    ], note='No product-specific legal approval, signed distribution agreement, repair-routing guarantee or RVI quotation is inferred.')
    capsules('Survey register: question-by-question denominators', 'workstreams/friend_surveys/survey_claims.json', 'claim_id', [
        ('study','Study'),('edition','Edition'),('country','Geography'),('metric','Metric'),('value','Published or supplied value'),('unit','Unit'),('question_cohort','Question cohort'),('country_question_n','Country base'),('regional_question_n','Regional base'),('verification_status','Verification status'),('comparison_limit','Comparison boundary'),('source_locator','Locator'),('source_url','Source')
    ], note='Do not add bases or reuse a regional denominator as an Indonesian subgroup. User-supplied unverified chart values retain that status.')
    capsules('Market register: all scoped external observations', 'workstreams/market/evidence.json', 'evidence_id', [
        ('observation','Observation'),('population_or_scope','Population or scope'),('evidence_period','Period'),('sample_n','Reported base'),('evidence_state','Evidence state'),('interpretation','Interpretation'),('strongest_rival_or_negative_case','Rival or negative case'),('limitation','Limit'),('ownership_cluster','Source lineage'),('locator','Locator'),('source_url','Source')
    ], note='Rows are source observations; repeated issuer/study lineages are not independent surveys.')
    capsules('Extension stakeholder register: new scoped observations', 'workstreams/extension_stakeholders/evidence_register.json', 'evidence_id', [
        ('fact_or_scoped_observation','Scoped observation'),('scope','Scope'),('source_urls','Primary URLs'),('source_ids','Source IDs'),('limitation','Limit'),('implication_hypothesis','Possible implication'),('evidence_kind','Evidence kind'),('independent_need_count','Independent need count'),('causal_effect_established','Causal effect established')
    ])
    capsules('Lifecycle register: all twenty-six analytical job units', 'workstreams/extension_stakeholders/lifecycle_jobs.json', 'job_id', [
        ('stage','Lifecycle stage'),('canonical_customer_job','Customer or institutional outcome'),('analytical_unit','Analytical unit'),('decision_owners','Decision owners'),('menu_ids','Frozen menu links'),('evidence_ids','Evidence references'),('powertrain_boundary','Powertrain boundary'),('excluded_or_disadvantaged_customer','Potential reach or exclusion boundary'),('coverage_status','Coverage state'),('decision_rights_status','Authority qualification'),('count_note','Counting rule'),('overlap_rule','Overlap rule')
    ], note='Twenty-five customer/fleet outcome units plus one institutional risk layer. Linked rows can be dependencies within one case and are not summed as demand.')
    capsules('Stakeholder register: all decision-right and incentive lenses', 'workstreams/extension_stakeholders/stakeholder_decision_rights.json', 'stakeholder_id', [
        ('actor_or_lens','Actor or lens'),('decision_right_or_constraint','Decision right or constraint'),('grounded_scope','Grounded source scope'),('incentive_hypothesis_not_observed','Unobserved incentive hypothesis'),('material_conflict','Material conflict'),('customer_at_risk_of_exclusion','Potential exclusion'),('evidence_ids','Evidence references'),('internal_authority_or_incentive_verified','Internal authority or incentive verified')
    ], note='Stakeholder perspectives organize questions. They are not interviews, verified internal incentives or additional independent needs.')
    capsules('Independent menu audit: all twenty-seven concept updates', 'workstreams/extension_stakeholders/all_27_option_audit.json', 'solution_id', [
        ('new_evidence_ids','New evidence references'),('baseline_or_counterevidence','Baseline or counterevidence'),('remaining_possible_distinction','Remaining distinction'),('simpler_or_existing_alternative','Simpler or existing alternative'),('decisive_uncertainty_or_falsifier','Decisive uncertainty or falsifier'),('excluded_or_disadvantaged_group','Potentially excluded group'),('audit_disposition','Audit disposition'),('decision_rights','Decision rights'),('linked_canonical_jobs','Lifecycle links'),('linkage_note','Linkage rule'),('excluded_group_status','Exclusion evidence status'),('no_new_unmet_need_or_effect_established','No new unmet need or effect established')
    ], note='This is an extension audit of the same frozen menu, not twenty-seven new concepts or a rank.')
    capsules('Extension candidate: separate from the frozen menu', 'workstreams/extension_stakeholders/new_option_candidates.json', 'candidate_id', [
        ('title','Candidate'),('canonical_job_id','Lifecycle job'),('material_difference','Distinct task'),('existing_baseline','Existing baseline'),('possible_unresolved_difference','Unresolved difference'),('support_evidence_ids','Evidence'),('counterevidence','Counterevidence'),('decision_rights','Decision rights'),('benefit_hypothesis','Benefit hypothesis'),('commercial_mechanism','Commercial boundary'),('excluded_customers','Reach limits'),('failure_condition','Failure condition'),('status','Status')
    ], note='Not a selected solution or automatic 28th menu item.')
    capsules('External mechanism register: seven studies or instruments', 'workstreams/extension_hypotheses/EXTERNAL_MECHANISM_EVIDENCE.json', 'id', [
        ('title','Title'),('authors','Authors'),('year','Publication year'),('design','Design'),('observed_endpoint','Actual endpoint'),('finding','Scoped finding'),('limits','Limits'),('hypothesis_links','Original hypothesis links'),('transferability','Transfer boundary'),('primary_locator','Locator'),('url','Primary reference')
    ])

    # Compact numeric receipts retain actual details without embedding millions of rows.
    numeric_rel = [
        'workstreams/friend_capabilities/economic_diagnostics.json',
        'workstreams/extension_geography/KEY_FINDINGS.json',
        'workstreams/extension_economics/portfolio_decompositions.json',
        'workstreams/extension_economics/program_distinctions.json',
        'workstreams/extension_economics/dated_service_estimate_sums.json',
        'workstreams/extension_economics/constructed_aggregate_risk.json',
        'workstreams/extension_economics/constructed_contract_tail.json',
        'workstreams/extension_battery/SIGN_ENDPOINT_AUDIT.json',
        'workstreams/extension_battery/BATTERY_SUMMARY.json',
        'workstreams/extension_battery/KEY_FINDINGS.json',
        'workstreams/extension_battery/RAW_PRIVACY_AND_LICENSE_REVIEW.json',
        'workstreams/extension_battery/QA_RECEIPT.json',
        'workstreams/extension_reviews/interpretation_summary.json',
        'workstreams/extension_reviews/validation.json',
        'workstreams/extension_journeys/summary.json',
    ]
    numeric = ['These receipts are structured calculations or status summaries. They do not add source observations and are not forecasts. Original signal counts exclude time and epoch fields; numeric maxima do not overturn a sign distribution.', '']
    for rel in numeric_rel:
        data = jread(rel)
        if data is not None:
            numeric += ['### ' + rel, '', '```json', json.dumps(data, ensure_ascii=False, indent=2), '```', '']
    add('Detailed calculation and status receipts', '\n'.join(numeric))

    report('Reproducibility, dependency and acquisition boundaries', 'reports/REPRODUCIBILITY.md')
    report('Raw dataset rights and exact-byte/transformed distinctions', 'raw_licensed_data/README.md')
    report('Data guide and source tracing', 'DATA_GUIDE.md', 'This first-wave guide remains useful; the current ledger and extension chapters give later counts.')

    # Named anchors replace the six private storage URLs while retaining source identity.
    add('Named references for privately supplied historical documents', '''
The following names identify material referenced by the original context; they do not publish the private documents. Public re-verification and our own summaries are in the cited workstreams. A source name is not proof that the original dossier's masked chart was independently read in this run.

### Source reference: casebook

**IBSC 2026 Semifinal Casebook**, user-supplied competition baseline. Full private PDF excluded. The user's historical context preserves their relevant summary. Current numerical checks are in reports/NUMERICAL_QA.md. Do not call its financial exhibit audited public Auto2000 accounts.

### Source reference: Astra annual report

**Astra Annual Report 2025**, source filename equivalent: Astra-Annual-Report-2025.pdf. Reverified from its official public host; source locators and scoped capability checks are in workstreams/friend_capabilities/. The original private storage link is unnecessary and removed.

### Source reference: Statista EV

**Statista, Electric vehicle market in Indonesia**, user-supplied dossier named in the historical context. Full private dossier excluded. Current survey_claims.json distinguishes primary checked values, metadata-only access and user-provided unverified chart values.

### Source reference: Statista automotive

**Statista, Automotive industry in Indonesia**, user-supplied dossier including the cited awareness slide. Full private dossier excluded. Original chart values 57/28/55/45 remain user-provided where not independently inspectable; arithmetic on them does not verify the source or establish causality.

### Source reference: prior analysis Markdown

**Earlier strategic analysis, Markdown**, named in the user's original context. Its private Library URL is redacted. The current master context includes the supplied historical summary and the research's newer evidence, not an invented reconstruction of an inaccessible private document.

### Source reference: prior analysis PDF

**Earlier strategic analysis, PDF**, reading companion named in the original context. Private PDF not redistributed. Current reports and the historical appendix preserve the relevant decision distinctions without including account links.
''')

    add('Historical appendix: original friend master context with private-storage links redacted', f'''
**HISTORICAL USER-SUPPLIED TEXT.** This appendix preserves the original supplied document's wording, tables, public references and language. It is not the current instruction set, verified final finding set or a selected plan. Earlier implementation/pilot suggestions, Indonesian writing preferences and unresolved values must be read through the current mandate and evidence above.

Original filename: `{args.original.name}`. Original words: {len(original.split()):,}. Original SHA256: `{original_hash}`. The original external file has not been modified. **Historical text is preserved except for six private-storage URL redactions**, replacing their reference-definition targets with the named source anchors immediately above. No private file ID or account URL is retained. Exactly six source lines change and line count remains unchanged.

---

{historical}

---

**END HISTORICAL APPENDIX.** Current English research-only scope, latest corrected evidence, privacy exclusions and user choice take precedence over any historical instructions or speculation in the appendix.
''')

    # The source manifest is about input versions, not a new collection or completion claim.
    manifest = ['Every listed input was read from this workspace without new public retrieval by this builder. SHA256 values identify the exact build inputs. A report may itself summarize the same source as another report; this inventory is not an independence count.', '', '| Input | Bytes | SHA256 |', '|---|---:|---|']
    for rel, meta in sorted(used_inputs.items()):
        manifest.append(f"| `{rel}` | {meta['bytes']:,} | `{meta['sha256']}` |")
    if missing_inputs:
        manifest += ['', '### Missing expected readable artifacts at this build', '', '; '.join(sorted(set(missing_inputs))) + '. These remain pending and must not be represented as completed results.']
    add('Build provenance and pending-artifact receipt', '\n'.join(manifest))

    toc = ['# Auto2000 Digiroom: updated master AI context', '', f'Built {NOW}. Current English synthesis plus preserved historical input. Detailed evidence context, not an implementation or selected strategy.', '', '## Contents', '']
    for idx, (title, _) in enumerate(sections, 1):
        toc.append(f'{idx}. {title}')
    body = '\n'.join(toc) + '\n\n'
    for idx, (title, text) in enumerate(sections, 1):
        body += f'\n\n## Chapter {idx}. {title}\n\n{text}\n'
    body = clean_private_links(body)
    # Strict public-context safeguards, not a claim of universal privacy certification.
    forbidden = ['chatgpt.com/library', 'libfile_', 'oai-library://', 'account_id=']
    for marker in forbidden:
        if marker in body:
            raise RuntimeError('Private-storage marker survived redaction: ' + marker)
    historical_start = body.index('\n'.join(historical.splitlines()[:3]), body.index('**HISTORICAL USER-SUPPLIED TEXT.**'))
    historical_end = body.index('\n\n---\n\n**END HISTORICAL APPENDIX.**', historical_start)
    assert body[historical_start:historical_end].rstrip() == historical.rstrip(), 'Output historical text changed beyond the six permitted redactions.'
    words = len(body.split())
    if words < 30000:
        raise RuntimeError(f'Substantive context is only {words} words; expected 30k+ from actual reports and source capsules. Do not pad with invented content.')
    assert hashlib.sha256(args.original.read_bytes()).hexdigest() == original_hash
    local_link_checks = []
    for destination in re.findall(r'\]\(([^)]+)\)', body):
        if destination.startswith(('http:', 'https:', '#', 'mailto:', 'data:')) or ' ' in destination or '"' in destination:
            continue
        target = (args.output.parent / destination).resolve()
        local_link_checks.append({'target': destination, 'exists': target.exists()})
    unresolved_local_links = sorted({item['target'] for item in local_link_checks if not item['exists']})
    profile_markers_found = [marker for marker in ['Yang Mulia', 'Dosen S3', 'AGENTS.md'] if marker in body]
    if profile_markers_found:
        raise RuntimeError('Unrelated profile/instruction markers appeared in the context.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(body)
    receipt = {
        'built_utc': NOW, 'output': args.output.name, 'words_whitespace': words, 'bytes_utf8': len(body.encode()),
        'sha256': hashlib.sha256(body.encode()).hexdigest(), 'chapters': len(sections),
        'historical_original_sha256': original_hash, 'historical_source_words': len(original.split()),
        'historical_private_url_redactions': replacements, 'historical_lines_changed': len(redacted_lines),
        'historical_output_matches_redacted_original': True,
        'original_source_unchanged': True, 'private_storage_markers_found': 0,
        'unrelated_profile_markers_found': 0, 'local_link_targets_checked': len(local_link_checks), 'unresolved_local_links': unresolved_local_links,
        'inputs': used_inputs, 'missing_expected_artifacts': sorted(set(missing_inputs)),
        'battery_signal_values_excluding_clocks': actual_values, 'battery_mat_files_downloaded': len(bmanifest),
        'battery_mat_files_staged': len(raw_mats), 'mobile_journeys_current_summary': mobile_n,
        'new_reviews': reviews.get('new_rows'), 'combined_review_ids': reviews.get('combined_unique_review_ids'),
        'identical_report_aliases': report_aliases,
        'visual_reference': visual_reference_meta, 'final_visual_pdf': final_pdf_meta,
        'visual_memo_qa_receipts': story_qa_receipts,
        'final_visual_qa_state': final_visual_qa_state,
        'no_new_retrieval_by_builder': True, 'human_validation': False, 'winning_strategy_selected': False,
    }
    (args.output.parent / 'MASTER_CONTEXT_BUILD_RECEIPT.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2))
    print(json.dumps({k: v for k, v in receipt.items() if k != 'inputs'}, ensure_ascii=False))

if __name__ == '__main__':
    main()
