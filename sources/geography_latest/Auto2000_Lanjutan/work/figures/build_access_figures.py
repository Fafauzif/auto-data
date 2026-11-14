from pathlib import Path
import json,math
import pandas as pd,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator,FormatStrFormatter
R=Path(__file__).resolve().parents[2];W=R/'work';O=R/'output/figures';O.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10.5,'axes.titlesize':13,'axes.labelsize':10.5,'xtick.labelsize':10,'ytick.labelsize':10,'legend.fontsize':9.5,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#fbfaf6','axes.facecolor':'#fbfaf6','savefig.facecolor':'#fbfaf6'})
T='#166979';A='#c65032';G='#8c9da2';D='#173b43';GOLD='#b18b24'
reg=[]
def save(fig,name,title,caption,source):
 fig.savefig(O/name,dpi=210,bbox_inches='tight');plt.close(fig);reg.append({'file':'figures/'+name,'title':title,'caption':caption,'source':source})
def geo(ax,ps):
 w,e=ps.longitude.min(),ps.longitude.max();s,n=ps.latitude.min(),ps.latitude.max();px=max((e-w)*.1,.005);py=max((n-s)*.1,.005);ax.set_xlim(w-px,e+px);ax.set_ylim(s-py,n+py);ax.set_aspect(1/math.cos(math.radians((s+n)/2)));ax.set_xlabel('Bujur timur (derajat)');ax.set_ylabel('Lintang (derajat)');ax.grid(alpha=.16);ax.xaxis.set_major_locator(MaxNLocator(4));ax.yaxis.set_major_locator(MaxNLocator(5));ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'));ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'));ax.text(.97,.97,'U ↑',transform=ax.transAxes,ha='right',va='top',color=D)
d=pd.read_csv(W/'access/origin_trip_scenarios.csv');s=pd.read_csv(W/'access/origin_robustness_summary.csv');dest=pd.read_csv(W/'access/new_destinations.csv')
#8 Same-market route-cost test of an additional journey, using both actual model directions.
j=d[(d.market=='JakartaBridge')&(d.scenario=='snap_le_250m')].dropna(subset=['auto2000_roundtrip_minutes','oil_network_roundtrip_minutes']).copy()
fig,ax=plt.subplots(figsize=(8.5,5.2));fields=['roundtrip_gap_minutes','auto_one_visit_vs_competitor_two_visits_gap','auto_two_visits_vs_competitor_one_visit_gap'];cols=[G,T,A]
for i,(field,col) in enumerate(zip(fields,cols)):
 vals=j[field].to_numpy();xs=np.linspace(i-.15,i+.15,len(vals));ax.scatter(xs,vals,s=35,c=col,alpha=.75,zorder=3);med=np.median(vals);ax.plot([i-.23,i+.23],[med,med],c=col,lw=4);ax.text(i+.27,med,f'{med:.1f}'.replace('.',','),va='center',fontweight='bold',color=col)
ax.axhline(0,c=D,lw=1);ax.set_xticks([0,1,2],['Keduanya 1 kunjungan\nA - C','Auto2000 1; alternatif 2\nA - 2C','Auto2000 2; alternatif 1\n2A - C']);ax.set_ylabel('Selisih waktu jalan pelanggan (menit model)');ax.set_xlim(-.4,2.5);ax.set_title('Satu kunjungan ulang dapat mengalahkan selisih lokasi',loc='left',fontweight='bold',color=D,pad=12);ax.grid(axis='y',alpha=.15);ax.text(.01,.97,f'n={len(j)} origin bangunan, bridge Jakarta Selatan\nPositif: Auto2000 lebih lama; garis tebal: median',transform=ax.transAxes,va='top',color=D,fontsize=10);fig.tight_layout()
save(fig,'08_satu_kunjungan_tambahan.png','Konfirmasi penyelesaian mengubah perbandingan total perjalanan','A dan C adalah durasi pergi+pulang yang dirutekan terpisah untuk Auto2000 umum dan jaringan oli pada origin yang sama. Tambahan kunjungan adalah skenario, bukan frekuensi kegagalan yang diobservasi. Mode perjalanan diasumsikan profil mobil yang sama; waktu menunggu/kerja tidak dimasukkan. Origin bangunan bukan rumah penulis ulasan.','work/access/new_bidirectional_od.csv; origin_trip_scenarios.csv; customer_journey evidence ledger')
#9 Bridge map. Actual business points, never reviewer homes.
build=j[['longitude','latitude']].copy();social=pd.read_csv(W/'customer_journey/maps_listing_inventory.csv');social['title']=social.title.fillna('');sel=social[social.title.str.contains('Cilandak|Radio Dalam|Simprug',case=False)&~social.permanently_closed.astype(str).str.lower().eq('true')]
# keep labels for the actual source endpoints only
sel=sel[sel.title.str.contains('Auto|Nawilis|Otoklix',case=False)].drop_duplicates('place_id')
fig,ax=plt.subplots(figsize=(8,6));q=dest[dest.market=='JakartaBridge']
for kind,label,col,marker in [('shopanddrive','Shop&Drive',G,'o'),('auto2000','Auto2000 umum',T,'^'),('otoxpert_auto2000','OtoXpert Auto2000',GOLD,'D'),('otoxpert_other','OtoXpert operator lain','#c5b27e','D')]:
 qq=q[q.kind==kind];ax.scatter(qq.longitude,qq.latitude,s=38,c=col,marker=marker,label=label,alpha=.8)
