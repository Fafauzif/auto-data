from pathlib import Path
import pandas as pd,json
R=Path(__file__).resolve().parent;B=R.parents[1]/'extracted/baseline/Auto2000_Geographic_Study'
p=pd.read_csv(B/'workstreams/providers/provider_inventory.csv');a=pd.read_csv(B/'workstreams/routing/output/origin_accessibility.csv');a=a[a.scenario=='snap_le_250m']
od=pd.read_csv(B/'workstreams/routing/output/od_pairs.csv');od=od[(od.origin_snap_metres<=250)&(od.destination_snap_metres<=250)&od.duration_seconds.notna()]
flagged={
'79721181-b04a-4ee7-98f5-6aed57ce44f9':('housing estate','https://sikumbang.tapera.go.id/lokasi-perumahan/PLG1010042021T005','Housingestate name/area and TaqwaMataMerah address; published government registry'),
'028b7203-ab24-48cf-a2ea-3be6aab87a06':('railway locomotive depot','https://railcertification.kai.id/tuk.php','KAI UnitPelaksanaTeknis DepoLokomotifBesarAKertapati JlDipoLorongAmal; search retrieval; directpage502'),
'44a5fd69-cf49-47a1-ba9d-bdce17a00a84':('electric motorcycle centre','https://www.alvaauto.com/blog/pakai-motor-listrik-alva-cervo-di-surabaya-gak-takut-kemalingan/','OfficialALVA article matches KertajayaIndah59 address; motorcycle centre notToyota oilservice')}
rows=[]
for _,z in a.iterrows():
 id=str(z.independent_destination_id).replace('independent:','');x=p[p.id==id]
 if x.empty:continue
 x=x.iloc[0];rows.append({'market':z.market,'origin_id':z.origin_id,'generic_winner_id':id,'name':x['name'],'category':x.primary_category,'source_confidence':x.confidence,'public_audit_type':flagged[id][0] if id in flagged else 'not task-verified in this audit','source_url':flagged[id][1] if id in flagged else '', 'source_locator':flagged[id][2] if id in flagged else '', 'remove_in_confirmed_noncar_sensitivity':id in flagged})
d=pd.DataFrame(rows);d.to_csv(R/'generic_minimum_origin_audit.csv',index=False)
new=[]
for market,g in a.groupby('market'):
 sub=od[(od.market==market)&(od.kind=='independent')];clean=sub[~sub.destination_id.isin(['independent:'+id for id in flagged])];times=clean.groupby('origin_id').duration_seconds.min();orig=g.set_index('origin_id');gap=(orig.auto2000_nearest_seconds-times)/60
 new.append({'market':market,'paired_n':int(gap.notna().sum()),'baseline_median_gap_minutes':g.auto2000_minus_mapped_independent_seconds.median()/60,'excluding_3_publicly_noncar_median_gap_minutes':gap.median(),'origins_with_flagged_generic_winner':int(((d.market==market)&d.remove_in_confirmed_noncar_sensitivity).sum()),'scope':'Targeted confirmed-noncar sensitivity, remainingpool notverifiedjob providers; not population/errorprevalence'})
pd.DataFrame(new).to_csv(R/'generic_confirmed_noncar_sensitivity.csv',index=False);print(pd.DataFrame(new).to_string(index=False))
