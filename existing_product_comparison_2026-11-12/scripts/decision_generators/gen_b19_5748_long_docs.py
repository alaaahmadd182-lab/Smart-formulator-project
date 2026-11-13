"""Sixteenth pass, batch 19: the 18 long documents naming HiTEC 5748 (product link AFTON_HITEC_5748) that were limited to the
name-hit passages since the third pass. In each, EVERY page that names HiTEC 5748 or 5748A was read in full (text layer), with the
title / contents pages for identity; on two CDPs the long final-formulation pages were read for their composition blocks and every
HiTEC 5748 line only (stated per link). Document read scope is stated per link; it is a full-document read only where every page was read.
Writes decisions/zzzzzzzzzzzzzzzz_b19_5748_long_docs_sixteenth_pass.json."""
# Runs from any directory: it changes to the workspace root.
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import json
B = 'existing_product_comparison_2026-11-12'
T = '(sixteenth pass, 2026-11-14)'
P = 'AFTON_HITEC_5748'
o = ("re-read manually: Afton HiTEC 5748 PDS 05/23 (registered copy retrieved 2026-11-13, SHA-256 matches the registry; "
     "retrieved_evidence_2026-11-13/HiTEC-5748_PDS__registered_url.pdf) pp.1-2 whole text (fourteenth pass)")
POLICY = "the recipe doses are package-route data, handled by the existing 'treat_range_by_sae_grade' no_change / not_comparable row (not a HiTEC 5748 treat range); no row"
C22 = 'HiTEC%2022300%20CDP_API%20SL%20AramcoPrima.pdf'
C11 = 'HiTEC%2011356_API%20SQ%20CDP%20-%20Version%201_20260525_updated.pdf'
links, F = [], []


def link(f, cat, scope, cov):
    links.append(dict(p=P, f=f, cat=cat, status='completed', fields_status=f'{scope} {T}',
                      coverage=f'assessed by reading (2026-11-14, sixteenth pass) for {scope}: {cov}', identity="exact 'HiTEC® 5748' (grade suffix checked: 5748 vs 5748A kept apart)",
                      note="HiTEC 5748 named in another product's document; every page naming it read in full."))


def row(f, page, path, old, text, form, action, outcome, reason, cond='', cmp='existing: not recorded'):
    F.append(dict(p=P, tier=1, path=path, old=old, new_f=f, new_p=page, new_text=text, unit='as printed', form=form, qual='as printed', method='as printed', cond=cond, basis='',
                  outcome=outcome, action=action, reason=reason, old_rev=o, cmp_override=cmp))


# ---------------- reports and catalogues ----------------
link('DL2-13684.pdf', 'D', 'pp.2-5, 8, 9, 16, 20, 26, 31, 36, 42 (title, contents and every page naming HiTEC 5748) read in full; the other pages (engine-test matrices and summaries) not read',
     f"HiTEC 8788LA report No. 1099, September 2014. p.5: 'HiTEC® 8788LA program has been run using HiTEC® 5748 VM, a cost effective OCP diluted in group I base oil, and Yubase 6' and 'VM rationalisation with HiTEC® 5748 broad coverage of PCMO and HDEO segments' -> carrier open-question row. pp.8-42: SAE 10W-40 test-oil tables (HiTEC 5748 5.0 / 5.2 / 6.3 / 7.5 % wt with EYB 5284C / 5284G or HiTEC 8788LA 15.5, HiTEC 672 0.1, Yubase 6 / 4); {POLICY}.")
row('DL2-13684.pdf', 5, 'open_questions', "The record's carrier identity and share are Missing ('Active content, carrier identity/share ... are not printed; left Missing and not inferred').",
    "'HiTEC® 8788LA program has been run using HiTEC® 5748 VM, a cost effective OCP diluted in group I base oil, and Yubase 6.' (HiTEC 8788LA report No. 1099, September 2014, p.5). Related print, quoted for context only: DL2-11597.pdf (HiTEC 9450 report, November 2016) p.4 'The total interchange of Grp I to Grp II base oil (in the switch between viscosity modifiers only) is <10% so no engine testing is required.'",
    "manufacturer statement about HiTEC 5748 in another product's report (carrier described, no share)", 'propose_open_question_update', 'additional',
    "A manufacturer (Afton) sentence naming HiTEC 5748 and describing it as an OCP 'diluted in group I base oil'. It is a lead for the Missing carrier identity, not a fill: it comes from a 2014 report on another product, names a base-oil group rather than a carrier identity, gives no share, and is not in the HiTEC 5748 PDS. Propose adding it to the carrier open question with its date and source and asking Afton to confirm the carrier; carrier.identity and share_wt_pct stay Missing. The DL2-11597 sentence is quoted only as related print; nothing is derived from it.",
    cmp='existing: carrier Missing; open question says not printed')
