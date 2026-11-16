from pathlib import Path
import csv, math, json
p=Path('draft_work/charts')
repo=Path('repo')
geo=repo/'analysis/geography/tables'
def rows(f):
 with f.open() as a: return list(csv.DictReader(a))
markets={r['market']: r for r in rows(geo/'raw_recomputed_markets.csv')}
orig=rows(geo/'raw_recomputed_origins.csv')
coords=rows(repo/'archive/session_work_products/analysis_followup/geographic_source/Auto2000_Geographic_Study/workstreams/routing/output/origins.csv')
coord={(r['market'],r['origin_id']):(float(r['longitude']),float(r['latitude'])) for r in coords}
pre=r'''\documentclass[tikz,border=2pt]{standalone}
\pdfmapfile{+cm.map}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\usetikzlibrary{arrows.meta}
\definecolor{ink}{HTML}{202B30}
\definecolor{red}{HTML}{971D2C}
\definecolor{soft}{HTML}{F4E9EB}
\definecolor{gray}{HTML}{51636D}
\definecolor{line}{HTML}{D6DDE0}
\definecolor{pale}{HTML}{F0F3F4}
\begin{document}
'''
def write(n,s,h):
 (p/f'{n}.tex').write_text(pre+r'\begin{tikzpicture}[x=1cm,y=1cm,font=\sffamily\fontsize{10.5}{12}\selectfont,text=ink,arr/.style={-{Stealth[length=2mm]},draw=gray,thick}]'+'\n'+rf'\path[use as bounding box] (0,0) rectangle (16.4,{h});'+'\n'+s+r'\end{tikzpicture}\end{document}')
def label(x,y,s,style=''):
 return rf'\node[anchor=west,inner sep=0pt,{style}] at ({x},{y}) {{{s}}};'+'\n'
def center(x,y,s,style=''):
 return rf'\node[align=center,inner sep=0pt,{style}] at ({x},{y}) {{{s}}};'+'\n'
def rule(x,y,X,Y,style='line'):
 return rf'\draw[{style}] ({x},{y}) -- ({X},{Y});'+'\n'
def rect(x,y,X,Y,c):
 return rf'\fill[{c}] ({x},{y}) rectangle ({X},{Y});'+'\n'
def box(x,y,w,title,body):
 body=body.replace(chr(92),chr(92)*2)
 return rect(x,y-1.0,x+w,y+0.43,'pale')+label(x+.16,y+.15,title,r'font=\sffamily\bfseries')+label(x+.16,y-.41,body,r'align=left')
s=label(.1,2.35,'Share of service bookings',r'font=\sffamily\bfseries')
for x,width,c,name in [(0,1.78,'red',r'16\%'),(1.78,4.22,'gray',r'38\%'),(6,5.11,'ink',r'46\%')]:
 s+=rect(x,1.02,x+width,1.86,c)+center(x+width/2,1.44,name,r'text=white,font=\sffamily\bfseries')
for x,st in [(.0,'Digiroom'),(2.65,'WhatsApp'),(7.4,'Phone or walk-in')]: s+=label(x,.58,st)
s+=rule(11.48,.22,11.48,2.62)+label(11.82,2.36,'App audience',r'font=\sffamily\bfseries')+label(11.82,1.67,r'21,000 active monthly')+label(11.82,1.06,r'1.6 sessions per active user')+label(11.82,.45,r'500,000+ total downloads')
write('f1',s,2.8)
s=''
for x,t,b in [(0,'Check in',r'Paid arrival went\unacknowledged'),(4.2,'Explain the scope',r'Avanza owner faced\different repair scopes'),(8.4,'Get payer approval',r'Yaris driver visits;\family approves extras'),(12.6,'Close the job',r'Record work, payment\and any open issue')]: s+=box(x,1.43,3.78,t,b)
for x in [3.82,8.02,12.22]: s+=rule(x,1.2,x+.31,1.2,'arr')
write('f2',s,2.05)
s=label(.14,3.05,'Reported household experiences',r'font=\sffamily\bfseries')
for i,(t,b) in enumerate([('Wuling Air EV',r'Apartment charging fits\the routine'),('BYD Atto',r'Low charge changed one trip\and prompted a charger search'),('Auto2000 prospect',r'Reported being unable to\find a test-drive vehicle')]): s+=box(i*5.5+.02,2.31,5.25,t,b)
s+=rule(.1,.93,16.25,.93)+label(.12,.47,'Use the actual vehicle to check regular routes, parking, passengers and charging where relevant.')
write('f3',s,3.3)
s=''
for x,t,a,b,d in [(0,'Cash due upfront','154.85','109.53','45.31 less'),(8.3,'Monthly instalment','9.27','10.40','1.13 more')]:
 s+=label(x+.13,2.49,t,r'font=\sffamily\bfseries')+rect(x+.1,.73,x+7.78,1.98,'pale')+label(x+.35,1.53,a,r'font=\sffamily\bfseries')+rule(x+2.09,1.52,x+2.97,1.52,'arr')+label(x+3.2,1.53,b,r'font=\sffamily\bfseries')+label(x+5.19,1.53,d,'text=red')+label(x+.35,1.0,'Paid upfront')+label(x+3.20,1.0,'Financed')
