from pathlib import Path
import json
import numpy as np,pandas as pd,geopandas as gpd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
P=Path(__file__).parent; ROOT=P.parents[1]; F=ROOT/'figures';F.mkdir(exist_ok=True)
INK='#153341';TEAL='#087e8b';ORANGE='#d76a37';MUTED='#73848a';LAND='#e7e6df';SEA='#f5f8fa'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'axes.labelcolor':INK,'text.color':INK,'axes.edgecolor':'#c5cfd2','xtick.color':INK,'ytick.color':INK,'figure.facecolor':'white','axes.spines.top':False,'axes.spines.right':False,'axes.titleweight':'bold'})
b=pd.read_csv(ROOT/'workstreams/branches/official_branches_unique.csv')
o=pd.read_csv(P/'otoxpert_official_inventory.csv');s=pd.read_csv(P/'screening.csv')
w=gpd.read_file(ROOT/'sources/natural_earth_countries.geojson')
valid=b[b.coordinate_status.eq('official_direction_candidate')].copy()
reg=[]
def save(fig,name,title,caption,sources):
 fig.savefig(F/name,dpi=200,bbox_inches='tight',facecolor='white');plt.close(fig)
 reg.append({'filename':'figures/'+name,'title':title,'caption':caption,'sources':sources,'created_by':'context workstream, original matplotlib/geopandas figure'})
def basemap(ax,xlim,ylim):
 ax.set_facecolor(SEA);w.plot(ax=ax,color=LAND,edgecolor='#bfc8c7',linewidth=.4)
 ax.set_xlim(*xlim);ax.set_ylim(*ylim);ax.set_aspect(1/np.cos(np.deg2rad(np.mean(ylim))));ax.grid(alpha=.2,linewidth=.6)
 ax.set_xlabel('Longitude (degrees east)');ax.set_ylabel('Latitude (degrees north)')
# Figure1: full country with Java detail, operational categories remain distinct.
fig,(ax,az)=plt.subplots(2,1,figsize=(11,10.5),gridspec_kw={'height_ratios':[1.05,.8]})
fig.suptitle('Observed directories reveal multiple service channels',x=.06,ha='left',fontsize=19,fontweight='bold')
for a,x,y in [(ax,(94,142),(-11,7)),(az,(105.1,115.4),(-8.9,-5.6))]:
 basemap(a,x,y)
 a.scatter(valid.longitude,valid.latitude,s=22,color=INK,alpha=.75,label='Auto2000 official direction candidates',zorder=4)
 other=o[~o.auto2000_operator.astype(str).str.lower().eq('true')];own=o[o.auto2000_operator.astype(str).str.lower().eq('true')]
 a.scatter(other.longitude,other.latitude,s=70,marker='^',facecolors='white',edgecolors=ORANGE,linewidths=1.3,zorder=5)
 a.scatter(own.longitude,own.latitude,s=65,marker='^',color=ORANGE,edgecolor='white',linewidths=.5,zorder=6)
ax.set_title('Indonesia context | 127 mapped Auto2000 candidates + 37 OtoXpert entries',loc='left',fontsize=12,pad=12)
az.set_title('Java detail | proximity does not establish equivalent job capability',loc='left',fontsize=12,pad=12)
for name,lon,lat,dx,dy in [('Medan',98.67,3.58,1,.9),('Palembang',104.76,-2.98,1,1),('Bandung',107.61,-6.92,-1,-.9),('Surabaya',112.75,-7.26,.5,.6)]:
 ax.annotate(name,(lon,lat),(lon+dx,lat+dy),fontsize=10,color=TEAL,arrowprops={'arrowstyle':'-','color':TEAL,'lw':.8})
for name,lon,lat,dx,dy in [('Bandung',107.61,-6.92,-.8,-1),('Surabaya',112.75,-7.26,.3,.6),('Jakarta',106.84,-6.2,.25,.2)]:
 az.annotate(name,(lon,lat),(lon+dx,lat+dy),fontsize=11,color=TEAL,arrowprops={'arrowstyle':'-','color':TEAL,'lw':.8})
