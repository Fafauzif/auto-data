from pathlib import Path
import json,hashlib,py_compile
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
checks=[]
def check(name,ok):checks.append({'check':name,'pass':bool(ok)})
s=json.loads((OUT/'BATTERY_SUMMARY.json').read_text());a=pd.read_csv(OUT/'bundle_signal_audit.csv');ct=pd.read_csv(OUT/'scalar_count_receipt.csv');it=pd.read_csv(OUT/'gap_aware_signed_integrals.csv');sg=pd.read_csv(OUT/'gap30_segment_metrics.csv');ch=pd.read_csv(OUT/'charging_interval_soc_slope_diagnostics.csv');mi=json.loads((OUT/'STAGED_RAW_MANIFEST.json').read_text())
check('Five exact source bundles',len(a)==5)
check('Actual scientific signal count excluding clocks and Epoch',ct.loc[ct.role=='signal_value','stored_values'].sum()==56507201==s['physical_or_BMS_signal_scalar_values_excluding_clocks_epoch'])
check('Clock scalar count kept separate',ct.loc[ct.role=='clock','stored_values'].sum()==56599111)
check('Epoch values kept separate',ct.loc[ct.role=='absolute_time_metadata','stored_values'].sum()==91910)
check('No nonfinite source scalars',ct.nonfinite.sum()==0)
check('Five source payload bytes reconcile',a.source_bytes.sum()==283141466==s['selected_raw_payload_bytes'])
check('Largest source file byte count',a.source_bytes.max()==95036227)
check('Current and voltage clocks actually identical in every bundle',a.raw_current_voltage_clocks_identical.all())
check('SOC exact-clock matches only two bundles',a.soc_clock_identical_to_current.sum()==2)
check('Temperature exact-clock matches no bundle',a.temperature_clock_identical_to_current.sum()==0)
check('Sign counts partition current samples',((a.negative_current_samples+a.positive_current_samples+a.zero_current_samples)==a.current_sample_n).all())
check('Rare charge positive values correctly counted',a[a.source_mode_label=='Charge'].positive_current_samples.sum()==239)
check('Charge convention overwhelmingly negative',((a[a.source_mode_label=='Charge'].negative_current_samples/a[a.source_mode_label=='Charge'].current_sample_n)>.998).all())
check('Current recorded on integer grid',a.recorded_current_on_integer_ampere_grid.all())
check('Signed Ah equals separate positive less negative integrals',np.allclose(it.signed_Ah,it.positive_Ah-it.negative_magnitude_Ah))
check('Signed energy equals positive less negative integrals',np.allclose(it.signed_terminal_kWh,it.positive_terminal_kWh-it.negative_magnitude_terminal_kWh))
check('Absolute terminal integral equals sum of magnitudes',np.allclose(it.absolute_terminal_kWh,it.positive_terminal_kWh+it.negative_magnitude_terminal_kWh))
for folder,g in it.groupby('folder'):
 g=g.set_index('max_integrated_step_seconds');restricted=g.loc[['1','30','300']]
 check('Retained duration nondecreasing '+folder,(np.diff(restricted.supported_seconds)>=0).all())
 check('Energy stable across specified gap bounds '+folder,np.allclose(restricted.absolute_terminal_kWh,restricted.absolute_terminal_kWh.iloc[0]))
 check('Unbounded time equals source span '+folder,np.isclose(g.loc['UNBOUNDED_NAIVE_COUNTEREXAMPLE','supported_seconds'],a.set_index('folder').loc[folder,'wall_span_days']*86400))
check('Gap30 segments106 rather than source files or trips',len(sg)==106==s['gap30_segments'])
check('Common support no longer than segment duration',(sg.aligned_common_seconds.fillna(0)<=sg.duration_seconds+1e-6).all())
check('Four eligible partial charging diagnostics',len(ch)==4)
check('Partial diagnostic slope arithmetic matches exact table',np.allclose(ch.observed_negative_Ah_per_reported_soc_percentage_point,ch.aligned_negative_magnitude_Ah/ch.aligned_soc_change_percentage_points))
check('No health groundtruth claim',s['health_reference_capacity_data_public'] is False)
check('Published time metadata explicitly retained and qualified',s['privacy']['absolute_epoch_time_present'] is True and s['privacy']['direct_identifier_field_screen_not_comprehensive_privacy_certification'] is True)
check('Separate raw manifest has five MAT files and README',len(mi)==6 and sum(e['source_filename']=='Raw.mat' for e in mi)==5)
for e in mi:
 p=ROOT/e['release_path'];check('Exact source SHA256 '+e['release_path'],p.stat().st_size==e['source_size'] and hashlib.sha256(p.read_bytes()).hexdigest()==e['source_sha256'])
check('Earlier manifest remains separate17entries',len(json.loads((ROOT/'raw_licensed_data/DATASET_SOURCE_MANIFEST.json').read_text()))==17)
check('No full paper in telemetry raw appendix',not any(p.name=='paper.pdf' for p in (ROOT/'raw_licensed_data/EV_TELEMETRY_CC_BY_NC_3_0').rglob('*')))
for p in OUT.glob('*.py'):py_compile.compile(str(p),doraise=True)
check('All reproduction scripts compile',True)
for p in OUT.glob('*.json'):json.loads(p.read_text())
for p in OUT.glob('*.csv'):pd.read_csv(p)
check('All JSON and CSV parse',True)
receipt={'checks_total':len(checks),'passed':sum(x['pass'] for x in checks),'failed':sum(not x['pass'] for x in checks),'checks':checks,'visual_qa':'Analysis agent inspected both figures and revised the gap-integration chart to readable linear percentage excess. No human field validation claimed.','scope':'This new receipt covers telemetry files and calculations only; it is separate from earlier17-source-file QA. It does not validate source accuracy, health inference or anonymity.'}
(OUT/'QA_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:v for k,v in receipt.items() if k!='checks'},indent=2));print('FAILED',[x for x in checks if not x['pass']]);assert receipt['failed']==0
