#!/usr/bin/env python3
"""Task 4 coverage matrix from source JSON ZIP; no property values are inferred."""
import json, zipfile, collections, sys, os
from artifact_tool import Workbook, SpreadsheetFile
INPUT=sys.argv[1] if len(sys.argv)>1 else '/mnt/data/Products_json.zip'
OUTPUT=sys.argv[2] if len(sys.argv)>2 else '/mnt/data/Task_4_Coverage_Matrix_Corrected.xlsx'
CLASSES={'base_oil':'Base Oils','additive_package':'Additive Packages','additive_component':'Additive Components'}
STATUS={'reported':'reported','calculated':'calculated','missing':'missing','not required':'not_applicable','not_applicable':'not_applicable','not applicable':'not_applicable','n/a':'not_applicable'}
records={};issues=[]; statuses=collections.Counter(); json_count=0

def leaf_status(x,path):
    """Return leaf status list; mark unclassified evidence for audit, never assume reported."""
    if isinstance(x,dict):
        if 'status' in x:
            raw=str(x['status']).strip(); key=raw.lower(); statuses[raw]+=1
            if key in STATUS: return [STATUS[key]]
            issues.append((path,'Unknown status',raw));return ['missing']
        vals=[]
        for k,v in x.items():
            if k in ('source','notes','calculation_note','method','printed_text','external_fill_notes'):continue
            if isinstance(v,(dict,list)):vals+=leaf_status(v,path+'/'+k)
        if vals:return vals
        # status-free data cannot be certified as reported
        if any(k in x for k in ('value','min','max','wt_pct','type','form')):
            issues.append((path,'Unclassified status-free field','Needs manual status review'))
        return ['missing']
    if isinstance(x,list):
        if not x:return ['missing']
        vals=[]
        for i,v in enumerate(x):vals+=leaf_status(v,path+'/'+str(i))
        return vals or ['missing']
    return ['missing']

def summarize(x,path):
    vals=leaf_status(x,path)
    u=set(vals)
    if len(u)>1:
        issues.append((path,'Mixed nested statuses (review)',', '.join(sorted(u))))
        # Reported if any explicit reported or calculated, with mixed-status audit flag.
    for s in ('reported','calculated','missing','not_applicable'):
        if s in u:return s
    return 'missing'

with zipfile.ZipFile(INPUT) as z:
    for path in sorted(z.namelist()):
        if not path.lower().endswith('.json'):continue
        json_count+=1
        try:doc=json.loads(z.read(path))
        except Exception as e:issues.append((path,'Invalid JSON',str(e)));continue
        cl=doc.get('material_class'); rid=doc.get('record_id'); tier=doc.get('tier')
        if cl not in CLASSES or not rid:
            issues.append((path,'Invalid identity',str((cl,rid))));continue
        key=(cl,path.rsplit('/',1)[0]); item=records.setdefault(key,{'files':[],'tiers':{},'product':{},'fields':{},'record_id':path.rsplit('/',2)[-2]})
        item['files'].append(path);item['product'].update({k:v for k,v in doc.get('product',{}).items() if v is not None})
        if tier in item['tiers']:issues.append((path,'Duplicate tier',str(tier)))
        item['tiers'][tier]=path
        for name,value in doc.get('fields',{}).items():
            # Expose meaningful nested properties as columns while retaining parent aggregation.
            candidates={name:value}
            if name=='api_group_chemistry' and isinstance(value,dict):
                candidates={f'api_group_chemistry.{k}':v for k,v in value.items()}
            if name=='elements' and isinstance(value,dict):
                candidates={f'elements.{k}':v for k,v in value.items()}
            for field,val in candidates.items():
                if field in item['fields']:issues.append((path,'Duplicate property',field))
                item['fields'][field]=summarize(val,path+'/'+field)

wb=Workbook.create()
summary=wb.worksheets.add('Overview')
summary.get_range('A1:D1').values=[['TASK 4 | COVERAGE MATRIX','Products','JSON files','Source archive']]
summary.get_range('A2:D2').values=[['Corrected Task 3 JSON audit',len(records),json_count,os.path.basename(INPUT)]]
summary.get_range('A4:E4').values=[['Material class','Products','Reported cells','Calculated cells','Missing / N.A. cells']]

