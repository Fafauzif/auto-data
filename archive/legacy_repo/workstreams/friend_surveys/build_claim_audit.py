from pathlib import Path
import csv,json,hashlib
OUT=Path(__file__).resolve().parent; rows=[]
def add(id,study,edition,country,metric,value,unit,cohort,country_n,regional_n,locator,url,status='verified_primary',note=''):
 rows.append(dict(claim_id=id,study=study,edition=edition,country=country,metric=metric,value=value,unit=unit,question_cohort=cohort,country_question_n=country_n,regional_question_n=regional_n,source_locator=locator,source_url=url,verification_status=status,comparison_limit=note))
rak='https://insight.rakuten.com/how-to-win-the-ev-shift-in-2026/';sta='https://www.statista.com/statistics/1028942/indonesia-brand-awareness-of-electric-cars/'
add('RAK_SCOPE','Rakuten Electric Cars',2026,'SEA6','Survey total',27372,'respondents','Six-market publicblog sample',None,27372,'Publicblog10Sep2026',rak)
add('RAK_ID_META','Rakuten via Statista',2026,'Indonesia','Published survey metadata sample',6467,'respondents','Awareness chart reported base; exact screening/wording unavailable',6467,None,'Public index metadata,field23–30Jun2026',sta,'verified_metadata_only','Not primary questionnaire; directchart403/masked. Does not establish full targetpopulation or chartscreening.')
for id,metric,val in [('RAK_BYD','BYD awareness',57),('RAK_TOYOTA','Toyota awareness',28),('RAK_WULING','Wuling awareness',55),('RAK_HYUNDAI','Hyundai awareness',45)]:
 add(id,'Rakuten via supplied friendcontext',2026,'Indonesia',metric,val,'percent','Brand/model awareness as reported by usercontext; screeningunknown',None,None,'Usercontext citing Statista dossier slide37,not available',sta,'user_provided_not_independently_verified','Neither underlying dossier nor numeric primarychart available in thissession. Do not infer Auto2000awareness or causality.')
p24='https://www.pwc.com/id/en/publications/automotive/indonesia-electric-vehicle-readiness-consumer-insights-2024.pdf'
for id,metric,val in [('P24_CHARGE','Charging-duration barrier',60),('P24_RANGE','Limited-range barrier',59),('P24_BATTERY','Uncertain battery-life barrier',47),('P24_UPFRONT','Higher upfrontcost barrier',31)]:
 add(id,'PwC Indonesia eReadiness',2024,'Indonesia',metric,val,'percent','EV prospects,passengerBEV/PHEV',None,None,'PDFp23;methodp6',p24,note='Country subgroupN and fielddates not stated at observedchart. Not allrespondents or currentDigiroomusers.')
for id,metric,val in [('P24_PRICE','Price as purchase criterion',78),('P24_SAFETY','Safety as purchase criterion',54),('P24_BUYRANGE','Battery range as purchase criterion',52)]:
 add(id,'PwC Indonesia eReadiness',2024,'Indonesia',metric,val,'percent','EV prospects,passengerBEV/PHEV',None,None,'PDFp22;methodp6',p24,note='Question-specific criterion share,not causalchoiceweight.')
p25='https://www.pwc.com/id/en/publications/automotive/pwcid-ereadiness-2025-asean-report.pdf'
add('P25_SAMPLE','PwC ASEAN6 eReadiness',2025,'ASEAN6','Actual survey respondent base',3822,'respondents','CAWI private drivingpopulation,passengerBEV/PHEV',None,3822,'PDFp14;methodp2',p25,note='Roundedmethod says4000; detailedanalysis3822. Not3822Indonesians.')
add('P25_SWITCH','PwC ASEAN6 eReadiness',2025,'Indonesia','Considering return to ICE',33,'percent','EVowners responding to switchback question',None,408,'PDFp21',p25,note='CountryN unspecified;408isASEANquestionbase. Intention is notactualdefection.')
for id,metric,val in [('P25_COST','Higher maintenance cost than expected',71),('P25_DRIVE','Driving experience worse than expected',61),('P25_RANGE','Insufficient driving range',52),('P25_CHARGE','Charging experience worse than expected',42)]:
 add(id,'PwC ASEAN6 eReadiness',2025,'Indonesia',metric,val,'percent','EVowners who wouldconsiderreturntoICE',None,158,'PDFp22,visuallychecked',p25,note='Conditionalreasonamongreverters;158isASEANbase,notIndonesiaN. Not71%ofallEVowners.')
for id,metric,val in [('P25_SCEPTIC_RANGE','Limited range',55),('P25_SCEPTIC_BATTERY','Uncertain battery life',53),('P25_SCEPTIC_CHARGE','Recharging time',42)]:
 add(id,'PwC ASEAN6 eReadiness',2025,'Indonesia',metric,val,'percent','EVsceptics,do notplanBEV/PHEVwithin5years',None,510,'PDFp46;cohortp44',p25,note='Notprospects,allowners orDeloitteallquestionrespondents.')