ax.scatter(build.longitude,build.latitude,s=65,c=A,marker='s',label=f'{len(j)} origin bangunan')
for _,r in sel.iterrows():
 ax.scatter(r.longitude,r.latitude,s=150,facecolor='none',edgecolor=D,lw=1.5,zorder=6)
 nm='Auto2000 Cilandak' if 'Cilandak' in r.title else 'Nawilis Radio Dalam' if 'Nawilis' in r.title else 'Otoklix Simprug'
 offset=(.05,.13) if 'Cilandak' in nm else (.05,.55) if 'Nawilis' in nm else (.05,.94)
 ax.annotate(nm,(r.longitude,r.latitude),xytext=offset,textcoords='axes fraction',fontsize=10.5,fontweight='bold',color=D,arrowprops={'arrowstyle':'-','color':D,'lw':.7})
geo(ax,pd.concat([build,sel[['longitude','latitude']]],ignore_index=True));ax.set_title('Cilandak menyatukan bukti perilaku\ndan akses dalam pasar yang sama',loc='left',fontweight='bold',color=D,pad=12);ax.legend(loc='upper left',bbox_to_anchor=(-.04,-.16),ncol=2,frameon=False);fig.tight_layout()
save(fig,'09_bridge_jakarta_selatan.png','Bridge Cilandak memisahkan lokasi, harga dan kepastian selesai','Titik lingkaran adalah lokasi outlet dalam ekspor ulasan, bukan rumah penulis. Akun positif/negatif digunakan untuk mekanisme, bukan prevalensi keluhan. Destinasi rute mencakup jendela lebih luas daripada peta detail ini. Listing B-Quik Lebak Bulus berstatus tutup tidak dijadikan endpoint aktif.','work/customer_journey/maps_listing_inventory.csv; social_evidence_ledger.csv; work/access/new_destinations.csv; origin_trip_scenarios.csv')
#10 Paired origin robustness, baseline subset not a different sample's city median.
ss=s[(s.scenario=='snap_le_250m')&s.case.isin(['AYani','Kertajaya','TanjungApiApi','SoekarnoHatta'])].copy();order=['AYani','Kertajaya','TanjungApiApi','SoekarnoHatta'];labels=['Surabaya / A. Yani','Surabaya / Kertajaya','Palembang / Tanjung Api-Api','Bandung / Soekarno-Hatta']
fig,ax=plt.subplots(figsize=(8.8,5.4))
for i,case in enumerate(order):
 for typ,offset,col in [('half_cell_shift',-.13,A),('mapped_building_representative_point',.13,T)]:
  z=ss[(ss.case==case)&(ss.origin_type==typ)]
  if not len(z):continue
  r=z.iloc[0];old=r.baseline_median_oneway_gap_same_selected_origins;new=r.median_outbound_optimized_gap_minutes
  ax.plot([old,new],[i+offset,i+offset],c=col,lw=2,alpha=.6);ax.scatter(old,i+offset,s=60,facecolor='none',edgecolor=col,lw=1.5);ax.scatter(new,i+offset,s=65,c=col,marker='D',zorder=3);ax.text(max(old,new)+.14,i+offset,f'baru {new:.2f}; n={int(r.outbound_optimized_paired_origins)}'.replace('.',','),va='center',color=col,fontsize=10)
