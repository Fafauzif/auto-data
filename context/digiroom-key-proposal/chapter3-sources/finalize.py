"""Repair appendix anchors and set TOC pages from a freshly rendered PDF."""
from pathlib import Path
import argparse,re
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import fitz

B=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--docx',type=Path,default=B/'drafts/Digiroom_KEY_Chapters_1_to_3.docx')
p.add_argument('--pdf',type=Path,required=True,help='Fresh proof rendered from this DOCX before updating its TOC')
a=p.parse_args();d=Document(a.docx)
existing={e.get(qn('w:name')) for e in d.element.xpath('.//w:bookmarkStart')}
serial=max((int(e.get(qn('w:id'))) for e in d.element.xpath('.//w:bookmarkStart')),default=0)
for para in d.paragraphs:
 m=re.match(r'^(A\d+)\s{2}',para.text)
 if m and para.style.name.startswith('Heading') and m.group(1) not in existing:
  serial+=1;start=OxmlElement('w:bookmarkStart');start.set(qn('w:name'),m.group(1));start.set(qn('w:id'),str(serial))
  end=OxmlElement('w:bookmarkEnd');end.set(qn('w:id'),str(serial));para._p.extend([start,end]);existing.add(m.group(1))
with fitz.open(a.pdf) as pdf:
 texts=[' '.join(x.get_text().split()) for x in pdf]
for para in d.paragraphs[1:]:
 if para.style.name=='Heading 1':break
 label=''.join(para._p.xpath('./w:hyperlink//w:t/text()'))
 if not label:continue
 hits=[i+1 for i,t in enumerate(texts) if i>0 and ' '.join(label.split()) in t]
 if not hits:raise ValueError(f'TOC heading not found in proof: {label}')
 for child in list(para._p):
  if child.tag==qn('w:r'):para._p.remove(child)
 para.add_run('  '+str(hits[0]))
d.save(a.docx)
print(f'Updated anchors and TOC: {a.docx}')