link('DL2-12557.pdf', 'D', 'pp.1-3 and 8 (title, contents and the only page naming HiTEC 5748) read in full; the other pages not read',
     f"HiTEC 8801 STOU report No. 423/18, March 2011. p.8 'Further Formulations': 10W-30 / 10W-40 / 15W-30 / 15W-40 with HiTEC 8801 13, HiTEC 623 0.5 and HiTEC 5748 7.5 / 10 / 5 / 8 in 150SN / 100SN / 600SN / Nexbase 3043, and 'Note that not all performance claims are permitted in all viscosity grades.'; {POLICY}.")
link('DL2-11597.pdf', 'D', 'pp.1-2, 4, 6-11, 18, 23, 27 (title and every page naming HiTEC 5748) read in full; the other pages not read',
     f"HiTEC 9450 report No. 1100-3, November 2016. p.4 interchange statement already proposed (compatibility note). Final formulations use HiTEC 5748A (8.5 / 4.5 / 6.2 %); intermediate and initial oils use HiTEC 5748 (4.20-7.80 %). pp.10-11 print a 'Polymer content' row per oil -> scoped note row (no active content derived). Doses: {POLICY}.")
row('DL2-11597.pdf', 10, 'open_questions', "The record's active content is Missing; nothing about polymer content is recorded.",
    "p.10 'Core Data Set ACEA C3/C2-12' rows 'HiTEC® 5748 7.40 7.40 4.20 7.40 7.40 7.80 7.40 - - -', 'HiTEC® 5748A - - - - - - 8.50 4.50 6.20' and 'Polymer content 0.93 0.93 0.53 0.93 0.93 0.98 0.93 1.06 0.56 0.78' (finished-oil columns; no unit printed for the polymer row).",
    'finished-oil composition row as printed (polymer content of each test oil, unit not printed)', 'propose_note', 'additional',
    "Preserve as printed with its scope: the polymer content is a property of each finished test oil, printed without a unit, not a property of HiTEC 5748. No active content is derived (no registered calculation; the unit and basis are not printed) and active_content stays Missing. The 5748A columns are listed only because they share the row: no 5748A data is used for HiTEC 5748 and the separate interchange statement is not extended.",
    cmp='existing: active content Missing')
link('DL2-15140.pdf', 'D', 'pp.1, 16 and 32 (title and the pages naming HiTEC 5748) read in full; the other pages not read (p.2 opening only)',
     f"HiTEC 9490 presentation (ACEA 2016). p.16 field-trial 5W-40 A3/B4: HiTEC 9490 12.6, HiTEC 5748 12.9, HiTEC 672 0.2, Nexbase 3043 74.3; {POLICY}. p.32 'HiTEC® 9490 with low ethylene OCP delivers: a flexible, non-dedicated VI improver ...' beside 'Fresh Oil HiTEC® 9490 in Group III base oil with HiTEC® 5748 VII' -> open-question row (attribution not explicit).")
row('DL2-15140.pdf', 32, 'open_questions', "The record's polymer_chemistry is Missing (chemical family 'Non-dispersant olefin copolymer (OCP)' from the PDS).",
    "p.32: 'HiTEC® 9490 with low ethylene OCP delivers: a flexible, non-dedicated VI improver to blend a growing portfolio of oils' and, on the same slide, 'Fresh Oil HiTEC® 9490 in Group III base oil with HiTEC® 5748 VII'.",
    "manufacturer slide wording beside a HiTEC 5748 mention (descriptor not explicitly attributed)", 'propose_open_question_update', 'additional',
    "The slide pairs 'low ethylene OCP' with HiTEC 5748 as the VII but does not say in one sentence that HiTEC 5748 is the low-ethylene OCP. Propose recording the wording as a question for Afton; polymer_chemistry stays Missing and nothing is inferred about ethylene content.",
    cmp='existing: polymer_chemistry Missing')
link('DL2-15465.pdf', 'D,E', 'pp.1, 13, 14 and 20 (title and every page naming HiTEC 5748) read in full; the other pages not read',
     "HiTEC 11456 presentation, July 2021: 'Viscosity Modifier HiTEC® 5748 (25 SSI)' (p.13) and 'HiTEC® 5748 (25 SSI olefin copolymer viscosity modifier)' (p.20) are already proposed (SSI open-question row); p.14 base-oil coverage table 'Viscosity Modifiers: HiTEC® 5748' (Ultra-S, ADNOC, YuBase, CTL, Petro-Canada, Chevron, EHC, aramcoPRIMA, aramcoPRIMA S (48% max), Phillips 66 PP; 'Trim stock Grp III might be required for 5W final formulation'). No new row.")
