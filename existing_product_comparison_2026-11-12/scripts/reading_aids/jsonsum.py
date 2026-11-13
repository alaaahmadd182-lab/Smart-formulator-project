"""Compact JSON summary for a product (read-only): every non-missing value object (nested included) with value, min/max,
qualifier, unit, method, source file/page; plus open-question and conflict counts. Usage: python jsonsum.py PID [PID ...]"""
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import glob, json, sys
for pid in sys.argv[1:]:
    out = []
    for jf in sorted(glob.glob(f'Products_json/**/{pid}/*.json', recursive=True)):
        d = json.load(open(jf, encoding='utf-8'))
        def walk(k, v):
            if isinstance(v, dict):
                if 'status' in v and v.get('status') not in ('Missing', None) and ('value' in v or 'printed_text' in v):
                    s = v.get('source') if isinstance(v.get('source'), dict) else {}
                    out.append(f"{k}={v.get('value')}{'' if v.get('min') is None and v.get('max') is None else ' ['+str(v.get('min'))+'..'+str(v.get('max'))+']'} {v.get('qualifier') or ''}{v.get('unit') or ''} {v.get('method') or ''} <{s.get('file')} p{s.get('page')}> '{str(v.get('printed_text'))[:70]}'")
                for a, b in v.items():
                    if a not in ('source', 'alternate_entries'):
                        walk(f'{k}.{a}' if k else a, b)
            elif isinstance(v, list):
                for i, b in enumerate(v):
                    walk(f'{k}[{i}]', b)
        walk('', d['fields'])
        oq = d.get('open_questions', [])
        out.append(f"[{_os.path.basename(jf)[-34:]}] OQ {len(oq)}: " + ' || '.join((q if isinstance(q, str) else json.dumps(q, ensure_ascii=False))[:160] for q in oq))
    print('#####', pid); print('\n'.join(dict.fromkeys(out)))
