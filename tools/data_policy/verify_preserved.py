"""Verify the preserved files and the audit evidence against their original manifests, whatever the checkout's
line-ending conversion (read-only).

Manifests (never edited):
  tools/PRESERVED_SHA256.txt                           49 preserved scripts and data (original bytes, 2026-11-02)
  reconciliation/audit_evidence/evidence_manifest.md   11 evidence copies (SHA-256 column)

For each file three byte forms are hashed and compared with the manifest hash:
  worktree    the exact bytes on disk in this checkout
  blob        the committed Git blob at --ref (default HEAD), byte for byte
  blob+crlf   the committed blob with every LF written as CRLF (what a core.autocrlf=true checkout writes); computed
              only when the blob contains no CR, so it is an exact, reversible reconstruction
A file VERIFIES when at least one form matches: that form reproduces the original bytes exactly. The result names the
form, so a reader can see, for example, that a file was committed with normalised line endings and its original
CRLF bytes are reproduced by a CRLF checkout. Any file with no matching form is a MISMATCH (exit 1).

The archive 'Manual + Data to share.zip' has no manifest hash; its worktree bytes are compared with the blob at --ref
and at --baseline.

Usage: python tools/data_policy/verify_preserved.py [--ref HEAD] [--baseline f4d97e7...] [--out results.csv]
Exit codes: 0 every file verifies; 1 a mismatch or a missing file.
"""
import argparse, csv, hashlib, io, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASELINE = 'f4d97e71f72598df601b72403775581c34061ad1'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def blob(ref, path):
    r = subprocess.run(['git', 'show', f'{ref}:{path}'], cwd=ROOT, capture_output=True)
    return r.stdout if r.returncode == 0 else None


def preserved_entries():
    with open(os.path.join(ROOT, 'tools', 'PRESERVED_SHA256.txt'), 'rb') as fh:
        text = fh.read().decode('utf-8')
    for line in text.splitlines():
        m = re.match(r'^([0-9a-f]{64}) [ *](.+?)\s*$', line)
        if m:
            yield 'preserved', m.group(1), 'tools/' + m.group(2)


def evidence_entries():
    with open(os.path.join(ROOT, 'reconciliation', 'audit_evidence', 'evidence_manifest.md'), encoding='utf-8') as fh:
        for line in fh:
            cells = [c.strip() for c in line.split('|')]
            if len(cells) > 8:
                h = cells[7].strip('`')
                if re.fullmatch(r'[0-9a-f]{64}', h):
                    name = re.sub(r'^\[|\]\(.*$', '', cells[1].strip('`'))
                    yield 'evidence', h, 'reconciliation/audit_evidence/' + name


def check(kind, want, path, ref):
    full = os.path.join(ROOT, path)
    wt = open(full, 'rb').read() if os.path.exists(full) else None
    b = blob(ref, path)
    forms = {'worktree': wt, 'blob': b,
             'blob+crlf': b.replace(b'\n', b'\r\n') if b is not None and b'\r' not in b else None}
    hashes = {k: (sha(v) if v is not None else '') for k, v in forms.items()}
    match = [k for k, h in hashes.items() if h == want]
    return dict(kind=kind, path=path, manifest_sha256=want, worktree_sha256=hashes['worktree'], blob_sha256=hashes['blob'],
                blob_crlf_sha256=hashes['blob+crlf'], matching_forms=';'.join(match),
                verdict='VERIFIED' if match else ('MISSING' if wt is None and b is None else 'MISMATCH'),
                note=('original bytes are the committed blob' if 'blob' in match else
                      'original CRLF bytes reproduced by a CRLF (core.autocrlf=true) checkout; the blob is LF-normalised'
                      if 'blob+crlf' in match else 'only the worktree bytes match' if match else ''))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--ref', default='HEAD')
    ap.add_argument('--baseline', default=BASELINE)
    ap.add_argument('--out')
    a = ap.parse_args(argv)
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    rows = [check(k, h, p, a.ref) for k, h, p in list(preserved_entries()) + list(evidence_entries())]
    zp = 'Manual + Data to share.zip'
    with open(os.path.join(ROOT, zp), 'rb') as fh:
        zh = sha(fh.read())
    zr, zb = blob(a.ref, zp), blob(a.baseline, zp)
    zrow = dict(kind='archive', path=zp, manifest_sha256='(no manifest)', worktree_sha256=zh,
                blob_sha256=sha(zr) if zr else '', blob_crlf_sha256='', matching_forms=f'blob at {a.ref}' if zr and sha(zr) == zh else '',
                verdict='VERIFIED' if zr and zb and sha(zr) == zh == sha(zb) else 'MISMATCH',
                note=f'worktree = blob at {a.ref} = blob at baseline {a.baseline[:7]}' if zr and zb and sha(zr) == zh == sha(zb) else 'differs')
    rows.append(zrow)
    if a.out:
        with open(a.out, 'w', encoding='utf-8', newline='') as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator='\n')
            w.writeheader(); w.writerows(rows)
    for kind in ('preserved', 'evidence', 'archive'):
        sub = [r for r in rows if r['kind'] == kind]
        forms = {}
        for r in sub:
            forms[r['matching_forms'] or r['verdict']] = forms.get(r['matching_forms'] or r['verdict'], 0) + 1
        print(f'{kind}: {sum(r["verdict"] == "VERIFIED" for r in sub)}/{len(sub)} verified; matching forms: {forms}')
    bad = [r for r in rows if r['verdict'] != 'VERIFIED']
    for r in bad:
        print(f'  {r["verdict"]}: {r["path"]}')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