legend=[Line2D([],[],marker='o',ls='',color=INK,label='Auto2000: 127 coordinate candidates'),Line2D([],[],marker='^',ls='',color=ORANGE,label='OtoXpert: 15 Auto2000-operated'),Line2D([],[],marker='^',ls='',markerfacecolor='white',markeredgecolor=ORANGE,label='OtoXpert: 22 other operators')]
fig.legend(handles=legend,loc='lower center',bbox_to_anchor=(.5,.015),ncol=1,frameon=False,fontsize=11)
fig.subplots_adjust(top=.91,bottom=.15,hspace=.42)
save(fig,'context_national_channels.png','Observed directories reveal multiple service channels','Mapped are127 official-direction candidates from131 unique observed Auto2000 entries;4 invalid/conflicted/virtual entries excluded. Both service and showroom candidates appear. OtoXpert37 includes15 Auto2000-operated and22 other operators. Marker overlap can conceal individual locations. Official links are not field-verified entrances. Natural Earth country outlines are small-scale context, not administrative verification.','Official Auto2000 directories; OtoXpert directory pages1–4, retrieved14Nov2026; Natural Earth admin0 countries')
# Figure2 operator counts
counts=o.groupby('operator').size().sort_values(ascending=True)
fig,ax=plt.subplots(figsize=(10,7.2));colors=[ORANGE if x=='Auto2000' else '#8aa5ad' for x in counts.index]
ax.barh(counts.index,counts.values,color=colors,height=.67)
for y,v in enumerate(counts.values):ax.text(v+.18,y,str(v),va='center',fontsize=12,fontweight='bold')
ax.set_xlim(0,17);ax.set_xlabel('Directory entries observed (not a reconciled national outlet total)');ax.set_xticks([0,5,10,15]);ax.grid(axis='x',alpha=.18);ax.set_axisbelow(True)
ax.set_title('Only 15 of 37 observed OtoXpert entries name Auto2000',loc='left',fontsize=17,pad=22)
fig.text(.06,.025,'Published operator identity helps separate Toyota-network retention from Auto2000 attribution.',fontsize=11,color=MUTED)
fig.subplots_adjust(left=.27,right=.95,top=.88,bottom=.14)
save(fig,'context_otoxpert_operators.png','Only 15 of 37 observed OtoXpert entries name Auto2000','Operator counts from37 official listings retrieved across four directory pages. These are observed listings, not independently verified businesses or a current national total. Published Toyota totals elsewhere differ (38/40). Operator identity alone does not establish contribution sharing or accounting treatment.','OtoXpert official workshop directory pages1–4; workstreams/context/otoxpert_official_inventory.csv')
# Figure3 alphabetic screen, deliberately no rank construction.
s=s.sort_values('market').reset_index(drop=True);ys=np.arange(len(s));primary=s.market.isin(['Surabaya','Medan','Bandung','Palembang']);cs=np.where(primary,TEAL,'#a2afb3')
fig,(ax,ar)=plt.subplots(1,2,figsize=(11,8.7),sharey=True,gridspec_kw={'width_ratios':[1.1,.9]})
ax.scatter(s.source_charging_rows,ys,c=cs,s=65,zorder=3);ax.set_xscale('log');ax.set_xlim(6,850);ax.set_xticks([10,30,100,300]);ax.set_xticklabels(['10','30','100','300'])
ax.set_yticks(ys);ax.set_yticklabels(s.market);ax.invert_yaxis();ax.set_xlabel('Charging records (log scale)');ax.set_title('SPKLU snapshot | 16 June 2026',loc='left',fontsize=12,pad=12)
for y,v in enumerate(s.source_charging_rows):ax.text(v*1.10,y,str(v),va='center',fontsize=10)
ar.scatter(s.observed_otoxpert_directory_entries,ys,c=cs,s=65,zorder=3);ar.set_xlim(-.3,5.4);ar.set_xticks(range(5));ar.set_xlabel('OtoXpert directory entries');ar.set_title('Observed directory | 14 November 2026',loc='left',fontsize=12,pad=12)
for y,v in enumerate(s.observed_otoxpert_directory_entries):ar.text(v+.17,y,str(v),va='center',fontsize=10)
for a in [ax,ar]:a.grid(axis='x',alpha=.2);a.spines['left'].set_visible(False);a.tick_params(axis='y',length=0)
fig.suptitle('The 15-market screen describes source coverage',x=.06,ha='left',fontsize=18,fontweight='bold')
fig.text(.06,.025,'Alphabetical order. Teal = deep-dive markets. Administrative selections differ in area.\nThese counts do not rank demand, workshop opportunity or charging adequacy.',fontsize=11,color=MUTED)
fig.subplots_adjust(left=.23,right=.96,top=.88,bottom=.13,wspace=.12)
save(fig,'context_market_screen.png','The 15-market screen describes source coverage','Fifteen explicit administrative-label selections, alphabetical rather than ranked. Charging counts are existing source records dated16Jun2026; OtoXpert counts are retrieved directory entries dated14Nov2026. City/county selections differ in size; some markets include counties and others only city cores. No observed OtoXpert record does not establish absence. No eligible Toyota owner denominator is available.','SPKLU V2 DOI10.17632/z2bvd5r574.2, CC BY-NC3.0; official OtoXpert directory; workstreams/context/screening.csv')
# Figure4 audit stages
labels=['Official directory card occurrences','Unique name-coordinate entries','Official-direction coordinate candidates','Routing-eligible general-workshop candidates'];vals=[155,131,127,96]
fig,ax=plt.subplots(figsize=(11,5.8));y=np.arange(4)
ax.barh(y,vals,height=.6,color=[ '#b7c5ca','#8daab3','#587c89',TEAL]);ax.invert_yaxis();ax.set_yticks(y);ax.set_yticklabels(labels,fontsize=12);ax.set_xlim(0,180);ax.set_xlabel('Records retained at each stated stage');ax.grid(axis='x',alpha=.16);ax.set_axisbelow(True)
for yy,v in zip(y,vals):ax.text(v+2,yy,str(v),va='center',fontweight='bold',fontsize=15)
fig.suptitle('Directory cards are not a national workshop total',x=.055,ha='left',fontsize=18,fontweight='bold')
fig.text(.055,.03,'Deduplication, coordinate checks and service filters change the denominator.\nA general-workshop tag still does not verify the selected job, model, appointment or capacity.',fontsize=11,color=MUTED)
fig.subplots_adjust(left=.43,right=.96,top=.85,bottom=.21)
save(fig,'context_inventory_denominators.png','Directory cards are not a national workshop total','The acquisition contains155 card occurrences,131 unique name-coordinate entries,127 official-direction candidates and96 coordinate-valid general-workshop candidates eligible for exploratory routing.99 unique entries advertise general workshop services before coordinate exclusions. These are observed public-directory outputs, not an independently reconciled national network. No branch-specific selected-job audit was completed.','workstreams/branches/official_branches_unique.csv; branch_inventory_summary.json, retrieved14Nov2026')
(P/'figure_registry.json').write_text(json.dumps(reg,indent=2))
print(json.dumps([r['filename'] for r in reg],indent=2))
