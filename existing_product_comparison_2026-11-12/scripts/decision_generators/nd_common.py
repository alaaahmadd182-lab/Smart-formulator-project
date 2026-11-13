"""Shared helpers for the nineteenth-pass non-duplicate (category D etc.) link reviews (batches 34 onward).
Each generator carries its links frozen (file, product, categories, name-hit pages, first printed name, pages) as printed
by scripts/reading_aids/freeze_links.py, and states the reading scope per link: every name-hit page of the document
(for all of its open links) read in full on the text layer; the other pages NOT read. That is a targeted reading,
never a full-document read."""
import json
import os

B = 'existing_product_comparison_2026-11-12'
T = 'nineteenth pass, 2026-11-14'


def to_root():
    os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))


class Batch:
    def __init__(self, name):
        self.name, self.links, self.F, self.docs = name, [], [], {}

    def doc(self, f, what, date, frozen, role, cov=None, ident=None, scope_extra=''):
        """Close every frozen open link of document f. role: how the products appear on the hit pages.
        cov / ident: optional per-product overrides {pid: text}."""
        rows = [r for r in frozen if r[0] == f]
        allhp = sorted({int(p) for r in rows for p in r[3].split(',') if p})
        n = int(rows[0][5])
        self.docs[f] = dict(what=what, printed_date=date, read=f"name-hit pages {', '.join(map(str, allhp))} read in full (text layer){scope_extra}; the other {n - len(allhp)} of {n} pages not read",
                            kind='another product\'s document (base oils named in it)', limits='targeted reading; pages without a name hit not read')
        cov, ident = cov or {}, ident or {}
        for f_, pid, cat, hp, first, pages in rows:
            fs = (f"name-hit pages p.{hp} for this product read in full (text layer), with all other name-hit pages of the document "
                  f"(pp.{','.join(map(str, allhp))}){scope_extra}; the other {n - len(allhp)} of {n} pages not read ({T})")
            c = cov.get(pid) or (f"not applicable: another product's document ({what}); on the name-hit pages read the product appears only as {role}; "
                                 f"no property of the neat base oil is printed on those pages (pages without the name not read)")
            self.links.append(dict(p=pid, f=f, cat=cat, status='completed', fields_status=fs, coverage=c,
                                   identity=ident.get(pid) or f"printed '{first}' (name in the document; no lot or supplier identifier)",
                                   note=f'Nineteenth-pass targeted review of all name-hit pages ({T}).'))

    def row(self, **k):
        k.setdefault('qual', ''); k.setdefault('method', ''); k.setdefault('cond', ''); k.setdefault('basis', '')
        self.F.append(k)

    def write(self, fname):
        d = dict(batch=self.name, reviewed_on='2026-11-14 (nineteenth pass)',
                 note='Non-duplicate links; every name-hit page read in full, other pages not read (stated per link).',
                 documents=self.docs, links=self.links, fields=self.F)
        json.dump(d, open(f'{B}/decisions/{fname}', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(len(self.links), len(self.F))
