from pathlib import Path
import json,math,textwrap
import pandas as pd,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator, FormatStrFormatter
from matplotlib.patches import Patch
R=Path(__file__).resolve().parents[2]; B=R/'extracted/baseline/Auto2000_Geographic_Study'; W=R/'work'; O=R/'output/figures';O.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10.5,'axes.titlesize':13,'axes.labelsize':10.5,'xtick.labelsize':10,'ytick.labelsize':10,'legend.fontsize':9.5,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#fbfaf6','axes.facecolor':'#fbfaf6','savefig.facecolor':'#fbfaf6'})
T='#166979'; A='#c65032'; G='#8c9da2'; D='#173b43'; F='#e4e6e0'; GOLD='#b18b24'
base=pd.read_csv(W/'branch_analysis/market_recomputed.csv');cor=pd.read_csv(W/'branch_analysis/corrected/market_recomputed.csv')
orig=pd.read_csv(W/'branch_analysis/corrected/origin_channels_recomputed.csv');orig=orig[(orig.scenario=='snap_le_250m')&orig.oil_gap_minutes.notna()].copy()
bro=pd.read_csv(W/'branch_analysis/corrected/all_27_branches_recomputed.csv');bro=bro[bro.scenario=='snap_le_250m'].copy()
branches=pd.concat([pd.read_csv(B/f'workstreams/routing/inputs/{m}_destinations.csv') for m in ['surabaya','medan','bandung','palembang']]);branches=branches[branches.kind=='auto2000'].copy()
corr=pd.read_csv(W/'coordinates/corrected_endpoints.csv').copy();corr['kind']='auto2000';branches=pd.concat([branches,corr],ignore_index=True)
reg=[]
def save(fig,name,title,caption,source):
 fig.savefig(O/name,dpi=210,bbox_inches='tight');plt.close(fig);reg.append({'file':'figures/'+name,'title':title,'caption':caption,'source':source})
def geo(ax,points,title=None,labels=False):
 ax.set_xlabel('Bujur timur (derajat)');ax.set_ylabel('Lintang (derajat)');ax.grid(alpha=.17,zorder=0)
 if len(points):
  w,e=points.longitude.min(),points.longitude.max();s,n=points.latitude.min(),points.latitude.max();px=max((e-w)*.08,.004);py=max((n-s)*.08,.004);ax.set_xlim(w-px,e+px);ax.set_ylim(s-py,n+py);ax.set_aspect(1/math.cos(math.radians((s+n)/2)))
 if title:ax.set_title(title,loc='left',fontweight='bold',color=D,pad=10)
 ax.xaxis.set_major_locator(MaxNLocator(4));ax.yaxis.set_major_locator(MaxNLocator(5));ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'));ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
 ax.text(.97,.97,'U ↑',transform=ax.transAxes,ha='right',va='top',color=D,fontsize=10)

def nameshort(x):
 return x.replace('Auto2000 ','').replace('Surabaya A. Yani - Dealer dan Bengkel Resmi Toyota','A. Yani').replace('Soekarno - Hatta','Soekarno-Hatta').replace('Tanjung Api - Api','Tanjung Api-Api')

# 1 Comparators and coordinate correction, same screened origin set.
x=base[base.scenario=='snap_le_250m'].set_index('market');z=cor[cor.scenario=='snap_le_250m'].set_index('market');markets=['Surabaya','Medan','Bandung','Palembang']
fig,ax=plt.subplots(figsize=(8.5,5));yy=np.arange(4)
for i,m in enumerate(markets):
 vals=[x.loc[m,'median_generic_gap_min'],x.loc[m,'median_oil_gap_min'],z.loc[m,'median_oil_gap_min']]
 ax.plot([min(vals),max(vals)],[i,i],color='#cbd3d2',lw=3,zorder=1)
 for val,off,col,marker,label in zip(vals,[-.14,0,.14],[G,A,T],['s','o','D'],['Generik awal','Jaringan oli awal','Jaringan oli + koreksi koordinat']):
  ax.scatter(val,i+off,s=70,color=col,marker=marker,label=label if i==0 else None,zorder=3)
  ax.text(val+.08,i+off,f'{val:.2f}'.replace('.',','),va='center',fontsize=10,color=col,fontweight='bold')
 ax.text(5.75,i,f'n={int(z.loc[m,"paired_n"])}',va='center',fontsize=10,color=D)