for idx,(cl,label) in enumerate(CLASSES.items()):
    subset=sorted([(rid,item) for (c,rid),item in records.items() if c==cl])
    fields=sorted(set().union(*(set(item['fields']) for _,item in subset))) if subset else []
    headers=['Record ID','Product name','Supplier','Source document','Tiers present']+fields
    matrix=[headers]; counts=collections.Counter()
    for folder,item in subset:
        rid=item['record_id']; p=item['product']; row=[rid,p.get('product_name',rid),p.get('supplier',''),p.get('source_file',''),', '.join(map(str,sorted(item['tiers'])))];
        for f in fields:
            if f in item['fields']:v=item['fields'][f]
            else:
                v='missing';issues.append((rid,'Property absent from JSON',f))
            counts[v]+=1;row.append(v)
        matrix.append(row)
        expected={'base_oil':{1,2,3},'additive_package':{1,2},'additive_component':{1}}[cl]
        if not expected.issubset(item['tiers']):issues.append((rid,'Expected tier missing',str(sorted(expected-set(item['tiers'])))))
    sh=wb.worksheets.add(label)
    # Write blocks to keep memory bounded.
    for start in range(0,len(matrix),75):
        block=matrix[start:start+75]
        sh.get_range_by_indexes(start,0,len(block),len(headers)).values=block
    sh.get_range_by_indexes(0,0,1,len(headers)).format={'fill':'#17324D','font':{'bold':True,'color':'#FFFFFF'},'row_height':30}
    sh.get_range_by_indexes(0,0,len(matrix),1).format.column_width=26
    sh.get_range_by_indexes(0,1,len(matrix),1).format.column_width=28
    sh.get_range_by_indexes(0,2,len(matrix),1).format.column_width=32
    sh.get_range_by_indexes(0,3,len(matrix),1).format.column_width=23
    sh.get_range_by_indexes(0,4,len(matrix),1).format.column_width=16
    if fields:
        sh.get_range_by_indexes(0,5,len(matrix),len(fields)).format.column_width=20
    sh.freeze_panes.freeze_rows(1)
    summary.get_range_by_indexes(4+idx,0,1,5).values=[[label,len(subset),counts['reported'],counts['calculated'],counts['missing']+counts['not_applicable']]]

# Record all normalization warnings and anomalies without editing input JSON.
issues=sorted(set(tuple(str(t) for t in i) for i in issues))
audit=wb.worksheets.add('Validation Issues')
audit.get_range('A1:C1').values=[['JSON path / product','Issue','Detail']]
for start in range(0,len(issues),200):
    block=[list(x) for x in issues[start:start+200]]
    audit.get_range_by_indexes(start+1,0,len(block),3).values=block
audit.get_range('A1:C1').format={'fill':'#17324D','font':{'bold':True,'color':'#FFFFFF'}}
audit.get_range('A:A').format.column_width=62
audit.get_range('B:B').format.column_width=27
audit.get_range('C:C').format.column_width=65
audit.freeze_panes.freeze_rows(1)
summary.get_range('A10:B15').values=[['STATUS KEY','Interpretation'],['reported','Explicit source-reported'],['calculated','Calculated in JSON'],['missing','Missing, empty, or unclassified'],['not_applicable','Not Required / N/A'],['Mixed nested statuses','Priority status displayed; see Validation Issues']]
summary.get_range('A1:D1').format={'fill':'#17324D','font':{'bold':True,'color':'#FFFFFF'},'row_height':28}
summary.get_range('A4:E4').format={'fill':'#245B73','font':{'bold':True,'color':'#FFFFFF'}}
summary.get_range('A10:B10').format={'fill':'#245B73','font':{'bold':True,'color':'#FFFFFF'}}
summary.get_range('A:A').format.column_width=34
summary.get_range('B:B').format.column_width=26
summary.get_range('C:C').format.column_width=22
summary.get_range('D:D').format.column_width=27
summary.get_range('E:E').format.column_width=27
summary.get_range('A8:B9').values=[['Validation findings',len(issues)],['Unrecognized statuses / structural errors',sum(1 for i in issues if i[1] != 'Mixed nested statuses (review)')]]
SpreadsheetFile.export_xlsx(wb).save(OUTPUT)
print('OUTPUT',OUTPUT,'products',len(records),'json',json_count,'issues',len(issues),'classes',collections.Counter(k[0] for k in records),'status',statuses)
