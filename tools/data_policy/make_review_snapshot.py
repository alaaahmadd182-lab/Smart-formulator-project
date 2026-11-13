"""Freeze a dated review snapshot of the work, with a SHA-256 manifest (read-only on everything it copies).

Copies the relevant code, policy inputs, reports, documentation and test results byte for byte into
review_snapshots/<name>/files/ and writes:
  MANIFEST.sha256   one line per copied file: '<sha256>  <path relative to files/>' (the copy is hashed, and the copy
                    is compared with its source before the line is written)
  REFERENCES.txt    things the snapshot refers to by hash instead of duplicating: the original datasheet archive, the
                    product-data fingerprints, the git commit, and the number of product JSON files
  README.md         what the snapshot is and how to verify it

The product JSON is copied too, because two of its files differ from the last commit. Not copied: .git, __pycache__,
earlier snapshots, the source archive (referenced by its SHA-256), and anything outside the listed paths. A dataset
that is not part of this repository is never touched.

Usage: python tools/data_policy/make_review_snapshot.py --name review_snapshot_2026-11-12 [--verify]
  --verify   recompute the hashes of an existing snapshot and compare them with its manifest; writes nothing
Exit codes: 0 ok; 1 verification mismatch or the snapshot already exists.
"""
import argparse, datetime, hashlib, os, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'review_snapshots')
ARCHIVE = 'Manual + Data to share.zip'
INCLUDE = ['tools/data_policy', 'tools/mandatory_properties', 'tools/maintenance_2026-11-11', 'tools/README.md',
           'build_coverage_matrix.py', 'integrate_products.py', 'build_conflicts_report.py', 'requirements.txt',
           'source_registry.json', 'json_templates', 'CLAUDE.md', 'README.md', 'PROJECT_FILE_GUIDE.md', 'open_questions_and_conflicts.md',
           'Coverage_Matrix.xlsx', 'reports', 'docs/data_policy_mandatory_review', 'Products_json']
SKIP_DIRS = {'__pycache__', '.git', 'review_snapshots'}


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def lp(p):
    p = os.path.abspath(p)
    return '\\\\?\\' + p if os.name == 'nt' and not p.startswith('\\\\?\\') else p


def files():
    for inc in INCLUDE:
        src = os.path.join(ROOT, inc)
        if os.path.isfile(src):
            yield inc
        for d, dirs, fs in os.walk(src):
            dirs[:] = sorted(x for x in dirs if x not in SKIP_DIRS)
            for f in sorted(fs):
                yield os.path.relpath(os.path.join(d, f), ROOT).replace(os.sep, '/')


def git(*a):
    r = subprocess.run(['git', *a], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    return r.stdout.strip()


def verify(name):
    base = os.path.join(OUT, name)
    bad, n = [], 0
    with open(os.path.join(base, 'MANIFEST.sha256'), encoding='utf-8') as fh:
        listed = [ln.rstrip('\n').split('  ', 1) for ln in fh if ln.strip()]
    for h, rel in listed:
        n += 1
        p = lp(os.path.join(base, 'files', rel))
        if not os.path.exists(p) or sha(p) != h:
            bad.append(rel)
    present = sum(len(fs) for _, _, fs in os.walk(lp(os.path.join(base, 'files'))))
    print(f'{name}: {n} manifest entries; files present {present}; mismatches {len(bad)}')
    for b in bad[:20]:
        print('  MISMATCH', b)
    return 1 if bad or present != n else 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--name', required=True)
    ap.add_argument('--verify', action='store_true')
    a = ap.parse_args(argv)
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if a.verify:
        return verify(a.name)
    base = os.path.join(OUT, a.name)
    if os.path.exists(base):
        print(f'STOP: {base} already exists; a snapshot is never overwritten')
        return 1
    sys.path.insert(0, os.path.join(ROOT, 'tools', 'mandatory_properties'))
    import build_eligibility as BE
    lines, total = [], 0
    for rel in files():
        src, dst = lp(os.path.join(ROOT, rel)), lp(os.path.join(base, 'files', rel))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)
        h = sha(dst)
        if h != sha(src):
            print('STOP: copy differs from source:', rel)
            return 1
        lines.append(f'{h}  {rel}\n')
        total += os.path.getsize(dst)
    with open(os.path.join(base, 'MANIFEST.sha256'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.writelines(lines)
    arch = os.path.join(ROOT, ARCHIVE)
    n_json = len(BE.product_paths())
    refs = [f'created: {datetime.datetime.now().isoformat(timespec="seconds")}',
            f'git branch: {git("rev-parse", "--abbrev-ref", "HEAD")}',
            f'git HEAD: {git("rev-parse", "HEAD")} (the snapshot is the working tree: HEAD plus uncommitted changes)',
            f'uncommitted paths (git status --porcelain, lines): {len(git("status", "--porcelain").splitlines())}',
            f'original datasheet archive: {ARCHIVE}',
            f'  size (bytes): {os.path.getsize(arch)}',
            f'  SHA-256: {sha(arch)}',
            '  not copied into the snapshot; referenced by this hash',
            f'product data: Products_json, {n_json} JSON files, copied into the snapshot',
            f'  fingerprint, exact bytes of this checkout (authoritative): {BE.snapshot_sha256()}',
            f'  fingerprint, LF-normalised (informational): {BE.snapshot_sha256_lf()}',
            f'manifest: MANIFEST.sha256, {len(lines)} files, {total} bytes',
            f'manifest SHA-256: {sha(os.path.join(base, "MANIFEST.sha256"))}']
    with open(os.path.join(base, 'REFERENCES.txt'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(refs) + '\n')
    with open(os.path.join(base, 'README.md'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(f'# {a.name}\n\nA frozen copy of the Workstream A code, policy inputs, product JSON, reports, documentation and test results, made by '
                 '`python tools/data_policy/make_review_snapshot.py`.\n\n'
                 '- `files/` holds byte-for-byte copies, at their repository paths.\n'
                 '- `MANIFEST.sha256` lists the SHA-256 of every copied file.\n'
                 '- `REFERENCES.txt` gives what is referenced by hash instead of copied: the original datasheet archive, the product-data '
                 'fingerprints and the git commit.\n\n'
                 f'Verify: `python tools/data_policy/make_review_snapshot.py --name {a.name} --verify`\n\n'
                 'Not included: `.git`, the source archive, earlier snapshots, and any dataset outside this repository.\n')
    print(f'{a.name}: {len(lines)} files, {total} bytes')
    print('\n'.join(refs))
    return 0


if __name__ == '__main__':
    sys.exit(main())
