from pathlib import Path
import csv,json
out=Path(__file__).resolve().parent
fields=['programme_id','ecosystem','model_scope','coverage_kind','years','odometer_km','limit_rule','annual_km_limit','owner_transfer_condition','use_condition','maintenance_condition','price_idr','tax_basis','offer_date_or_cohort','source_id','evidence_ids','comparison_limit']
rows=[
['PRG01','Toyota','eligible models excluding named models','scheduled_labor_and_parts',3,60000,'first reached; up to seven services',None,'unknown','model exclusions','programme conditions',None,None,'purchases from July 2022','T02','COMP-003','service entitlement is not warranty'],
['PRG02','Toyota','eligible post-TCare vehicles','conditional_warranty_extension_maximum',2,40000,'first reached',None,'unknown','GBSB excluded','regular authorized scheduled service',None,None,'current page; undated','T02','COMP-004','extension maximum; not total vehicle cover'],
['PRG03','BYD','Dolphin/Atto3/Seal','vehicle',6,150000,'first reached',None,'unknown','full manual governs','authorized service/current manual',None,None,'2024-02-20 announcement','B03','COMP-026','historical named-model promise'],
['PRG04','BYD','Dolphin/Atto3/Seal','traction_battery',8,160000,'first reached; SoH condition at least70%',None,'unknown','full manual governs','authorized service/current manual',None,None,'2024-02-20 announcement','B03','COMP-026','historical named-model promise'],
['PRG05','BYD','Dolphin/Atto3/Seal','drive_unit',8,150000,'first reached',None,'unknown','full manual governs','authorized service/current manual',None,None,'2024-02-20 announcement','B03','COMP-026','component scope differs from battery'],
['PRG06','Hyundai','all except IONIQ5/IONIQ6','vehicle',4,100000,'first reached',None,'unknown','normal use; exclusions apply','authorized dealer/mobile scheduled servicing',None,None,'retail from2025-09-01 or vehicle booklet','H01','COMP-043','vehicle model exception must be preserved'],
['PRG07','Hyundai','IONIQ5/IONIQ6','vehicle',3,100000,'first reached',None,'unknown','normal use; exclusions apply','authorized dealer/mobile scheduled servicing',None,None,'retail from2025-09-01 or vehicle booklet','H01','COMP-043','do not replace with general4year headline'],
['PRG08','Hyundai','electric/hybrid high voltage battery','high_voltage_battery',8,160000,'first reached',None,'unknown','normal use; exclusions apply','authorized dealer/mobile scheduled servicing',None,None,'retail from2025-09-01 or vehicle booklet','H01','COMP-027','not same as general vehicle warranty'],
['PRG09','Hyundai','IONIQ5','paid_warranty_and_RSA_extension',1,15000,'first reached',None,'unknown','full package eligibility applies','vehicle booklet/package conditions',9030000,'before tax','current page; undated','H01','COMP-028','price is retail package; not dealer cost'],
['PRG10','Wuling','BinguoEV410km prebook cohort','lifetime_core_EV_components',None,None,'lifetime claim subject to eligibility',30000,'first private owner; excludes transfer','not operational/commercial','official service and original parts',None,None,'2023-11-17; first1000prebookers','W02','COMP-034','historical campaign not current universal benefit'],
['PRG11','Chery','OMODAE5 early-buyer cohort','lifetime_battery_campaign',None,None,'lifetime claim subject to eligibility',30000,'first4000buyer cohort; transfer detail unverified','normal private use; commercial excluded','full campaign terms govern',None,None,'2024-07-26','C01','COMP-036','index-only historical terms; direct source access failed'],
['PRG12','Chery','E5 June2025 launch','traction_battery',8,180000,'first reached',None,'unknown','full model/campaign terms govern','full model/campaign terms govern',None,None,'2025-06-25','C02','COMP-037','index-only dated source; not all2026vehicles'],
]
records=[dict(zip(fields,r)) for r in rows]
with (out/'normalized_programmes.csv').open('w',newline='',encoding='utf8') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(records)
(out/'normalized_programmes.json').write_text(json.dumps(records,indent=2))
print('normalized rows',len(records),'derived from existing source records; not additional independent observations')
