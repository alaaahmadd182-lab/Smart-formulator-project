"""One-off helper (2026-11-12): corrects two sentences that described the review snapshot before it existed. Applied."""
R = 'C:/Users/windo/sf-wsA/docs/data_policy_mandatory_review/'
NOTE = ('The snapshot is created after this document is final, so this text cannot contain its manifest hash: see '
        '`REFERENCES.txt` inside the snapshot, and `snapshot_verification_2026-11-12.txt` in this folder for the verification '
        'output and exit code (written after the snapshot, so it is not part of it).')
for name, start, new in (
        ('HANDOFF.md', 'No unexpected failure. **Snapshot:**',
         'No unexpected failure. **Snapshot:** `review_snapshots/review_snapshot_2026-11-12/` (`MANIFEST.sha256`, `REFERENCES.txt`), made with '
         '`python tools/data_policy/make_review_snapshot.py --name review_snapshot_2026-11-12` and never overwritten. ' + NOTE),
        ('CHANGELOG_2026-11-10.md', '5. **Baseline.** New `make_review_snapshot.py`;',
         '5. **Baseline.** New `make_review_snapshot.py`; snapshot `review_snapshots/review_snapshot_2026-11-12/`. ' + NOTE)):
    ls = open(R + name, encoding='utf-8').read().split('\n')
    hit = [i for i, x in enumerate(ls) if x.startswith(start)]
    assert len(hit) == 1, name
    ls[hit[0]] = new
    open(R + name, 'w', encoding='utf-8', newline='\n').write('\n'.join(ls))
print('ok')