link('DL2-15748.pdf', 'C', 'pp.1 and 12-14 (title and every page naming HiTEC 5748) read in full; the other pages not read',
     f"HiTEC 11500 presentation, September 2021. p.12 'OCP – Efficiency through Viscosity Modifier' list naming HiTEC 5748 as the VII of HiTEC 9387X, 9388X, 9490, 9450, 9458, 11500, 8799B(+), 8788LA, 12200, and 'HiTEC® 5748/54' for HiTEC 8744X (printed so; '5748/54' not interpreted); p.13 profile summary 'OCP: HiTEC® 5748'; p.14 formulations; {POLICY}. No new row (package-level VM pairings without route conditions).")
link('DL2-12551.pdf', 'C', 'pp.1, 12-14 and 17 (title and every page naming HiTEC 5748) read in full; the other pages not read (p.2 opening only)',
     f"HiTEC 11500 presentation (2019): the same p.12 VM list as DL2-15748.pdf (incl. 'HiTEC® 5748/54' for 8744X), p.13 profile summary, p.14 formulations and p.17 '0% PAO formulation targeting MB 229.71, ACEA C5, API SN Plus, and API SP capability in development' (HiTEC 5748 VM 3.5); {POLICY}. No new row.")
link('DL2-12552.pdf', 'D', 'pp.1-9 read in full (all 9 pages)',
     f"HiTEC 11500 formulation sheets, April 2019 (LBB-020319-A ... LBB-020646-A): HiTEC 5748 ND-OCP 3.2-7.8 % wt with HiTEC 11500 13.1 and HiTEC 672 0.2 in Yubase / PAO 6; p.9 '○Submitted, awaiting approval letter'; {POLICY}. No new row.")
link('DL2-15778.pdf', 'D', 'pp.1-9 read in full (all 9 pages)',
     f"HiTEC 11500 'Formulation Catalogue December 2025': the same eight oil codes as DL2-12552.pdf with HiTEC 5748 ND-OCP 3.2-7.8 % wt, rounded KV values, MRV '(NYS)' and 'Δ Approval expired' marks on four oils; {POLICY}. No new row.")
link('DL2-15013.pdf', 'D', 'pp.1-2 and 6-13 (title and every page naming HiTEC 5748) read in full; the other pages not read',
     f"HiTEC 11410 presentation, July 2022 (ACEA C2/C3/C5/C6, API SP, 10.6 %): HiTEC 5748 VM 4.30-9.50 % in Yubase, Chevron 100R + Yubase / Ultra-S / NEXBASE / ADNOC; claim summaries 'HiTEC® 5748 OCP VM'; footnote '* For guidance on claiming ACEA C2 with ACEA C3, please contact your Afton Chemical representative'; {POLICY}. The bulletins of the same package are already proposed as route-bound co-use notes. No new row.")
link('DL2-15070.pdf', 'D', 'pp.1 and 24-25 (title and the pages naming HiTEC 5748) read in full; the other pages not read (p.2 opening only)',
     "HiTEC 11600 presentation, March 2022: 'Full-treat coverage in SK Yubase Group III and HiTEC® 5748' (12.6 %) and 'Full-treat and down-treat coverage in ExxonMobil EHC Group II and HiTEC® 5748' (12.6 % / 10.5 %; 'API SP capable but not licensable (phosphorus limit)'). The 11600 bulletin co-use note is already proposed. No new row.")
for f in ('DL2-15678.pdf', 'DL2-15688.pdf'):
    link(f, 'D', 'pp.1 and 9-12 (title and every page naming HiTEC 5748) read in full; the other pages not read. The text layers of DL2-15678.pdf and DL2-15688.pdf were compared by machine page by page and are identical on each of the 23 (a text comparison, not a reading); the files differ in bytes and their images were not compared',
         f"Afton 'GO BEYOND PERFORMANCE - Next generation PCMO solutions' (2024), HiTEC 11455 + HiTEC 11571 GF-7 / API SQ coverage plans: 'Viscosity Modifiers: HiTEC® 5748' for Group III and Group II slates; target formulations with HiTEC 5748 4.70-8.00 %, 'DI HiTEC® 11455 (with PPD)', 'PPD booster Viscoplex® 6-850 0.02' (0W-16 only) and footnote '3 GF-7B with HiTEC® 7133 & EVONIK Viscoplex® 6-850 boosters'; {POLICY}. No new row.")

