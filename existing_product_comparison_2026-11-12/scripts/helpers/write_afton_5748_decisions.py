"""One-off helper (kept for the record): writes decisions/zzz_afton_5748_third_pass.json from the review of the 30
documents that name HiTEC 5748. Re-running it rewrites the same file. Usage: python write_afton_5748_decisions.py
"""
import json, os

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = 'AFTON_HITEC_5748'
REC = "Dose evidence inside formulations of another package; it stays with those recipes and is not a treat range of the viscosity modifier. "
OLD = ("Afton HiTEC 5748 PDS 05/23 (registered external source; local evidence copy "
       "reconciliation/audit_evidence/Afton_HiTEC-5748_PDS_05-23__wayback_20241005085229.pdf) re-read in this pass, p.2: ")
REV = 're-read manually (local evidence copy of the cited 05/23 bulletin, 2 pages)'


def L(f, cat, note, ident='exact name; neighbouring grade HiTEC 5748A excluded by the search pattern'):
    return dict(p=P, f=f, cat=cat, status='completed', fields_status='hit lines read in the text layer; tables not verified visually',
                coverage='not applicable (evidence about other packages; the HiTEC 5748 record has no field for recipe doses)', identity=ident, note=note)


links = [
    L('DL2-11597.pdf', 'D', "Afton HiTEC 9450 book (31 pp.). p.4: 'HiTEC 5748 VM was used in Engine testing and HiTEC 5748A will be used in the final formulation. It possible to interchange between viscosity modifiers HiTEC 5748 & HiTEC 5748A by following ... API 1509 Base Oil Interchangeability guidelines'. Formulation tables pp.10-27 not read."),
    L('DL2-13684.pdf', 'D', REC + "Afton HiTEC 8788LA book (49 pp.); p.5 'HiTEC 5748 VM, a cost effective OCP diluted in group I base oil'. Formulation pages not read."),
    L('DL2-12557.pdf', 'D', REC + "Afton HiTEC 8801 book (55 pp.); p.8 recipes with HiTEC 5748 7.5 and 10."),
    L('DL2-12552.pdf', 'D', REC + "HiTEC 11500 formulation sheets (9 pp.): 3.5-3.7 with HiTEC 11500 13.1 in Yubase 4+."),
    L('DL2-15778.pdf', 'D', REC + "HiTEC 11500 formulation sheets (9 pp.), same layout as DL2-12552.pdf."),
    L('DL2-15777.pdf', 'D', REC + "HiTEC 11500 API SQ programme book (18 pp.)."),
    L('DL2-15678.pdf', 'D', REC + "Afton API SQ presentation (23 pp.): 5.70-7.40 %wt, p.10."),
    L('DL2-15688.pdf', 'D', REC + "Afton API SQ presentation (23 pp.), same hit lines as DL2-15678.pdf."),
    L('DL2-15591.pdf', 'D', REC + "One-page formulation table: 3.00-10.20."),
    L('DL2-15013.pdf', 'D', REC + "HiTEC 11410 presentation (27 pp.): 4.30 in SAE 0W-20 with Yubase 4 plus."),
    L('DL2-15140.pdf', 'D', REC + "HiTEC 9490 book (37 pp.): 12.9 with HiTEC 9490 12.6 in Nexbase 3043 (p.16)."),
    L('DL2-15070.pdf', 'D', "HiTEC 11600 presentation (42 pp.): names HiTEC 5748 as the VM of SK Yubase and EHC routes (pp.24-25); no dose in the hit lines."),
    L('DL2-15799.pdf', 'D', REC + "HiTEC 11455 GF-7B programme book (36 pp.); p.5 lists HiTEC 5748 and HiTEC 5748A as viscosity modifiers tested, in different columns."),
    L('HiTEC%2011356_API%20SQ%20CDP%20-%20Version%201_20260525_updated.pdf', 'D', REC + "HiTEC 11356 API SQ programme book (35 pp.); p.6 read-across limit 'HiTEC 5748 <= 13.50%'."),
    L('HiTEC%2022300%20CDP_API%20SL%20AramcoPrima.pdf', 'D', REC + "HiTEC 22300 API SL programme book in Aramco Prima (40 pp.)."),
    L('DL2-15690.pdf', 'D', REC + "HiTEC 11356 API SP programme summary (14 pp.). The inventory classified it as an SDS; it is a programme document. p.4 lists HiTEC 5748A and HiTEC 5748 in different columns."),
    L('DL2-12086.pdf', 'D', "HiTEC 9490 book, March 2018 (5 pp.): 'with HiTEC 5748 or HiTEC 5748A Non-Dispersant OCP (ND-OCP) Viscosity Modifier' (p.1)."),
    L('DL2-15362.pdf', 'D', "Afton reduced-SAPS bulletin: footnotes name 'HiTEC 5748 OCP VM, HiTEC 672 PPD' for Yubase / Ultra-S routes; no dose."),
    L('DL2-15012.pdf', 'D', "HiTEC 11410 bulletin: footnotes name 'HiTEC 5748 OCP VM'; no dose."),
    L('DL2-13580.pdf', 'D', "HiTEC 11410 bulletin (ACEA 2016): 'Yubase Group III, HiTEC 5748 OCP VM, HiTEC 672 PPD'; no dose."),
    L('DL2-14894.pdf', 'D', "Afton full-SAPS bulletin: 'Viscosity Modifier: HiTEC 5748 OCP'; no dose."),
    L('DL2-15689.pdf', 'C,D', "HiTEC 11356 bulletin: 'Afton's OCP VM solution HiTEC 5748'; pairing statement, no dose."),
    L('DL2-14882.pdf', 'C,D', "HiTEC 11456 bulletin: 'Afton's OCP VM solution HiTEC 5748, both are produced in Singapore'; no dose."),
    L('DL2-15336.pdf', 'C,D', "Afton GF-6 bulletin: 'Afton liquid VM HiTEC 5748 Made In Singapore'; no dose."),
    L('DL2-12551.pdf', 'C', "Portfolio slide p.12 pairing packages with HiTEC 5748; further hits pp.13-17 not read."),
    L('DL2-15748.pdf', 'C', "Portfolio slide p.12; further hits pp.13-14 not read."),
    L('DL2-15465.pdf', 'D,E', "HiTEC 11456 presentation, July 2021 (20 pp.): p.13 'Viscosity Modifier HiTEC 5748 (25 SSI)'; p.20 'HiTEC 5748 (25 SSI olefin copolymer viscosity modifier)'. A statement about the product itself."),
    L('DL2-14915.pdf', 'D,E', REC + "'Final Formulations, last updated by SA 20211224' (4 pp.): two recipes in % wt. AND % vol. with Etro plus 4 / Etro plus 6, HiTEC 11456 8.30 and HiTEC 5748 3.50 / 6.40 % wt. (3.43 / 6.28 % vol.); the component column prints Density @ 15.6 C 0.8603 for HiTEC 5748. Result values are not paired with rows in the text layer. Lead for the Petronas batch: 'Etro plus 4' kV100 4.137, density 0.8290; 'Etro plus 6' 6.057, 0.8416."),
    L('HiTEC-5825K_PDS.pdf', 'D,E', "Afton bulletin of HiTEC 5825K (solid OCP): 'HiTEC 5825K may be dissolved in a wide range of base oils to produce liquid HiTEC 5748 Viscosity Modifier'. A statement about how HiTEC 5748 is made; the bulletin is not a HiTEC 5748 sheet.", ident='HiTEC 5748 named in the text of the HiTEC 5825K bulletin'),
    L('DL2-11395.pdf', 'C,G', "Afton note 'Manufacturing Process of Liquid Viscosity Modifier from Polymer HiTEC 5825H', October 2016: typical properties of 'a viscosity modifier ANALOGOUS to Afton's HiTEC 5748' (12.5 +/- 0.5 wt% 5825H in Group I 150N). Analogous is not identical: nothing here is a property of HiTEC 5748.", ident="name used only in 'analogous to Afton's HiTEC 5748'"),
]