ax.set_yticks(yy,markets);ax.invert_yaxis();ax.set_xlim(-.1,6.4);ax.set_xlabel('Median selisih Auto2000 - alternatif (menit model)');ax.axvline(0,color='#869495',lw=.8);ax.grid(axis='x',alpha=.15);ax.legend(loc='upper center',bbox_to_anchor=(.5,-.16),ncol=1,frameon=False)
ax.set_title('Medan mendekati paritas; koreksi Suci memperkecil gap Bandung',loc='left',fontweight='bold',color=D,pad=15)
fig.tight_layout();save(fig,'01_pembanding_dan_koreksi.png','Pembanding mengubah keputusan, koreksi koordinat mengubah Bandung','Origin berpasangan yang sama, snap kedua endpoint≤250m. Angka generik dan jaringan oli adalah skenario pembanding, bukan dampak intervensi. Koreksi menambahkan kandidat koordinat Suci dan Sidoarjo; cakupan pelayanan aktual tetap berbeda dari akses model.','work/branch_analysis/market_recomputed.csv; corrected/market_recomputed.csv; work/coordinates/coordinate_corrections.csv')

# 2 Surabaya: same catchment size, opposite burden and internal redundancy.
s=orig[orig.market=='Surabaya'];targets=bro[(bro.market=='Surabaya')&bro.branch_name.str.contains('Yani|Kertajaya')].copy();colors={targets.iloc[0].branch_id:T,targets.iloc[1].branch_id:A}
# Explicit deterministic colour assignment independent of row order.
colors={r.branch_id:(T if 'Yani' in r.branch_name else A) for _,r in targets.iterrows()}
fig,(ax,bx)=plt.subplots(1,2,figsize=(9,5.6),gridspec_kw={'width_ratios':[1.1,1]})
ax.scatter(s.longitude,s.latitude,s=22,color='#d5dcd8',marker='s')
for _,r in targets.iterrows():
 q=s[s.auto2000_id==r.branch_id];col=colors[r.branch_id];ax.scatter(q.longitude,q.latitude,s=60,color=col,marker='s',label=f'{nameshort(r.branch_name)}: n={len(q)}')
 b=branches[branches.destination_id==r.branch_id].iloc[0];ax.scatter(b.longitude,b.latitude,s=100,c=col,marker='^',edgecolor='white',zorder=4);ax.annotate(nameshort(r.branch_name),(b.longitude,b.latitude),xytext=(5,6),textcoords='offset points',fontsize=10,fontweight='bold',color=col)
geo(ax,s,'Origin sama banyak, lokasinya berbeda');ax.legend(loc='lower left',bbox_to_anchor=(-.05,-.30),frameon=False)
a=targets[targets.branch_name.str.contains('Yani')].iloc[0];k=targets[targets.branch_name.str.contains('Kertajaya')].iloc[0]
y=np.arange(2);w=.32
bx.barh(y-w/2,[a.median_oil_gap_min,k.median_oil_gap_min],height=w,color=A,label='Gap ke jaringan oli')
bx.barh(y+w/2,[a.second_branch_penalty_median_min,k.second_branch_penalty_median_min],height=w,color=T,label='Tambahan waktu ke Auto2000 kedua')
bx.set_yticks(y,['A. Yani (11 origin)','Kertajaya (11 origin)']);bx.invert_yaxis();bx.axvline(0,color=G,lw=1);bx.set_xlabel('Median menit pada catchment masing-masing');bx.set_title('Peran jaringan berlawanan',loc='left',fontweight='bold',color=D,pad=10);bx.grid(axis='x',alpha=.15)
for j,row in enumerate([a,k]):
 for off,val in [(-w/2,row.median_oil_gap_min),(w/2,row.second_branch_penalty_median_min)]:bx.text(val+(.08 if val>=0 else -.08),j+off,f'{val:.2f}'.replace('.',','),va='center',ha='left' if val>=0 else 'right',fontsize=10,fontweight='bold')
