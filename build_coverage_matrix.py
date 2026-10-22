#!/usr/bin/env python3
"""Task 4 coverage matrix built from the Products_json folder; no property values are inferred.

Reads every product JSON file (read-only) and writes one Excel workbook:
Overview, one sheet per material class, Validation Issues, Status Detail and
Traceability Audit. Cell classification follows the original Task 4 rules.

Exit codes: 0 = passed, output written; 1 = usage / file error;
2 = validation failed, diagnostic workbook written instead of the output.
"""
import argparse, collections, json, os, sys, tempfile
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

CLASSES = {'base_oil': 'Base Oils', 'additive_package': 'Additive Packages', 'additive_component': 'Additive Components'}
STATUS = {'reported': 'reported', 'calculated': 'calculated', 'missing': 'missing', 'not required': 'not_applicable',
          'not_applicable': 'not_applicable', 'not applicable': 'not_applicable', 'n/a': 'not_applicable'}
PRIORITY = ('reported', 'calculated', 'missing', 'not_applicable')
SKIP_KEYS = ('source', 'notes', 'calculation_note', 'method', 'printed_text', 'external_fill_notes')
VALUE_KEYS = ('value', 'min', 'max', 'wt_pct', 'type', 'form')
EXPECTED_TIERS = {'base_oil': {1, 2, 3}, 'additive_package': {1, 2}, 'additive_component': {1}}
UNRECOGNIZED = 'unrecognized: '
# Issue types that make the run fail: the official workbook is never written when any occur.
BLOCKING = ('Unknown status', 'Invalid JSON', 'Unreadable file', 'Unreadable folder', 'Invalid identity', 'Duplicate tier', 'Duplicate property',
            'Expected tier missing', 'Unclassified status-free field')
MIXED = 'Mixed nested statuses (review)'
CONTRADICTION, OUT_OF_RANGE, TEMP_MISMATCH = ('Status contradicts value (review)', 'Value outside its own min/max (review)',
                                              'Test temperature differs from property (review)')
# Non-blocking findings that ask for a human check rather than signalling a structural error.
REVIEW = (MIXED, CONTRADICTION, OUT_OF_RANGE, TEMP_MISMATCH)
PROPERTY_TEMPERATURE = {'kv40': 40, 'kv100': 100}
WARN, INFO = 'warning', 'info'
REGISTRY_STATUSES = ('verified', 'unreachable', 'unverified')

HEADER_FILL, SUBHEADER_FILL = PatternFill('solid', fgColor='17324D'), PatternFill('solid', fgColor='245B73')
MIXED_FILL, ERROR_FILL = PatternFill('solid', fgColor='FFE9A8'), PatternFill('solid', fgColor='F4B6B6')
WHITE_BOLD = Font(bold=True, color='FFFFFF')

records = {}; issues = []; statuses = collections.Counter(); details = []; trace = []; json_count = 0
sources = {}  # external URL -> source_registry.json entry


def detail(ctx, path, raw, norm, counted, node=None, note=''):
    """Record one nested property for the Status Detail sheet."""
    src = node.get('source') if isinstance(node, dict) else None
    src = src if isinstance(src, dict) else {}
    value = node.get('value') if isinstance(node, dict) else None
    details.append([ctx['class'], ctx['record_id'], ctx['tier'], ctx['file'], ctx['field'], path or '(property)',
                    raw, norm, 'yes' if counted else 'no', None, cell_text(value),
                    cell_text(src.get('file') or src.get('url')), cell_text(src.get('page')), note])


