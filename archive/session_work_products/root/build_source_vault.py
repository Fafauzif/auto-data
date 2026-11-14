#!/usr/bin/env python3
"""Preserve exact historical delivery ZIPs separately from the active repo."""
from pathlib import Path
import importlib.util,json,shutil
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('archival_builder',Path(__file__).with_name('build_archive.py'))
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
module.OUT=ROOT/'integration_work/source_vault'
b=module.Builder()
archives=list(ROOT.glob('*.zip'))+list((ROOT/'analysis_followup').glob('*.zip'))+list((ROOT/'planning_audit').glob('*.zip'))+[ROOT/'integration_work/intake/Auto2000_Keputusan_Lanjutan_Sumber_Lengkap.zip']
for p in sorted(archives):
 if p.is_file():b.ingest(p,Path('original_containers')/p.name,'exact_original_archive',p)
for p in sorted((ROOT/'integration_work/intake').glob('*.json')):
 b.ingest(p,Path('intake_receipts')/p.name,'source_receipt',p)
b.write()
(module.OUT/'scripts').mkdir(exist_ok=True)
shutil.copy2(ROOT/'integration_work/release_repo/scripts/source_archive.py',module.OUT/'scripts/source_archive.py')
(module.OUT/'.gitignore').write_text('.restored/\n__pycache__/\n')
(module.OUT/'README.md').write_text('''# Auto2000 exact source-container vault

Private companion to the integrated research repository. The primary repository
already contains the source members and analytical outputs. This companion
preserves the original delivery ZIP bytes, including their original compression
and metadata. It is not an alternative analytical reading route.

All files are at most 90,000,000 bytes. The large latest ZIP is divided into
80,000,000-byte binary parts; original SHA-256 and per-part hashes are recorded in
`manifests/source_inventory.jsonl`. Duplicate container bytes are stored once.

Verify all exact original containers:

```console
python scripts/source_archive.py verify
```

Restore the latest original source ZIP under ignored `.restored/`:

```console
python scripts/source_archive.py restore "original_containers/Auto2000_Keputusan_Lanjutan_Sumber_Lengkap.zip"
```

Keep restored large ZIPs outside a tracked Git tree. The source-container vault
is optional for reading or reproducing the primary repository analyses.
''')