bx.set_xlim(-1.7,4.6);bx.legend(loc='lower left',bbox_to_anchor=(-.1,-.30),frameon=False)
fig.tight_layout(w_pad=2);save(fig,'02_surabaya_dua_mandat.png','A. Yani dan Kertajaya sama-sama11origin, tetapi peran jaringan berlawanan','Skenario koordinat diperbaiki, snap≤250m. Selisih negatif berarti Auto2000 lebih dekat daripada jaringan oli. Penalti Auto2000 kedua menunjukkan substitusi geografis internal, bukan kapasitas kosong, omzet, atau dasar penutupan. Segitiga=cabang; kotak=origin model.','work/branch_analysis/corrected/all_27_branches_recomputed.csv; corrected/origin_channels_recomputed.csv; baseline routing inputs')

#3 Palembang concentration not river conjecture.
p=orig[orig.market=='Palembang'];fig,(ax,bx)=plt.subplots(1,2,figsize=(9,5.6),gridspec_kw={'width_ratios':[1.3,.8]})
ax.scatter(p.longitude,p.latitude,s=28,c='#d4dcd7',marker='s',label='Gap≤5 menit')
h=p[p.oil_gap_minutes>5];ax.scatter(h.longitude,h.latitude,s=80,c=A,marker='s',label='Gap>5 menit',zorder=4)
ties=h[h.nearest_tied_auto2000_count>1];ax.scatter(ties.longitude,ties.latitude,s=180,c='none',edgecolor=D,marker='o',linewidth=1.8,label='Nearest seri TAA/Veteran',zorder=5)
for _,r in branches[branches.market=='Palembang'].iterrows():
 ax.scatter(r.longitude,r.latitude,s=90,c=T,marker='^',edgecolor='white',zorder=5);ax.annotate(nameshort(r['name']),(r.longitude,r.latitude),xytext=(5,6),textcoords='offset points',color=T,fontweight='bold',fontsize=10)
geo(ax,p,'Gap awal >5 menit berada di utara');ax.legend(loc='lower left',bbox_to_anchor=(-.08,-.29),frameon=False)
bx.barh([0,1,2],[7,1,0],color=[A,G,T],height=.6);bx.barh([0],[1],left=[7],color='none',edgecolor=D,hatch='////',height=.6)
bx.set_yticks([0,1,2],['Tanjung Api-Api','Veteran','Plaju']);bx.invert_yaxis();bx.set_xlim(0,9);bx.set_xticks([0,3,6,9]);bx.set_xlabel('Origin gap >5 menit');bx.set_title('7 unik + 1 seri di TAA',loc='left',fontweight='bold',color=D,pad=10);bx.grid(axis='x',alpha=.15)
bx.text(7.5,0,'1 seri',va='center',ha='center',fontsize=9);bx.text(1.1,1,'1 unik',va='center',fontsize=10);bx.text(.1,2,'0',va='center',fontsize=10)
fig.tight_layout(w_pad=2);save(fig,'03_palembang_kantong_utara.png','Prioritaskan kantong Tanjung Api-Api, bukan narasi penyeberangan Plaju','9origin berpasangan memiliki gapoli>5menit. TAA memiliki7unik+1seri denganVeteran; urutanbaseline mengalokasikan seri keTAA sehingga menghasilkan8/9. Veteran1unik+1seri; Plaju0. Peta tidak menetapkan sungai/jembatan sebagai penyebab.','work/branch_analysis/corrected/origin_channels_recomputed.csv; work/review/NEAREST_BRANCH_TIES.json')

