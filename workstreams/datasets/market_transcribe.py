from acquire import OUT,CACHE
import csv,json,hashlib,pandas as pd
# Values transcribed from actual downloaded official GAIKINDO graphics, visually checked.
source2025='https://www.gaikindo.or.id/overview-of-indonesias-automotive-whole-sales-january-december-2025/'
category={'4x2':466978,'LCGC':122686,'pickup':107008,'truck':56754,'double_cabin':22384,'4x4':19252,'bus':4541,'sedan':4084}
assert sum(category.values())==803687
pd.DataFrame([{'year':2025,'category':k,'units':v,'share':v/803687,'source_url':source2025,'method':'manual transcription and visual verification from downloaded official infographic','input_sha256':hashlib.sha256((CACHE/'gaikindo_2025_overview.avif').read_bytes()).hexdigest()} for k,v in category.items()]).to_csv(OUT/'gaikindo_2025_category_derived.csv',index=False)
cats=['sedan','4x2','4x4','bus','pickup','truck','double_cabin','LCGC']
months=[
[243,38472,1285,297,8932,4966,1609,10694],
[303,46422,1601,321,14500,5137,1551,11412],
[210,37942,1589,235,7947,5042,1581,6725],
[307,47098,1971,278,13337,6737,2057,8992],
[352,40923,1327,428,9965,6068,2024,8232],
[252,45581,1090,409,11323,7984,1419,9451],
[339,46098,1005,421,11843,10031,2373,9127],
[217,46976,1413,274,11347,9528,2374,9675],
[265,45072,1404,338,11119,9695,1958,9689]]
url='https://www.gaikindo.or.id/wp-content/uploads/2026/10/wstrendsep26.avif';sha=hashlib.sha256((CACHE/'gaikindo_wholesale_trend_sep2026.avif').read_bytes()).hexdigest()
long=[]
for m,values in enumerate(months,1):
 for cat,val in zip(cats,values):long.append({'year':2026,'month':m,'category':cat,'units':val,'source_url':url,'method':'manual transcription and visual verification from downloaded official infographic','input_sha256':sha})
x=pd.DataFrame(long);x.to_csv(OUT/'gaikindo_2026_monthly_category_derived.csv',index=False)
x.groupby(['year','month']).units.sum().reset_index(name='monthly_units').to_csv(OUT/'gaikindo_2026_monthly_totals_derived.csv',index=False)
url='https://www.gaikindo.or.id/indonesias-vehicle-retail-sales-january-december-2025/'
retail={'Toyota':258923,'Daihatsu':137855,'Honda':71233,'Mitsubishi Motors':70338,'Suzuki':64838,'BYD':44342,'Mitsubishi Fuso':25613,'Isuzu':25295,'Hino':20517,'Wuling':20607}
pd.DataFrame([{'year':2025,'brand':k,'retail_units':v,'source_url':url,'scope':'Selected brands stated in operator article; not complete market table'} for k,v in retail.items()]).to_csv(OUT/'gaikindo_2025_selected_brand_retail.csv',index=False)
url='https://www.gaikindo.or.id/innova-zenix-pimpin-penjualan-mobil-hybrid-nasional-tahun-2025/'
models=[('Toyota','Innova Zenix',23934),('Suzuki','Fronx',10458),('Suzuki','XL7',9759),('Honda','HR-V e:HEV',6040),('Toyota','Yaris Cross',3380),('Toyota','Alphard Hybrid',1901),('Suzuki','Grand Vitara',1821),('Hyundai','Santa Fe',1290),('Suzuki','Ertiga Hybrid',1168),('Hyundai','Palisade',1081)]
pd.DataFrame([{'year':2025,'brand':b,'model':m,'wholesale_units':v,'source_url':url,'scope':'Selected hybrid models in Detik article republished by GAIKINDO; includes mild hybrids'} for b,m,v in models]).to_csv(OUT/'gaikindo_2025_hybrid_selected_models.csv',index=False)
summary={'wholesale2025':803687,'category_total_check':sum(category.values()),'hybrid_total2025_source':65943,'Toyota_hybrid2025_source':30110,'Toyota_hybrid_share_computed':30110/65943,'Toyota_Zenix_share_of_Toyota_hybrid_computed':23934/30110,'Toyota_Zenix_share_of_total_hybrid_computed':23934/65943,'Toyota_selected_three_models_share_of_Toyota_hybrid':(23934+3380+1901)/30110,'market_hybrid_growth_computed_2024to2025':65943/59903-1,'first9months2026_total_computed_from_category_chart':int(x.units.sum()),'2026_monthly_cells_transcribed':len(x),'limits':['No powertrain decomposition from vehicle-category chart','Hybrid source includes mild hybrids; not necessarily homogeneous technology','2025 retail brand list incomplete; no total market denominator invented','2025 brand Toyota_hybrid30110 is source figure distinct from case33950 estimated electrified']}
(OUT/'market_analysis_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2));print(x.groupby('month').units.sum().to_string())