add('P25_TIME','PwC ASEAN6 eReadiness',2025,'Indonesia','Mean acceptablechargingtime',41.1,'minutes','EVprospects',None,2904,'PDFp43,visuallychecked',p25,note='Stated acceptabletime,notactualchargingduration,SLA orpublicchargingconcernpercentage.')
add('P25_CHINA_TIME','PwC global eReadiness',2025,'China','Acceptablechargingtime in narrative',36,'minutes','Narrativeconsumerstatement;exactcountrychartbaseunavailable',None,None,'Globalprimarysummary', 'https://www.pwc.com/gx/en/1/issues/reinvention/e-readiness-survey/2025.html',note='Do notequate toIndonesiaDeloitte46%concern: differentmetric/unit/cohort. NoChina-to-Indonesia transferassumption.')
d25='https://www.deloitte.com/content/dam/assets-zone1/southeast-asia/en/docs/industries/consumer/2025/sea-cb-2025-sea-automotive-consumer-study.pdf'
add('D25_SAMPLE','Deloitte Global Automotive Consumer Study',2025,'Indonesia','Overallcountry sample',1004,'respondents','Driving-age onlinepanel respondents',1004,6029,'PDFp4',d25,note='Edition2025,fielded2024;do notuse1004asbaseforeverychart.')
for id,metric,val in [('D25_HOME','Expected primaryhomecharging',62),('D25_PUBLIC','Expected primaryonstreet/publiccharging',29)]:
 add(id,'Deloitte Global Automotive Consumer Study',2025,'Indonesia',metric,val,'percent','BEV/PHEVintenders,Q43',178,None,'PDFp9,Q43',d25,note='Distinct from all1004respondents;intention notobservedusage.')
add('D25_FUEL','Deloitte Global Automotive Consumer Study',2025,'Indonesia','Lowerfuelcost asreasonforEV',61,'percent','Electrifiednextvehicleintenders,Q42',273,None,'PDFp8,Q42',d25,note='Multiselect;BEV/PHEV/HEVbasisdiffersfromchargingquestion.')
d26='https://www.deloitte.com/content/dam/assets-zone1/southeast-asia/en/docs/industries/consumer/2026/sea-cb-2026-sea-automotive-consumer-study.pdf'
for id,metric,val in [('D26_ICE','NextpreferredICE',55),('D26_HEV','NextpreferredHEV',16),('D26_PHEV','NextpreferredPHEV',15),('D26_BEV','NextpreferredBEV',11)]:
 add(id,'Deloitte Global Automotive Consumer Study',2026,'Indonesia',metric,val,'percent','Q41eligibleIndonesianrespondents',863,None,'PDFp9,Q41,parentactualfile',d26,note='Preferrednextpowertrain,not5yeargeneralpurchaseintention orforecastactualsales.')
for id,metric,val in [('D26_BATTERY','Batteryreplacementcostconcern',39),('D26_RESALE','Futureresalevalueconcern',38),('D26_CHARGE','Chargingtimeconcern',46)]:
 add(id,'Deloitte Global Automotive Consumer Study',2026,'Indonesia',metric,val,'percent','BEVconcerns,Q48eligibleIndonesianrespondents',863,None,'PDFp13,Q48,parentactualfile',d26,note='Multiselect concerns,not measuredbarrierimpact orsamecohortasPwCsceptics.')
add('D26_HOME','Deloitte Global Automotive Consumer Study',2026,'Indonesia','Expectedprimaryhomecharging',61,'percent','BEV/PHEVintenders,Q43',223,None,'PDFp10,Q43,parentactualfile',d26,note='Not61%ofallIndonesians.')
add('D26_DEDICATED','Deloitte Global Automotive Consumer Study',2026,'Indonesia','Dedicatedresidentialchargeraccess',54,'percent','Subsetexpectinghomecharging,Q44',136,None,'PDFp10,Q44,parentactualfile',d26,note='Conditionaldenominator;not54%ofallEVintenders.')
pop='https://www.mobil123.com/berita/13-tantangan-punya-mobil-dan-motor-listrik-di-indonesia-menurut-pemilik-137158/137158'
for id,metric,val in [('POP_BATTERY','Worryaboutbatteryremaining',65),('POP_RANGE','Limitedrange',61),('POP_WORKSHOP','Workshoprepairacceptance',49),('POP_INFRA','Chargingfacilitylimitations',43),('POP_LOCATION','Few/distantchargingstations',42),('POP_WAIT','Longerservicewaiting',23)]:
 add(id,'Populix EV Dynamics reportedbyMobil123',2024,'Indonesia selectedlocations',metric,val,'percent','MixedEVusersinclcar/motorcycle/e-bike;car-onlybaseunavailable',None,350,'Field15–25Mar2024;secondarypublication7Jun2024',pop,'secondary_report_primary_table_unavailable','Mediauniverseconflict:Jakartavs5metroregions. Agesalsoinconsistentacrossreports. NoToyota-specificorcar-onlyinference.')
(OUT/'survey_claims.json').write_text(json.dumps(rows,indent=2))
with (OUT/'survey_claims.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
print('records',len(rows),'statuscounts',__import__('collections').Counter(r['verification_status'] for r in rows))
