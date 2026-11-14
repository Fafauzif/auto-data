#!/usr/bin/env python3
"""Render the integrated Markdown report to an editable Word document.
Run with the Codex primary Python runtime; render_docx.py supplies the PDF.
"""
from pathlib import Path
import argparse,re,json
from docx import Document
from docx.shared import Inches,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT,WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

BLACK='000000'; BLUE='17324D'; GRAY='D9D9D9'
def runs(par,text):
    text=text.replace('—',', ').replace('–','-').replace('→',' to ')
    # Fix authored narrative spacing without changing values, IDs or paths.
    text=re.sub(r'(?<=[A-Za-z])[,:;](?=\d)',lambda m:m.group(0)+' ',text)
    text=re.sub(r';(?=\d)','; ',text)
    text=re.sub(r'\b(is|are|the|within|from|for|all|across|contains|contributes|and|of|not|exactly|following|about|than|in|after|before|First|Days|Months)(?=\d)',r'\1 ',text)
    text=re.sub(r'(?<=[a-z])(?=Rp\b)',' ',text)
    # Preserve link label and readable destination for traceability.
    text=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'\1 (\2)',text)
    for part in re.split(r'(\*\*.*?\*\*|`[^`]+`)',text):
        if not part:continue
        rr=par.add_run(part[2:-2] if part.startswith('**') else part[1:-1] if part.startswith('`') else part)
        if part.startswith('**'):rr.bold=True
        if part.startswith('`'):
            rr.font.name='Consolas';rr.font.size=Pt(9)

