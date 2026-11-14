#!/usr/bin/env python3
"""Rebuild analytical map figures from the packaged cleaned source layers and OD outputs.
No tiles, online basemap, population inference, or interpolated isochrones.
Run from any working directory with matplotlib,pandas,numpy installed.
"""
from pathlib import Path
import json,math
import numpy as np,pandas as pd,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm,Normalize
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'figures';OUT.mkdir(exist_ok=True)
MARKETS={'surabaya':[112.64,-7.38,112.84,-7.18],'medan':[98.59,3.48,98.77,3.69],'bandung':[107.51,-6.99,107.74,-6.82],'palembang':[104.66,-3.07,104.85,-2.88]}
COL={'auto2000':'#d5523a','independent':'#236d80','otoxpert':'#aa8135','excluded':'#8b8c89'}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#fbfaf6','axes.facecolor':'#fbfaf6','savefig.facecolor':'#fbfaf6','axes.titleweight':'bold'})
REG=[]
def save(fig,name,title,caption,sources):
 p=OUT/(name+'.png');fig.savefig(p,dpi=190,bbox_inches='tight');plt.close(fig)
 REG.append({'file':str(p.relative_to(ROOT)),'title':title,'caption':caption,'sources':sources})
def setup(ax,bbox,pad=.012):
 w,s,e,n=bbox;ax.set(xlim=(w-pad,e+pad),ylim=(s-pad,n+pad),xlabel='Longitude (degrees east)',ylabel='Latitude (degrees north)');ax.set_aspect(1/math.cos(math.radians((s+n)/2)));ax.grid(alpha=.18,zorder=0)
 ax.add_patch(Rectangle((w,s),e-w,n-s,fill=False,ls='--',ec='#777777',lw=1,zorder=1))
 # WGS84 approximate scale at central latitude. Context, not a road distance.
 km=5;dx=km/(111.32*math.cos(math.radians((s+n)/2)));x=w+.01;y=s-.006;ax.plot([x,x+dx],[y,y],c='#333',lw=2,zorder=6);ax.text(x+dx/2,y+.003,'5 km straight-line',ha='center',fontsize=8,zorder=6,bbox={'facecolor':'#fbfaf6','edgecolor':'none','alpha':.9,'pad':1})
 ax.text(.98,.97,'N ↑',ha='right',va='top',transform=ax.transAxes,fontsize=11)
def sources():return 'Official Auto2000/OtoXpert directories collected 14 Nov 2026; Overture Places 2026-10-21.0; OSRM retrieval in packaged logs.'