def audit_trace(ctx, path, node):
    """Classify the source of a Reported value. Warnings need attention; info rows document valid sources."""
    src = node.get('source') if isinstance(node.get('source'), dict) else {}
    file, url, page = src.get('file'), src.get('url'), src.get('page')
    location = file or url
    base = [ctx['class'], ctx['record_id'], ctx['file'], ctx['field'], path or '(property)', node.get('status'),
            cell_text(node.get('value')), cell_text(node.get('basis')), cell_text(location), cell_text(page)]
    add = lambda finding, severity, note: trace.append([finding, severity] + base + [note])
    no_page = page in (None, '')
    if node.get('basis') == 'general_knowledge':
        add('Unsupported reported value (basis: general_knowledge)', WARN,
            'Value is not printed in any source document; status left unchanged pending supplier confirmation.')
    if not location:
        add('Reported value without source', WARN, 'No source file or URL recorded.')
    elif not str(location).lower().startswith(('http://', 'https://')):
        if no_page:
            add('Archive source without page reference', WARN, 'Archive file recorded but no page number.')
    else:
        reg = sources.get(location)
        if reg is None:
            add('External source not in source registry', WARN, 'Add this URL to source_registry.json after checking it.')
        elif reg['host'] == 'third-party':
            add('External source on a non-authoritative host', WARN, reg.get('note') or '')
        elif reg['status'] != 'verified':
            add(f'External source {reg["status"]}', WARN, reg.get('note') or '')
        elif reg['host'] == 'archive':
            add('Verified archived copy of a manufacturer document', WARN if no_page and reg['format'] == 'pdf' else INFO, reg.get('title') or '')
        elif reg['format'] == 'html':
            add('Verified external web page (no page numbers)', INFO, reg.get('title') or '')
        elif no_page:
            add('Verified external PDF without page reference', WARN, reg.get('title') or '')
        else:
            add('Verified external PDF with page', INFO, reg.get('title') or '')


def review_checks(ctx, path, node, norm):
    """Non-blocking consistency checks on one status-bearing node."""
    where = ctx['issue_path'] + path
    value = node.get('value')
    if norm in ('missing', 'not_applicable') and value not in (None, '', []):
        issues.append((where, CONTRADICTION, f'status {node.get("status")} but value {cell_text(value)}'))
    lo, hi = node.get('min'), node.get('max')
    if all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in (value, lo, hi)) and not lo <= value <= hi:
        issues.append((where, OUT_OF_RANGE, f'{value} not in [{lo}, {hi}]'))
    expected = PROPERTY_TEMPERATURE.get(ctx['field']) if not path else None
    if expected is not None and norm == 'reported' and node.get('test_temperature_c') not in (None, expected):
        issues.append((where, TEMP_MISMATCH, f'{node.get("test_temperature_c")} C recorded for {ctx["field"]}'))


def scan_nested(x, path, ctx, top=True):
    """List status nodes nested inside a status-bearing node; they do not count toward the cell."""
    if isinstance(x, dict):
        if not top and 'status' in x:
            raw = str(x['status']).strip(); norm = STATUS.get(raw.lower(), UNRECOGNIZED + raw)
            detail(ctx, path, raw, norm, False, x, 'Nested inside a status-bearing property (legacy rule: not counted in cell)')
            if norm.startswith(UNRECOGNIZED): issues.append((ctx['issue_path'] + path, 'Unknown status', raw))
            if norm == 'reported': audit_trace(ctx, path, x)
            review_checks(ctx, path, x, norm)
        for k, v in x.items():
            if k not in SKIP_KEYS and isinstance(v, (dict, list)): scan_nested(v, f'{path}/{k}', ctx, False)
    elif isinstance(x, list):
        for i, v in enumerate(x): scan_nested(v, f'{path}/{i}', ctx, False)


def leaf_status(x, path, ctx):
    """Return leaf status list; flag unclassified evidence for audit, never assume reported."""
    issue_path = ctx['issue_path'] + path
    if isinstance(x, dict):
        if 'status' in x:
            raw = str(x['status']).strip(); key = raw.lower(); statuses[raw] += 1
            norm = STATUS.get(key)
            if norm is None:
                issues.append((issue_path, 'Unknown status', raw)); norm = UNRECOGNIZED + raw
            detail(ctx, path, raw, norm, True, x)
            if norm == 'reported': audit_trace(ctx, path, x)
            review_checks(ctx, path, x, norm)
            scan_nested(x, path, ctx)
            return [norm]
        vals = []
        for k, v in x.items():
            if k in SKIP_KEYS: continue
            if isinstance(v, (dict, list)): vals += leaf_status(v, f'{path}/{k}', ctx)
        if vals: return vals
        # status-free data cannot be certified as reported
        if any(k in x for k in VALUE_KEYS):
            issues.append((issue_path, 'Unclassified status-free field', 'Needs manual status review'))
            detail(ctx, path, '(no status key)', 'missing', True, x, 'Status-free data; needs manual status review')
        else:
            detail(ctx, path, '(no status key)', 'missing', True, x, 'Object with no status and no values')
        return ['missing']
    if isinstance(x, list):
        if not x:
            detail(ctx, path, '(empty list)', 'missing', True, None, 'Empty list'); return ['missing']
        vals = []
        for i, v in enumerate(x): vals += leaf_status(v, f'{path}/{i}', ctx)
        if not vals: detail(ctx, path, '(no status key)', 'missing', True, None, 'List without status entries')
        return vals or ['missing']
    detail(ctx, path, '(non-object value)', 'missing', True, None, f'Plain value {cell_text(x)}')
    return ['missing']


