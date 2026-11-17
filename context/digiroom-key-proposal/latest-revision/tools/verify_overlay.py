"""Verify FILES.sha256 from a repo root containing the extracted overlay."""
from pathlib import Path
import hashlib,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.')
failed=[];count=0
for line in (root/'DIGIROOM_KEY_FINAL_FILES.sha256').read_text().splitlines():
 expected,name=line.split('  ',1);p=root/name;count+=1
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=expected:failed.append(name)
print({'checked':count,'failed':failed})
raise SystemExit(bool(failed))