# ---------------- candidate data packages ----------------
link('DL2-15777.pdf', 'D', 'pp.1, 3, 5, 6, 10 and 12-14 (title, introduction and every page naming HiTEC 5748) read in full; p.2 contents list read; the other pages not read',
     f"HiTEC 11500 API SQ CDP Book 1, issue date Sep 2025: introduction 'HiTEC® 11500 additive package at 13.10% wt. and HiTEC® 5748 non-dispersant Viscosity Modifier (VM)'; test summaries 'Viscosity Modifier Tested HiTEC® 5748' (3.23-8.22 %); final formulations pp.13-14 list 'HiTEC® 5748, Non-Dispersant Viscosity Modifier' with 'Typical Density' 0.855 (no temperature or unit printed) -> component-density open-question row; doses: {POLICY}.")
link('DL2-15690.pdf', 'D', 'pp.1 and 3-13 (title and every page naming HiTEC 5748 or 5748A) read in full; p.2 opening only; p.14 not read',
     f"HiTEC 11356 'Market General API SP Version 1.0 Apr, 2024': engine-test matrices print 'Viscosity Modifier Tested HiTEC® 5748A' for most test oils and HiTEC 5748 for LBR-027650-A (EHC 30 %, 5W-40), with read-across conditions such as '11.55% max HiTEC 5748A' and '20.50% max HiTEC 5748A'; final formulations pp.9-13 (Apr 2, 2024) name 'HiTEC® 5748, Non-Dispersant Viscosity Modifier' with 'Density @ 15.6ºC' 0.8556 -> scoped note and density row; doses: {POLICY}.")
link('DL2-15799.pdf', 'D', 'pp.1-3, 5, 6, 17 and 21-28 (title, contents, introduction and every page naming HiTEC 5748 or 5748A) read in full; the other pages not read',
     f"HiTEC 11455 ILSAC GF-7B / API SQ CDP Book 1, issue date June 2025: introduction 'HiTEC® 11455 additive package at 7.0% wt., 0.3% wt. HiTEC® 7133 booster and HiTEC® 5748'; matrix 'Viscosity Modifier Tested' HiTEC 5748 (LBR-024697-A) or 5748A (the others), '* Requires 0.30% wt. HiTEC® 7133 Booster'; p.17 formulation row 'HiTEC® 5748 or HiTEC 5748A VM'; final formulations pp.21-28 (June 9-10, 2025) name 'HiTEC® 5748, Non-Dispersant Viscosity Modifier' with 'Typical Density' 0.864 and 'Viscoplex 6-850, PPD booster 0.05' -> scoped note and density row; doses: {POLICY}.")
link(C22, 'D', 'pp.1-3, 5-9, 12 and 15-17 read in full; pp.18-21 read for the composition block and the HiTEC 5748 line of each formulation (finished-oil result columns not read); the other pages not read',
     f"HiTEC 22300 motorcycle / PCMO CDP Version 2, API SL (5.35 %): introduction names 'HiTEC® 5748 non-dispersant viscosity modifier (VM)'; every test oil 'Viscosity Modifier Tested HiTEC® 5748' (no 5748A on any page); p.12 prints 'HiTEC® 672 Viscosity Modifier 0.20' (HiTEC 672 is labelled PPD elsewhere; recorded as printed, not a 5748 matter); final formulations pp.15-21 print 'HiTEC® 5748 | Density @ 15.6ᴼC 0.8550'; p.16 prints the 10W-40 column 'HiTEC® 5748 ... 10.00 | 5.06' (the volume % equals the 10W-30 column's; recorded as printed, not corrected) -> density row; doses: {POLICY}.")
link(C11, 'D', 'pp.1-3, 5-10 and 14 read in full; pp.17-24 read for the composition block and the HiTEC 5748 line of each formulation (finished-oil result columns not read); the other pages not read',
     f"HiTEC 11356 API SQ CDP Book 1, issue date Mar 2025 (file name '20260525_updated'): introduction 'HiTEC® 11356 additive package at 6.8% wt and HiTEC® 5748'; matrices print 'Viscosity Modifier Tested HiTEC® 5748A' for the engine-tested oils except LBR-031191-A (HiTEC 5748), while the read-across conditions are written on HiTEC 5748 ('HiTEC® 5748 ≤ 13.50%', '≤ 20.50%', '≤ 11.55%', '≤ 8.2%', '≤10.80%'); p.14 row 'HiTEC® 5748 or HiTEC 5748A VM'; final formulations print 'HiTEC® 5748, Non-Dispersant Viscosity Modifier' with 'Density @ 15.6ºC' 0.856 (pp.17-18, 21-22) or 0.8556 (pp.19-20, 23-24) -> scoped note and density row; doses: {POLICY}.")

