import json,os
from pathlib import Path
from docx import Document
from docx.shared import Inches,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT,WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
base=Path(__file__).parent
src=json.loads((base/'report_source.json').read_text()); d=Document(); sec=d.sections[0]
sec.page_width=Inches(8.5);sec.page_height=Inches(11);sec.top_margin=Inches(.65);sec.bottom_margin=Inches(.65);sec.left_margin=Inches(.75);sec.right_margin=Inches(.75)
styles=d.styles
for name in ['Normal','Title','Subtitle','Heading 1','Heading 2','Heading 3','Caption']:
 s=styles[name];s.font.name='Arial';s.font.color.rgb=RGBColor(0,0,0)
styles['Normal'].font.size=Pt(11);styles['Normal'].paragraph_format.line_spacing=1.12;styles['Normal'].paragraph_format.space_after=Pt(9)
styles['Title'].font.size=Pt(24);styles['Title'].font.bold=True;styles['Title'].paragraph_format.space_after=Pt(12)
styles['Subtitle'].font.size=Pt(12);styles['Subtitle'].paragraph_format.space_after=Pt(10)
styles['Heading 1'].font.size=Pt(17);styles['Heading 1'].paragraph_format.space_before=Pt(0);styles['Heading 1'].paragraph_format.space_after=Pt(13)
styles['Heading 2'].font.size=Pt(12);styles['Heading 2'].paragraph_format.space_before=Pt(10);styles['Heading 2'].paragraph_format.space_after=Pt(6)
for name in ['Title','Subtitle','Heading 1','Heading 2','Heading 3']:
 ppr=styles[name].element.find(qn('w:pPr'))
 if ppr is not None:
  for el in list(ppr):
   if el.tag==qn('w:pBdr'):ppr.remove(el)
footer=sec.footer.paragraphs[0];footer.alignment=WD_ALIGN_PARAGRAPH.RIGHT
r=footer.add_run('Auto2000 research assessment  |  ');r.font.size=Pt(9)
fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');footer._p.append(fld)
def p(text,small=False):
 x=d.add_paragraph(text)
 if small:
  x.paragraph_format.space_after=Pt(6)
  for r in x.runs:r.font.size=Pt(9.5)
 return x

def table(obj):
 heads=obj['headers'];rows=obj['rows'];t=d.add_table(rows=1,cols=len(heads));t.alignment=WD_TABLE_ALIGNMENT.CENTER;t.autofit=False
 widths=[2.15,4.85] if len(heads)==2 else ([3.0,2.0,2.0] if len(heads)==3 else [1.4]*len(heads))
 if len(heads)==3 and heads[0]=='Deloitte 2026 measure':widths=[2.7,1.25,3.05]
 for c,w in zip(t.columns,widths):c.width=Inches(w)
 pr=t._tbl.tblPr;b=OxmlElement('w:tblBorders')
 for edge in ['top','left','bottom','right','insideH','insideV']:
  z=OxmlElement('w:'+edge);z.set(qn('w:val'),'single');z.set(qn('w:sz'),'4');z.set(qn('w:color'),'D9D9D9');b.append(z)
 pr.append(b)
 for i,vals in enumerate([heads]+rows):
  row=t.rows[0] if i==0 else t.add_row()
  rp=row._tr.get_or_add_trPr()
  if i==0:
   rep=OxmlElement('w:tblHeader');rp.append(rep)
  keep=OxmlElement('w:cantSplit');rp.append(keep)
  for j,(cell,txt) in enumerate(zip(row.cells,vals)):
   cell.width=Inches(widths[j]);cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
   tcpr=cell._tc.get_or_add_tcPr();mar=OxmlElement('w:tcMar')
   for side,v in [('top','90'),('bottom','90'),('left','110'),('right','110')]:
    z=OxmlElement('w:'+side);z.set(qn('w:w'),v);z.set(qn('w:type'),'dxa');mar.append(z)
   tcpr.append(mar)
   sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'23384D' if i==0 else ('F2F5F7' if i%2==0 else 'FFFFFF'));tcpr.append(sh)
   cell.text=txt
   for x in cell.paragraphs:
    x.paragraph_format.space_after=Pt(0);x.paragraph_format.line_spacing=1.06
    if len(heads)>2 and j>0:x.alignment=WD_ALIGN_PARAGRAPH.CENTER
    for r in x.runs:r.font.name='Arial';r.font.size=Pt(10);r.font.bold=(i==0);r.font.color.rgb=RGBColor(255,255,255) if i==0 else RGBColor(0,0,0)
 d.add_paragraph().paragraph_format.space_after=Pt(0)
for idx,page in enumerate(src['pages']):
 if idx:d.add_page_break()
 if idx==0:
  d.add_paragraph(src['title'],'Title');d.add_paragraph(src['subtitle'],'Subtitle');p(src['date'],True)
 d.add_heading(page['heading'],1)
 for txt in page['paragraphs']:p(txt)
 if page.get('table'):table(page['table'])
 for title,desc,url in page.get('references',[]):
  x=p(title+'  '+desc,True);x.runs[0].bold=True;p(url,True)
 if page.get('end'):p(page['end'],True)
d.add_page_break();d.add_heading('Machine readable evidence appendix',1)
p('Paths below identify the evidence tables in the research project. The register namespaces prevent repeated labels from being mistaken for the same claim. Counts describe review records, not independent studies.')
paths=[('Friend context challenge register','friend_challenge/claims.csv','40 analytical groups and 148 scoped subclauses; completed source checks do not confer causal confirmation.'),('Astra capability checks','friend_capabilities/claim_matrix.csv','35 source-scoped checks; use source IDs and printed/PDF locators.'),('Existing and proposed function overlap','friend_capabilities/option_overlap.csv','Nine directions with baseline, added distinction and rival explanation.'),('Survey denominators and verification','friend_surveys/survey_claims.csv','Question cohorts, known bases, source locators and unverified awareness inputs.'),('Insurance and residual risk checks','friend_insurance/claim_matrix.csv','29 claims with contract or official-document scope and limits.'),('Observed journey follow-up','journeys/friendcontext_JX_observations.csv','Seven focused desktop cells; no owner identity or submitted transaction.'),('Observed finance illustrations','journeys/finance_scenarios.csv','Ten simulator outputs across two insurance timing states and five tenors.'),('Dated OEM service estimates','journeys/tcare_observed_costs.csv','Four paid service-visit estimates with March 2024 basis.'),('Hypothetical residual risk arithmetic','friend_insurance/illustrative_risk_scenarios.csv','51 deterministic scenarios; zero observed transactions or quoted probabilities.')]
root=Path('/workspace/scratch/70444ed5f561/auto2000_run/workstreams')
for title,path,desc in paths:
 d.add_heading(title,2);p(desc,True);p(str(root/path),True)
d.core_properties.title=src['title'];d.core_properties.subject='Evidence checks of Auto2000 Digiroom research context';d.core_properties.author='Research assessment';d.core_properties.keywords='Auto2000 Digiroom research evidence'
out=base.parent/'FRIEND_RESEARCH_CHALLENGE.docx';d.save(out)
text=[]
for pg in src['pages']:
 text.extend([pg['heading'],'',*pg['paragraphs']])
 if pg.get('table'):text.extend([' | '.join(pg['table']['headers'])]+[' | '.join(x) for x in pg['table']['rows']])
 for ref in pg.get('references',[]):text.extend(ref)
 text.extend([pg.get('end',''),''])
for title,path,desc in paths:text.extend([title,desc,str(root/path),''])
(base/'report_plaintext.txt').write_text('\n\n'.join(text))
print(out)