def F(tier, path, old, new_f, new_p, new_text, unit, form, cond, basis, outcome, action, reason, tokens=None):
    d = dict(p=P, tier=tier, path=path, old=OLD + old, new_f=new_f, new_p=new_p, new_text=new_text, unit=unit, form=form, qual='', method='not printed', cond=cond, basis=basis,
             outcome=outcome, action=action, reason=reason, old_rev=REV)
    if tokens:
        d['check_tokens'] = tokens
    return d


fields = [
    F(2, 'shear_stability', "'Shear Stability Index %: 22'. The record's open_questions already list 22 (05/23, 04/21, 03/18), '23 SSI polymer' (07/11) and '25SSI' from DL2-13692.pdf (07/20).",
      'DL2-15465.pdf', 13, "Viscosity Modifier | HiTEC 5748 (25 SSI); p.20 'HiTEC 5748 (25 SSI olefin copolymer viscosity modifier)'", 'SSI', "descriptive label in another product's presentation", 'July 2021', '',
      'already_captured', 'propose_open_question_update',
      "A second Afton document calling HiTEC 5748 '25 SSI'. The discrepancy with the bulletin's 22 is ALREADY recorded in the record (from DL2-13692.pdf); this adds one more citation to that open question and nothing else. Not resolved, not averaged; the selected 22 stays.",
      ['25SSI', '22']),
    F(2, 'polymer_chemistry', "title 'Non-Dispersant Olefin Copolymer Viscosity Modifier'; no statement on how the liquid is made; no polymer content.",
      'HiTEC-5825K_PDS.pdf', 2, "HiTEC 5825K may be dissolved in a wide range of base oils to produce liquid HiTEC 5748 Viscosity Modifier. (Also printed, for 5825K only: 'Properties of 12.0% wt. HiTEC 5825K dissolved in ExxonMobil EHC 50')",
      '', 'text', '', '', 'additional', 'propose_note',
      "New fact about the product: liquid HiTEC 5748 is made by dissolving the solid OCP HiTEC 5825K in base oil. Propose a note in polymer_chemistry. The 12.0 % wt. figure describes a 5825K solution in EHC 50 and is NOT stated to be the polymer content of HiTEC 5748: active_polymer stays Missing.",
      ['5825K', 'solid polymer']),
    F(1, 'compatibility_restrictions', 'no statement on interchange with HiTEC 5748A.',
      'DL2-11597.pdf', 4, "HiTEC 5748 VM was used in Engine testing and HiTEC 5748A will be used in the final formulation. It possible to interchange between viscosity modifiers HiTEC 5748 & HiTEC 5748A by following the Guidelines documented in Annex E section E. 2.1.3 of ... API 1509 Base Oil Interchangeability guidelines.",
      '', 'text', 'HiTEC 9450 programme (ACEA C3/C2-12), Yubase Group III', '', 'additional', 'propose_note',
      "A conditional interchange statement made for one programme. Propose a note with that scope; it does not make the two grades the same product and no 5748A data may be used for HiTEC 5748."),
    F(1, '(no template field) density', "'Specific Gravity @ 15.6/15.6 C: 0.855' (kept in open_questions; no template field).",
      'DL2-14915.pdf', 1, "Components | kV100, cSt | Density @ 15.6 C: 'HiTEC 5748, Non-Dispersant Viscosity Modifier | -- | 0.8603'", 'not printed (density column)',
      'component value used in a formulation calculation (not a typical or a specification)', '15.6 C', '', 'changed_or_conflicting', 'no_change',
      "0.8603 against the bulletin's 0.855. The formulation sheet does not say whether 0.8603 is a batch value; it is not a data-sheet typical and there is no template field. Recorded as evidence only."),
    F(2, 'treat_range_by_sae_grade', "'HiTEC 5748 (vol.)' 5W-30 8.0% (8.0%); 10W-30 5.7% (5.8%); 10W-40 11.6% (11.8%); 15W-40 5.4% (5.5%); 20W-50 5.4% (5.5%), captured in the record as vol.% dosages.",
      'DL2-12552.pdf', 2, "Recipe doses in other packages' formulations across 17 documents, e.g. 3.5-3.7 (HiTEC 11500), 4.30 (HiTEC 11410 0W-20), 12.9 (HiTEC 9490 5W-40), 5.70-7.40 (API SQ), in % wt",
      '% wt', 'doses in individual recipes of other packages', 'per recipe', 'mass', 'not_comparable', 'no_change',
      "Recipe doses depend on package, grade and base oil; they are not the viscosity modifier's treat range and are not comparable with the bulletin's stay-in-grade vol.% dosages. No change to the HiTEC 5748 record; the recipes belong with the packages when those are reviewed or ingested."),
]
docs = {l['f']: dict(what=l['note'][:170], printed_date='as stated in the note where read', kind='see note', read='lines around each hit of the product name (text layer)',
                     limits='not read beyond the hit lines unless the note says so') for l in links}
