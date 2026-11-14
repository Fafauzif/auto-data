from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

work=Path(__file__).parent;d=json.loads((work/'workbook_inputs.json').read_text(encoding='utf-8'));out=work/'figures';out.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.spines.left':False,'axes.titleweight':'bold','axes.titlelocation':'left','figure.facecolor':'white'})
fig,ax=plt.subplots(figsize=(9,4.5),constrained_layout=True)
m=d['markets'];x=np.arange(4);before=[r['oil_tail_before_owned_network_n'] for r in m];after=[r['oil_tail_after_owned_network_n'] for r in m]
a=ax.bar(x-.18,before,.36,color='#94A3B8',label='General branches only');b=ax.bar(x+.18,after,.36,color='#17324D',label='Existing owned oil channels included')
ax.bar_label(a,padding=4);ax.bar_label(b,padding=4);ax.set_xticks(x,[r['market'] for r in m]);ax.set_ylim(0,21);ax.set_yticks([0,5,10,15,20]);ax.set_ylabel('Model origins with oil-access gap >5 minutes');ax.legend(frameon=False,loc='upper left');ax.set_title('Existing channels remove 19 of 39 modelled oil-access tails',pad=19)
ax.text(0,-.17,'Latest corrected scenario. Counts describe 284 paired model origins, not customers or demand.',transform=ax.transAxes,fontsize=9,color='#475569');fig.savefig(out/'existing_channels_and_residual_access.png',dpi=180,bbox_inches='tight');plt.close(fig)
fig,ax=plt.subplots(figsize=(9,3.7),constrained_layout=True)
rev=sum(r['revenue_idr_billion'] for r in d['case']);gp=sum(r['gross_profit_idr_billion'] for r in d['case']);vals=[sum(r['revenue_idr_billion'] for r in d['case'][1:])/rev*100,sum(r['gross_profit_idr_billion'] for r in d['case'][1:])/gp*100]
bars=ax.barh(['Share of case revenue','Share of case gross profit'],vals,color=['#94A3B8','#17324D'],height=.5);ax.invert_yaxis();ax.set_xlim(0,60);ax.set_xticks([0,15,30,45,60],['0%','15%','30%','45%','60%']);ax.bar_label(bars,labels=[f'{v:.1f}%' for v in vals],padding=6);ax.set_title('After-sales carries 46.7% of case gross profit',pad=17)
ax.text(0,-.25,'Supplied FY2025 case P&L. All powertrains. Combined after-sales gross margin is 35.0%.',transform=ax.transAxes,fontsize=9,color='#475569');fig.savefig(out/'case_after_sales_profit_weight.png',dpi=180,bbox_inches='tight');plt.close(fig)