s+=label(.12,.28,'Amounts in Rp million. Upfront payments include instalment 1.',r'font=\sffamily\fontsize{9}{10}\selectfont')
write('f4',s,2.75)
s=label(.05,4.12,r'Origins with a modeled oil-service gap $>$5 minutes',r'font=\sffamily\bfseries')
s+=r'''\begin{axis}[at={(3.4cm,.8cm)},anchor=south west,width=11.2cm,height=3.03cm,scale only axis,xmin=-.7,xmax=18.5,ymin=.54,ymax=4.46,ytick={1,2,3,4},yticklabels={Palembang (69),Medan (78),Surabaya (59),Bandung (78)},xtick={0,5,10,15},tick style={draw=none},axis x line*=bottom,axis y line=none,xmajorgrids,grid style={line},tick label style={font=\sffamily\small},clip=false]'''
for k,y in [('Palembang',1),('Medan',2),('Surabaya',3),('Bandung',4)]:
 a,b=[int(markets[k][v]) for v in ('oil_tail_before_n','oil_tail_after_n')]
 s+=rf'\draw[thick,line] (axis cs:{b},{y}) -- (axis cs:{a},{y});\fill[red] (axis cs:{b},{y}) circle (2.4pt);\fill[gray] (axis cs:{a},{y}) circle (2.4pt);\node[above,text=red] at (axis cs:{b},{y}) {{{b}}};\node[above] at (axis cs:{a},{y}) {{{a}}};'
s+=r'\end{axis}'+label(.12,.22,'Dealer only', 'text=gray')+label(2.62,.22,'With eligible OtoXpert','text=red')+label(9.17,.22,'Paired origins in parentheses.')
for y,st in [(3.47,'Bandung (78)'),(2.70,'Surabaya (59)'),(1.93,'Medan (78)'),(1.16,'Palembang (69)')]: s+=label(.1,y,st)
write('f5',s,4.42)
s=rect(.25,.94,13.6,1.84,'pale')+label(.4,1.60,'2026--2028 investment window',r'font=\sffamily\bfseries')+rule(.5,1.13,15.9,1.13,'arr')
for x,t,b in [(.7,'Jan 2026','Delivery'),(2.6,'Feb 2026','Visit 1'),(6.67,'2027','Included visits'),(10.78,'2028','Included visits'),(13.6,'Jan 2029','Visit 7'),(15.58,'Jul 2029','Visit 8')]:
 s+=rf'\fill[red] ({x},1.13) circle (2.2pt);'+center(x,.68,t)+center(x,.25,b,'text=gray')
write('f6',s,2.03)
s=label(.1,3.25,'Trade-in arithmetic',r'font=\sffamily\bfseries')+label(4.42,3.25,'Worked example, Rp million','text=gray')
for x,n,t,c in [(0,'248.0','Inspected offer','pale'),(4.2,'174.0','Loan payoff','pale'),(8.4,'2.5','Trade-in fees','pale'),(12.6,'71.5','Usable equity','soft')]:
 s+=rect(x,1.56,x+3.67,2.89,c)+center(x+1.835,2.44,n,r'font=\sffamily\Large\bfseries')+center(x+1.835,1.9,t)
for x,t in [(3.93,'$-$'),(8.13,'$-$'),(12.33,'$=$')]: s+=center(x,2.36,t)
for x,t in [(.1,'Confirm dated terms'),(5.9,'Reserve the replacement'),(12,'Settle and hand over')]: s+=label(x,.77,t,r'font=\sffamily\bfseries')
s+=rule(4.39,.78,5.57,.78,'arr')+rule(10.66,.78,11.66,.78,'arr')
write('f7',s,3.5)
s=box(.02,3.97,3.07,'Transaction loss',r'xEV sales and\paid service')
for y,stage,b,c in [(4.73,'Buy',r'Household fit and cash due',r'Confirmed drive and offer\New-to-Auto2000 xEV delivery'),(2.88,'Service',r'Eligible outlet and agreed work',r'Confirmed scope and completion\Eligible paid work order'),(1.03,'Upgrade',r'Usable equity and settlement',r'Inspected offer and reserved unit\Repeat xEV delivery')]:
 s+=box(3.89,y,5.41,stage,b)+box(10.15,y,6.19,'Commercial outcome',c)
 s+=rule(9.38,y-.19,10.07,y-.19,'arr')
 s+=rf'\draw[arr] (3.14,3.74) -- (3.49,3.74) -- (3.49,{y-.19}) -- (3.8,{y-.19});'
