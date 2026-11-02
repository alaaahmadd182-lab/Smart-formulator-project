"""Read-only: extract the .git folder of each Desktop project backup and test whether every object, ref, stash
and reflog commit in it already exists in the current repository."""
import os, shutil, subprocess, sys, zipfile
sys.stdout.reconfigure(encoding='utf-8')
REPO = r'C:\Users\windo\OneDrive\Desktop\Smart formulator project'
DESK = r'C:\Users\windo\OneDrive\Desktop'
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'bk')
SAFE = ['-c', 'core.fsmonitor=false', '-c', 'core.hooksPath=NUL', '-c', 'safe.directory=*']


def git(gd, *a):
    r = subprocess.run(['git', *SAFE, '--git-dir', gd, *a], capture_output=True, text=True, encoding='utf-8', errors='replace')
    return r.stdout


cur = os.path.join(REPO, '.git')
cur_objs = set(git(cur, 'cat-file', '--batch-all-objects', '--batch-check=%(objectname)').split())
print('current repo objects', len(cur_objs))
for name in ('Smart formulator project.zip', 'Smart formulator project (2).zip'):
    dst = os.path.join(OUT, name.replace(' ', '_').replace('(', '').replace(')', ''))
    shutil.rmtree(dst, ignore_errors=True)
    z = zipfile.ZipFile(os.path.join(DESK, name))
    for i in z.infolist():
        parts = i.filename.split('/')
        if len(parts) > 2 and parts[1] == '.git' and not i.is_dir():
            p = os.path.join(dst, *parts[1:])
            os.makedirs(os.path.dirname(p), exist_ok=True)
            open(p, 'wb').write(z.read(i))
    gd = os.path.join(dst, '.git')
    objs = set(git(gd, 'cat-file', '--batch-all-objects', '--batch-check=%(objectname)').split())
    refs = git(gd, 'for-each-ref', '--format=%(objectname) %(refname)').splitlines()
    stash = git(gd, 'stash', 'list')
    reflog_commits = set(git(gd, 'reflog', '--all', '--format=%H').split())
    head = git(gd, 'rev-parse', 'HEAD').strip(); branch = git(gd, 'symbolic-ref', '-q', 'HEAD').strip()
    missing = objs - cur_objs
    print(f'\n=== {name}\n   HEAD {head[:7]} on {branch}; objects {len(objs)}; objects missing from current repo: {len(missing)}')
    for r in refs:
        sha, ref = r.split(' ', 1)
        print(f'   ref {ref} {sha[:7]} present in current repo: {sha in cur_objs}')
    print('   stash entries:', len(stash.splitlines()), '| reflog commits', len(reflog_commits), 'missing:', len(reflog_commits - cur_objs))
    for sha in sorted(missing)[:30]:
        t = git(gd, 'cat-file', '-t', sha).strip()
        info = git(gd, 'log', '-1', '--format=%h %ad %s', sha).strip() if t == 'commit' else ''
        print(f'      missing {t} {sha[:10]} {info}')
    print('   fsck (connectivity):', (git(gd, 'fsck', '--connectivity-only', '--no-progress') or 'ok').strip()[:300])
    # index: files staged in the backup that are not in any current object (uncommitted staged work)
    idx = [l.split() for l in git(gd, 'ls-files', '-s').splitlines()]
    print('   index entries', len(idx), '| index blobs missing from current repo:', [l[3:] for l in idx if l[1] not in cur_objs][:10])
