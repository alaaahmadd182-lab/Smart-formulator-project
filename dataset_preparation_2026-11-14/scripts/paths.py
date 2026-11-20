"""Locations of the source archive and the page-text caches (not committed: large / derived).

Each location can be set by an environment variable; otherwise the default inside this checkout is used. In a second
worktree, point the variables at the checkout that holds the caches, e.g. (Git Bash):
  export SF_ARCHIVE_ZIP="C:/Users/<you>/OneDrive/Desktop/Smart formulator project/Downloaded lubricants sheets.zip"
  export SF_TEXT_CACHE="C:/Users/<you>/sf-wsA/incoming_dataset_review_2026-11-12/_cache/text"
  export SF_OCR_CACHE="C:/Users/<you>/sf-wsA/dataset_preparation_2026-11-14/_cache/ocr"
Archive SHA-256: 62565d5c7a2afc2203536c241004cd4af7f62866a4bfe4f70801b378cf2c78b1 (4,422 files / 4,186 unique documents).
Text cache: one '<sha256>.txt.gz' per text-layer document (pages separated by form feed), built by
incoming_dataset_review_2026-11-12; OCR cache: one '<sha256>.json.gz' per document, built by 01_ocr.py / 01_text_cache.py."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
ROOT = os.path.dirname(PKG)
INV = os.path.join(ROOT, 'incoming_dataset_review_2026-11-12')
ARCHIVE_ZIP = os.environ.get('SF_ARCHIVE_ZIP') or os.path.join(ROOT, 'Downloaded lubricants sheets.zip')
TEXT_CACHE = os.environ.get('SF_TEXT_CACHE') or os.path.join(INV, '_cache', 'text')
OCR_CACHE = os.environ.get('SF_OCR_CACHE') or os.path.join(PKG, '_cache', 'ocr')


def describe():
    def n(d):
        return len(os.listdir(d)) if os.path.isdir(d) else 0
    return dict(archive_zip=ARCHIVE_ZIP, archive_present=os.path.exists(ARCHIVE_ZIP), text_cache=TEXT_CACHE, text_cache_files=n(TEXT_CACHE),
                ocr_cache=OCR_CACHE, ocr_cache_files=n(OCR_CACHE))