write('f8',s,5.28)

# Market atlas uses actual origin coordinates without implying routes or street precision.
for key in ('Bandung','Surabaya','Medan','Palembang'):
 rr=[r for r in orig if r['market']==key]
 xy=[coord[key,r['origin_id']] for r in rr]
 minx,maxx=min(x for x,y in xy),max(x for x,y in xy)
 miny,maxy=min(y for x,y in xy),max(y for x,y in xy)
 s=''
 for left,metric,title in [(.35,'oil_gap_min','Dealer only'),(8.32,'owned_gap_min','With eligible operated OtoXpert')]:
  s+=label(left,4.35,title,r'font=\sffamily\bfseries')
  s+=rect(left,.58,left+7.57,4.03,'pale')
  for r,(xx,yy) in zip(rr,xy):
   x=left+.85+5.87*(xx-minx)/(maxx-minx); y=.82+2.91*(yy-miny)/(maxy-miny)
   s+=rf'\fill[{"red" if float(r[metric])>5 else "gray!45"}] ({x:.3f},{y:.3f}) circle (2.45pt);'
  s+=label(left+.11,.70,r'W',r'font=\sffamily\scriptsize')+label(left+7.22,.70,r'E',r'font=\sffamily\scriptsize')+label(left+.11,3.83,r'N',r'font=\sffamily\scriptsize')
 s+=label(.36,.23,'Red: over 5 minutes behind comparator','text=red')+label(7.4,.23,'Grey: at or below threshold')
 write('atlas_'+key,s,4.61)

s=''
for i,(name,raw,unique) in enumerate([('X posts',14892,14291),('Maps reviews',8385,8119),('YouTube comments',74,74)]):
 y=3.34-i*1.05
 s+=label(.08,y+.24,name,r'font=\sffamily\bfseries')
 x=4.03
 s+=rect(x,y-.29,x+8*raw/15000,y+.36,'pale')
 s+=rect(x,y-.29,x+8*unique/15000,y+.10,'gray')
 if i==2:
  s+=label(x+.25,y-.1,f'{raw:,} rows  /  {unique:,} unique')
 else:
  s+=label(x+8*raw/15000+.15,y-.04,f'{raw:,} / {unique:,}')
s+=label(.08,.28,'Pale: export rows','text=gray')+label(4.03,.28,'Dark: unique platform IDs')
write('corpus',s,3.85)
s=label(.05,2.85,'Digiroom reviews by publication date',r'font=\sffamily\bfseries')
for y,t,total,task in [(1.9,'Before relaunch',37,19),(.91,'On or after relaunch',13,6)]:
 s+=label(.06,y,t)+rect(4.6,y-.25,4.6+total*.24,y+.25,'pale')+rect(4.6,y-.25,4.6+task*.24,y+.25,'red')+label(4.8+total*.24,y,f'{task} of {total}')
s+=label(.06,.21,'Relaunch date: 6 Dec 2025. Red: specific self-reported app interactions.')
write('app_reviews',s,3.1)
s=label(.05,2.95,'Comments returned by video',r'font=\sffamily\bfseries')
for y,t,n in [(2.24,'Neta resale price',45),(1.43,'BYD M6 owner experience',26),(.64,'BYD M6 editorial review',3)]:
 s+=label(.05,y,t)+rect(5.25,y-.21,5.25+n*.193,y+.21,'gray')+label(5.47+n*.193,y,f'{n}')
write('yt',s,3.2)
s=label(.05,2.88,r'2025 Toyota hybrid wholesales in the published model breakdown',r'font=\sffamily\bfseries')
for x,w,c,t in [(0,12.48,'red','23,934 Zenix'),(12.48,3.22,'gray','6,176 other')]:
 s+=rect(x,1.22,x+w,2.16,c)+center(x+w*.5,1.69,t,'text=white')
s+=label(.05,.61,'Zenix accounts for 79.5\% of the 30,110 Toyota hybrid units in this publication.')
write('hybrid',s,3.1)
