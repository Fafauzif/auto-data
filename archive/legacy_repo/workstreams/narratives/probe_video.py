import sys,json,urllib.robotparser
from pathlib import Path
sys.path.insert(0,'/workspace/scratch/70444ed5f561/auto2000_run/shared')
from public_http import fetch
base=Path(__file__).parent; out=[]
r=fetch('https://www.youtube.com/robots.txt',source='narratives_transcript_probe')
out.append({'url':'https://www.youtube.com/robots.txt','status':r.status,'request_id':r.request_id,'error':r.error})
rp=urllib.robotparser.RobotFileParser();rp.parse(r.text.splitlines())
url='https://www.youtube.com/watch?v=0JbuBPDEKAA'
allowed=r.status==200 and rp.can_fetch('*',url)
if allowed:
 v=fetch(url,source='narratives_transcript_probe',max_bytes=5000000)
 out.append({'url':url,'status':v.status,'request_id':v.request_id,'error':v.error,'robots_allowed':allowed,'caption_tracks_marker': 'captionTracks' in v.text,'body_bytes':len(v.content)})
else:out.append({'url':url,'status':'not_requested','robots_allowed':allowed})
(base/'video_probe.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