for f, page, txt, prog in [
    ('DL2-15690.pdf', 3, "p.3-5 'Viscosity Modifier Tested HiTEC® 5748A' (LBR-023617-A, LBR-023151-A, LBR-024823-A, ...) and 'HiTEC® 5748' (LBR-027650-A); conditions '11.55% max HiTEC 5748A', '(20.50% max HiTEC 5748A)'; final formulations pp.9-13 'HiTEC® 5748, Non-Dispersant Viscosity Modifier'.", 'HiTEC 11356 API SP programme (Apr 2024)'),
    ('DL2-15799.pdf', 17, "p.5 'Viscosity Modifier Tested' HiTEC 5748 (LBR-024697-A) and HiTEC 5748A (LBR-031054-A and others); p.17 'HiTEC® 5748 or HiTEC 5748A VM'; final formulations pp.21-28 'HiTEC® 5748, Non-Dispersant Viscosity Modifier'.", 'HiTEC 11455 + HiTEC 7133 GF-7B / API SQ programme (June 2025)'),
    (C11, 14, "pp.5-10 'Viscosity Modifier Tested HiTEC® 5748A' for the engine-tested oils (HiTEC 5748 for LBR-031191-A); read-across conditions 'HiTEC® 5748 ≤ 13.50%', '≤ 20.50%', '≤ 11.55%'; p.14 'HiTEC® 5748 or HiTEC 5748A VM'; final formulations 'HiTEC® 5748, Non-Dispersant Viscosity Modifier'.", 'HiTEC 11356 API SQ programme (Mar 2025)')]:
    row(f, page, 'compatibility_restrictions', 'The HiTEC 5748 PDS (05/23, cited) does not mention HiTEC 5748A or this programme.', txt,
        "programme data package naming either VM (another product's document)", 'propose_note', 'additional',
        f"Within one programme ({prog}) the engine tests were run largely with HiTEC 5748A while the final formulations name HiTEC 5748 and the composition row allows either. Propose a note limited to that scope: the programme's interchange of the two VMs, as printed. It does not make the grades one product, no 5748A data is used for HiTEC 5748 (no SSI, density, dose or performance is transferred), and the dose limits are package read-across conditions, not HiTEC 5748 treat ranges.",
        cond=f'{prog} only')

row('DL2-15799.pdf', 21, 'open_questions', "The HiTEC 5748 PDS (05/23) prints the specific gravity 0.855 (open question: typical characteristics without a template field); the earlier formulation sheet DL2-14915.pdf ('Density @ 15.6 C') prints 0.8603 (no_change evidence row).",
    "Component density printed for 'HiTEC® 5748, Non-Dispersant Viscosity Modifier' in Afton final-formulation sheets: DL2-15799.pdf pp.21-28 'Typical Density' 0.864 (June 2025; no temperature, no unit); DL2-15777.pdf pp.13-14 'Typical Density' 0.855 (Sep 2025; no temperature, no unit); DL2-15690.pdf pp.9-13 'Density @ 15.6ºC' 0.8556 (Apr 2024); HiTEC 11356 API SQ CDP pp.17-24 'Density @ 15.6ºC' 0.856 or 0.8556; HiTEC 22300 CDP pp.15-21 'Density @ 15.6ᴼC' 0.8550.",
    'component density as printed in formulation sheets (used there for wt% / vol% conversion); conditions as printed', 'propose_open_question_update', 'additional',
    "Several printings of a density for HiTEC 5748 itself, from Afton documents of different dates, with and without a stated temperature (0.8550 / 0.8556 / 0.856 at 15.6 °C; 0.855 and 0.864 'Typical Density' without temperature; 0.8603 at 15.6 °C earlier). There is no template field. Propose listing them, each with its source, date and condition, in the open question beside the PDS specific gravity, and asking Afton which value applies; none is selected, averaged or converted, and the 0.864 vs 0.855 difference is not resolved.",
    cmp='existing: PDS specific gravity 0.855 in open questions; 0.8603 evidence row')

d = dict(batch='HiTEC 5748 mentions, batch 19: the 18 long documents (sixteenth pass)', reviewed_on='2026-11-14 (sixteenth pass)',
         note='Every page naming HiTEC 5748 / 5748A read in full (text layer); document read scope stated per link and is a full-document read only for DL2-12552.pdf and DL2-15778.pdf (all pages).',
         documents={}, links=links, fields=F)
json.dump(d, open(f'{B}/decisions/zzzzzzzzzzzzzzzz_b19_5748_long_docs_sixteenth_pass.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(links), len(F))
