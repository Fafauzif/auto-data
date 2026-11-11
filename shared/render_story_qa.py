"""Render the current reading edition for AI visual inspection; no network."""
from pathlib import Path
import fitz,json,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];pdf=ROOT/'output/pdf/Auto2000_Research_Findings.pdf';out=Path('/tmp/auto2000_story_final_v4');out.mkdir(exist_ok=True);doc=fitz.open(pdf);issues=[]
for i,page in enumerate(doc):
 page.get_pixmap(matrix=fitz.Matrix(4/3,4/3),alpha=False).save(out/f'page-{i+1:03d}.png')
 for w in page.get_text('words'):
  if w[0]<0 or w[1]<0 or w[2]>page.rect.width+.3 or w[3]>page.rect.height+.3:issues.append({'page':i+1,'word':w[4],'bbox':w[:4]})
for start in range(0,len(doc),4):
 sheet=Image.new('RGB',(1612,2300),'#cbd5dc');draw=ImageDraw.Draw(sheet)
 for k in range(4):
  n=start+k+1
  if n>len(doc):continue
  im=Image.open(out/f'page-{n:03d}.png');im.thumbnail((790,1125));x=8+(k%2)*806;y=20+(k//2)*1150;sheet.paste(im,(x,y));draw.text((x+4,y-16),str(n),fill='black')
 sheet.save(out/f'contact-{start//4+1:02d}.png')
receipt={'pages':len(doc),'sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'rendered_all_pages':True,'render_dpi':96,'outside_page_text_boxes':issues,'visual_review_pending':True,'rendered_directory_not_delivered':str(out)}
(ROOT/'reports/STORY_RENDER_QA.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt))
