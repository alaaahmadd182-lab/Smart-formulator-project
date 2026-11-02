"""Read-only: files on disk vs tracked, empty dirs, and an inventory of every Smart Formulator ZIP on the Desktop."""
import collections, hashlib, os, subprocess, sys, zipfile
sys.stdout.reconfigure(encoding='utf-8')
REPO = r'C:\Users\windo\OneDrive\Desktop\Smart formulator project'
DESK = r'C:\Users\windo\OneDrive\Desktop'
LONG = '\\\\?\\'
os.chdir(REPO)
disk, empty = set(), []
for dp, dn, fn in os.walk(LONG + REPO):
    if '.git' in dn:
        dn.remove('.git')
    if not dn and not fn:
        empty.append(dp)
    for f in fn:
        disk.add(os.path.relpath(os.path.join(dp, f), LONG + REPO).replace(os.sep, '/'))
tracked = set(subprocess.run(['git', 'ls-files', '-z'], capture_output=True).stdout.decode('utf-8').split('\0')) - {''}
print('on disk', len(disk), '| tracked', len(tracked), '| disk only', sorted(disk - tracked), '| tracked missing', sorted(tracked - disk), '| empty dirs', empty)

# HEAD blob hashes (sha1 of git blob) for comparing zip members against the repository history
def blob_sha(data):
    return hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()

all_blobs = set(subprocess.run(['git', 'rev-list', '--all', '--objects'], capture_output=True, text=True).stdout.split())
head_files = {}
for line in subprocess.run(['git', 'ls-tree', '-r', 'HEAD'], capture_output=True, text=True, encoding='utf-8').stdout.splitlines():
    meta, path = line.split('\t', 1)
    head_files[path] = meta.split()[2]

for z in sorted(os.listdir(DESK)):
    if not z.lower().endswith('.zip') or ('smart' not in z.lower() and 'formulator' not in z.lower()):
        continue
    p = os.path.join(DESK, z)
    zf = zipfile.ZipFile(p)
    infos = [i for i in zf.infolist() if not i.is_dir()]
    tops = collections.Counter(i.filename.split('/')[0] for i in infos)
    print(f'\n=== {z}  size {os.path.getsize(p):,}  members {len(infos)}  top-level {dict(tops.most_common(6))}')
    git_dirs = [i.filename for i in infos if '/.git/' in i.filename or i.filename.startswith('.git/')]
    print('   contains .git files:', len(git_dirs))
    # map each member to a repo-relative path by stripping the first folder that precedes a known repo path
    in_history = in_head_same = differs_from_head = not_in_repo = 0
    unique = []
    for i in infos:
        name = i.filename
        if '/.git/' in name or name.startswith('.git/'):
            continue
        parts = name.split('/')
        rel = None
        for k in range(len(parts)):
            cand = '/'.join(parts[k:])
            if cand in head_files or cand.startswith(('Products_json/', 'reconciliation/', 'json_templates/')):
                rel = cand; break
        data = zf.read(i)
        sha = blob_sha(data)
        # git stores text files with LF (autocrlf); try the LF form too
        sha_lf = blob_sha(data.replace(b'\r\n', b'\n'))
        hit = sha in all_blobs or sha_lf in all_blobs
        in_history += hit
        if rel in head_files:
            if head_files[rel] in (sha, sha_lf): in_head_same += 1
            else: differs_from_head += 1
        else:
            not_in_repo += 1
        if not hit:
            unique.append((name, len(data)))
    print(f'   members whose bytes exist in git history: {in_history}; same path+bytes as HEAD: {in_head_same}; '
          f'path in HEAD but different bytes: {differs_from_head}; path not in HEAD: {not_in_repo}')
    print(f'   members NOT found anywhere in git history: {len(unique)}')
    for n, s in unique[:40]:
        print(f'      {s:>10,}  {n}')
    if len(unique) > 40:
        print('      ...', len(unique) - 40, 'more')