def summarize(x, ctx):
    """Cell status for one property: unrecognized first, then the legacy priority order."""
    start = len(details)
    vals = leaf_status(x, '', ctx)
    u = set(vals)
    if len(u) > 1: issues.append((ctx['issue_path'], MIXED, ', '.join(sorted(u))))
    unknown = sorted(v for v in u if v.startswith(UNRECOGNIZED))
    cell = '; '.join(unknown) if unknown else next((s for s in PRIORITY if s in u), 'missing')
    for row in details[start:]: row[9] = cell
    return cell, len(u) > 1


def cell_text(v):
    """Excel-safe text for lists / objects; lists are joined with ',' as in the original matrix."""
    if v is None or isinstance(v, (int, float, bool)): return v
    if isinstance(v, list): v = ','.join(str(i) for i in v)
    elif isinstance(v, dict): v = json.dumps(v, ensure_ascii=False)
    v = str(v)
    return v[:32000] + ' [truncated]' if len(v) > 32000 else v


def long_path(p):
    """Windows extended-length path so files beyond the 260-character limit are never skipped."""
    s = str(p)
    return '\\\\?\\' + s if os.name == 'nt' and not s.startswith('\\\\?\\') else s


def discover(input_dir):
    """Every .json file under input_dir, as sorted posix paths starting with the folder name."""
    root = long_path(input_dir); found = []
    def unreadable(err): issues.append((str(err.filename), 'Unreadable folder', str(err)))
    for dirpath, dirnames, filenames in os.walk(root, onerror=unreadable):
        rel = os.path.relpath(dirpath, root)
        for f in filenames:
            if f.lower().endswith('.json'):
                parts = [input_dir.name] + ([] if rel == '.' else rel.split(os.sep)) + [f]
                found.append('/'.join(parts))
    return sorted(found)


def load(input_dir):
    global json_count
    for path in discover(input_dir):
        json_count += 1
        try:
            with open(long_path(input_dir.parent.joinpath(*path.split('/'))), encoding='utf-8') as fh: doc = json.load(fh)
        except OSError as e:
            issues.append((path, 'Unreadable file', str(e))); continue
        except Exception as e:
            issues.append((path, 'Invalid JSON', str(e))); continue
        cl = doc.get('material_class'); rid = doc.get('record_id'); tier = doc.get('tier')
        if cl not in CLASSES or not rid:
            issues.append((path, 'Invalid identity', str((cl, rid)))); continue
        folder = path.rsplit('/', 1)[0]
        item = records.setdefault((cl, folder), {'files': [], 'tiers': {}, 'product': {}, 'fields': {}, 'mixed': set(),
                                                 'record_id': path.rsplit('/', 2)[-2]})
        item['files'].append(path); item['product'].update({k: v for k, v in doc.get('product', {}).items() if v is not None})
        if tier in item['tiers']: issues.append((path, 'Duplicate tier', str(tier)))
        item['tiers'][tier] = path
        for name, value in doc.get('fields', {}).items():
            # Expose meaningful nested properties as columns while retaining parent aggregation.
            candidates = {name: value}
            if name == 'api_group_chemistry' and isinstance(value, dict):
                candidates = {f'api_group_chemistry.{k}': v for k, v in value.items()}
            if name == 'elements' and isinstance(value, dict):
                candidates = {f'elements.{k}': v for k, v in value.items()}
            for field, val in candidates.items():
                if field in item['fields']: issues.append((path, 'Duplicate property', field))
                ctx = {'class': cl, 'record_id': item['record_id'], 'tier': tier, 'file': path, 'field': field,
                       'issue_path': f'{path}/{field}'}
                item['fields'][field], mixed = summarize(val, ctx)
                if mixed: item['mixed'].add(field)


def header(ws, ref_row, ncols, fill=HEADER_FILL, height=None):
    for c in range(1, ncols + 1):
        cell = ws.cell(ref_row, c); cell.fill = fill; cell.font = WHITE_BOLD
        cell.alignment = Alignment(vertical='center', wrap_text=True)
    if height: ws.row_dimensions[ref_row].height = height


