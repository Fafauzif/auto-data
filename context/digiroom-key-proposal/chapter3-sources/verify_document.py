from pathlib import Path
from zipfile import ZipFile
from collections import Counter
from lxml import etree
import fitz,json,re
B=Path(__file__).resolve().parents[1]
p=B/'drafts/Digiroom_KEY_Chapters_1_to_3.docx'
with ZipFile(p) as z:
 root=etree.fromstring(z.read('word/document.xml'));names=z.namelist()
 ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
 keys=root.xpath('//w:bookmarkStart/@w:name',namespaces=ns);links=root.xpath('//w:hyperlink/@w:anchor',namespaces=ns)
 missing=sorted(set(links)-set(keys));duplicates={k:v for k,v in Counter(keys).items() if v>1}
 text=' '.join(root.xpath('//w:t/text()',namespaces=ns))
 tables=root.xpath('//w:tbl',namespaces=ns)
 borders=[len(t.xpath('./w:tblPr/w:tblBorders/*',namespaces=ns))==6 for t in tables]
 sizes=[r.xpath('./w:rPr/w:sz/@w:val',namespaces=ns) for t in tables for r in t.xpath('.//w:r[w:t]',namespaces=ns)]
 report={'missing_links':missing,'duplicate_bookmarks':duplicates,'appendix_bookmarks':sum(bool(re.fullmatch('A\\d+',k)) for k in keys),'internal_links':len(links),'editable_tables':len(tables),'all_tables_full_grid':all(borders),'all_table_runs_10pt':all(v==['20'] for v in sizes),'casebook_mentions':len(re.findall('casebook',text,re.I)),'comments_parts':[n for n in names if 'comment' in n.lower()],'tracked_changes':len(root.xpath('//w:ins|//w:del',namespaces=ns))}
assert not missing and not duplicates
assert all(borders) and all(v==['20'] for v in sizes)
assert not report['casebook_mentions'] and not report['comments_parts'] and not report['tracked_changes']
print(json.dumps(report,indent=2))

