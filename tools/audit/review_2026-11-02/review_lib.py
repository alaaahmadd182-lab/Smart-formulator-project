"""Shared, read-only helpers for the 2026-11-02 review of the comprehensive conflicts audit.

Paths are relative to the repository root (this file lives in tools/audit/review_2026-11-02/). Nothing here writes to
the repository.
"""
import csv, io, json, os, re, subprocess, zipfile

import pymupdf

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
HERE = os.path.dirname(os.path.abspath(__file__))
ZIP = os.path.join(ROOT, 'Manual + Data to share.zip')
EVIDENCE = os.path.join(ROOT, 'reconciliation', 'audit_evidence')
REPORT_MD = os.path.join(ROOT, 'reconciliation', 'comprehensive_conflicts_audit.md')
REPORT_CSV = os.path.join(ROOT, 'reconciliation', 'comprehensive_conflicts_audit.csv')
SNAPSHOT_FINDINGS = os.path.join(ROOT, 'tools', 'audit', 'original_2026-10-27_to_30', 'intermediate', 'findings_v4.json')
SNAPSHOT_COMMIT = 'e6617ca'  # PR #4 head: the 2026-10-30 audit snapshot
CORRECTIONS_COMMIT = '28265fd'  # 2026-10-31 product-data corrections

CONF, POT = 'Confirmed contradiction', 'Potential contradiction (comparability uncertain)'
TYPES = [CONF, POT, 'Edition difference', 'Explainable difference', 'Data-quality issue']
FU = ['Supplier clarification', 'Edition-selection policy', 'Correctable from existing evidence (data owner)',
      'Data-owner decision (field-selection rule)', 'Standard or further source needed', 'No follow-up needed beyond documentation']


def lp(p):
    """Long-path form on Windows (some Products_json paths exceed 260 characters)."""
    s = os.path.normpath(os.path.abspath(p))
    return '\\\\?\\' + s if os.name == 'nt' and not s.startswith('\\\\?\\') else s


def read_csv(path=REPORT_CSV, text=None):
    if text is None:
        text = open(path, encoding='utf-8-sig', newline='').read()
    return list(csv.DictReader(io.StringIO(text.lstrip('﻿'))))


def git_show(rev, path):
    return subprocess.run(['git', 'show', f'{rev}:{path}'], cwd=ROOT, capture_output=True, check=True).stdout.decode('utf-8')


def load_json_at(rev, rel):
    """A repository JSON file at a commit (rev) or in the working tree (rev=None)."""
    if rev is None:
        return json.load(open(lp(os.path.join(ROOT, rel)), encoding='utf-8'))
    return json.loads(git_show(rev, rel))


class Archive:
    """Text layer of every archive document, read in memory from the source ZIP."""

    def __init__(self, zpath=ZIP):
        self.z = zipfile.ZipFile(zpath)
        self.members = {}
        for n in self.z.namelist():
            if not n.endswith('/'):
                self.members.setdefault(self.key(os.path.basename(n)), n)
        self._cache = {}

    @staticmethod
    def key(name):
        n = str(name).replace('�', '%').replace('%20', ' ').replace('%', '').lower().strip()
        return re.sub(r'\s+', ' ', n)

    def member(self, name):
        if not name or str(name).lower().startswith(('http://', 'https://')):
            return None
        return self.members.get(self.key(os.path.basename(str(name))))

    def pages(self, name):
        """List of page texts, [] for an image file or a PDF without text, None if not in the archive."""
        m = self.member(name)
        if m is None:
            ev = os.path.join(EVIDENCE, os.path.basename(str(name)))
            if not os.path.exists(ev):
                return None
            m = ev
        if m not in self._cache:
            if not m.lower().endswith('.pdf'):
                self._cache[m] = []
            else:
                data = open(m, 'rb').read() if os.path.isabs(m) else self.z.read(m)
                doc = pymupdf.open(stream=data, filetype='pdf')
                self._cache[m] = [p.get_text() for p in doc]
        return self._cache[m]


def norm(s):
    s = str(s or '').replace('−', '-').replace('–', '-').replace(' ', ' ').replace('℃', '°C').replace('ºC', '°C')
    return re.sub(r'\s+', ' ', s).strip()


def number_forms(v):
    """Printed forms a numeric value may take on a page: 0.8720 / 0,8720 / 0.872 / 998 / 998.0 ..."""
    s = str(v).strip().replace('−', '-')
    m = re.fullmatch(r'[<>≥≤≮]?\s*(-?\d+(?:[.,]\d+)?)', s)
    if not m:
        return []
    t = m.group(1).replace(',', '.')
    f = float(t)
    forms = {t, t.replace('.', ',')}
    if '.' in t:
        forms.add(t.rstrip('0').rstrip('.'))
    if f.is_integer():
        forms.update({str(int(f)), f'{int(f)}.0'})
    return sorted(forms, key=len, reverse=True)


def on_page(value, text):
    """True when the numeric value appears as a separate number on the page text."""
    t = norm(text)
    for form in number_forms(value):
        tail = r'0*(?![\d])' if re.search(r'[.,]', form) else r'(?![\d])'  # 1.013 also matches a printed 1.0130
        if re.search(r'(?<![\d.,])' + re.escape(form).replace('\\-', '[-−]') + tail, t):
            return True
        if form.startswith('-') and re.search(r'(?<![\d.,])-\s' + re.escape(form[1:]) + r'(?![\d])', t):
            return True
    return False
