# Reading aids (read-only)

Saved from the session scratchpad on 2026-11-13. Each script changes to the workspace root first, so it runs from any directory.

| Script | Purpose |
|---|---|
| `cmpsrc.py PID\|FILE ...` | JSON entries citing FILE, all non-missing JSON values, and the full text of cited / section-9 pages (old-archive text cache) |
| `pages.py FILE a b` | Full text of pages a-b from the old-archive text cache |
| `ztext.py NAME a b` | Full text of pages a-b of a NEW-archive file (for files that are only in the new archive) |
| `wdiff.py`, `catdiff.py` | Word-level and catalogue diffs used in earlier passes |

Page images are made with `../render.py`.

These are reading aids. Their output is not a review: claims and tables whose meaning depends on layout must be viewed as
images.