ax.set_yticks(range(4),labels);ax.invert_yaxis();ax.axvline(0,c=G,lw=1);ax.grid(axis='x',alpha=.15);ax.set_xlim(-1.4,5.5);ax.set_xlabel('Median gap pergi ke jaringan oli (menit model)');ax.set_title('Keunggulan A. Yani berubah tanda;\ngap Kertajaya dan Soekarno-Hatta bertahan',loc='left',fontweight='bold',color=D,pad=14)
legend=[Line2D([0],[0],color=A,marker='D',label='Grid digeser setengah sel'),Line2D([0],[0],color=T,marker='D',label='Titik bangunan terpetakan'),Line2D([0],[0],color=G,marker='o',markerfacecolor='none',ls='None',label='Baseline pada subset origin yang sama')]
ax.legend(handles=legend,loc='upper left',bbox_to_anchor=(-.02,-.18),frameon=False);fig.tight_layout()
save(fig,'10_robustness_origin_keputusan.png','Soekarno-Hatta bertahan sebagai kantong akses; kontras Surabaya tidak universal','Setiap garis membandingkan baseline pada subset origin yang sama dengan origin baru; titik kosong=baseline, wajik=baru. N berbeda antar skenario, bukan estimasi populasi. Bangunan dipakai sebagai jangkar aktivitas fisik, tidak diklasifikasikan otomatis sebagai permukiman atau pemilik Toyota. Sensitivitas ini memakai minimum durasi pergi yang dihitung ulang per kanal; snap pergi≤250m, sehingga tidak mencampur perubahan origin dengan optimasi pergi+pulang.','work/access/origin_robustness_summary.csv; origin_trip_scenarios.csv; selected_building_footprints.geojson')
#11 Boundary counterexample Sidoarjo.
sid=d[(d.case=='Sidoarjo_extension')&(d.scenario=='snap_le_250m')].dropna(subset=['auto2000_roundtrip_minutes','oil_network_roundtrip_minutes']);sde=dest[(dest.market=='Surabaya')&dest.name.str.contains('Sidoarjo')].iloc[0]
fig,(ax,bx)=plt.subplots(1,2,figsize=(8.7,5),gridspec_kw={'width_ratios':[1.1,1]})
ax.scatter(sid.longitude,sid.latitude,s=70,c=A,marker='s',label='Origin bangunan di selatan');ax.scatter(sde.longitude,sde.latitude,c=T,s=140,marker='^',edgecolor='white',label='Auto2000 Sidoarjo');ax.annotate('Sidoarjo',(sde.longitude,sde.latitude),xytext=(6,6),textcoords='offset points',fontweight='bold',color=T)
geo(ax,pd.concat([sid[['longitude','latitude']],pd.DataFrame([sde])[['longitude','latitude']]]));ax.set_title('Origin baru di luar jendela lama',loc='left',fontweight='bold',color=D,pad=10);ax.legend(loc='upper left',bbox_to_anchor=(-.05,-.17),frameon=False)
xx=np.arange(len(sid));bx.bar(xx-.16,sid.auto2000_roundtrip_minutes,width=.32,color=T,label='Auto2000 terdekat');bx.bar(xx+.16,sid.oil_network_roundtrip_minutes,width=.32,color=A,label='Jaringan oli terdekat');bx.set_xticks(xx,['_'.join(str(x).split('_')[-2:]) for x in sid.origin_id]);bx.set_xlabel('ID origin bangunan (akhiran)');bx.set_ylabel('Pergi + pulang (menit model)');bx.set_title('Sidoarjo terdekat bagi 6 origin baru',loc='left',fontweight='bold',color=D,pad=10);bx.grid(axis='y',alpha=.15);bx.legend(loc='upper left',bbox_to_anchor=(-.05,-.17),frameon=False);fig.tight_layout(w_pad=2)
save(fig,'11_sidoarjo_batas_jendela.png','Nol origin pada grid lama bukan alasan menurunkan prioritas Sidoarjo','Enam origin bangunan yang ditambahkan di sekitar Sidoarjo semuanya memiliki Sidoarjo sebagai Auto2000 terdekat setelah koordinat dipulihkan. Median gap pergi+pulang ke jaringanoli sekitar0,02menit. Ini uji batas studi, bukan penambahan enam pelanggan atau dasar klaim permintaan.','work/access/origin_trip_scenarios.csv; selected_building_footprints.geojson; work/coordinates/coordinate_corrections.csv')
fp=R/'work/figures/figure_registry.json';old=json.loads(fp.read_text()) if fp.exists() else [];files={x['file'] for x in reg};allreg=[x for x in old if x['file'] not in files]+reg;fp.write_text(json.dumps(allreg,indent=2,ensure_ascii=False));print('Access figures',len(reg))
