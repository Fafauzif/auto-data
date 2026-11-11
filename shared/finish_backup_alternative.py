"""Upload only missing public backup objects to an allowed alternative host."""
from pathlib import Path
import datetime, hashlib, json, subprocess, urllib.parse

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT.parent
LOG = ROOT / 'private_cache/backup_uploads'
RECEIPT = BASE / 'Auto2000_Backup_Receipt.json'
receipt = json.loads(RECEIPT.read_text())
files = [BASE / 'Auto2000_Public_Backup_Core.zip'] + [BASE / 'backup_volumes' / f'Auto2000_Telemetry_Volume_{n:02d}.zip' for n in range(1, 6)]
done = {x['file'] for x in receipt['files'] if x.get('verified')}

def persist():
    RECEIPT.write_text(json.dumps(receipt, indent=2))

def request(args, tag):
    body = LOG / (tag + '.body')
    result = subprocess.run(['curl', '-sS', '-L', '--max-time', '240', '-D', str(LOG / (tag + '.headers')), '-o', str(body), '-w', '%{http_code}', *args], capture_output=True, timeout=255)
    return int(result.stdout.decode().strip() or 0), body, result.returncode

for p in files:
    if p.name in done:
        continue
    assert p.is_file() and p.stat().st_size < 95000000 and 'IGAR' not in p.name
    sha = hashlib.sha256(p.read_bytes()).hexdigest()
    for host in ['TmpFiles', 'Catbox']:
        if any(x['host'] == host and x['file'] == p.name for x in receipt['attempts']):
            continue
        args = ['-F', 'file=@' + str(p), '-F', 'expire=172800', 'https://tmpfiles.org/api/v1/upload'] if host == 'TmpFiles' else ['-F', 'reqtype=fileupload', '-F', 'fileToUpload=@' + str(p), 'https://catbox.moe/user/api.php']
        code, body, rc = request(args, 'remaining_' + host + '_' + p.stem)
        row = {'host': host, 'file': p.name, 'http_status': code, 'curl_exit_code': rc, 'at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
        receipt['attempts'].append(row)
        persist()
        print(json.dumps(row), flush=True)
        if host == 'TmpFiles':
            try:
                data = json.loads(body.read_text())
            except Exception:
                data = {}
            url = data.get('data', {}).get('url', '')
            parsed = urllib.parse.urlsplit(url)
            if code not in (200, 201) or rc != 0 or data.get('status') != 'success' or parsed.hostname not in ['tmpfiles.org', 'www.tmpfiles.org']:
                continue
            url = 'https://tmpfiles.org' + parsed.path
            direct = 'https://tmpfiles.org/dl' + parsed.path
        else:
            url = body.read_text(errors='replace').strip()
            parsed = urllib.parse.urlsplit(url)
            if code != 200 or rc != 0 or parsed.scheme != 'https' or parsed.hostname != 'files.catbox.moe':
                continue
            direct = url
        dc, db, drc = request(['--max-filesize', str(p.stat().st_size + 65536), direct], 'remaining_verify_' + host + '_' + p.stem)
        downloaded_sha = hashlib.sha256(db.read_bytes()).hexdigest() if db.exists() else ''
        ok = dc == 200 and drc == 0 and db.stat().st_size == p.stat().st_size and downloaded_sha == sha
        result = {'file': p.name, 'bytes': p.stat().st_size, 'sha256': sha, 'host': host, 'url': url, 'download_url': direct, 'download_http_status': dc, 'download_bytes': db.stat().st_size, 'download_sha256': downloaded_sha, 'verified': ok, 'verification': 'Full downloaded bytes SHA256 and size comparison', 'expiry_confirmed_by_response': False}
        if host == 'TmpFiles':
            result['retention_seconds_requested'] = 172800
        receipt['files'].append(result)
        persist()
        print(json.dumps({'file': p.name, 'host': host, 'verified': ok}), flush=True)
        if ok:
            done.add(p.name)
            break

receipt['complete_verified_public_backup'] = {p.name for p in files} <= done
receipt['preferred_host'] = 'Filebin with alternative for remaining object'
receipt['bin_url'] = 'https://filebin.net/auto2000-5abdf26a9e353ecfe7a2'
receipt['finished_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
persist()
print(json.dumps({'complete_verified_public_backup': receipt['complete_verified_public_backup'], 'verified_objects': len(done)}), flush=True)
