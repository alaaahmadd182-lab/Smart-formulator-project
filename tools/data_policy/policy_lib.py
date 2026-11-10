"""Shared, read-only helpers for Workstream A (source-selection policy, TDS-SDS review, Tier 1 completeness).

Paths are relative to the repository root that contains this tools/ folder, so the code works in any checkout.
Importing this module reads and writes nothing.
"""
import collections, json, os, re, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PRODUCTS = os.path.join(ROOT, 'Products_json')
ARCHIVE = os.path.join(ROOT, 'Manual + Data to share.zip')
REPORTS = os.path.join(ROOT, 'reports')
DOCS = os.path.join(ROOT, 'docs', 'data_policy_mandatory_review')
CLASSES = ('base_oil', 'additive_package', 'additive_component')
OWN_KEYS = ('value_final', 'unit_final', 'min_final', 'max_final', 'unit_conversion', 'integration_flags', 'resolution')


def lp(p):
    """Long-path form on Windows (some product paths are long)."""
    s = os.path.normpath(os.path.abspath(p))
    return '\\\\?\\' + s if os.name == 'nt' and not s.startswith('\\\\?\\') else s


def rel(p):
    return os.path.relpath(p.replace('\\\\?\\', ''), ROOT).replace(os.sep, '/')


def product_files():
    """Sorted project-relative POSIX paths of every Products_json/**/*.json file."""
    out = []
    for dp, _, fs in os.walk(lp(PRODUCTS)):
        for f in fs:
            if f.endswith('.json'):
                out.append(rel(os.path.join(dp, f)))
    return sorted(out)


def load(relpath):
    with open(lp(os.path.join(ROOT, relpath)), encoding='utf-8') as fh:
        return json.load(fh)


def load_products():
    """{product_id: {'class', 'folder', 'files': {relpath: doc}}}; product_id is the record folder name."""
    prods = collections.OrderedDict()
    for f in product_files():
        d = load(f)
        folder = f.rsplit('/', 1)[0]
        pid = folder.rsplit('/', 1)[1]
        p = prods.setdefault(pid, {'class': d.get('material_class'), 'folder': folder, 'files': collections.OrderedDict()})
        if p['folder'] != folder:
            raise ValueError(f'product id {pid} used by two folders: {p["folder"]} and {folder}')
        p['files'][f] = d
    return prods


def value_objects(node, path=''):
    """(path, value object) for every dict carrying both 'status' and 'value' (alternate entries excluded)."""
    out = []
    def rec(n, p):
        if isinstance(n, dict):
            if 'status' in n and 'value' in n and not isinstance(n['status'], dict):
                out.append((p, n))
            for k, v in n.items():
                if k in ('source', 'alternate_entries') or k in OWN_KEYS:
                    continue
                rec(v, f'{p}.{k}' if p else k)
        elif isinstance(n, list):
            for i, v in enumerate(n):
                rec(v, f'{p}[{i}]')
    rec(node, path)
    return out


def src(node):
    s = node.get('source') if isinstance(node, dict) else None
    if isinstance(s, dict):
        return s.get('file') or s.get('url'), s.get('page'), s.get('revision_date')
    return None, None, None


class Archive:
    """Text layer of the archive documents, read in memory from the source ZIP (never extracted)."""

    def __init__(self, path=ARCHIVE):
        self.z = zipfile.ZipFile(path)
        self.members = {}
        for n in self.z.namelist():
            if not n.endswith('/'):
                self.members.setdefault(self.key(os.path.basename(n)), n)
        self._pages = {}

    @staticmethod
    def key(name):
        n = str(name).replace('�', '%').replace('%20', ' ').replace('%', '').lower().strip()
        return re.sub(r'\s+', ' ', n)

    def member(self, name):
        if not name or str(name).lower().startswith(('http://', 'https://')):
            return None
        return self.members.get(self.key(os.path.basename(str(name))))

    def pages(self, name):
        """Page texts; [] for images; None when the file is not in the archive."""
        m = self.member(name)
        if m is None:
            return None
        if m not in self._pages:
            if m.lower().endswith('.pdf'):
                import pymupdf
                self._pages[m] = [p.get_text() for p in pymupdf.open(stream=self.z.read(m), filetype='pdf')]
            else:
                self._pages[m] = []
        return self._pages[m]
