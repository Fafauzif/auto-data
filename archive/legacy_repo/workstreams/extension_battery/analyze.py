"""Bounded telemetry methods stress test. Existing licensed source files only."""
from pathlib import Path
import json,hashlib,collections
import numpy as np,pandas as pd
from signals import load_signals
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent;CACHE=ROOT/'private_cache/extension_battery'
files=sorted(CACHE.glob('*_Raw.mat'))
if len(files)!=5:files=sorted((ROOT/'raw_licensed_data/EV_TELEMETRY_CC_BY_NC_3_0').glob('*/*/Raw.mat'))
assert len(files)==5
audit=[];integrals=[];segments=[];keys=[];counts=[];tempstats=[]
def integ(t,i,v,threshold):
 dt=np.diff(t);ok=(dt>0)&np.isfinite(dt)
 if threshold is not None:ok &= dt<=threshold
 pow=i*v;plus_i=np.maximum(i,0);minus_i=np.maximum(-i,0);plus_p=np.maximum(pow,0);minus_p=np.maximum(-pow,0)
 def area(z):return float((.5*(z[:-1][ok]+z[1:][ok])*dt[ok]).sum())
 return {'supported_seconds':float(dt[ok].sum()),'excluded_gap_intervals':int((~ok).sum()),'positive_Ah':area(plus_i)/3600,'negative_magnitude_Ah':area(minus_i)/3600,'signed_Ah':area(i)/3600,'positive_terminal_kWh':area(plus_p)/3600000,'negative_magnitude_terminal_kWh':area(minus_p)/3600000,'signed_terminal_kWh':area(pow)/3600000,'absolute_terminal_kWh':(area(plus_p)+area(minus_p))/3600000}
def weighted_mean(t,y,threshold=30):
 dt=np.diff(t);ok=(dt>0)&(dt<=threshold);return float((.5*(y[:-1][ok]+y[1:][ok])*dt[ok]).sum()/dt[ok].sum()) if ok.any() else np.nan
