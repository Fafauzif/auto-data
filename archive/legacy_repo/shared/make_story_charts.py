"""Large-label figures for the readable research story. No source retrieval."""
from pathlib import Path
import json,hashlib,textwrap
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'figures/story';OUT.mkdir(parents=True,exist_ok=True)
BLUE='#245A78';ORANGE='#B97032';GRAY='#A6B4BE';INK='#183A50'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'axes.spines.top':False,'axes.spines.right':False,'axes.titleweight':'bold','axes.labelcolor':INK,'text.color':INK,'axes.titlepad':16,'savefig.facecolor':'white'})
def asset(n):
 fs=list(ROOT.rglob(n));assert len(fs)==1,(n,fs);return json.loads(fs[0].read_text())
def new(size=(7.2,3.75)):
 f,a=plt.subplots(figsize=size);a.set_axisbelow(True);a.grid(axis='x',alpha=.12);return f,a
def save(f,name):
 f.tight_layout(pad=1.4);p=OUT/(name+'.png');f.savefig(p,dpi=220);plt.close(f);return p
def wrap(s,n=24):return '\n'.join(textwrap.wrap(s,n))
records=[]
econ=asset('economic_story.json')['pages'];data=asset('data_story.json')['pages'];review=asset('review_story.json')['pages'];journey=asset('journey_story.json')['pages']
for i,p in enumerate(econ):
 d=p['plot_data'];f,a=new()
 if i==0:
  vals=[x['gross_profit_idr_billion'] for x in d];labels=[x['business_line'] for x in d];y=np.arange(4)
  a.barh(y,vals,color=[BLUE,ORANGE,ORANGE,ORANGE],height=.58);a.set_yticks(y,labels);a.invert_yaxis();a.set_xlim(0,4300);a.set_xlabel('Gross profit in the supplied case (Rp billion)')
  for j,x in enumerate(d):a.text(vals[j]+60,j,f"{vals[j]:,}  |  {x['display_share_pct']:.1f}%",va='center',fontsize=12)
 elif i==1:
  for j,x in enumerate(d):
   lo=min(x['start_vehicles'],x['end_vehicles']);height=abs(x['end_vehicles']-x['start_vehicles']);a.bar(j,height,bottom=lo,color=BLUE if x['bar_type']=='total' else ORANGE,width=.64)
   a.text(j,max(x['start_vehicles'],x['end_vehicles'])+1050,f"{x['value_vehicles']:,.0f}",ha='center',fontsize=12)
   if j<3:a.plot([j+.32,j+.68],[x['end_vehicles']]*2,color=GRAY,lw=1)
  a.set_xticks(range(4),['2024 xEV','Scale\nallocation','Mix\nallocation','2025 xEV']);a.set_ylim(0,43000);a.set_ylabel('Toyota and Lexus vehicles');a.grid(False)
 elif i==2:
  # Programme coverage is drawn as vector evidence in the PDF.
  plt.close(f);continue
 elif i==3:
  x=np.arange(4);labor=np.array([z['labor_estimate_idr'] for z in d])/1e6;parts=np.array([z['parts_estimate_idr'] for z in d])/1e6
  a.bar(x,labor,label='Labor',color=BLUE,width=.58);a.bar(x,parts,bottom=labor,label='Parts',color=ORANGE,width=.58)
  for j,z in enumerate(d):a.text(j,(labor+parts)[j]+.12,f"{z['total_estimate_idr']/1e6:.3f}",ha='center',fontsize=12)
  a.set_xticks(x,[f"Visit {z['service_event']}" for z in d]);a.set_ylim(0,4.5);a.set_ylabel('Displayed estimate (Rp million)');a.legend(frameon=False,ncol=2,loc='upper left');a.grid(False)
 elif i==4:
  plt.close(f);f,axs=plt.subplots(1,2,figsize=(7.2,3.9),gridspec_kw={'width_ratios':[1.3,1]})
  a,b=axs;a.bar(range(3),[160,170,200],color=[GRAY,BLUE,ORANGE],width=.6);a.set_xticks(range(3),['Market\noffer','Capped\ncredit','Full\nfloor']);a.set_ylim(0,230);a.set_ylabel('Customer credit (Rp million)');a.set_title('ILLUSTRATION',fontsize=12)
  for j,v in enumerate([160,170,200]):a.text(j,v+5,str(v),ha='center')
  b.bar(0,25,color=ORANGE,label='Dealer residual');b.bar(0,15,bottom=25,color=BLUE,label='Assumed recovery');b.set_ylim(0,45);b.set_xticks([0],['Full-floor\nshortfall']);b.set_ylabel('Rp million');b.text(0,12.5,'25',ha='center',va='center',color='white',weight='bold');b.text(0,32.5,'15',ha='center',va='center',color='white',weight='bold');b.legend(frameon=False,loc='upper center',bbox_to_anchor=(.5,-.18),fontsize=10);b.set_title('ILLUSTRATION',fontsize=12)
 elif i==5:
  x=np.arange(4);v=[z['dealer_residual_idr']/1e6 for z in d];a.bar(x,v,color=[BLUE,BLUE,ORANGE,ORANGE],width=.6)
  for j,z in enumerate(d):a.text(j,v[j]+17,f'{v[j]:.0f}',ha='center')
  a.set_xticks(x,['Dispersed\nState A','Dispersed\nState B','Together\nState A','Together\nState B']);a.set_ylim(0,820);a.set_ylabel('Illustrative dealer residual (Rp million)');a.grid(False)
 path=save(f,f'economic_{i+1:02d}');records.append({'figure':str(path.relative_to(ROOT)),'asset':'economic_story.json','page_id':p['page_id'],'plot_data':d})
