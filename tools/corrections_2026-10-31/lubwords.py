import sys, zipfile, io, re, fitz
sys.stdout.reconfigure(encoding='utf-8')
z = zipfile.ZipFile(sys.argv[1])
for name in ('DL2-11503.pdf', 'DL2-15722.pdf'):
    ent = [n for n in z.namelist() if n.endswith('/' + name) or n == name]
    print('=====', name, ent)
    doc = fitz.open(stream=z.read(ent[0]), filetype='pdf')
    for pno in range(len(doc)):
        rows = {}
        for w in doc[pno].get_text('words'):
            rows.setdefault(round(w[1]), []).append((round(w[0]), w[4]))
        for y in sorted(rows):
            line = ' '.join(f'{t}@{x}' for x, t in sorted(rows[y]))
            if re.search(r'(?i)minimum|typical|target|weight|sulfated|sulfur|zinc|calcium|effective|characteristics|method', line):
                print(f'p{pno+1} y{y}:', line)