queue = [dict(name_as_printed=n, supplier='Afton', file=f, page=p, evidence=e) for n, f, p, e in [
    ('HiTEC 5825K', 'HiTEC-5825K_PDS.pdf', '1-2', 'own product bulletin (solid OCP; precursor of liquid HiTEC 5748)'), ('HiTEC 5825H', 'DL2-11395.pdf', '1-7', 'manufacturing note, October 2016'),
    ('HiTEC 9450', 'DL2-11597.pdf', '1-31', 'PCMO package programme book'), ('HiTEC 8788LA', 'DL2-13684.pdf', '1-49', 'programme book'), ('HiTEC 8801', 'DL2-12557.pdf', '1-55', 'programme book'),
    ('HiTEC 11500', 'DL2-15777.pdf', '1-18', 'API SQ programme book and formulation sheets'), ('HiTEC 11410', 'DL2-15013.pdf', '1-27', 'presentation and bulletins'),
    ('HiTEC 11456', 'DL2-15465.pdf', '1-20', 'presentation, bulletin, final formulations'), ('HiTEC 11356', 'DL2-15689.pdf', '1-2', 'bulletin and programme books'),
    ('HiTEC 11455', 'DL2-15799.pdf', '1-36', 'programme book'), ('HiTEC 11600', 'DL2-15070.pdf', '24-25', 'presentation'),
    ('HiTEC 22300', 'HiTEC%2022300%20CDP_API%20SL%20AramcoPrima.pdf', '1-40', 'API SL programme book in Aramco Prima')]]
out = dict(batch='afton', reviewed_on='2026-11-12 (third pass)',
           note='HiTEC 5748 named in 30 documents of other products. Read: the text around every hit; the cited 05/23 bulletin was re-read from its local evidence copy.',
           documents=docs, links=links, fields=fields, new_product_candidates=queue)
with open(os.path.join(BASE, 'decisions', 'zzz_afton_5748_third_pass.json'), 'w', encoding='utf-8') as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
print(len(links), 'links;', len(fields), 'field rows')
