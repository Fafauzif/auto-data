from pathlib import Path
import csv,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];out=ROOT/'figures';out.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.spines.left':False,'axes.titleweight':'bold','savefig.facecolor':'white'})
# Survey cells: full same-question series, no pooled bases
rows=list(csv.DictReader((ROOT/'workstreams/market/deloitte_service_indonesia.csv').open()))
series=[r for r in rows if r['question']=='Q17'];series=sorted(series,key=lambda r:int(r['published_percent']))
labels={'Quality of work':'Work quality','Personal relationship with mechanic/technician':'Mechanic relationship','Convenience (location/hours)':'Location and hours'}
fig,ax=plt.subplots(figsize=(9.2,5.6));vals=[int(r['published_percent']) for r in series];bars=ax.barh([labels.get(r['metric_label'],r['metric_label']) for r in series],vals,color='#244a68')
for b,v in zip(bars,vals):ax.text(v+.35,b.get_y()+b.get_height()/2,f'{v}%',va='center')
ax.set_xlim(0,29);ax.set_xlabel('Published percentage in this survey question');ax.set_title('Quality trust and warranty lead these stated service choice reasons',loc='left',pad=17)
fig.text(.02,.025,'Source: Deloitte 2026 SEA Automotive Consumer Study, p.33, Q17, Indonesia n=618.\nFieldwork Oct-Nov 2025. Descriptive survey; percentages are rounded and do not establish causes.',fontsize=8,color='#444')
fig.tight_layout(rect=[0,.10,1,1]);fig.savefig(out/'service_choice_factors.png',dpi=220);plt.close(fig)
# Actual finance outputs under same vehicle/locality; not binding quotes
rows=list(csv.DictReader((ROOT/'workstreams/journeys/finance_scenarios.csv').open()));series=[r for r in rows if r['tenor_months']=='60']
fig,axes=plt.subplots(1,2,figsize=(10,4.8));names=['Insurance paid upfront','Insurance paid in instalments']
for ax,key,title in zip(axes,['total_upfront_idr','monthly_idr'],['Cash required upfront','Displayed monthly instalment']):
 values=[int(r[key])/1e6 for r in series];bars=ax.bar(names,values,color=['#244a68','#b66735'],width=.5)
 ax.set_ylabel('Rp million');ax.set_title(title,loc='left',fontsize=12);ax.tick_params(axis='x',labelsize=8)
 for b,v in zip(bars,values):ax.text(b.get_x()+b.get_width()/2,v+.02*max(values),f'{v:,.2f}',ha='center',fontsize=10)
 ax.set_ylim(0,max(values)*1.2)
fig.suptitle('An existing simulator exposes a liquidity tradeoff',x=.02,ha='left',fontweight='bold',fontsize=15)
fig.text(.02,.02,'Observed Auto2000 public simulator, 11 Nov 2026, UX03-UX04. Same Innova Zenix G HV CVT, Jakarta Pusat,\nRp475.4m, base DP20%, ADDM, 60-month tenor with59 displayed remaining instalments. Conditional estimates, not binding quotes.',fontsize=8)
fig.tight_layout(rect=[0,.12,1,.90]);fig.savefig(out/'finance_cash_tradeoff.png',dpi=220);plt.close(fig)
# Dataset coordinate agreement checks
rows=list(csv.DictReader((ROOT/'workstreams/datasets/five_branch_coordinate_crosscheck.csv').open()))
fig,ax=plt.subplots(figsize=(9.2,4.8));values=[float(r['straight_line_disagreement_km']) for r in rows];names=[r['location_name'].replace('AUTO2000 ','').replace(' (Khusus Toyota & Lexus)','') for r in rows]
bars=ax.barh(names,values,color=['#b66735' if v>1 else '#244a68' for v in values]);ax.set_xscale('log');ax.set_xlim(.004,160)
for b,v in zip(bars,values):ax.text(v*1.15,b.get_y()+b.get_height()/2,f'{v:.3f} km',va='center')
ax.set_xlabel('Straight-line separation on a logarithmic scale');ax.set_title('One location conflict can distort a geographic conclusion',loc='left',pad=16)
fig.text(.02,.02,'Source: original analysis of Mendeley SPKLU v2 (16 Jun2026) and five official branch direction links (11 Nov2026).\nFive selected cases; official directions are a comparison source, not field verification of each charger.',fontsize=8)
fig.tight_layout(rect=[0,.12,1,1]);fig.savefig(out/'branch_coordinate_checks.png',dpi=220);plt.close(fig)
print('Created3 original research figures')
