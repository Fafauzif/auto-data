"""Create meaningful public-host data volumes without truncating MAT files."""
from pathlib import Path
import zipfile,json,hashlib
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT.parent/'backup_volumes';OUT.mkdir(exist_ok=True)
raws=sorted((ROOT/'raw_licensed_data').rglob('*.mat'))
assert len(raws)==5,'Expected the explicitly selected five source bundles'
records=[]
for n,p in enumerate(raws,1):
 rel=p.relative_to(ROOT);file=OUT/f'Auto2000_Telemetry_Volume_{n:02d}.zip'
 note=f'''# Auxiliary EV telemetry volume {n}\n\nExtract this ZIP and Auto2000_Public_Backup_Core.zip into the same directory. Their common Auto2000_Research_Project folder restores the public evidence package. Each telemetry volume contains one complete source MAT bundle; it is not a fragment requiring binary concatenation.\n\nIncluded source path: {rel}\n\nSource: Allam, A., Pulvirenti, L., Pozzato, G., Herson, K., Negoita, A., Paxton, W., and Onori, S. (2023), Real-world electric vehicle data: driving and charging, Mendeley Data V2, https://doi.org/10.17632/7vdkzpnjgj.2. License: CC BY-NC 3.0, https://creativecommons.org/licenses/by-nc/3.0/. Original source bytes are preserved. Noncommercial qualification and attribution apply; no blanket license is assigned to the rest of the project.\n\nOne Audi e-tron in California, purposeful subset of published folder windows. Arrays are asynchronous and source-processed; stored scalar values are not independent customer observations. This source cannot validate a Toyota health certificate or a hidden capacity reference. See the core report and extension_battery source/analysis manifests.\n\nThe public backup excludes the original two IGAR review-text CSVs. The primary full ZIP contains them. This volume does not restore those withheld text files.\n'''
 with zipfile.ZipFile(file,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  z.write(p,'Auto2000_Research_Project/'+str(rel));z.writestr(f'Auto2000_Research_Project/TELEMETRY_VOLUME_{n:02d}_README.md',note)
 with zipfile.ZipFile(file) as z:assert z.testzip() is None
 assert file.stat().st_size<98000000,'Must fit both decimal100MB and binary100MiB documented limits'
 records.append({'file':file.name,'local_path':str(file),'bytes':file.stat().st_size,'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'restores_path':str(rel),'source_bytes':p.stat().st_size,'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source_doi':'10.17632/7vdkzpnjgj.2','license':'CC BY-NC 3.0'})
(OUT/'TELEMETRY_VOLUME_MANIFEST.json').write_text(json.dumps(records,indent=2))
print(json.dumps(records))
