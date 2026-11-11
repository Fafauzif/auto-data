"""Resume the interrupted, user-authorized Filebin backup without duplicate uploads."""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT.parent
LOG = ROOT / 'private_cache/backup_uploads'
RECEIPT = BASE / 'Auto2000_Backup_Receipt.json'
receipt = json.loads(RECEIPT.read_text())
inventory = json.loads((LOG / 'resume_bin_inventory.json').read_text())
bin_id = inventory['bin']['id']
assert bin_id == 'auto2000-5abdf26a9e353ecfe7a2'
bin_url = 'https://filebin.net/' + bin_id
files = [BASE / 'Auto2000_Public_Backup_Core.zip'] + [BASE / 'backup_volumes' / f'Auto2000_Telemetry_Volume_{n:02d}.zip' for n in range(1, 6)]
remote = {r['filename']: r for r in inventory['files']}

def persist():
    RECEIPT.write_text(json.dumps(receipt, indent=2))

for p in files:
    assert p.is_file() and p.stat().st_size < 95000000 and 'IGAR' not in p.name
    digest = hashlib.sha256(p.read_bytes()).hexdigest()
    if p.name in remote:
        assert remote[p.name]['sha256'] == digest and remote[p.name]['bytes'] == p.stat().st_size
        print('Already verified: ' + p.name, flush=True)
        continue
    tag = 'resume_' + p.stem
    body, headers = LOG / (tag + '.body'), LOG / (tag + '.headers')
    cmd = ['curl', '-sS', '--max-time', '240', '-D', str(headers), '-o', str(body), '-w', '%{http_code}', '-X', 'POST', '-H', 'Accept: application/json', '-H', 'Content-Type: application/octet-stream', '-H', 'Content-SHA256: ' + digest, '--data-binary', '@' + str(p), bin_url + '/' + p.name]
    result = subprocess.run(cmd, capture_output=True, timeout=255)
    code = int(result.stdout.decode().strip() or 0)
    try:
        data = json.loads(body.read_text())
    except Exception:
        data = {}
    ok = code == 201 and result.returncode == 0 and data.get('file', {}).get('sha256') == digest
    receipt['attempts'].append({'host': 'Filebin', 'file': p.name, 'http_status': code, 'curl_exit_code': result.returncode, 'verified_server_checksum': ok, 'at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'resumed_after_interruption': True})
    if ok:
        receipt['files'].append({'file': p.name, 'bytes': p.stat().st_size, 'sha256': digest, 'host': 'Filebin', 'url': bin_url + '/' + p.name, 'verified': True, 'verification': 'Server201 SHA256 metadata match', 'expires_at': data.get('bin', {}).get('expired_at')})
    persist()
    print(json.dumps({'file': p.name, 'http_status': code, 'verified': ok}), flush=True)
    if not ok:
        raise SystemExit('Stopped at an unverified upload; retained receipt for concrete follow-up.')

assert {p.name for p in files} <= {r['file'] for r in receipt['files'] if r.get('verified')}
receipt['complete_verified_public_backup'] = True
receipt['bin_url'] = bin_url
receipt['preferred_host'] = 'Filebin'
receipt['finished_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
persist()
print('Complete verified public backup: 6 files', flush=True)