for i,p in enumerate(data):
 z=p['chart'];t=z['type']
 if t=='unit_cards':continue
 f,a=new()
 if t=='grouped_bar':
  x=np.arange(len(z['categories']));w=.32
  for j,s in enumerate(z['series']):
   b=a.bar(x+(j-.5)*w,s['values'],w,color=s['color'],label=s['name']);a.bar_label(b,padding=5,fontsize=13)
  a.set_xticks(x,z['categories']);a.set_ylim(0,33);a.set_ylabel('Locations, out of 28');a.legend(frameon=False,loc='upper left',fontsize=11);a.grid(False)
 elif t=='horizontal_bar':
  y=np.arange(len(z['categories']));v=z['values'];a.barh(y,v,color=[ORANGE if j==0 and i==1 else BLUE for j in range(len(v))],height=.54);a.set_yticks(y,[wrap(x,25) for x in z['categories']]);a.invert_yaxis();maximum=z.get('x_max',max(v)*1.25 if max(v)>0 else 1);a.set_xlim(0,maximum);a.set_xlabel(z['x_label'])
  for j,x in enumerate(v):a.text(x+maximum*.018,j,z.get('display_values',[str(x) for x in v])[j],va='center',fontsize=12)
  if i==4:a.set_xlim(0,6.5);a.set_xticks(range(6))
 elif t=='dumbbell':
  for j,(b,af) in enumerate(zip(z['before_values'],z['after_values'])):a.plot([af,b],[j,j],color=GRAY,lw=4);a.scatter([b],[j],s=95,color=ORANGE,zorder=3,label='Direct match' if j==0 else None);a.scatter([af],[j],s=95,color=BLUE,zorder=3,label='Boundary aligned' if j==0 else None);a.text(b+.8,j,f'{b:.2f}',va='center',fontsize=12);a.text(af-1,j+.15,f'{af:.2f}',ha='right',fontsize=12)
  a.set_yticks(range(2),['West Papua\n(old boundary)','Papua\n(old boundary)']);a.invert_yaxis();a.set_ylim(1.6,-.7);a.set_xlim(0,57);a.set_xlabel(z['x_label']);a.legend(frameon=False,loc='upper right',fontsize=10)
 else:
  x=np.arange(len(z['values']));b=a.bar(x,z['values'],color=z.get('colors',[BLUE]*len(x)),width=.56)
  a.set_xticks(x,[wrap(s,23) for s in z['categories']]);a.set_ylim(0,z.get('y_max',max(z['values'])*1.22));a.set_ylabel('Charge Ah per SOC point' if i==6 else z['y_label']);a.grid(False)
  for j,v in enumerate(z['values']):a.text(j,v+max(z['values'])*.035,z.get('display_values',[str(v) for v in z['values']])[j],ha='center',fontsize=12)
 path=save(f,f'data_{i+1:02d}');records.append({'figure':str(path.relative_to(ROOT)),'asset':'data_story.json','page_id':p['id'],'plot_data':z})
# Consistent rating threshold, same app/country parameter, language differs.
f,a=new();a.barh([0,1],[19,3],color=[BLUE,ORANGE],height=.5);a.set_yticks([0,1],['Indonesian view','English view']);a.invert_yaxis();a.set_xlim(0,23);a.set_xticks([0,5,10,15,20]);a.set_xlabel('Displayed reviews rated 4 or 5 stars, out of 20')
for j,v in enumerate([19,3]):a.text(v+.5,j,f'{v}/20',va='center',fontsize=14,weight='bold')
save(f,'review_language')
f,a=new();a.barh([0,1],[37,13],color=[GRAY,BLUE],height=.5);a.set_yticks([0,1],['Before 6 Dec 2025','On / after 6 Dec 2025']);a.invert_yaxis();a.set_xlim(0,45);a.set_xlabel('Captured Digiroom review IDs')
for j,v in enumerate([37,13]):a.text(v+.8,j,str(v),va='center',fontsize=14,weight='bold')
save(f,'review_dates')
# Matched simulator settings; amounts have different axes, never stacked.
f,axs=plt.subplots(1,2,figsize=(7.2,3.8));vals=[[154847741/1e6,109533402/1e6],[9271161/1e6,10403402/1e6]]
for a,v,title,top in zip(axs,vals,['Cash upfront','Remaining monthly payment'],[185,12.5]):
 a.bar([0,1],v,color=[BLUE,ORANGE],width=.58);a.set_xticks([0,1],['Insurance\nupfront','Insurance in\ninstalments']);a.set_ylim(0,top);a.set_title(title,fontsize=12);a.set_ylabel('Rp million')
 for j,n in enumerate(v):a.text(j,n+top*.025,f'{n:.2f}',ha='center',fontsize=13)
save(f,'finance_timing')
# Single-question survey, same base; no comparison against a different question.
f,a=new((7.2,4.2));labels=['Work quality','Trust','Warranty coverage','Customer experience','Location / hours','Cost','Mechanic relationship','Work complexity'];v=[23,21,18,14,12,7,3,2];a.barh(range(8),v,color=BLUE,height=.6);a.set_yticks(range(8),labels);a.invert_yaxis();a.set_xlim(0,27);a.set_xlabel('Published rounded share in this question (%)')
for j,x in enumerate(v):a.text(x+.5,j,f'{x}%',va='center',fontsize=12)
save(f,'service_choice')
manifest={'figures':records,'new_collection':False,'readable_figures_from_existing_verified_inputs':True,'note':'No effect size imported or inferred. Review and survey chart arrays are separately verified in the story assets and source CSVs.'}
(OUT/'STORY_CHART_MANIFEST.json').write_text(json.dumps(manifest,indent=2));print('Created',len(list(OUT.glob('*.png'))),'readable figures')
