# Saved from the session scratchpad on 2026-11-13 (thirteenth pass). Runs from any directory: it changes to the
# workspace root (the folder that holds Products_json and existing_product_comparison_2026-11-12).
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import subprocess,sys,re,difflib
S='existing_product_comparison_2026-11-12/scripts/show.py'
def t(side,f,p):
    o=subprocess.run([sys.executable,S,side,f,p,'100000'],capture_output=True,text=True,encoding='utf-8').stdout
    return o.split('---',2)[-1]
for a in sys.argv[1:]:
    cat,pg,side,old,opg=a.split('|')
    A,Bt=t(side,old,opg),t('new',cat,pg)
    wa,wb=re.findall(r'[A-Za-z0-9.%≥≤≯≮℃\-]+',A),re.findall(r'[A-Za-z0-9.%≥≤≯≮℃\-]+',Bt)
    sm=difflib.SequenceMatcher(None,wa,wb,autojunk=False)
    d=[(op,' '.join(wa[i1:i2])[:200],' '.join(wb[j1:j2])[:200]) for op,i1,i2,j1,j2 in sm.get_opcodes() if op!='equal']
    print(f'== {cat} p{pg} vs {old} ({side}) words {len(wa)}/{len(wb)} ratio {sm.ratio():.3f}')
    for x in d[:25]: print('   ',x)