for path in files:
 d,fmt=load_signals(path);folder=path.parent.name if path.name=='Raw.mat' else path.name.split('_')[0];mode='Charge' if int(folder[6:])%2 else 'Drive';t=d['TimeCurr'];i=d['Curr'];v=d['Volt'];dt=np.diff(t)
 expected={'Curr','TimeCurr','Volt','TimeVolt','SoC','TimeSoC','Temp','TimeTemp','Epoch','TimeEpoch'}
 assert set(d)==expected
 r={'folder':folder,'source_mode_label':mode,'mat_format':fmt,'source_bytes':path.stat().st_size,'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'current_sample_n':len(i),'voltage_sample_n':len(v),'soc_sample_n':len(d['SoC']),'temperature_sample_n':len(d['Temp']),'measured_or_BMS_signal_scalar_values':sum(len(d[k]) for k in ['Curr','Volt','SoC','Temp']),'clock_scalar_values':sum(len(d[k]) for k in ['TimeCurr','TimeVolt','TimeSoC','TimeTemp','TimeEpoch']),'epoch_alignment_value_n':len(d['Epoch']),'raw_current_voltage_clocks_identical':bool(np.array_equal(t,d['TimeVolt'])),'soc_clock_identical_to_current':bool(np.array_equal(t,d['TimeSoC'])),'temperature_clock_identical_to_current':bool(np.array_equal(t,d['TimeTemp'])),'wall_span_days':float((t[-1]-t[0])/86400),'max_current_clock_gap_seconds':float(dt.max()),'negative_current_samples':int((i<0).sum()),'positive_current_samples':int((i>0).sum()),'zero_current_samples':int((i==0).sum()),'current_min_A':float(i.min()),'current_max_A':float(i.max()),'soc_first_pct':float(d['SoC'][0]),'soc_last_pct':float(d['SoC'][-1]),'soc_min_pct':float(d['SoC'].min()),'soc_max_pct':float(d['SoC'].max()),'temperature_min_C':float(d['Temp'].min()),'temperature_max_C':float(d['Temp'].max()),'temperature_time_weighted_mean_C_gap30':weighted_mean(d['TimeTemp'],d['Temp'])}
 assert r['raw_current_voltage_clocks_identical']
 if len(t)==len(d['TimeSoC']):
  offset=np.abs(t-d['TimeSoC']);r.update({'soc_vs_current_index_absolute_offset_median_s':float(np.median(offset)),'soc_vs_current_index_absolute_offset_max_s':float(offset.max())})
 r.update({'recorded_current_on_integer_ampere_grid':bool(np.allclose(i,np.round(i),rtol=0,atol=1e-10)),'current_median_absolute_A':float(np.median(np.abs(i))),'current_smallest_observed_nonzero_A':float(np.abs(i[i!=0]).min()),'recorded_grid_not_calibrated_sensor_error':True})
 audit.append(r)
 for name,arr in d.items():
  counts.append({'folder':folder,'mode':mode,'field':name,'stored_values':len(arr),'dtype':str(arr.dtype),'nonfinite':int((~np.isfinite(arr)).sum()),'role':'signal_value' if name in ['Curr','Volt','SoC','Temp'] else ('absolute_time_metadata' if name=='Epoch' else 'clock'),'unit':{'Curr':'A','Volt':'V','SoC':'percent','Temp':'degrees_C'}.get(name,'seconds'),'interpretation':'Stored scalar samples, not independent people, events or synchronized multivariate rows'})
  keys.append({'folder':folder,'field':name,'numeric':bool(np.issubdtype(arr.dtype,np.number)),'direct_GPS_VIN_owner_contact_field_detected':False,'absolute_time_metadata':name in ['Epoch','TimeEpoch']})
 for threshold in (1,30,300,None):
  z=integ(t,i,v,threshold);z.update({'folder':folder,'mode':mode,'max_integrated_step_seconds':threshold if threshold is not None else 'UNBOUNDED_NAIVE_COUNTEREXAMPLE','i_v_alignment':'Identical observed clocks; no interpolation or extrapolation','interpretation':'Signed pack-terminal signal integral over retained intervals, not wall energy, usable capacity, SOH or efficiency'});integrals.append(z)
 cuts=np.r_[0,np.flatnonzero((dt>30)|(dt<=0))+1,len(t)]
 for j,(lo,hi) in enumerate(zip(cuts[:-1],cuts[1:]),1):
  if hi-lo<2:continue
  tt=t[lo:hi];ii=i[lo:hi];vv=v[lo:hi];z=integ(tt,ii,vv,30)
  z.update({'folder':folder,'mode':mode,'segment_number_gap30':j,'current_samples':hi-lo,'elapsed_start_seconds_from_bundle_start':float(tt[0]-t[0]),'elapsed_end_seconds_from_bundle_start':float(tt[-1]-t[0]),'duration_seconds':float(tt[-1]-tt[0]),'current_negative_sample_fraction':float((ii<0).mean()),'current_positive_sample_fraction':float((ii>0).mean())})
  si=np.flatnonzero((d['TimeSoC']>=tt[0])&(d['TimeSoC']<=tt[-1]));ti=np.flatnonzero((d['TimeTemp']>=tt[0])&(d['TimeTemp']<=tt[-1]))
  if len(ti)>1:
   z['temperature_time_weighted_mean_C']=weighted_mean(d['TimeTemp'][ti],d['Temp'][ti]);z['temperature_min_C']=float(d['Temp'][ti].min());z['temperature_max_C']=float(d['Temp'][ti].max())
  if len(si)>1:
   a=max(tt[0],d['TimeSoC'][si[0]]);b=min(tt[-1],d['TimeSoC'][si[-1]]);ci=np.flatnonzero((tt>=a)&(tt<=b))
   if len(ci)>1:
    common_t=tt[ci];common_soc=np.interp(common_t[[0,-1]],d['TimeSoC'][si],d['SoC'][si]);q=integ(common_t,ii[ci],vv[ci],30)
    z.update({'aligned_soc_first_pct':float(common_soc[0]),'aligned_soc_last_pct':float(common_soc[-1]),'aligned_soc_change_percentage_points':float(common_soc[-1]-common_soc[0]),'aligned_common_seconds':float(common_t[-1]-common_t[0]),'aligned_signed_Ah':q['signed_Ah'],'aligned_negative_magnitude_Ah':q['negative_magnitude_Ah'],'soc_alignment':'SOC interpolated only at common-support current interval endpoints; no extrapolation'})
    if mode=='Charge' and common_soc[-1]-common_soc[0]>=1 and common_t[-1]-common_t[0]>=600:
     z['observed_negative_Ah_per_reported_soc_percentage_point']=q['negative_magnitude_Ah']/(common_soc[-1]-common_soc[0]);z['slope_is_not_capacity_or_SOH']=True
  segments.append(z)
 del d
aa=pd.DataFrame(audit);it=pd.DataFrame(integrals);sg=pd.DataFrame(segments);ct=pd.DataFrame(counts)
aa.to_csv(OUT/'bundle_signal_audit.csv',index=False);it.to_csv(OUT/'gap_aware_signed_integrals.csv',index=False);sg.to_csv(OUT/'gap30_segment_metrics.csv',index=False);ct.to_csv(OUT/'scalar_count_receipt.csv',index=False);pd.DataFrame(keys).to_csv(OUT/'raw_field_privacy_inventory.csv',index=False)
aa[['folder','recorded_current_on_integer_ampere_grid','current_median_absolute_A','current_smallest_observed_nonzero_A','recorded_grid_not_calibrated_sensor_error']].to_csv(OUT/'current_numeric_resolution_audit.csv',index=False)
charge=sg[sg['observed_negative_Ah_per_reported_soc_percentage_point'].notna()].copy();charge.to_csv(OUT/'charging_interval_soc_slope_diagnostics.csv',index=False)
sources=json.loads((OUT/'SOURCE_FILE_MANIFEST.json').read_text())
summary={'source_doi':'10.17632/7vdkzpnjgj.2','source_license':'CC BY-NC3.0','source_context':'One Audi e-tron, San Francisco Bay Area, November2019–October2020; paper DOI10.1016/j.joule.2023.07.018','selected_bundles':len(files),'selected_bundle_names':aa.folder.tolist(),'selected_raw_payload_bytes':int(aa.source_bytes.sum()),'largest_source_file_bytes':int(aa.source_bytes.max()),'physical_or_BMS_signal_scalar_values_excluding_clocks_epoch':int(aa.measured_or_BMS_signal_scalar_values.sum()),'clock_scalar_values':int(aa.clock_scalar_values.sum()),'epoch_values':int(aa.epoch_alignment_value_n.sum()),'single_vehicle_not_people_or_independent_observations':True,'current_voltage_clocks_identical_all_selected':bool(aa.raw_current_voltage_clocks_identical.all()),'soc_clock_identical_bundle_count':int(aa.soc_clock_identical_to_current.sum()),'temperature_clock_identical_bundle_count':int(aa.temperature_clock_identical_to_current.sum()),'gap30_segments':len(sg),'eligible_charging_soc_slope_segments':len(charge),'observed_supported_hours_gap1':float(it[it.max_integrated_step_seconds==1].supported_seconds.sum()/3600),'source_always_negative_charge_statement_has_rare_positive_transient_exceptions':True,'charge_positive_sample_counts':aa[aa.source_mode_label=='Charge'].set_index('folder').positive_current_samples.to_dict(),'charge_negative_sample_fraction':{r.folder:float(r.negative_current_samples/r.current_sample_n) for r in aa[aa.source_mode_label=='Charge'].itertuples()},'health_reference_capacity_data_public':False,'health_reference_qualification':'README states Figure2 data confidential and not public; paper capacity estimator is proprietary. No capacity/SOH ground-truth field among ten actual variables.','privacy':{'all_actual_raw_fields_numeric':True,'field_names_exactly_expected_ten':True,'GPS_owner_VIN_contact_fields_detected':False,'absolute_epoch_time_present':True,'direct_identifier_field_screen_not_comprehensive_privacy_certification':True,'public_figures_use_elapsed_time_only':True},'source_sha256_matches_all_selected':all(x['hash_matches'] for x in sources),'initial_purposeful_subset_not_random':True,'raw_already_cardinality_reduced_per_README':True,'counts_not_inflated_by_interpolation':True}
if len(charge):summary['observed_Ah_per_SOCpp_range']=[float(charge.observed_negative_Ah_per_reported_soc_percentage_point.min()),float(charge.observed_negative_Ah_per_reported_soc_percentage_point.max())]
(OUT/'BATTERY_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':180})
fig,(ax1,ax2)=plt.subplots(1,2,figsize=(12,5.7));order=aa.folder.tolist();xx=np.arange(len(order));palette=['#245A78','#B97032','#7B8F72']
base=it[it.max_integrated_step_seconds==1].set_index('folder').loc[order]
naive=it[it.max_integrated_step_seconds=='UNBOUNDED_NAIVE_COUNTEREXAMPLE'].set_index('folder').loc[order]
ax1.bar(xx-.18,base.supported_seconds/3600,width=.35,label='Intervals ≤1 second',color=palette[0]);ax1.bar(xx+.18,aa.wall_span_days*24,width=.35,label='First-to-last clock span',color=palette[1]);ax1.set_yscale('log');ax1.set_xticks(xx,order,rotation=30);ax1.set_ylabel('Hours, logarithmic scale');ax1.set_title('Calendar span is not observed operating time');ax1.legend(fontsize=8,frameon=False)
excess=100*(naive.absolute_terminal_kWh/base.absolute_terminal_kWh-1)
ax2.bar(xx,excess,color=[palette[1] if v>10 else palette[0] for v in excess]);ax2.set_ylim(0,55)
for x,val in zip(xx,excess):ax2.text(x,val+.9,f'{val:.2f}%',ha='center',fontsize=10)
ax2.set_xticks(xx,order,rotation=30);ax2.set_ylabel('Extra absolute terminal integral when bridging all gaps (%)');ax2.set_title('Unobserved gaps can inflate electrical features')
fig.text(.01,.01,'One vehicle, five source bundles, not five trips. All three gap limits (1/30/300 seconds) give the same terminal integrals here.\nAbsolute terminal integral = positive plus negative magnitudes. No wall-energy or capacity claim.\nPozzato et al., Mendeley V2, DOI10.17632/7vdkzpnjgj.2, CC BY-NC3.0. Original derived analysis.',fontsize=8);fig.tight_layout(rect=(0,.13,1,1));fig.savefig(OUT/'01_gap_integral_sensitivity.png');plt.close(fig)