def widths(ws, values):
    for i, w in enumerate(values, 1): ws.column_dimensions[get_column_letter(i)].width = w


def write_rows(ws, rows, start=1):
    for r, row in enumerate(rows, start):
        for c, v in enumerate(row, 1): ws.cell(r, c, v)


def build(input_dir):
    wb = Workbook(); summary = wb.active; summary.title = 'Overview'
    write_rows(summary, [['TASK 4 | COVERAGE MATRIX', 'Products', 'JSON files', 'Source folder'],
                         ['Corrected Task 3 JSON audit', len(records), json_count, input_dir.name], [],
                         ['Material class', 'Products', 'Reported cells', 'Calculated cells', 'Missing / N.A. cells']])
    unknown_cells = 0
    for idx, (cl, label) in enumerate(CLASSES.items()):
        subset = sorted(((folder, item) for (c, folder), item in records.items() if c == cl), key=lambda t: t[0])
        fields = sorted(set().union(*(set(item['fields']) for _, item in subset))) if subset else []
        headers = ['Record ID', 'Product name', 'Supplier', 'Source document', 'Tiers present'] + fields
        sh = wb.create_sheet(label); write_rows(sh, [headers]); counts = collections.Counter()
        for r, (folder, item) in enumerate(subset, 2):
            rid = item['record_id']; p = item['product']
            row = [rid, cell_text(p.get('product_name', rid)), cell_text(p.get('supplier', '')),
                   cell_text(p.get('source_file', '')), ', '.join(map(str, sorted(item['tiers'], key=str)))]
            for c, f in enumerate(fields, 6):
                if f in item['fields']: v = item['fields'][f]
                else:
                    v = 'missing'; issues.append((rid, 'Property absent from JSON', f))
                counts[v] += 1; row.append(v)
                if v.startswith(UNRECOGNIZED): sh.cell(r, c).fill = ERROR_FILL; unknown_cells += 1
                elif f in item['mixed']: sh.cell(r, c).fill = MIXED_FILL
            for c, v in enumerate(row, 1): sh.cell(r, c, v)
            if not EXPECTED_TIERS[cl].issubset(item['tiers']):
                issues.append((rid, 'Expected tier missing', str(sorted(EXPECTED_TIERS[cl] - set(item['tiers'])))))
        header(sh, 1, len(headers), height=30)
        widths(sh, [26, 28, 32, 23, 16] + [20] * len(fields)); sh.freeze_panes = 'A2'
        write_rows(summary, [[label, len(subset), counts['reported'], counts['calculated'],
                              counts['missing'] + counts['not_applicable']]], start=5 + idx)

    # Record all normalization warnings and anomalies without editing input JSON.
    all_issues = sorted(set(tuple(str(t) for t in i) for i in issues))
    audit = wb.create_sheet('Validation Issues')
    write_rows(audit, [['JSON path / product', 'Issue', 'Detail']] + [list(i) for i in all_issues])
    header(audit, 1, 3); widths(audit, [62, 27, 65]); audit.freeze_panes = 'A2'

    sd = wb.create_sheet('Status Detail')
    write_rows(sd, [['Material class', 'Record ID', 'Tier', 'JSON file', 'Property (matrix column)', 'Sub-path',
                     'Original status', 'Normalized status', 'Counted in matrix cell', 'Matrix cell status', 'Value',
                     'Source file / URL', 'Source page', 'Note']] + details)
    header(sd, 1, 14); widths(sd, [18, 26, 6, 60, 28, 34, 16, 18, 12, 18, 30, 30, 10, 50]); sd.freeze_panes = 'A2'
    sd.auto_filter.ref = sd.dimensions

    ta = wb.create_sheet('Traceability Audit')
    write_rows(ta, [['Finding', 'Severity', 'Material class', 'Record ID', 'JSON file', 'Property (matrix column)', 'Sub-path',
                     'Status', 'Value', 'Basis', 'Source file / URL', 'Source page', 'Note']] + trace)
    header(ta, 1, 13); widths(ta, [44, 10, 18, 26, 60, 28, 30, 10, 30, 30, 40, 10, 60]); ta.freeze_panes = 'A2'
    ta.auto_filter.ref = ta.dimensions

    blocking = [i for i in all_issues if i[1] in BLOCKING]
    trace_counts = collections.Counter((t[0], t[1]) for t in trace)
    write_rows(summary, [['Validation findings', len(all_issues)],
                         ['Unrecognized statuses / structural errors', sum(1 for i in all_issues if i[1] not in REVIEW)],
                         ['STATUS KEY', 'Interpretation'], ['reported', 'Explicit source-reported'],
                         ['calculated', 'Calculated in JSON'], ['missing', 'Missing, empty, or unclassified'],
                         ['not_applicable', 'Not Required / N/A'],
                         ['Mixed nested statuses', 'Priority status displayed; see Validation Issues'],
                         ['Note on parent cells', 'A cell marked reported may still contain missing subfields '
                          '(e.g. one CCS temperature reported, another missing). Every subfield and its original '
                          'status is listed in Status Detail; mixed cells are shaded amber.'],
                         [], ['RUN STATUS', 'FAILED - diagnostic workbook, not the official matrix' if blocking else 'PASSED'],
                         ['Blocking findings', len(blocking)], ['Unrecognized status cells', unknown_cells],
                         ['Status Detail rows', len(details)], [],
                         ['TRACEABILITY AUDIT', 'Findings', 'Severity']]
               + [[k, v, sev] for (k, sev), v in sorted(trace_counts.items(), key=lambda kv: (kv[0][1] != WARN, kv[0][0]))],
               start=8)
    for ref in ('A1:D1', 'A4:E4', 'A10:B10', 'A18:B18', 'A23:C23'):
        first, last = ref.split(':'); r = int(first[1:])
        header(summary, r, ord(last[0]) - 64, HEADER_FILL if r == 1 else SUBHEADER_FILL, 28 if r == 1 else None)
    summary['B16'].alignment = Alignment(wrap_text=True, vertical='top'); summary.row_dimensions[16].height = 60
    if blocking: summary['B18'].fill = ERROR_FILL
    widths(summary, [34, 26, 22, 27, 27])
    return wb, all_issues, blocking


