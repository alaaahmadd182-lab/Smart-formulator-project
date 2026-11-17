"""Fix three issues found during validation before merging into Products_json.

Issue 1 (MEDIUM): 5 TURKMENBASHY tier1 files — density unit "g/cm3" with values 870-905
  is physically impossible. Correct to "kg/m3"; add open_question noting the printed unit
  is a likely misprint.

Issue 2 (MINOR): 2 FORMOSA tier1 files — api_group.value holds the full cargo name.
  Set value = "Group II"; move cargo name to notes.

Issue 3 (LOW): KANGTAI_BDC010/general.json — TBN intra-document conflict is in
  alternate_entries.notes but not in conflicts[]. Add conflict entry.
"""

import json
import glob
import os
import sys

ROOT = os.path.dirname(os.path.dirname(__file__))
JSON_OUT = os.path.join(ROOT, "json_output")

changes = []
errors = []


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def save(path, data):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


# ---------------------------------------------------------------------------
# Issue 1: TURKMENBASHY tier1 — density unit g/cm3 → kg/m3 + open_question
# ---------------------------------------------------------------------------
TURKMENBASHY_T1 = sorted(glob.glob(
    os.path.join(JSON_OUT, "Base_oils_json", "TURKMENBASHY", "**",
                 "*tier1_blocking.json"),
    recursive=True
))

for path in TURKMENBASHY_T1:
    d = load(path)
    dens = d["fields"]["density"]

    if dens.get("unit") != "g/cm3":
        print(f"SKIP (unit already fixed?): {path}")
        continue

    old_unit = dens["unit"]
    old_notes = dens.get("notes", "")
    printed = dens.get("printed_text", "")

    # Correct unit
    dens["unit"] = "kg/m3"
    dens["notes"] = (
        (old_notes + "; " if old_notes else "")
        + "printed unit 'g/cm3' is physically impossible for a liquid (water=1 g/cm3); "
        "almost certainly a misprint for 'kg/m3'; value "
        + str(dens.get("max", ""))
        + " kg/m3 is plausible for a Group I mineral base oil; unit corrected to kg/m3 in this record"
    )

    # Add open_question
    oq_entry = {
        "property": "density_unit",
        "printed_text": printed,
        "notes": (
            "printed unit 'g/cm3' is physically impossible for a liquid; "
            "almost certainly a misprint for 'kg/m3'; "
            "value " + str(dens.get("max", "")) + " kg/m3 is plausible for Group I mineral base oil; "
            "unit corrected to kg/m3 in this record"
        ),
        "source": dens.get("source", {})
    }
    # Avoid duplicate
    already = any(oq.get("property") == "density_unit" for oq in d.get("open_questions", []))
    if not already:
        d.setdefault("open_questions", []).append(oq_entry)

    save(path, d)
    changes.append(f"Issue1 fixed: {os.path.basename(os.path.dirname(path))}")

print(f"Issue 1: fixed {len(TURKMENBASHY_T1)} files")

# ---------------------------------------------------------------------------
# Issue 2: FORMOSA tier1 — api_group.value = cargo name → "Group II"
# ---------------------------------------------------------------------------
FORMOSA_T1 = sorted(glob.glob(
    os.path.join(JSON_OUT, "Base_oils_json", "FORMOSA", "**",
                 "*tier1_blocking.json"),
    recursive=True
))

for path in FORMOSA_T1:
    d = load(path)
    ag = d["fields"]["api_group_chemistry"]["api_group"]
    current_val = ag.get("value", "")

    if current_val == "Group II":
        print(f"SKIP (already Group II): {path}")
        continue

    # Move cargo name to notes, set clean label
    old_notes = ag.get("notes", "")
    ag["notes"] = (
        (old_notes + "; " if old_notes else "")
        + "printed cargo name used as evidence: \"" + current_val + "\""
    ).strip("; ")
    ag["value"] = "Group II"

    save(path, d)
    changes.append(f"Issue2 fixed: {os.path.basename(os.path.dirname(path))}")

print(f"Issue 2: fixed {len(FORMOSA_T1)} files")

# ---------------------------------------------------------------------------
# Issue 3: KANGTAI_BDC010 — add TBN conflict to conflicts[]
# ---------------------------------------------------------------------------
bdc010_path = os.path.join(
    JSON_OUT, "Additive_components_json", "KANGTAI", "KANGTAI_BDC010", "general.json"
)

if os.path.exists(bdc010_path):
    d = load(bdc010_path)
    tbn = d["fields"]["function_specific_markers"]["tbn"]

    already = any(c.get("property") == "function_specific_markers.tbn"
                  for c in d.get("conflicts", []))
    if not already:
        conflict_entry = {
            "property": "function_specific_markers.tbn",
            "value_a": {
                "qualifier": tbn["qualifier"],
                "max": tbn["max"],
                "unit": tbn["unit"],
                "printed_text": tbn["printed_text"],
                "source": tbn["source"]
            },
            "value_b": {
                "qualifier": tbn["alternate_entries"][0]["qualifier"],
                "max": tbn["alternate_entries"][0]["max"],
                "unit": tbn["alternate_entries"][0]["unit"],
                "printed_text": tbn["alternate_entries"][0]["printed_text"],
                "source": tbn["alternate_entries"][0]["source"]
            },
            "notes": (
                "intra-document conflict: specification table prints 'TBN, mg KOH/g | 30 max' "
                "while product title prints 'TBN=MAX10' (no unit stated); "
                "both values from DL2-12942.pdf page 1; unresolved"
            )
        }
        d.setdefault("conflicts", []).append(conflict_entry)
        save(bdc010_path, d)
        changes.append("Issue3 fixed: KANGTAI_BDC010")
        print("Issue 3: fixed KANGTAI_BDC010")
    else:
        print("Issue 3: conflict entry already present — SKIP")
else:
    errors.append(f"Issue3: file not found: {bdc010_path}")
    print(f"Issue 3: ERROR — file not found")

# ---------------------------------------------------------------------------
print(f"\nTotal changes: {len(changes)}")
for c in changes:
    print(f"  {c}")
if errors:
    print(f"\nErrors: {len(errors)}")
    for e in errors:
        print(f"  {e}")
    sys.exit(1)