#4 Suci restoration.
bef=pd.read_csv(W/'branch_analysis/coordinate_before_after_origins.csv');bb=bef[(bef.market=='Bandung')&bef.auto2000_id_old.notna()&bef.auto2000_id_new.notna()].copy();changed=bb[bb.auto2000_id_old.fillna('')!=bb.auto2000_id_new.fillna('')]
fig,(ax,bx)=plt.subplots(1,2,figsize=(9,5.5),gridspec_kw={'width_ratios':[1.2,1]})
ax.scatter(bb.longitude_new,bb.latitude_new,s=24,c='#d5dcd8',marker='s');ax.scatter(changed.longitude_new,changed.latitude_new,s=65,c=A,marker='s',label=f'Cabang terdekat berubah: {len(changed)} origin')
for _,r in branches[branches.market=='Bandung'].iterrows():
 if 'Suci' in r['name'] or 'Cibiru' in r['name'] or 'Soekarno' in r['name'] or 'Setiabudi' in r['name']:
  ax.scatter(r.longitude,r.latitude,s=100,c=T if 'Suci' in r['name'] else G,marker='^',edgecolor='white',zorder=4);ax.annotate(nameshort(r['name']),(r.longitude,r.latitude),xytext=(4,5),textcoords='offset points',fontsize=10,color=T if 'Suci' in r['name'] else D,fontweight='bold')
geo(ax,bb.rename(columns={'longitude_new':'longitude','latitude_new':'latitude'}),'Suci kembali masuk dalam jaringan');ax.legend(loc='upper left',bbox_to_anchor=(-.05,-.19),frameon=False)
oldbro=pd.read_csv(W/'branch_analysis/all_27_branches_recomputed.csv');oldbro=oldbro[(oldbro.market=='Bandung')&(oldbro.scenario=='snap_le_250m')]
newbro=bro[bro.market=='Bandung'];labs=['Suci','Cibiru','Soekarno - Hatta'];olds=[];news=[]
for lab in labs:
 q=oldbro[oldbro.branch_name.str.contains(lab,regex=False)];olds.append(int(q.nearest_origins_n.iloc[0]) if len(q) else 0);news.append(int(newbro[newbro.branch_name.str.contains(lab,regex=False)].nearest_origins_n.iloc[0]))
y=np.arange(3);bx.barh(y-.16,olds,height=.3,color=G,label='Sebelum koreksi');bx.barh(y+.16,news,height=.3,color=T,label='Setelah koreksi');bx.set_yticks(y,['Suci','Cibiru','Soekarno-Hatta']);bx.invert_yaxis();bx.set_xlabel('Origin terdekat');bx.set_title('Beban prioritas bergeser',loc='left',fontweight='bold',color=D,pad=10)
for i,(a,b) in enumerate(zip(olds,news)):bx.text(a+.4,i-.16,str(a),va='center');bx.text(b+.4,i+.16,str(b),va='center')
bx.set_xlim(0,25);bx.grid(axis='x',alpha=.15);bx.legend(loc='lower left',bbox_to_anchor=(-.1,-.23),frameon=False);fig.tight_layout(w_pad=2)
save(fig,'04_suci_mengubah_prioritas.png','Koreksi Suci mengurangi tekanan Cibiru; Soekarno-Hatta tetap kantong utama','Origin berpasangan Bandung sama(n=78). Suci menggunakan kandidatkoordinat alternatif sejalanalamatresmi danOverture, bukan lapangan. BaselineSuci dikeluarkan karena tautankoordinatmenyalinSetiabudi. Koreksi juga menambahkanSidoarjo keSurabaya; hasilnya tersedia dalamCSV.','work/coordinates/coordinate_corrections.csv; work/branch_analysis/coordinate_before_after_origins.csv; corrected/all_27_branches_recomputed.csv')

#5 OwnedOX marginal threshold and substantive savings.
ox=pd.read_csv(W/'branch_analysis/corrected/owned_otoxpert_marginal.csv');ox=ox[ox.scenario=='snap_le_250m'].set_index('market').loc[markets]
fig,(ax,bx)=plt.subplots(1,2,figsize=(9,5.3))
vals=ox[[f'added_le_{v}min' for v in [10,15,20,30]]].to_numpy();im=ax.imshow(vals,cmap='YlGnBu',vmin=0,vmax=max(4,vals.max()),aspect='auto');ax.set_xticks(range(4),['10','15','20','30']);ax.set_yticks(range(4),markets);ax.set_xlabel('Batas akses (menit model)');ax.set_title('Tambahan origin dalam cakupan',loc='left',fontweight='bold',color=D,pad=10)
for i in range(4):
 for j in range(4):ax.text(j,i,str(int(vals[i,j])),ha='center',va='center',color='white' if vals[i,j]>=3 else D,fontweight='bold',fontsize=12)
