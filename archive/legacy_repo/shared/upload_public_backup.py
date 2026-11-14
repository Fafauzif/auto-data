"""User-authorized anonymous backup of the public-safe core and MAT volumes.
Never uploads the IGAR original-text files or their private-delivery volume.
No accounts, credentials, source-rule bypass, or automatic upload retries.
"""
from pathlib import Path
import json,subprocess,hashlib,datetime,secrets,urllib.parse
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT.parent
LOG=ROOT/'private_cache/backup_uploads';LOG.mkdir(parents=True,exist_ok=True)
RECEIPT=BASE/'Auto2000_Backup_Receipt.json'
files=[BASE/'Auto2000_Public_Backup_Core.zip']+[BASE/'backup_volumes'/f'Auto2000_Telemetry_Volume_{n:02d}.zip' for n in range(1,6)]
assert all(p.is_file() for p in files)
assert all(p.stat().st_size<95000000 for p in files),'Conservative host-size ceiling'
assert not any('IGAR' in p.name for p in files)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
expected={p.name:{'bytes':p.stat().st_size,'sha256':digest(p)} for p in files}
receipt={'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'authorization':'User requested Filebin and alternative backup hosts. Public-safe variant only.','primary_full_zip_is_separate':True,'omitted_from_anonymous_backup':['IGAR_CC_BY_4_0/Rating_labeled.csv','IGAR_CC_BY_4_0/VADER_labeled.csv'],'layout':'Core plus five whole-MAT ZIP volumes; extract into the same directory. No binary concatenation.','attempts':[],'files':[],'complete_verified_public_backup':False}
def persist():RECEIPT.write_text(json.dumps(receipt,indent=2))
def request(args,tag,max_seconds=240):
 body=LOG/(tag+'.body');headers=LOG/(tag+'.headers')
 cmd=['curl','-sS','-L','--max-time',str(max_seconds),'-D',str(headers),'-o',str(body),'-w','%{http_code}',*args]
 p=subprocess.run(cmd,capture_output=True,timeout=max_seconds+15);code=int(p.stdout.decode().strip() or 0) if p.stdout.decode().strip().isdigit() else 0
 return code,body,p.returncode
def record_attempt(host,file,code,returncode,extra=None):
 row={'host':host,'file':file,'http_status':code,'curl_exit_code':returncode,'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 if extra:row.update(extra)
 receipt['attempts'].append(row);persist();print(json.dumps(row),flush=True)
def download_verify(url,file,tag):
 code,body,rc=request(['--max-filesize',str(expected[file.name]['bytes']+65536),url],tag,max_seconds=300)
 return {'download_http_status':code,'download_bytes':body.stat().st_size if body.exists() else 0,'download_sha256':digest(body) if body.exists() else '', 'verified':bool(code==200 and rc==0 and body.exists() and body.stat().st_size==expected[file.name]['bytes'] and digest(body)==expected[file.name]['sha256'])}

# Filebin is tried once initially. If its service refuses the core, do not send
# five further uploads to the same unavailable service.
bin_id='auto2000-'+secrets.token_hex(10);filebin_url='https://filebin.net/'+bin_id
p=files[0];code,body,rc=request(['-X','POST','-H','Accept: application/json','-H','Content-Type: application/octet-stream','-H','Content-SHA256: '+expected[p.name]['sha256'],'--data-binary','@'+str(p),filebin_url+'/'+p.name],'filebin_core')
server={}
try:server=json.loads(body.read_text())
except Exception:pass
record_attempt('Filebin',p.name,code,rc,{'reason':'Storage limit reached' if code==507 else 'See private raw response; no success inferred from reachability'})
if code==201 and server.get('file',{}).get('sha256')==expected[p.name]['sha256']:
 result={'file':p.name,**expected[p.name],'host':'Filebin','url':filebin_url+'/'+p.name,'verified':True,'verification':'Server201 metadata matched client SHA256 supplied in upload header','expires_at':server.get('bin',{}).get('expired_at')};receipt['files'].append(result);persist()
 for p in files[1:]:
  code,body,rc=request(['-X','POST','-H','Accept: application/json','-H','Content-Type: application/octet-stream','-H','Content-SHA256: '+expected[p.name]['sha256'],'--data-binary','@'+str(p),filebin_url+'/'+p.name],'filebin_'+p.stem)
  try:s=json.loads(body.read_text())
  except Exception:s={}
  ok=code==201 and s.get('file',{}).get('sha256')==expected[p.name]['sha256'];record_attempt('Filebin',p.name,code,rc,{'verified_server_checksum':ok})
  if not ok:break
  receipt['files'].append({'file':p.name,**expected[p.name],'host':'Filebin','url':filebin_url+'/'+p.name,'verified':True,'verification':'Server201 SHA256 metadata match','expires_at':s.get('bin',{}).get('expired_at')});persist()
 if len(receipt['files'])==6:receipt['complete_verified_public_backup']=True;receipt['bin_url']=filebin_url

if not receipt['complete_verified_public_backup']:
 # Operator API documents anonymous uploads, <100MB, and optional 48h expiry.
 # Downloaded bytes, not an upload page alone, establish usable backup here.
 verified=[]
 for p in files:
  print('Uploading TmpFiles: '+p.name,flush=True)
  code,body,rc=request(['-F','file=@'+str(p),'-F','expire=172800','https://tmpfiles.org/api/v1/upload'],'tmp_'+p.stem,max_seconds=300)
  try:s=json.loads(body.read_text())
  except Exception:s={}
  url=s.get('data',{}).get('url','');parsed=urllib.parse.urlsplit(url)
  record_attempt('TmpFiles',p.name,code,rc,{'upload_response_success':s.get('status')=='success','requested_retention_seconds':172800})
  if code not in (200,201) or s.get('status')!='success' or parsed.hostname not in ('tmpfiles.org','www.tmpfiles.org'):break
  page_url=urllib.parse.urlunsplit(('https','tmpfiles.org',parsed.path,'',''));direct='https://tmpfiles.org/dl'+parsed.path
  check=download_verify(direct,p,'tmp_verify_'+p.stem);row={'file':p.name,**expected[p.name],'host':'TmpFiles','url':page_url,'download_url':direct,'retention_seconds_requested':172800,'expiry_confirmed_by_response':False,**check};receipt['files'].append(row);persist();print(json.dumps({'file':p.name,'host':'TmpFiles','verified':check['verified']}),flush=True)
  if not check['verified']:break
  verified.append(row)
 if len(verified)==6:receipt['complete_verified_public_backup']=True;receipt['preferred_host']='TmpFiles'

if not receipt['complete_verified_public_backup']:
 # The separately verified official Catbox API permits anonymous uploads by
 # omitting userhash. Stop if the actual POST is refused; no proxy or bypass.
 verified=[]
 for p in files:
  print('Uploading Catbox: '+p.name,flush=True)
  code,body,rc=request(['-F','reqtype=fileupload','-F','fileToUpload=@'+str(p),'https://catbox.moe/user/api.php'],'cat_'+p.stem,max_seconds=300)
  url=body.read_text(errors='replace').strip() if body.exists() else '';parsed=urllib.parse.urlsplit(url)
  record_attempt('Catbox',p.name,code,rc)
  if code!=200 or parsed.scheme!='https' or parsed.hostname!='files.catbox.moe':break
  check=download_verify(url,p,'cat_verify_'+p.stem);row={'file':p.name,**expected[p.name],'host':'Catbox','url':url,**check,'expiry_confirmed_by_response':False};receipt['files'].append(row);persist();print(json.dumps({'file':p.name,'host':'Catbox','verified':check['verified']}),flush=True)
  if not check['verified']:break
  verified.append(row)
 if len(verified)==6:receipt['complete_verified_public_backup']=True;receipt['preferred_host']='Catbox'
receipt['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();persist()
print(json.dumps({'complete_verified_public_backup':receipt['complete_verified_public_backup'],'verified_objects':sum(x.get('verified',False) for x in receipt['files']),'receipt':str(RECEIPT)}),flush=True)