def cell_style(cell,fill=None):
    cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
    tcPr=cell._tc.get_or_add_tcPr()
    borders=OxmlElement('w:tcBorders')
    for edge in ['top','left','bottom','right']:
        e=OxmlElement('w:'+edge);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4');e.set(qn('w:color'),GRAY);borders.append(e)
    tcPr.append(borders)
    margins=OxmlElement('w:tcMar')
    for edge in ['top','bottom','left','right']:
        e=OxmlElement('w:'+edge);e.set(qn('w:w'),'90');e.set(qn('w:type'),'dxa');margins.append(e)
    tcPr.append(margins)
    if fill:
        sh=OxmlElement('w:shd');sh.set(qn('w:fill'),fill);tcPr.append(sh)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('input');ap.add_argument('output');args=ap.parse_args()
    inp=Path(args.input);out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
    lines=inp.read_text(encoding='utf-8').splitlines();doc=Document();sec=doc.sections[0]
    sec.page_width=Inches(8.5);sec.page_height=Inches(11)
    sec.top_margin=Inches(.7);sec.bottom_margin=Inches(.7);sec.left_margin=Inches(.75);sec.right_margin=Inches(.75)
    styles=doc.styles
    # The bundled default Word template contains an accent border on Title.
    # Remove inherited paragraph rules so title treatment stays typographic.
    for border in list(styles.element.iter(qn('w:pBdr'))):
        border.getparent().remove(border)
    for name in ['Normal','Body Text','List Bullet','List Number']:
        st=styles[name];st.font.name='Calibri';st.font.size=Pt(11);st.font.color.rgb=RGBColor.from_string(BLACK)
        st.paragraph_format.space_after=Pt(6);st.paragraph_format.line_spacing=1.08
    for name,size in [('Title',25),('Subtitle',12),('Heading 1',17),('Heading 2',13),('Heading 3',11.5)]:
        st=styles[name];st.font.name='Calibri';st.font.size=Pt(size);st.font.color.rgb=RGBColor.from_string(BLACK)
        st.paragraph_format.space_before=Pt(13 if name!='Title' else 0);st.paragraph_format.space_after=Pt(7)
    footer=sec.footer.paragraphs[0];footer.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    r=footer.add_run('Auto2000 Integrated Research  |  ');r.font.size=Pt(8);r.font.color.rgb=RGBColor(90,90,90)
    fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');footer._p.append(fld)
    first=True;i=0
    while i<len(lines):
        line=lines[i].strip()
        if not line:i+=1;continue
        if line.startswith('```'):
            code=[];i+=1
            while i<len(lines) and not lines[i].strip().startswith('```'):code.append(lines[i]);i+=1
            for s in code:
                par=doc.add_paragraph();par.paragraph_format.space_after=Pt(1)
                rr=par.add_run(s);rr.font.name='Consolas';rr.font.size=Pt(8)
            i+=1;continue
        image=re.match(r'!\[([^\]]*)\]\(([^)]+)\)',line)
        if image:
            target=Path(image.group(2))
            if not target.is_absolute():target=inp.parent/target
            if target.exists():
                par=doc.add_paragraph();par.alignment=WD_ALIGN_PARAGRAPH.CENTER;par.add_run().add_picture(str(target),width=Inches(6.8))
                cap=doc.add_paragraph(image.group(1));cap.paragraph_format.space_after=Pt(9)
                for rr in cap.runs:rr.italic=True;rr.font.size=Pt(9)
            i+=1;continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                row=[v.strip() for v in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?',v or '') for v in row):rows.append(row)
                i+=1
            if not rows:continue
            n=max(map(len,rows));table=doc.add_table(rows=1,cols=n);table.alignment=WD_TABLE_ALIGNMENT.CENTER
            table.autofit=False
            # Give narrative columns more space according to content density.
            weights=[max(6,min(70,sum(len(r[c]) if c<len(r) else 0 for r in rows)/len(rows))) for c in range(n)]
            widths=[7*w/sum(weights) for w in weights]
            if n<=4 and widths[0]<1.35:
                others=sum(widths[1:]);widths=[1.35]+[5.65*w/others for w in widths[1:]]
            for c in range(n):table.columns[c].width=Inches(widths[c])
            header=table.rows[0];trpr=header._tr.get_or_add_trPr();rep=OxmlElement('w:tblHeader');rep.set(qn('w:val'),'true');trpr.append(rep)
            for ridx,row in enumerate(rows):
                cells=header.cells if ridx==0 else table.add_row().cells
                for c,cell in enumerate(cells):
                    cell.width=Inches(widths[c]);cell_style(cell,BLUE if ridx==0 else 'F3F6F8' if ridx%2==0 else 'FFFFFF')
                    par=cell.paragraphs[0];par.paragraph_format.space_after=Pt(2);par.paragraph_format.line_spacing=1.0
                    runs(par,row[c] if c<len(row) else '')
                    if ridx and c<len(row) and re.fullmatch(r'[()\d,.%\s+\-]+',row[c]):
                        par.alignment=WD_ALIGN_PARAGRAPH.RIGHT
                    for rr in par.runs:
                        rr.font.size=Pt(9.5 if n<=4 else 9)
                        if ridx==0:rr.bold=True;rr.font.color.rgb=RGBColor(255,255,255)
                # Avoid row split across pages where possible.
                pr=table.rows[ridx]._tr.get_or_add_trPr();no=OxmlElement('w:cantSplit');pr.append(no)
            doc.add_paragraph().paragraph_format.space_after=Pt(2)
            continue
        heading=re.match(r'^(#{1,4})\s+(.*)',line)
        if heading:
            level=len(heading.group(1));title=heading.group(2).replace('—',' ').replace('–',' ')
            title=re.sub(r'[*`:]','',title)
            par=doc.add_paragraph(style='Title' if first and level==1 else 'Heading '+str(min(level,3)))
            runs(par,title);first=False;i+=1;continue
        if line in ['---','***']:i+=1;continue
        if line.startswith('>'):
            par=doc.add_paragraph();par.paragraph_format.left_indent=Inches(.2);runs(par,line.lstrip('> ').strip())
            for rr in par.runs:rr.italic=True
            i+=1;continue
        bullet=re.match(r'^[-*]\s+(.*)',line)
        num=re.match(r'^\d+\.\s+(.*)',line)
        par=doc.add_paragraph(style='List Bullet' if bullet else 'List Number' if num else 'Normal')
        runs(par,bullet.group(1) if bullet else num.group(1) if num else line)
        i+=1
    doc.core_properties.title='Auto2000 Integrated Research and Decisions'
    doc.core_properties.subject='Integrated customer, geographical and commercial analysis'
    doc.core_properties.author='Auto2000 Research Project'
    doc.save(out);print(json.dumps({'docx':str(out),'paragraphs':len(doc.paragraphs),'tables':len(doc.tables)}))
if __name__=='__main__':main()
