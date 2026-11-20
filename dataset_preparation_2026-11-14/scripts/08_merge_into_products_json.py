"""DISABLED (2026-11-20 integration review). This script copied the json_output/ drafts into Products_json/ and was run
once (commit 8b2a119); that ingestion was reverted on main because production JSON creation is outside the dataset-
preparation workstream and the drafts are not source-verified (see HANDOFF_RESUME_2026-11-14.md, section 'Integration
review 2026-11-20'). The drafts stay in json_output/ as unverified conversion drafts. Ingestion needs an explicit project
decision and source-verified products first; the script refuses to run until then.

Original description follows.
Copy all 161 files from json_output/ into Products_json/.

Rules:
  - If the destination file already exists, report it and skip (do NOT overwrite).
  - Create intermediate directories as needed.
  - Print a summary: files copied, files skipped, any errors.
"""

import sys as _sys
_sys.exit('08_merge_into_products_json.py is disabled: production ingestion is not approved (see the module docstring).')
import glob
import json
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_BASE = os.path.join(ROOT, "json_output")
DST_BASE = os.path.join(os.path.dirname(ROOT), "Products_json")

files = sorted(glob.glob(os.path.join(SRC_BASE, "**", "*.json"), recursive=True))

copied = []
skipped = []
errors = []

for src in files:
    # Compute relative path from json_output/
    rel = os.path.relpath(src, SRC_BASE)
    dst = os.path.join(DST_BASE, rel)

    if os.path.exists(dst):
        skipped.append(rel)
        continue

    try:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        copied.append(rel)
    except Exception as e:
        errors.append(f"{rel}: {e}")

print(f"Copied : {len(copied)}")
print(f"Skipped: {len(skipped)}")
print(f"Errors : {len(errors)}")

if skipped:
    print("\nSkipped (destination already exists):")
    for s in skipped:
        print(f"  {s}")

if errors:
    print("\nErrors:")
    for e in errors:
        print(f"  {e}")
    sys.exit(1)

print("\nMerge complete.")