def save(wb, target):
    """Write to a temp file first so a failed save never leaves a half-written workbook."""
    fd, tmp = tempfile.mkstemp(suffix='.xlsx', dir=target.parent); os.close(fd)
    try:
        wb.save(tmp); os.replace(tmp, target)
    finally:
        if os.path.exists(tmp): os.remove(tmp)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--input', default='Products_json', help='product JSON folder (default: Products_json)')
    ap.add_argument('--output', default='Coverage_Matrix.xlsx', help='workbook to write (default: Coverage_Matrix.xlsx)')
    ap.add_argument('--overwrite', action='store_true', help='allow replacing an existing output workbook')
    ap.add_argument('--sources', default='source_registry.json',
                    help='registry of external sources (default: source_registry.json; if absent, every URL is reported as unregistered)')
    args = ap.parse_args()
    input_dir, output = Path(args.input).resolve(), Path(args.output).resolve()
    if not input_dir.is_dir(): sys.exit(f'ERROR: input folder not found: {input_dir}')
    registry = Path(args.sources)
    if registry.is_file():
        try:
            entries = json.loads(registry.read_text(encoding='utf-8'))['sources']
        except (OSError, ValueError, KeyError) as e:
            sys.exit(f'ERROR: cannot read source registry {registry}: {e}')
        for e in entries:
            if e.get('status') not in REGISTRY_STATUSES or e.get('format') not in ('pdf', 'html') or not e.get('url'):
                sys.exit(f'ERROR: invalid source registry entry: {e.get("url")}')
            sources[e['url']] = e
    if output.exists() and not args.overwrite:
        sys.exit(f'ERROR: {output} already exists; pass --overwrite to replace it')
    output.parent.mkdir(parents=True, exist_ok=True)
    load(input_dir)
    wb, all_issues, blocking = build(input_dir)
    if blocking:
        diag = output.with_name(output.stem + '_DIAGNOSTIC.xlsx'); save(wb, diag)
        print(f'VALIDATION FAILED: {len(blocking)} blocking finding(s); {output.name} was NOT written.')
        for path, kind, det in blocking[:20]: print(f'  {kind}: {path} ({det})')
        print(f'Diagnostic workbook: {diag}')
        sys.exit(2)
    save(wb, output)
    print('OUTPUT', output, 'products', len(records), 'json', json_count, 'issues', len(all_issues),
          'classes', dict(collections.Counter(k[0] for k in records)), 'status', dict(statuses))
    for sev in (WARN, INFO):
        print(f'traceability {sev}s', dict(collections.Counter(t[0] for t in trace if t[1] == sev)))


if __name__ == '__main__':
    main()