def main():
 providers=pd.read_csv(ROOT/'workstreams/providers/provider_inventory.csv')
 branches=pd.read_csv(ROOT/'workstreams/branches/official_branches.csv')
 bd=pd.read_csv(ROOT/'workstreams/branches/routing_destinations.csv')
 ox=pd.read_csv(ROOT/'workstreams/context/otoxpert_official_inventory.csv')
 access=pd.read_csv(ROOT/'workstreams/routing/output/origin_accessibility.csv')
 summary=pd.read_csv(ROOT/'workstreams/routing/output/market_summary.csv')
 snap=pd.read_csv(ROOT/'workstreams/routing/output/snapping.csv')
 for frame in (access,summary,snap): frame['market']=frame.market.str.lower()
 routes=json.loads((ROOT/'workstreams/routing/output/illustrative_routes.geojson').read_text())['features']
 def road_examples(ax,market):
  for f in routes:
   if f['properties']['market'].lower()!=market:continue
   xy=np.array(f['geometry']['coordinates']);ax.plot(xy[:,0],xy[:,1],c='#8a9590',lw=.6,alpha=.45,zorder=1)
 # Core-window counts preserve mapped candidates not qualified comparators.
 counts=[]
 for market,bbox in MARKETS.items():
  w,s,e,n=bbox
  pp=providers[(providers.market.str.lower()==market)&providers.longitude.between(w-.08,e+.08)&providers.latitude.between(s-.08,n+.08)].copy()
  if 'eligible_candidate' in pp:pp=pp[pp.eligible_candidate.astype(str).str.lower().isin(['true','1'])]
  dd=pd.read_csv(ROOT/f'workstreams/routing/inputs/{market}_destinations.csv')
  bb=dd[dd.kind=='auto2000'].dropna(subset=['longitude','latitude']).copy()
  oo=ox[ox.longitude.between(w-.08,e+.08)&ox.latitude.between(s-.08,n+.08)].copy()
  fig,ax=plt.subplots(figsize=(10,7));setup(ax,bbox,pad=.08);road_examples(ax,market)
  ax.scatter(pp.longitude,pp.latitude,s=15,c=COL['independent'],alpha=.5,label=f'Mapped repair/service\ncandidates ({len(pp)})',zorder=2)
  if len(oo):ax.scatter(oo.longitude,oo.latitude,s=90,marker='s',c=COL['otoxpert'],edgecolors='white',lw=.8,label='Official OtoXpert listings',zorder=4)
  for i,(_,b) in enumerate(bb.iterrows(),1):
   ax.scatter(b.longitude,b.latitude,s=105,marker='^',c=COL['auto2000'],edgecolors='white',lw=.7,zorder=5)
   ax.annotate(str(i),(b.longitude,b.latitude),xytext=(4,4),textcoords='offset points',fontsize=9,fontweight='bold',zorder=6)
  ax.scatter([],[],s=80,marker='^',c=COL['auto2000'],label=f'Official Auto2000 general-workshop\nlistings ({len(bb)})')
  ax.legend(loc='upper left',bbox_to_anchor=(1.01,1),frameon=False,fontsize=9)
  listing='\n'.join(f'{i}. {b["name"].replace("Auto2000 ","").replace(" - Dealer dan Bengkel Resmi Toyota","").replace(market.title()+" ","")}' for i,(_,b) in enumerate(bb.iterrows(),1))
  ax.text(1.02,.65,listing,transform=ax.transAxes,va='top',fontsize=9,linespacing=1.6)
  ax.set_title(f'{market.title()} | published service locations and mapped candidates',loc='left',pad=16,fontsize=13)
  fig.subplots_adjust(right=.7,bottom=.14)
  save(fig,'providers_'+market,'Published workshop locations in '+market.title(),f'Thin grey lines show selected illustrative OSRM routes, not the full road network. Dashed rectangle is the origin-study window, not a city boundary. Blue candidates are Overture automotive records without confirmed Toyota/job capability. Official branch map links are location candidates, not field-verified entrances. Provider points cover the expanded destination window; the inner dashed rectangle defines sampled origins.',sources())
  ar=access[(access.market==market)&(access.scenario=='snap_le_250m')].copy();ar['gap']=pd.to_numeric(ar.auto2000_minus_mapped_independent_seconds,errors='coerce')/60
  fig,ax=plt.subplots(figsize=(9,7));setup(ax,bbox);road_examples(ax,market)
  norm=TwoSlopeNorm(vmin=-10,vcenter=0,vmax=30)
  im=ax.scatter(ar.longitude,ar.latitude,c=ar.gap,cmap='RdBu_r',norm=norm,s=150,marker='s',edgecolors='white',linewidth=.7,zorder=3)
  ax.scatter(bb.longitude,bb.latitude,s=95,marker='^',c='black',edgecolors='white',lw=.7,zorder=4)
  miss=ar[ar.gap.isna()];ax.scatter(miss.longitude,miss.latitude,c='#bbb',s=150,marker='x')
  cb=fig.colorbar(im,ax=ax,shrink=.72,pad=.03,extend='both');cb.set_label('Auto2000 minus mapped-candidate time (minutes)')
  ax.set_title(f'{market.title()} | extra travel, {ar.gap.notna().sum()}/{len(ar)} paired origins',loc='left',pad=16,fontsize=13)
  fig.legend(handles=[Line2D([0],[0],marker='^',ls='',color='black',label='Auto2000 workshop listing'),Line2D([0],[0],marker='x',ls='',color='#aaa',label='No paired screened result'),Line2D([0],[0],color='#8a9590',lw=1,label='Selected all-routed trace')],loc='lower center',bbox_to_anchor=(.5,-.035),ncol=3,frameon=False,fontsize=8);fig.tight_layout();save(fig,'gap_'+market,'Additional modelled travel in '+market.title(),'Screened scenario: origin and destination snap displacement ≤250 m. Each coloured square is a paired sampled origin; grey crosses have no paired result after screening. No interpolation or customer weighting. Positive values mean the nearest listed Auto2000 destination has a longer modelled route than the nearest mapped repair/service candidate. Comparison is geographic and does not establish equivalent service capability. Fixed colour scale across all markets; values beyond its limits are saturated. This screen changes the paired-origin denominator and does not prove retained coordinates are correct.',sources())
  # Paired origin burden distribution.
  counts.append({'market':market,'expanded_mapped_candidates':len(pp),'listed_auto2000_destinations':len(bb),'otoxpert_in_margin':len(oo)})
  # Three actual returned route-pair examples, not a complete network map.
  fig,axes=plt.subplots(1,3,figsize=(13,6))
  for ax,(example,label) in zip(axes,[('minimum_gap','Smallest sampled gap'),('median_gap','Median sampled gap'),('maximum_gap','Largest sampled gap')]):
   ff=[f for f in routes if f['properties']['market'].lower()==market and f['properties']['example']==example]
   coords=[];labels=[];snapvals=[]
   for f in ff:
    pr=f['properties'];ss=snap[(snap.market==market)&(((snap.record_type=='origin')&(snap.record_id==pr['origin_id']))|((snap.record_type=='destination')&(snap.record_id==pr['destination_id'])))];snapvals.extend(pd.to_numeric(ss.snap_metres,errors='coerce').dropna().tolist());xy=np.array(f['geometry']['coordinates']);coords.extend(xy.tolist());kind=pr['kind'];cc=COL[kind]
    ax.plot(xy[:,0],xy[:,1],c=cc,lw=2,alpha=.9,label=('Auto2000' if kind=='auto2000' else 'Repair/service candidate'))
    ax.scatter(xy[-1,0],xy[-1,1],s=75,marker='^' if kind=='auto2000' else 'o',c=cc,edgecolors='white',zorder=4)
    ax.scatter(xy[0,0],xy[0,1],s=80,marker='*',c='#222222',edgecolors='white',zorder=5)
    labels.append(('A' if kind=='auto2000' else 'C')+f': {pr["duration_seconds"]/60:.1f} min / {pr["distance_metres"]/1000:.1f} km')
   if coords:
    q=np.array(coords);cy=q[:,1].mean();cx=(q[:,0].min()+q[:,0].max())/2;cy=(q[:,1].min()+q[:,1].max())/2;co=math.cos(math.radians(cy));half=max(.012,(q[:,0].max()-q[:,0].min())*co*.65,(q[:,1].max()-q[:,1].min())*.65);ax.set(xlim=(cx-half/co,cx+half/co),ylim=(cy-half,cy+half));ax.set_aspect(1/co)
   maxsnap=max(snapvals) if snapvals else float('nan');ax.set_title(label+'\n'+' | '.join(labels)+f'\nMaximum endpoint snap: {maxsnap:.0f} m',fontsize=9,pad=10);ax.set(xlabel='Longitude',ylabel='Latitude');ax.tick_params(labelsize=8);ax.grid(alpha=.15);ax.ticklabel_format(useOffset=False)
  hh,ll=axes[0].get_legend_handles_labels();fig.legend(hh,ll,frameon=False,loc='lower center',bbox_to_anchor=(.5,.005),ncol=2,fontsize=9)
  fig.suptitle(market.title()+' | all-routed illustrative journeys',x=.05,ha='left',fontsize=14,fontweight='bold');fig.tight_layout(rect=[0,.20,1,.89])
  save(fig,'route_examples_'+market,'Illustrative routed journeys in '+market.title(),'All-routed illustrations, including potentially large snaps. Three origins selected by minimum, median and maximum paired time gap in the all-routed grid. Black stars are snapped route starts; endpoints are returned road-graph positions. A=Auto2000, C=mapped repair/service candidate. Each panel has its own geographic extent. Lines are actual returned illustrative OSRM routes, not the full road network; route-request durations can differ from matrix values. Candidate job/model equivalence remains unverified.',sources())
  # PDF-readable single route pair; three-case figure retained for detailed ZIP inspection.
  import textwrap
  ff=[f for f in routes if f['properties']['market'].lower()==market and f['properties']['example']=='median_gap']
  fig=plt.figure(figsize=(8,5));ax=fig.add_axes([.09,.20,.52,.62]);coords=[];snapvals=[];info=[]
  for f in ff:
   pr=f['properties'];xy=np.array(f['geometry']['coordinates']);coords.extend(xy.tolist());kind=pr['kind'];cc=COL[kind]
   ax.plot(xy[:,0],xy[:,1],c=cc,lw=2.5,label='Auto2000' if kind=='auto2000' else 'Mapped candidate');ax.scatter(xy[-1,0],xy[-1,1],s=85,marker='^' if kind=='auto2000' else 'o',c=cc,edgecolors='white',zorder=4);ax.scatter(xy[0,0],xy[0,1],s=100,marker='*',c='#222',edgecolors='white',zorder=5)
   ss=snap[(snap.market==market)&(((snap.record_type=='origin')&(snap.record_id==pr['origin_id']))|((snap.record_type=='destination')&(snap.record_id==pr['destination_id'])))];snapvals.extend(pd.to_numeric(ss.snap_metres,errors='coerce').dropna().tolist())
   heading='Auto2000' if kind=='auto2000' else 'Mapped repair/service candidate';name=pr['destination_name'].replace('Auto2000 ','').replace(' - Dealer dan Bengkel Resmi Toyota','');info.extend([heading,textwrap.fill(name,width=28),f'{pr["duration_seconds"]/60:.1f} min | {pr["distance_metres"]/1000:.1f} km',''])
  if coords:
   q=np.array(coords);cy=(q[:,1].min()+q[:,1].max())/2;cx=(q[:,0].min()+q[:,0].max())/2;co=math.cos(math.radians(cy));half=max(.012,(q[:,0].max()-q[:,0].min())*co*.65,(q[:,1].max()-q[:,1].min())*.65);ax.set(xlim=(cx-half/co,cx+half/co),ylim=(cy-half,cy+half));ax.set_aspect(1/co)
  ax.set(xlabel='Longitude',ylabel='Latitude');ax.tick_params(labelsize=9);ax.ticklabel_format(useOffset=False);ax.grid(alpha=.15)
  maxsnap=max(snapvals) if snapvals else float('nan');fig.text(.64,.78,'\n'.join(info)+f'\nMaximum endpoint snap: {maxsnap:.0f} m',va='top',fontsize=10,linespacing=1.5)
  fig.suptitle(market.title()+' | median-gap all-routed illustration',x=.05,ha='left',fontsize=13,fontweight='bold');hh,ll=ax.get_legend_handles_labels();hh.append(Line2D([0],[0],marker='*',ls='',color='#222'));ll.append('Snapped start');fig.legend(hh,ll,loc='lower center',bbox_to_anchor=(.5,.025),ncol=3,frameon=False,fontsize=9)
  save(fig,'route_detail_'+market,'One returned route-pair example in '+market.title(),'Median-gap origin selected from the all-routed scenario. This may fail the ≤250 m snapping screen, as the annotated displacement shows. Lines are returned OSRM routes; stars are snapped starts. It is a model illustration, not a representative customer journey or an equivalent-job comparison. Three-case maps and exact records remain in the ZIP.',sources())
 pd.DataFrame(counts).to_csv(ROOT/'workstreams/cartography/map_counts.csv',index=False)
 # Candidate filters are deterministic source screens, not capability validation.
 fig,ax=plt.subplots(figsize=(10,6));xs=np.arange(4)
 raw=[];ret=[]
 for market in MARKETS:
  pp=providers[providers.market.str.lower()==market];raw.append(len(pp));ret.append(int(pp.eligible_candidate.astype(str).str.lower().isin(['true','1']).sum()))
 ax.bar(xs-.18,raw,.36,color='#a5b5b7',label='Retrieved automotive-category records')
 ax.bar(xs+.18,ret,.36,color='#236d80',label='Retained repair/service candidates')
 ax.set(xticks=xs,xticklabels=[m.title() for m in MARKETS],ylabel='Records in each expanded destination window',yscale='log')
 for i,(r,t) in enumerate(zip(raw,ret)):
  ax.text(i-.18,r*1.08,f'{r:,}',ha='center',fontsize=9);ax.text(i+.18,t*1.08,f'{t:,}',ha='center',fontsize=9)
 ax.legend(frameon=False,loc='upper left',bbox_to_anchor=(0,1.15),ncol=2);ax.grid(axis='y',alpha=.15);fig.tight_layout()
 save(fig,'candidate_filter_retention','Map discovery is not equivalent to a qualified workshop inventory','Logarithmic y-axis. Counts cover expanded study windows. Deterministic name/category/confidence/duplicate filters remove many records but do not verify ownership, Toyota fitment or job capability. Exact rules and each exclusion reason are retained in provider_inventory.csv.','Overture Maps Places release 2026-10-21.0; this study\'s documented candidate filters.')
 # CDF: common scale with plot edge values clipped only x-range marker.
 fig,axes=plt.subplots(2,2,figsize=(11,8),sharex=True,sharey=True)
 for ax,(market,bbox) in zip(axes.flat,MARKETS.items()):
  ar=access[(access.market==market)&(access.scenario=='all_routed')]
  for group,label in [('auto2000','Auto2000'),('independent','Mapped repair/service candidates'),('otoxpert','OtoXpert')]:
   v=pd.to_numeric(ar[group+'_nearest_seconds'],errors='coerce').dropna().sort_values().to_numpy()/60
   if len(v):ax.step(v,np.arange(1,len(v)+1)/len(ar)*100,where='post',label=label,c=COL[group],lw=2)
  ax.set(title=market.title(),xlim=(0,60),ylim=(0,101),xlabel='Modelled minutes to nearest listed destination',ylabel='Share of sampled grid origins (%)');ax.grid(alpha=.18)
 handles,labels=axes[0,0].get_legend_handles_labels();fig.legend(handles,labels,loc='lower center',ncol=3,frameon=False);fig.suptitle('Travel-time access varies by destination channel',x=.07,ha='left',fontsize=15,fontweight='bold');fig.tight_layout(rect=[0,.06,1,.94]);save(fig,'travel_cdf','Travel-time access by channel','All-routed scenario. Cumulative shares use all sampled grid origins as the denominator. Missing or unreachable origins do not become successful access. Curves beyond 60 minutes are outside the display. These grid shares are not population, vehicle-owner or customer shares.',sources())
 # Twenty minute access for all and snap-controlled scenarios.
 fig,ax=plt.subplots(figsize=(10,6));xs=np.arange(4);width=.24
 for j,(group,label) in enumerate([('auto2000','Auto2000'),('independent','Mapped repair/service candidates'),('otoxpert','OtoXpert')]):
  vals=[]
  for market in MARKETS:
   row=summary[(summary.market==market)&(summary.scenario=='all_routed')].iloc[0];vals.append(100*row[group+'_origins_le_20min']/row.grid_origins)
  ax.bar(xs+(j-1)*width,vals,width,color=COL[group],label=label)
 ax.set(xticks=xs,xticklabels=[m.title() for m in MARKETS],ylim=(0,105),ylabel='Sampled origins with a listed option within 20 min (%)');ax.legend(frameon=False,loc='upper left',bbox_to_anchor=(0,1.15),ncol=3);ax.grid(axis='y',alpha=.15);fig.tight_layout();save(fig,'access_20_minutes','Twenty-minute modelled access','All-routed scenario. The threshold is an analytical sensitivity setting, not a validated willingness-to-travel limit. Candidate garages do not have verified Toyota/job equivalence. Finite destination inventory and baseline routing apply.',sources())
 fig,ax=plt.subplots(figsize=(10,6))
 for j,(scenario,label,color) in enumerate([('all_routed','All routed origins','#236d80'),('snap_le_250m','Both endpoints snap ≤250 m','#d5523a')]):
  vals=[summary[(summary.market==m)&(summary.scenario==scenario)].iloc[0].median_paired_additional_minutes for m in MARKETS]
  ax.bar(xs+(j-.5)*.34,vals,.34,color=color,label=label)
 ax.axhline(0,color='black',lw=.7);ax.set(xticks=xs,xticklabels=[m.title() for m in MARKETS],ylabel='Median paired Auto2000 minus mapped-candidate minutes');ax.legend(frameon=False);ax.grid(axis='y',alpha=.15);fig.tight_layout();save(fig,'snap_sensitivity','Sensitivity to large endpoint snapping','The 250 m screen is an analyst-defined coordinate/routing sensitivity, not a diagnosis of wrong coordinates. Its paired-origin denominator may change across scenarios; inspect the accompanying tables.',sources())
 # Full distribution, not a single score.
 fig,ax=plt.subplots(figsize=(10,6));vv=[]
 for market in MARKETS:
  a=access[(access.market==market)&(access.scenario=='all_routed')];vv.append(pd.to_numeric(a.auto2000_minus_mapped_independent_seconds,errors='coerce').dropna()/60)
 bp=ax.boxplot(vv,tick_labels=[m.title() for m in MARKETS],patch_artist=True,showfliers=True)
 for patch in bp['boxes']:patch.set_facecolor('#a9c7ca')
 ax.axhline(0,color='#d5523a',lw=1);ax.set(ylabel='Auto2000 minus mapped-candidate modelled minutes');ax.grid(axis='y',alpha=.15);fig.tight_layout();save(fig,'gap_distributions','Origin-level travel burdens are uneven within markets','All-routed scenario. Boxes show medians and interquartile ranges of paired grid-origin time differences; whiskers use 1.5 IQR. Points are grid calculations, not independent customers or evidence of switching.',sources())
 # Quantify why destination margins matter.
 fig,ax=plt.subplots(figsize=(10,6))
 for j,(group,label,c) in enumerate([('auto2000','Auto2000','#d5523a'),('independent','Mapped repair/service candidates','#236d80')]):
  vals=[]
  for market in MARKETS:
   row=summary[(summary.market==market)&(summary.scenario=='all_routed')].iloc[0];vals.append(100*row[group+'_nearest_outside_origin_bbox_origins']/row.grid_origins)
  ax.bar(xs+(j-.5)*.34,vals,.34,color=c,label=label)
 ax.set(xticks=xs,xticklabels=[m.title() for m in MARKETS],ylabel='Sampled origins with nearest destination outside core (%)',ylim=(0,105));ax.legend(frameon=False);ax.grid(axis='y',alpha=.15);fig.tight_layout()
 save(fig,'destination_boundary_sensitivity','Administrative-style clipping can hide relevant destinations','Nearest means fastest among listed, routable destinations in the expanded window. Outside refers to the origin-study rectangle, not a city boundary. The expanded window is still finite; this diagnostic does not prove all relevant providers are captured.',sources())
 # Snap quality.
 fig,ax=plt.subplots(figsize=(10,6));ss=snap[snap.record_type=='origin']
 for market in MARKETS:
  v=pd.to_numeric(ss[ss.market==market].snap_metres,errors='coerce').dropna().sort_values().to_numpy();ax.step(v,np.arange(1,len(v)+1)/len(v)*100,where='post',label=market.title(),lw=2)
 ax.axvline(250,color='#d5523a',ls='--',lw=1);ax.set(xlabel='Origin displacement to the OSRM road graph (metres)',ylabel='Cumulative share of sampled origins (%)');ax.legend(frameon=False);ax.grid(alpha=.15);fig.tight_layout();save(fig,'origin_snapping','Road snapping is a measurable source of uncertainty','Large snapping can reflect inaccessible origin points, network gaps or coordinate placement. It is not automatically source error. The routing tables retain source and destination displacement separately.',sources())
 # Distinct official-network layer for the oil/filter path.
 sdpath=ROOT/'workstreams/providers/shopanddrive_official_study.csv'
 if sdpath.exists():
  sd=pd.read_csv(sdpath);fig,axes=plt.subplots(2,2,figsize=(12,10))
  for ax,(market,bbox) in zip(axes.flat,MARKETS.items()):
   setup(ax,bbox,pad=.035);w,s,e,n=bbox
   dd=pd.read_csv(ROOT/f'workstreams/routing/inputs/{market}_destinations.csv');bb=dd[dd.kind=='auto2000']
   oo=ox[ox.longitude.between(w-.08,e+.08)&ox.latitude.between(s-.08,n+.08)]
   ss=sd[sd.longitude.between(w-.08,e+.08)&sd.latitude.between(s-.08,n+.08)]
   ax.scatter(ss.longitude,ss.latitude,s=35,c='#665496',marker='o',alpha=.8,label='Shop & Drive')
   ax.scatter(oo.longitude,oo.latitude,s=70,c=COL['otoxpert'],marker='s',edgecolors='white',lw=.6,label='OtoXpert')
   ax.scatter(bb.longitude,bb.latitude,s=85,c=COL['auto2000'],marker='^',edgecolors='white',lw=.6,label='Auto2000')
   ax.set_title(market.title(),loc='left',fontsize=12)
  h,l=axes[0,0].get_legend_handles_labels();fig.legend(h,l,loc='lower center',ncol=3,frameon=False);fig.suptitle('Official network alternatives matter for the oil/filter path',x=.06,ha='left',fontsize=15,fontweight='bold');fig.tight_layout(rect=[0,.04,1,.95])
  save(fig,'official_oil_alternatives','Documented network offerings sharpen the oil-service comparison','Official directory coordinates for Auto2000, OtoXpert and Shop & Drive. Network-level oil/filter advertising provides a stronger service lead than a generic map tag, but Toyota fitment, exact parts, price and current slots remain unconfirmed. These are locations, not exclusive or independent ownership classes. Dashed rectangles are the origin windows; some margin destinations are outside the display.','Official Auto2000, OtoXpert and Shop & Drive directories retrieved 14 Nov 2026; network service evidence in sources register.')
 # Stronger service-lead comparator; exact local model/part fitment remains unknown.
 supp=ROOT/'workstreams/routing/supplement/combined_origin_accessibility.csv'
 if supp.exists():
  ca=pd.read_csv(supp);ca['market']=ca.market.str.lower();ca=ca[ca.scenario=='all_routed'];fig,axes=plt.subplots(2,2,figsize=(11,8),sharex=True,sharey=True)
  for ax,(market,bbox) in zip(axes.flat,MARKETS.items()):
   ar=ca[ca.market==market]
   for field,label,cc in [('auto2000_nearest_seconds','Auto2000','#d5523a'),('collected_advertised_oil_channels_nearest_seconds','Collected advertised oil channels','#665496'),('independent_nearest_seconds','Mapped repair/service candidates','#236d80')]:
    v=pd.to_numeric(ar[field],errors='coerce').dropna().sort_values().to_numpy()/60
    if len(v):ax.step(v,np.arange(1,len(v)+1)/len(ar)*100,where='post',label=label,c=cc,lw=2)
   ax.set(title=market.title(),xlim=(0,60),ylim=(0,101),xlabel='Modelled minutes to nearest listed destination',ylabel='Share of sampled grid origins (%)');ax.grid(alpha=.18)
  h,l=axes[0,0].get_legend_handles_labels();fig.legend(h,l,loc='lower center',ncol=3,frameon=False,fontsize=8);fig.suptitle('Advertised oil-service channels are a more specific geographic comparison',x=.07,ha='left',fontsize=14,fontweight='bold');fig.tight_layout(rect=[0,.06,1,.94])
  save(fig,'oil_access_comparison','Modelled access to collected advertised oil-service channels','All-routed scenario. The specific-service comparator uses the collected official network/local advertised oil-service destinations, not all Overture candidates. It is a finite public-source inventory, not all equivalent workshops. Exact Toyota model/year fitment, parts availability, current price and appointment capacity remain unconfirmed. Grid shares are not customer shares; these are baseline routing times.',sources()+' Shop & Drive official directory and additional advertised-provider evidence in supplemental routing inputs.')
 # Focal branches selected within each market using discrete grid influence.
 infl=ROOT/'workstreams/routing/output/focal12_branches.csv'
 if infl.exists():
  bi=pd.read_csv(infl);bi=bi[bi.scenario=='snap_le_250m'].copy();labels=[]
  for _,r in bi.iterrows():
   name=r.branch_name.replace('Auto2000 ','').replace(' - Dealer dan Bengkel Resmi Toyota','').replace(r.market+' ','');labels.append(r.market+' / '+name)
  yy=np.arange(len(bi));fig,axes=plt.subplots(1,2,figsize=(12,8),sharey=True,gridspec_kw={'width_ratios':[1,1.2]})
  axes[0].barh(yy,bi.origins_nearest_this_branch,color='#236d80');axes[0].set(yticks=yy,yticklabels=labels,xlabel='Grid origins where branch is nearest');axes[0].invert_yaxis()
  vals=pd.to_numeric(bi.median_additional_minutes_affected_origins_if_removed,errors='coerce').fillna(0);axes[1].barh(yy,vals,color='#d5523a');axes[1].set(xlabel='Median additional minutes among affected origins')
  for y,v,nn in zip(yy,vals,bi.origins_with_positive_increase_if_removed):axes[1].text(v+.1,y,f'n={int(nn)}',va='center',fontsize=8)
  for ax in axes:ax.grid(axis='x',alpha=.15)
  axes[1].set_xlim(0,max(vals)*1.3 if len(vals) and max(vals)>0 else 1);fig.suptitle('Focal branch influence on sampled access',x=.04,ha='left',fontsize=15,fontweight='bold');fig.tight_layout(rect=[0,0,1,.94])
  save(fig,'branch_influence','Focal branch leave-one-out access sensitivity','Screened scenario, both endpoints snap ≤250 m. Three branches per market selected by nearest grid-origin count, with the stated tie-break rule in focal12_branches.csv. Left counts are geographic assignment, not workloads or customers. Right shows the median extra modelled travel only among origins affected by omitting that branch; n is the affected-origin count. Omission is a computational sensitivity, not a closure recommendation or economic estimate.',sources())
 # Candidate-definition uncertainty matters independently of snap sensitivity.
 csfile=ROOT/'workstreams/routing/output/candidate_sensitivity_summary.csv'
 if csfile.exists():
  cs=pd.read_csv(csfile);cs['market']=cs.market.str.lower();fig,ax=plt.subplots(figsize=(10,6));xx=np.arange(4);wid=.25
  for j,(scenario,label,col) in enumerate([('baseline_candidates','Baseline candidates','#236d80'),('source_confidence_ge_0.9','Source confidence ≥0.9','#aa8135'),('explicit_car_name','Explicit car-name subset','#d5523a')]):
   vv=[cs[(cs.market==m)&(cs.scenario==scenario)].iloc[0].median_paired_additional_minutes for m in MARKETS];ax.bar(xx+(j-1)*wid,vv,wid,color=col,label=label)
  ax.axhline(0,c='black',lw=.7);ax.set(xticks=xx,xticklabels=[m.title() for m in MARKETS],ylabel='Median paired extra Auto2000 minutes');ax.legend(frameon=False,loc='upper left',bbox_to_anchor=(0,1.15),ncol=3,fontsize=9);ax.grid(axis='y',alpha=.15);fig.tight_layout()
  save(fig,'candidate_sensitivity_comparison','Candidate-definition uncertainty changes the travel-burden estimate','All-routed scenarios using the same 81 origins per market and frozen OD matrix. Provider confidence is an upstream source score, not audited capability. Explicit car-name selection is a lexical screen, not verified Toyota fitment or job equivalence. Compare magnitude changes rather than treating any candidate rule as ground truth. Main screened maps use a separate ≤250 m snapping rule.',sources()+' Derived candidate_sensitivity_summary.csv.')
 (ROOT/'workstreams/cartography/figure_registry.json').write_text(json.dumps(REG,indent=2))
 print(f'Created {len(REG)} figures')
if __name__=='__main__':main()
