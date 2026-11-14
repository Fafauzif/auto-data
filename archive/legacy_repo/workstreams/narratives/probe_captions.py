import sys,json,re,urllib.robotparser,urllib.parse
from pathlib import Path
sys.path.insert(0,'/workspace/scratch/70444ed5f561/auto2000_run/shared')
from public_http import fetch
p=Path(__file__).parent
robots=fetch('https://www.youtube.com/robots.txt',source='narratives_transcript_probe')
rp=urllib.robotparser.RobotFileParser();rp.parse(robots.text.splitlines())
r=fetch('https://www.youtube.com/watch?v=0JbuBPDEKAA',source='narratives_transcript_probe')
out=[]
m=re.search(r'"captionTracks"\s*:\s*(\[)',r.text)
if m:
 tracks,_=json.JSONDecoder().raw_decode(r.text[m.start(1):])
 for track in tracks:
  url=track.get('baseUrl','');allowed=rp.can_fetch('*',url)
  record={'language':track.get('languageCode'),'kind':track.get('kind'),'caption_endpoint_path':urllib.parse.urlsplit(url).path,'robots_allowed':allowed,'watch_request_id':r.request_id}
  if allowed:
   cap=fetch(url,source='narratives_transcript_probe')
   record.update(status=cap.status,bytes=len(cap.content),request_id=cap.request_id,error=cap.error)
   if cap.status==200 and cap.content:
    private=Path('/workspace/scratch/70444ed5f561/auto2000_run/private_cache')/'youtube_0JbuBPDEKAA_captions.xml';private.write_bytes(cap.content)
    record['caption_text_private_capture']=True
  else:record['status']='not_requested_disallowed'
  out.append(record)
else:out.append({'caption_tracks_found':False})
(p/'caption_probe.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
