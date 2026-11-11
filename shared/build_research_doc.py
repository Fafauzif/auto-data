from pathlib import Path
import re
from docx import Document
from docx.shared import Inches,Pt,RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.table import WD_TABLE_ALIGNMENT,WD_CELL_VERTICAL_ALIGNMENT
ROOT=Path(__file__).resolve().parents[1];d=Document();sec=d.sections[0]
sec.page_width=Inches(8.5);sec.page_height=Inches(11);sec.top_margin=sec.bottom_margin=Inches(.7);sec.left_margin=sec.right_margin=Inches(.75)
for name in ['Normal','Title','Subtitle','Heading 1','Heading 2','Heading 3','Caption']:
 s=d.styles[name];s.font.name='Calibri';s.font.color.rgb=RGBColor(0,0,0)
n=d.styles['Normal'];n.font.size=Pt(11);n.paragraph_format.space_after=Pt(7);n.paragraph_format.line_spacing=1.12
for name,size in [('Title',26),('Heading 1',16),('Heading 2',13)]:
 s=d.styles[name];s.font.size=Pt(size);s.paragraph_format.space_before=Pt(13);s.paragraph_format.space_after=Pt(7)
d.styles['Title'].paragraph_format.space_before=Pt(0)
header=sec.header.paragraphs[0];header.add_run('AUTO2000 DIGIROOM  |  RESEARCH FINDINGS').font.size=Pt(8)
f=sec.footer.paragraphs[0];f.alignment=2;f.add_run('11 November 2026  |  ');fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');f._p.append(fld)
lines=(ROOT/'reports/RESEARCH_REPORT.md').read_text().splitlines();i=0
while i<len(lines):
 line=lines[i]
 if line.startswith('|'):
  rows=[]
  while i<len(lines) and lines[i].startswith('|'):
   cells=[x.strip() for x in lines[i].strip('|').split('|')]
   if not all(set(x)<=set('-: ') for x in cells):rows.append(cells)
   i+=1
  t=d.add_table(rows=0,cols=len(rows[0]));t.alignment=WD_TABLE_ALIGNMENT.CENTER;t.autofit=False
  widths=[1.6,3.0,2.4] if len(rows[0])==3 else [7/len(rows[0])]*len(rows[0])
  for col,w in zip(t.columns,widths):col.width=Inches(w)
  for idx,row in enumerate(rows):
   cells=t.add_row().cells
   for j,txt in enumerate(row):
    c=cells[j];c.width=Inches(widths[j]);c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER;p=c.paragraphs[0];p.paragraph_format.space_before=Pt(5);p.paragraph_format.space_after=Pt(5);p.paragraph_format.line_spacing=1.08
    r=p.add_run(txt);r.font.size=Pt(9.5);r.bold=idx==0
    if idx==0:r.font.color.rgb=RGBColor(255,255,255)
    pr=c._tc.get_or_add_tcPr();b=OxmlElement('w:tcBorders')
    for edge in ['top','bottom','left','right']:
     x=OxmlElement('w:'+edge);x.set(qn('w:val'),'single');x.set(qn('w:sz'),'4');x.set(qn('w:color'),'D9D9D9');b.append(x)
    pr.append(b);shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'244A68' if idx==0 else ('F3F6F8' if idx%2==0 else 'FFFFFF'));pr.append(shade)
   tr=t.rows[-1]._tr.get_or_add_trPr();ns=OxmlElement('w:cantSplit');tr.append(ns)
   if idx==0:rep=OxmlElement('w:tblHeader');tr.append(rep)
  d.add_paragraph();continue
 if line.startswith('!['):
  m=re.match(r'!\[(.*?)\]\((.*?)\)',line)
  if m:
   p=d.add_paragraph();p.alignment=1;p.paragraph_format.keep_with_next=True;p.paragraph_format.space_after=Pt(0)
   p.add_run().add_picture(str((ROOT/'reports'/m.group(2)).resolve()),width=Inches(6.6))
   c=d.add_paragraph(m.group(1),'Caption');c.paragraph_format.space_before=Pt(0);c.paragraph_format.space_after=Pt(5)
   for r in c.runs:r.font.size=Pt(8.5)
 elif line.startswith('# '):d.add_paragraph(line[2:],'Title')
 elif line.startswith('## '):d.add_paragraph(line[3:],'Heading 1')
 elif line.startswith('- '):d.add_paragraph(line[2:],'List Bullet')
 elif line.strip():d.add_paragraph(line)
 i+=1
for el in list(d._element.xpath('//w:pBdr')):el.getparent().remove(el)
for style in d.styles:
 for el in list(style.element.xpath('.//w:pBdr')):el.getparent().remove(el)
d.save(ROOT/'reports/AUTO2000_RESEARCH_REPORT.docx');print('Createdmainreport')