y=np.arange(4);bx.barh(y-.17,ox.own_ox_benefit_gt3min_n,height=.32,color=T,label='Hemat >3 menit');bx.barh(y+.17,ox.own_ox_benefit_gt5min_n,height=.32,color=A,label='Hemat >5 menit');bx.set_yticks(y,markets);bx.invert_yaxis();bx.set_xlabel('Origin dengan penghematan');bx.set_title('Palembang menyimpan manfaat lokal',loc='left',fontweight='bold',color=D,pad=10);bx.legend(loc='upper left',bbox_to_anchor=(-.05,-.17),frameon=False)
for i,r in enumerate(ox.itertuples()):
 bx.text(r.own_ox_benefit_gt3min_n+.15,i-.17,str(r.own_ox_benefit_gt3min_n),va='center');bx.text(r.own_ox_benefit_gt5min_n+.15,i+.17,str(r.own_ox_benefit_gt5min_n),va='center')
bx.set_xlim(0,13);bx.grid(axis='x',alpha=.15);fig.tight_layout(w_pad=2)
save(fig,'05_otoxpert_marginal.png','OtoXpert-owned terutama memperkaya tawaran; Palembang punya penghematan lokal','BandingkanminimumAuto2000umumdenganminimumAuto2000+OtoXpertberlabelAuto2000-operated. n=59/78/78/69; snap≤250m; koordinatSuci/Sidoarjodiperbaiki. Tambahancakupan20menit0/0/0/2. Penghematanbukanmargintambahan; operatorlabeltidakmenunjukkanpembagianGP.','work/branch_analysis/corrected/owned_otoxpert_marginal.csv')

#6 Local comparator composition by assigned catchment among decision branches.
targetwords={'Surabaya':['Yani','Kertajaya'],'Medan':['Pancing','Gatot'],'Bandung':['Suci','Soekarno'],'Palembang':['Tanjung Api','Plaju']}
rows=[]
for m,ww in targetwords.items():
 for word in ww:
  r=bro[(bro.market==m)&bro.branch_name.str.contains(word,regex=False)].iloc[0];rows.append(r)
fig,ax=plt.subplots(figsize=(8.5,5.8));ys=np.arange(len(rows));left=np.zeros(len(rows));spec=[('nearest_oil_otoxpert_auto2000_n','OtoXpert Auto2000',T),('nearest_oil_otoxpert_other_n','OtoXpert operator lain',GOLD),('nearest_oil_shopanddrive_n','Shop&Drive',A)]
for field,label,col in spec:
 v=np.array([r[field] for r in rows]);ax.barh(ys,v,left=left,color=col,label=label,height=.65)
 for i,(val,l) in enumerate(zip(v,left)):
  if val:ax.text(l+val/2,i,str(int(val)),ha='center',va='center',color='white',fontweight='bold')
 left+=v
ax.set_yticks(ys,[r.market+' / '+nameshort(r.branch_name) for r in rows]);ax.invert_yaxis();ax.set_xlabel('Origin menurut jaringan oli terdekat');ax.set_title('Alternatif terdekat berada di perimeter laba yang berbeda',loc='left',fontweight='bold',color=D,pad=12);ax.legend(loc='upper left',bbox_to_anchor=(-.05,-.18),ncol=1,frameon=False);ax.grid(axis='x',alpha=.12);fig.tight_layout()
save(fig,'06_operator_alternatif_lokal.png','Perimeter operator mengubah arti memenangkan kembali pekerjaan','KlasifikasialternatifterdekatperoriginpadacatchmentAuto2000umumterpilih, snap≤250m, koordinatdiperbaiki. Shop&DrivedanOtoXpertoperatorlainbukanotomatisGPAuto2000. Labeljaringanmenyatakanofferingoli, bukankonfirmasiparts/slot/modelindividual.','work/branch_analysis/corrected/all_27_branches_recomputed.csv')

