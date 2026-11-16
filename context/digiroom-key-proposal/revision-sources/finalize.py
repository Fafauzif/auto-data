from pathlib import Path
from docx import Document
from docx.shared import Cm,Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
import fitz,json,collections
B=Path(__file__).resolve().parents[1];p=B/'drafts/Digiroom_KEY_Chapters_1_and_2_Revised.docx';d=Document(p)
for t in d.tables:
 is_interview=t.cell(0,0).text=='Question or topic'
 for row in t.rows:
  for j,c in enumerate(row.cells):
   if is_interview:c.width=Cm(5.8 if j==0 else 11.2)
   for para in c.paragraphs:para.alignment=WD_ALIGN_PARAGRAPH.LEFT
for para in d.paragraphs:
 if para.text.startswith('Return to') or para.text.startswith('Interview '):para.paragraph_format.keep_with_next=True
 if para.text.startswith('Exhibit A'):
  para.paragraph_format.keep_with_next=True
 for h in para._p.xpath('.//w:hyperlink'):
  rid=h.get(qn('r:id'))
  if rid and 'Google Play listing' in ''.join(h.xpath('.//w:t/text()')):
   # Reuse exact external source address from the original proposal.
   d.part.rels[rid]._target='https://play.google.com/store/apps/details?id=id.co.astra.ai.dev1&hl=id&gl=ID'
# Exact visible IDs at linked evidence destinations.
for para in d.paragraphs:
 for b in para._p.xpath('./w:bookmarkStart'):
  name=b.get(qn('w:name'))
  labels={'A6_1':'Exhibit A6.1  Exact payment comparison','A7_1':'Exhibit A7.1  Paired routing results','A12_1':'Exhibit A12.1  Usable equity calculation'}
  if name in labels and not para.text:para.add_run(labels[name]).bold=True
# TOC page references from current render; these do not affect main text pagination.
pdf=fitz.open('/tmp/digiroom-revised-render2/Digiroom_KEY_Chapters_1_and_2_Revised.pdf')
texts=[x.get_text() for x in pdf]
for para in d.paragraphs:
 if para._p.getprevious() is not None:
  hs=para._p.xpath('./w:hyperlink')
  if len(hs)==1:
   a=hs[0].get(qn('w:anchor'))
   if a in ['summary','intro','analysis','recommendations','implementation','conclusion','references','appendix_index'] or (a and a.startswith('claim')):
    # Only the front-matter entries (before the executive summary heading).
    prev=para._p.getprevious(); before=True
    for el in list(d.element.body):
     if el is para._p:break
     if ''.join(el.xpath('.//w:t/text()'))=='EXECUTIVE SUMMARY':before=False
    if before:
     label=''.join(hs[0].xpath('.//w:t/text()'))
     key=label[3:] if a.startswith('claim') else label
     found=[i+1 for i,t in enumerate(texts) if i>0 and key in t.replace('\n',' ')]
     if found:
      para.add_run('  '+str(found[0]))
d.save(p)
