"""Minimal GitHub REST helper. The token comes from `git credential fill` (Git Credential Manager) and stays in
memory: it is never printed or written. Usage: gh_api.py METHOD PATH [JSON_BODY]"""
import json, subprocess, sys, urllib.error, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
REPO = 'alaaahmadd182-lab/Smart-formulator-project'


def token():
    r = subprocess.run(['git', 'credential', 'fill'], input='protocol=https\nhost=github.com\n\n', capture_output=True, text=True)
    vals = dict(l.split('=', 1) for l in r.stdout.splitlines() if '=' in l)
    if not vals.get('password'):
        sys.exit('no GitHub credential available')
    return vals['password']


def call(method, path, body=None):
    url = path if path.startswith('http') else f'https://api.github.com/repos/{REPO}{path}'
    req = urllib.request.Request(url, method=method, data=json.dumps(body).encode() if body is not None else None,
                                 headers={'Authorization': f'Bearer {token()}', 'Accept': 'application/vnd.github+json',
                                          'X-GitHub-Api-Version': '2022-11-28', 'User-Agent': 'smart-formulator-publish'})
    try:
        with urllib.request.urlopen(req) as r:
            txt = r.read().decode()
            return r.status, (json.loads(txt) if txt else None)
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or 'null')


if __name__ == '__main__':
    body = json.loads(open(sys.argv[3], encoding='utf-8').read()) if len(sys.argv) > 3 else None
    status, data = call(sys.argv[1], sys.argv[2], body)
    print(status)
    print(json.dumps(data, ensure_ascii=False, indent=1)[:6000])