#7 Owned channel eliminates the >5min Palembang oil gap in the finite grid.
p=orig[orig.market=='Palembang'].copy();p['combined_gap']=(p.owned_oil_network_seconds-p.oil_network_seconds)/60;h=p[p.oil_gap_minutes>5].copy()
oxp=pd.read_csv(B/'workstreams/context/otoxpert_official_inventory.csv');oxp=oxp[oxp.name=='OtoXpert Palembang'].iloc[0]
fig,(ax,bx)=plt.subplots(1,2,figsize=(9,5.8),gridspec_kw={'width_ratios':[1.15,1]})
ax.scatter(p.longitude,p.latitude,s=22,c='#d9dfdb',marker='s',label='Origin lain')
ax.scatter(h.longitude,h.latitude,s=75,c=A,marker='s',label='9 origin gap awal >5 menit')
ax.scatter([oxp.longitude],[oxp.latitude],s=170,c=T,marker='*',edgecolor='white',zorder=6,label='OtoXpert Palembang (Auto2000)')
ax.annotate('OtoXpert Palembang',(oxp.longitude,oxp.latitude),xytext=(4,-16),textcoords='offset points',fontsize=10,color=T,fontweight='bold')
for _,r in branches[branches.market=='Palembang'].iterrows():
 ax.scatter(r.longitude,r.latitude,s=75,c=G,marker='^',edgecolor='white',zorder=4)
 ax.annotate(nameshort(r['name']),(r.longitude,r.latitude),xytext=(4,5),textcoords='offset points',fontsize=9.5,color=D)
geo(ax,p,'Salurkan oli ke OtoXpert\nPalembang yang sudah ada');ax.legend(loc='upper left',bbox_to_anchor=(-.05,-.19),frameon=False)
xx=np.arange(len(h));bx.plot(xx,h.oil_gap_minutes.to_numpy(),color=A,marker='o',lw=2,label='Auto2000 umum saja');bx.plot(xx,h.combined_gap.to_numpy(),color=T,marker='D',lw=2,label='Auto2000 + OtoXpert-owned');bx.axhline(5,color=G,ls='--',lw=1,label='Ambang diagnostik 5 menit');bx.set_ylim(-.4,7.6);bx.set_xticks(xx,[x.replace('g','') for x in h.origin_id],rotation=55);bx.set_ylabel('Gap ke jaringan oli terdekat (menit)');bx.set_xlabel('Sembilan origin tertinggal\npada baseline');bx.set_title('Origin gap >5 menit:\n9 menjadi 0',loc='left',fontweight='bold',color=D,pad=10);bx.grid(alpha=.15)
bx.legend(loc='upper left',bbox_to_anchor=(-.13,-.31),frameon=False)
fig.tight_layout(w_pad=2)
save(fig,'07_palembang_ox_menutup_gap.png','OtoXpert Palembang menghapus seluruhkantong gapoli>5menit tanpa cabangbaru','Origin berpasangan yang sama(n=69), snap≤250m, koordinatdiperbaiki. Sembilanorigin awal>5menit menjadi7originparitas dan2origin gap1,005menit denganAuto2000umum+OtoXpert-owned. Iniaksesmodelkeofferingjaringanoli; bukanbuktistok/slot/kapasitasatauGP. Tidakmenjumlahkanchannelmenjadibisnisbaru.','work/branch_analysis/corrected/origin_channels_recomputed.csv; baselineofficialOtoXpertinventory')

fp=R/'work/figures/figure_registry.json';old=json.loads(fp.read_text()) if fp.exists() else [];newfiles={x['file'] for x in reg};reg=[x for x in old if x['file'] not in newfiles]+reg;fp.write_text(json.dumps(reg,indent=2,ensure_ascii=False))
print('figures',len(reg))
