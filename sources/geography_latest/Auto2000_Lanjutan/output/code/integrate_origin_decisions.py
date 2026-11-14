"""Integrate targeted-origin tests into the29endpoint decision table; no network."""
from pathlib import Path
import pandas as pd
R=Path(__file__).resolve().parents[1];W=R.parent/'work';p=W/'branch_analysis/branch_decision_table_29.csv'
b=pd.read_csv(p).astype(object).fillna('');a=pd.read_csv(W/'access/origin_trip_scenarios.csv');a=a[a.scenario=='snap_le_250m']
for k in ['additional_stress_test_roundtrip_nearest_n','additional_stress_test_cases','additional_origin_metric_scope']:
 if k not in b:b[k]=''
for i,r in b.iterrows():
 s=a[a.auto2000_name==r.branch_name]
 b.at[i,'additional_stress_test_roundtrip_nearest_n']=len(s)
 b.at[i,'additional_stress_test_cases']=';'.join(sorted(s['case'].unique())) if len(s) else 'Tidak menjadi minimum roundtrip pada origin tambahan terarah; bukan uji demand'
 b.at[i,'additional_origin_metric_scope']='Origin stres terarah, minimum roundtrip; tidak dijumlah ke nearest baseline satu arah atau pelanggan'
 if 'Sidoarjo' in r.branch_name:
  b.at[i,'recommended_intervention']='Tujuan Benar Sidoarjo / Pilihan Selatan';b.at[i,'decision_objective']='Koreksi koordinat dan pertahankan pilihan selatan pada routing job'
  t='Enam origin bangunan ekstensi selatan semuanya memilih Sidoarjo, gap median roundtrip+0,021menit; nol baseline akibat bataswindow.'
  if t not in str(r.evidence_reason):b.at[i,'evidence_reason']=str(r.evidence_reason)+' '+t
  b.at[i,'deprioritised_choice']='Menurunkan prioritas Sidoarjo sebagai sekadar cadangan karena n0 pada window lama; seluruh6originekstensi memilihnya.'
  b.at[i,'priority_class']='Koreksi tujuan dan perluasan domain routing selatan'
 if 'A. Yani' in r.branch_name:
  t='Uji6shift/bangunan memberi gappergi+0,246menit, sehingga klaimunggul tidakuniversal; mandatkeandalan tetap.'
  if t not in str(r.evidence_reason):b.at[i,'evidence_reason']=str(r.evidence_reason)+' '+t
 if 'Soekarno - Hatta' in r.branch_name:
  t='Enamoriginshift dan6bangunantetaptertinggal pada minimumoutbound+3,557menit.'
  if t not in str(r.evidence_reason):b.at[i,'evidence_reason']=str(r.evidence_reason)+' '+t
b.to_csv(p,index=False,encoding='utf-8-sig');b.to_csv(R/'tables/branch_decision_table_29.csv',index=False,encoding='utf-8-sig')
print('29 endpoint decisions integrated with targeted-origin evidence')
