"""Read-only data model for the conflicts audit: products, value objects, sources and the archive text index."""
import collections, glob, json, os, re

REPO = r'C:\Users\windo\OneDrive\Desktop\Smart formulator project'
SCR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OWN = {'value_final', 'unit_final', 'min_final', 'max_final', 'unit_conversion', 'integration_flags', 'resolution',
       'status_final', 'source_final', 'qualifier_final', 'method_final', 'test_temperature_c_final'}
CLASS_LABEL = {'base_oil': 'Base oil', 'additive_package': 'Additive package', 'additive_component': 'Additive component'}


def lp(p):
    s = os.path.normpath(os.path.abspath(p))
    return '\\\\?\\' + s if os.name == 'nt' and not s.startswith('\\\\?\\') else s


def load_products():
    """{folder_rel: {'class','folder','record_id','supplier_folder','tiers': {tier_key: {'file','doc'}}}}"""
    root = os.path.join(REPO, 'Products_json'); prods = collections.OrderedDict()
    for dp, _, fs in sorted(os.walk(lp(root))):
        for f in sorted(fs):
            if not f.endswith('.json'): continue
            full = os.path.join(dp, f); doc = json.load(open(full, encoding='utf-8'))
            rel = os.path.relpath(full, lp(root)).replace(os.sep, '/')
            folder = rel.rsplit('/', 1)[0]
            p = prods.setdefault(folder, {'class': doc.get('material_class'), 'folder': folder, 'record_id': folder.split('/')[-1],
                                         'supplier_folder': folder.split('/')[1], 'tiers': collections.OrderedDict()})
            key = f"tier{doc.get('tier')}" + (f"/{f}" if doc.get('material_class') == 'additive_component' else '')
            p['tiers'][key] = {'file': 'Products_json/' + rel, 'doc': doc, 'tier': doc.get('tier')}
    return prods


def value_objects(fields, path=''):
    """(path, node, parent) for every value object (dict with status and value)."""
    out = []
    def rec(n, p, parent):
        if isinstance(n, dict):
            if 'status' in n and 'value' in n and not isinstance(n['status'], dict):
                out.append((p, n, parent))
            for k, v in n.items():
                if k not in ('source', 'alternate_entries') and k not in OWN:
                    rec(v, f'{p}.{k}' if p else k, n)
        elif isinstance(n, list):
            for i, v in enumerate(n):
                rec(v, f'{p}[{i}]', parent)
    rec(fields, path, None)
    return out


def all_status_nodes(fields):
    out = []
    def rec(n, p):
        if isinstance(n, dict):
            if 'status' in n and not isinstance(n['status'], dict): out.append((p, n))
            for k, v in n.items():
                if k != 'source': rec(v, f'{p}.{k}' if p else k)
        elif isinstance(n, list):
            for i, v in enumerate(n): rec(v, f'{p}[{i}]')
    rec(fields, '')
    return out


class Archive:
    def __init__(self):
        self.idx = json.load(open(os.path.join(SCR, 'audit', 'pdf_index.json'), encoding='utf-8'))
        self.by_key = {}
        for base, entries in self.idx.items():
            self.by_key[self.key(base)] = entries[0]

    @staticmethod
    def key(name):
        n = str(name).replace('\ufffd', '%').replace('%20', ' ').replace('%', '').lower().strip()
        return re.sub(r'\s+', ' ', n)

    def get(self, name):
        if not name or str(name).lower().startswith(('http://', 'https://')): return None
        return self.by_key.get(self.key(os.path.basename(str(name))))

    def page_text(self, name, page):
        e = self.get(name)
        if not e or not e.get('pages'): return None
        if isinstance(page, int) and 1 <= page <= len(e['pages']): return e['pages'][page - 1]
        return None

    def all_text(self, name):
        e = self.get(name)
        return '\n'.join(e['pages']) if e and e.get('pages') else None


NUM = re.compile(r'(?<![\w.])[-−–]?\d+(?:[.,]\d+)?')


def numbers(text):
    out = []
    for m in NUM.finditer(str(text or '')):
        s = m.group(0).replace('−', '-').replace('–', '-')
        if s.count(',') == 1 and '.' not in s and len(s.split(',')[1]) != 3: s = s.replace(',', '.')
        s = s.replace(',', '')
        try: out.append(float(s))
        except ValueError: pass
    return out


def fmt(v):
    if v is None: return ''
    if isinstance(v, float) and v.is_integer(): return str(v)
    return json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else str(v)


def src_of(node):
    s = node.get('source') if isinstance(node, dict) else None
    if isinstance(s, dict): return s.get('file') or s.get('url'), s.get('page'), s.get('revision_date')
    if isinstance(s, list) and s and isinstance(s[0], dict): return s[0].get('file') or s[0].get('url'), s[0].get('page'), s[0].get('revision_date')
    return None, None, None
