from pathlib import Path
import pandas as pd,numpy as np,json,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import geopandas as gpd
ROOT=Path(__file__).resolve().parents[1]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#fbfaf6','axes.facecolor':'#fbfaf6','savefig.facecolor':'#fbfaf6'})
s=pd.read_csv(ROOT/'sources/archive_inputs/raw_licensed_data/SPKLU_CC_BY_NC_3_0/data/spklu_stations.csv')
c=pd.read_csv(ROOT/'sources/archive_inputs/raw_licensed_data/SPKLU_CC_BY_NC_3_0/data/spklu_chargers.csv')
b=pd.read_csv(ROOT/'sources/archive_inputs/workstreams/datasets/bps_vehicle_stock_long.csv')
world=gpd.read_file(ROOT/'sources/natural_earth_countries.geojson')
fig,ax=plt.subplots(figsize=(12,5))
world.plot(ax=ax,color='#e0e4df',edgecolor='#c4ccc5',linewidth=.4)
ax.scatter(s.longitude,s.latitude,s=5,alpha=.4,c='#236a75',rasterized=True)
a=s[s.location_name.str.contains('auto.?2000',case=False,regex=True)]
ax.scatter(a.longitude,a.latitude,s=34,facecolor='#d64a34',edgecolor='white',linewidth=.7,label=f'Auto2000-name subset ({len(a)})')
ax.set(xlim=(94,142),ylim=(-12,8),xlabel='Longitude (degrees east)',ylabel='Latitude (degrees north)');ax.legend(loc='lower left',frameon=False);ax.set_title('Charging geography is national; the Auto2000-name subset is not the branch network',loc='left',fontsize=13,pad=12)
fig.tight_layout();fig.savefig(ROOT/'figures/national_charging.png',dpi=180);plt.close(fig)
g=s.groupby('province_name').size().sort_values(ascending=False)
fig,ax=plt.subplots(figsize=(10,5));g.head(15).sort_values().plot.barh(ax=ax,color='#236a75');ax.set(xlabel='Consolidated source station records',ylabel='');ax.set_title('The archived charging inventory is concentrated in a few provinces',loc='left',fontsize=13);fig.tight_layout();fig.savefig(ROOT/'figures/province_charging.png',dpi=180);plt.close(fig)
g.rename('station_records').to_csv(ROOT/'analysis/province_station_counts.csv')
old=pd.read_csv(ROOT/'sources/archive_inputs/workstreams/extension_geography/nearest_scenario_summary.csv');old.to_csv(ROOT/'analysis/archive_nearest_scenarios.csv',index=False)
summary={'station_records':len(s),'charger_box_records':len(c),'auto2000_name_anchors':len(a),'snapshot':'2026-06-16','not_live_uptime':True,'units_note':'Stations and hardware rows are different units; no Toyota-owner demand denominator.'}
(ROOT/'analysis/archive_context_summary.json').write_text(json.dumps(summary,indent=2))
print(summary)
