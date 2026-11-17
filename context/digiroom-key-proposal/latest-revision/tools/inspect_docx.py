"""Read-only DOCX structural inspection. Python 3.10+, standard library only."""
import sys,json,hashlib
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as E
p=Path(sys.argv[1]);ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
with ZipFile(p) as z:
 r=E.fromstring(z.read('word/document.xml'))
 bookmarks=[b.get('{'+ns['w']+'}name') for b in r.findall('.//w:bookmarkStart',ns)]
 anchors=[b.get('{'+ns['w']+'}anchor') for b in r.findall('.//w:hyperlink',ns) if b.get('{'+ns['w']+'}anchor')]
 out={'file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'tables':len(r.findall('.//w:tbl',ns)),'drawings':len(r.findall('.//w:drawing',ns)),'missing_anchors':sorted(set(anchors)-set(bookmarks)),'duplicate_bookmarks':len(bookmarks)-len(set(bookmarks)),'comment_parts':[n for n in z.namelist() if 'comment' in n.lower()],'tracked_changes':len(r.findall('.//w:ins',ns))+len(r.findall('.//w:del',ns))}
print(json.dumps(out,indent=2))
raise SystemExit(bool(out['missing_anchors'] or out['duplicate_bookmarks'] or out['tracked_changes'] or out['comment_parts']))
