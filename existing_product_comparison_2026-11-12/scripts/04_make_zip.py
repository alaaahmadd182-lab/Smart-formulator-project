"""Old-versus-new comparison, step 4: review ZIPs on the Desktop. Never overwrites an existing ZIP (numbered names).

  SmartFormulator_comparison_review_2026-11-12[_N].zip     summary, tables, decisions, scripts, logs (no caches)
  SmartFormulator_comparison_evidence_2026-11-12[_N].zip   the new-archive documents cited by field rows, exact bytes,
                                                           with SHA256SUMS.txt (each hash checked against the manifest)
Usage: python existing_product_comparison_2026-11-12/scripts/04_make_zip.py
"""
import csv, hashlib, os, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
ROOT = os.path.dirname(BASE)
DESK = r'C:\Users\windo\OneDrive\Desktop'
NEW_ZIP = r'C:\Users\windo\OneDrive\Desktop\Smart formulator project\Downloaded lubricants sheets.zip'


def free(stem):
    p, n = os.path.join(DESK, stem + '.zip'), 1
    while os.path.exists(p):
        n += 1
        p = os.path.join(DESK, f'{stem}_{n}.zip')
    return p


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main():
    out = free('SmartFormulator_comparison_review_2026-11-12')
    n = 0
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        for d, dirs, files in os.walk(BASE):
            dirs[:] = sorted(x for x in dirs if x not in ('_cache', '__pycache__', '.git'))
            for f in sorted(files):
                if f.endswith('.pyc'):
                    continue
                p = os.path.join(d, f)
                z.write(p, os.path.join('existing_product_comparison_2026-11-12', os.path.relpath(p, BASE)).replace('\\', '/'))
                n += 1
    print(f'{out}\n  files {n}; bytes {os.path.getsize(out)}; sha256 {sha(out)}')

    with open(os.path.join(BASE, 'tables', 'field_level_comparison.csv'), encoding='utf-8') as fh:
        need = {r['new_source_file']: r['new_source_sha256'] for r in csv.DictReader(fh)}
    with open(os.path.join(BASE, 'tables', 'visual_verification.csv'), encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            if len(r['sha256']) == 64 and r['result'] != 'NOT YET VERIFIED':
                need[r['file']] = r['sha256']
    ev = free('SmartFormulator_comparison_evidence_2026-11-12')
    lines, total = [], 0
    with zipfile.ZipFile(NEW_ZIP) as src, zipfile.ZipFile(ev, 'w', zipfile.ZIP_STORED) as z:
        retrieved = os.path.join(BASE, 'retrieved_evidence_2026-11-13')
        for f in sorted(os.listdir(retrieved)) if os.path.isdir(retrieved) else []:
            with open(os.path.join(retrieved, f), 'rb') as f2:
                data = f2.read()
            z.writestr('retrieved_registered_sources_2026-11-13/' + f, data)
            lines.append(f'{hashlib.sha256(data).hexdigest()}  retrieved_registered_sources_2026-11-13/{f}')
        for f in sorted(need):
            # not a new-archive document (e.g. a retrieved registered source, which since the eleventh pass carries its
            # computed hash in the tables): already written above from retrieved_evidence_2026-11-13
            if not need[f] or os.path.exists(os.path.join(retrieved, f)):
                continue
            data = src.read('Downloaded lubricants sheets/' + f)
            h = hashlib.sha256(data).hexdigest()
            if h != need[f]:
                sys.exit(f'hash mismatch for {f}')
            z.writestr('new_archive_documents/' + f, data)
            lines.append(f'{h}  new_archive_documents/{f}')
            total += len(data)
        # old sources cited by the compared products: exact bytes from the existing archive, and local evidence copies
        old_zip = os.path.join(ROOT, 'Manual + Data to share.zip')
        unavailable = []
        with open(os.path.join(BASE, 'tables', 'old_source_references.csv'), encoding='utf-8') as fh, zipfile.ZipFile(old_zip) as oz:
            for r in csv.DictReader(fh):
                av = r['availability']
                if av.startswith('Manual + Data to share.zip:'):
                    member = av.split(':', 1)[1].split(' (no text layer')[0]
                    data = oz.read(member)
                    h = hashlib.sha256(data).hexdigest()
                    if h != r['sha256']:
                        sys.exit('hash mismatch for old source ' + member)
                    z.writestr('existing_archive_documents/' + member.rsplit('/', 1)[-1], data)
                    lines.append(f'{h}  existing_archive_documents/{member.rsplit("/", 1)[-1]}')
                elif 'local evidence copy ' in av:
                    loc = av.split('local evidence copy ', 1)[1].split(' (')[0]
                    with open(os.path.join(ROOT, loc), 'rb') as f2:
                        data = f2.read()
                    z.writestr('registered_external_evidence/' + os.path.basename(loc), data)
                    lines.append(f'{hashlib.sha256(data).hexdigest()}  registered_external_evidence/{os.path.basename(loc)}')
                else:
                    unavailable.append(f'{r["reference"]} | sha256 {r["sha256"] or "none"} | {av}')
                total += len(data) if 'data' in dir() else 0
        z.writestr('OLD_SOURCES_NOT_AVAILABLE_LOCALLY.txt', '\n'.join(unavailable) + '\n')
        # the current product JSON files compared (exact working-tree bytes), read-only copies
        with open(os.path.join(BASE, 'tables', 'field_level_comparison.csv'), encoding='utf-8') as fh:
            jfiles = sorted({r['json_file'] for r in csv.DictReader(fh) if r['json_file']})
        for jf in jfiles:
            with open(os.path.join(ROOT, jf), 'rb') as f2:
                data = f2.read()
            z.writestr('current_json_files_READ_ONLY_COPIES/' + jf.replace('\\', '/'), data)
            lines.append(f'{hashlib.sha256(data).hexdigest()}  current_json_files_READ_ONLY_COPIES/{jf.replace(chr(92), "/")}')
        z.writestr('SHA256SUMS.txt', '\n'.join(lines) + '\n')
        z.writestr('README.txt',
                   'Evidence for the old-versus-new comparison. Everything here is an exact, unmodified copy; SHA256SUMS.txt lists every file.\n\n'
                   'new_archive_documents/                 NEW sources: documents of "Downloaded lubricants sheets.zip" cited by the field-level\n'
                   '                                       comparison or verified visually (hashes checked against the inventory manifest).\n'
                   'existing_archive_documents/            OLD sources: members of "Manual + Data to share.zip" cited by the compared product\n'
                   '                                       records (hashes checked against the archive).\n'
                   'registered_external_evidence/          OLD sources registered in source_registry.json for which a local evidence copy exists\n'
                   '                                       (folder absent when none applies).\n'
                   'retrieved_registered_sources_2026-11-13/  OLD sources registered in source_registry.json and retrieved read-only on\n'
                   '                                       2026-11-13; SHA-256 equal to the registered hashes (RETRIEVAL_LOG.txt).\n'
                   'OLD_SOURCES_NOT_AVAILABLE_LOCALLY.txt  cited old sources with a registered hash but no local copy: NOT included, NOT re-checked.\n'
                   'current_json_files_READ_ONLY_COPIES/   the CURRENT product JSON files compared (working-tree bytes), for reference only.\n\n'
                   'These files support PROPOSED changes only. Nothing has been ingested and no JSON has been changed.\n')
    print(f'{ev}\n  documents {len(lines)}; document bytes {total}; zip bytes {os.path.getsize(ev)}; sha256 {sha(ev)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
