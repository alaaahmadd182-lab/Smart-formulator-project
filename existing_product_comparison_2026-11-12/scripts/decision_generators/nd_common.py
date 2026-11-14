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
        self.visual, self.pending, self.queue = [], [], []

    def doc(self, f, what, date, frozen, role, cov=None, ident=None, scope_extra='', scope=None, route=None, viewed=None):
        """Close every frozen open link of document f. role: how the products appear on the hit pages.
        cov / ident: optional per-product overrides {pid: text}. scope: replaces the page-based reading statement where the
        text layer has no page breaks (e.g. a slide deck extracted as one block).
        route (batch 38 onward): the packages the document is formulation / route evidence for; when given, every coverage
        states the limited meaning of 'not applicable' (neat base-oil properties only), names that route evidence and says
        that absence on the pages read is not proof of absence. viewed: pages also viewed as images (appended to the scope)."""
        rows = [r for r in frozen if r[0] == f]
        allhp = sorted({int(p) for r in rows for p in r[3].split(',') if p})
        n = int(rows[0][5])
        if route:
            self.docs_route = getattr(self, 'docs_route', {}); self.docs_route[f] = route
        if viewed:
            scope_extra = f'{scope_extra}; {viewed}'
        rd = scope or f"name-hit pages {', '.join(map(str, allhp))} read in full (text layer){scope_extra}; the other {n - len(allhp)} of {n} pages not read"
        self.docs[f] = dict(what=what, printed_date=date, read=rd,
                            kind='another product\'s document (base oils named in it)',
                            limits='whole text layer read; images not viewed' if scope else 'targeted reading; pages without a name hit not read')
        cov, ident = cov or {}, ident or {}
        where = 'in the text read' if scope else 'on the name-hit pages read'
        tail = ('no property of the neat base oil is printed in the text read (images not viewed)' if scope
                else 'no property of the neat base oil is printed on those pages (pages without the name not read)')
        for f_, pid, cat, hp, first, pages in rows:
            fs = f'{scope} ({T})' if scope else (f"name-hit pages p.{hp} for this product read in full (text layer), with all other name-hit pages of the document "
                                                 f"(pp.{','.join(map(str, allhp))}){scope_extra}; the other {n - len(allhp)} of {n} pages not read ({T})")
            c = cov.get(pid) or f"not applicable: another product's document ({what}); {where} the product appears only as {role}; {tail}"
            if route:
                if c.startswith('not applicable'):
                    rest = c[len('not applicable'):].lstrip(' :')
                    c = (f'not applicable to neat base-oil properties only (limited meaning): {rest}. The document remains formulation / route evidence '
                         f'(recipes using this base oil, package claims, co-component doses) for {route}; that evidence is not assessed by this link; '
                         'absence of a neat property on the pages read is not proof that the document contains none')
                else:
                    c = (f'{c} Limited meaning: assessed for neat base-oil properties on the pages read only; the document remains formulation / route '
                         f'evidence for {route}; absence of a neat property on the pages read is not proof that the document contains none')
            self.links.append(dict(p=pid, f=f, cat=cat, status='completed', fields_status=fs, coverage=c,
                                   identity=ident.get(pid) or f"printed '{first}' (name in the document; no lot or supplier identifier)",
                                   note=f'Nineteenth-pass targeted review of all name-hit pages ({T}).'))

    def row(self, **k):
        k.setdefault('qual', ''); k.setdefault('method', ''); k.setdefault('cond', ''); k.setdefault('basis', '')
        self.F.append(k)

    def write(self, fname):
        for f, r in getattr(self, 'docs_route', {}).items():
            self.docs[f]['route_evidence_for'] = r
        d = dict(batch=self.name, reviewed_on='2026-11-14 (nineteenth pass)',
                 note='Non-duplicate links; every name-hit page read in full, other pages not read (stated per link).',
                 documents=self.docs, links=self.links, fields=self.F)
        if self.visual:
            d['visual'] = self.visual
        if self.pending:
            d['not_yet_verified_visually'] = self.pending
        if self.queue:
            d['new_product_candidates'] = self.queue
        json.dump(d, open(f'{B}/decisions/{fname}', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(len(self.links), len(self.F))
