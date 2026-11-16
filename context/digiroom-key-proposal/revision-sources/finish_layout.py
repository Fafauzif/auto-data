from pathlib import Path
from docx import Document
from docx.shared import Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE
B=Path('context/digiroom-key-proposal');p=B/'drafts/Digiroom_KEY_Chapters_1_and_2_Revised.docx';d=Document(p)
for t in d.tables:
 if t.cell(0,0).text=='Question or topic':
  for row in t.rows:
   for c in row.cells:
    for para in c.paragraphs:para.paragraph_format.space_before=Pt(1);para.paragraph_format.space_after=Pt(1)
for para in d.paragraphs:
 if para.text=='Figure 1. Service booking channels and the main activities of Digiroom’s monthly active users.':
  para.runs[0].text='Figure 1. Service booking channels and Digiroom audience measures.'
 if para.text.startswith('Included scheduled service follows'):
  for r in para.runs:r.text=r.text.replace('the time-only example;','the time-only example in Figure 6;')
 if para.text.startswith('Sources: selected public Google Play'):
  for el in list(para._p):
   if el.tag!=qn('w:pPr'):para._p.remove(el)
  para.add_run('Sources: selected Google Play and Apple App Store reviews; authors’ coding of task, rating, and publication date. ')
  h=OxmlElement('w:hyperlink');h.set(qn('r:id'),para.part.relate_to('https://play.google.com/store/apps/details?id=id.co.astra.ai.dev1&hl=id&gl=ID',RELATIONSHIP_TYPE.HYPERLINK,is_external=True));r=OxmlElement('w:r');pr=OxmlElement('w:rPr');u=OxmlElement('w:u');u.set(qn('w:val'),'single');pr.append(u);r.append(pr);t=OxmlElement('w:t');t.text='Digiroom on Google Play';r.append(t);h.append(r);para._p.append(h)
d.save(p)