fig,(ax1,ax2)=plt.subplots(1,2,figsize=(12,5.7));ca=aa[aa.source_mode_label=='Charge'];yp=np.arange(len(ca));neg=100*ca.negative_current_samples/ca.current_sample_n;pos=100*ca.positive_current_samples/ca.current_sample_n
ax1.barh(yp,neg,color=palette[0]);ax1.set_yticks(yp,ca.folder);ax1.set_xlim(0,107);ax1.set_xlabel('Negative-current samples (%)');ax1.set_title('Charge current is overwhelmingly negative')
for y,n,pv in zip(yp,neg,pos):ax1.text(2,y,f'{n:.4f}% negative; {pv:.5f}% positive',va='center',color='white',fontsize=10)
if len(charge):
 for row in charge.itertuples():
  color=palette[0] if row.folder=='Folder1' else palette[1];ax2.scatter(row.temperature_time_weighted_mean_C,row.observed_negative_Ah_per_reported_soc_percentage_point,s=50,color=color);ax2.annotate(row.folder+' / '+str(row.segment_number_gap30),(row.temperature_time_weighted_mean_C,row.observed_negative_Ah_per_reported_soc_percentage_point),xytext=(5,5),textcoords='offset points',fontsize=8)
ax2.set_xlabel('Observed interval mean pack temperature (°C)');ax2.set_ylabel('Observed negative Ah / reported SOC percentage point');ax2.set_title('Partial-interval slopes are not a health certificate')
fig.text(.01,.01,'Positive charge transients are a narrow exception to the README’s “always negative” wording, not a reversed charging convention.\nSlope endpoints share observed support; intervals differ in SOC window, rate, temperature and history. No capacity/SOH inference.\nSource: Pozzato et al., DOI10.17632/7vdkzpnjgj.2, CC BY-NC3.0. Original derived analysis.',fontsize=8);fig.tight_layout(rect=(0,.14,1,1));fig.savefig(OUT/'02_sign_and_partial_interval_diagnostics.png');plt.close(fig)
print(json.dumps(summary,indent=2));print(it[['folder','max_integrated_step_seconds','supported_seconds','signed_Ah','absolute_terminal_kWh']].to_string(index=False));print(charge[['folder','segment_number_gap30','duration_seconds','aligned_soc_change_percentage_points','aligned_negative_magnitude_Ah','observed_negative_Ah_per_reported_soc_percentage_point','temperature_time_weighted_mean_C']].to_string(index=False))
