"""Rule 2, step C: property-specific TDS-SDS screening rules (PROPOSED, awaiting review; not applied to findings).

A screening rule only sorts numerical TDS-SDS differences between COMPARABLE values into "below the proposed project
review threshold" and "at or above it (retain for review)". It is not an industry standard and not an acceptance
tolerance; being below it does not show that the two documents agree, and being above it is not a confirmed scientific
contradiction. Every threshold here is an EMPIRICAL PROJECT SCREENING CHOICE: no independently supported technical
tolerance (for example an ASTM reproducibility limit) could be verified from an accessible authoritative source in this
review (docs/data_policy_mandatory_review/threshold_proposal.md, section 3). A reporting increment, such as the 3 °C
pour-point examination interval, is not treated as a tolerance.

APPROVAL is 'proposed' until the reviewer approves the table; tools must not reclassify findings while it is 'proposed'.
"""

APPROVAL = 'proposed'
VERSION = 'thresholds-2026-11-10-proposed.2'

BELOW = 'below proposed project review threshold'
ABOVE = 'at or above proposed project review threshold: retain for review'
ROUNDING = 'difference within print rounding of the less precise value'
BOUND_OK = 'point value logically compatible with the other document\'s bound (not evidence of agreement)'
BOUND_BAD = 'point value outside the other document\'s bound: retain for review'

EMPIRICAL = 'empirical project screening choice (no verified technical tolerance)'
# property -> rule. kind: 'relative' (% of the TDS value), 'absolute' (canonical unit), or None (no threshold: pending)
RULES = {
    'kv40':  dict(group='viscosity', canonical_unit='mm²/s', kind='relative', threshold=3.0, basis=EMPIRICAL,
                  alternatives=[1.0, 2.0, 3.0, 5.0, 7.0, 10.0],
                  conditions='same test temperature (40 °C); kinematic viscosity on both sides; both point values of the same kind (typical/single)',
                  zero='viscosity is never 0; a 0 is treated as unparsed and the pair stays pending',
                  missing_metadata='method not printed on one side: allowed and flagged; label/unit inconsistency: pending'),
    'kv100': dict(group='viscosity', canonical_unit='mm²/s', kind='relative', threshold=3.0, basis=EMPIRICAL,
                  alternatives=[1.0, 2.0, 3.0, 5.0, 7.0, 10.0],
                  conditions='same test temperature (100 °C); kinematic viscosity on both sides; both point values of the same kind',
                  zero='as kv40', missing_metadata='as kv40'),
    'density': dict(group='density', canonical_unit='g/cm³', kind='absolute', threshold=0.005, basis=EMPIRICAL,
                    alternatives=[0.001, 0.002, 0.003, 0.005, 0.010],
                    conditions='same reference temperature printed on both sides; density (mass/volume) on both sides',
                    zero='not applicable', missing_metadata='temperature not printed, or a relative-density label with a density unit: pending'),
    'specific_gravity': dict(group='density', canonical_unit='dimensionless', kind='absolute', threshold=0.005, basis=EMPIRICAL,
                             alternatives=[0.001, 0.002, 0.003, 0.005, 0.010],
                             conditions='same reference-temperature pair (e.g. 15.6/15.6 °C) printed on both sides',
                             zero='not applicable', missing_metadata='reference temperatures not printed on both sides: pending'),
    'flash_point': dict(group='flash point', canonical_unit='°C', kind='absolute', threshold=10.0, basis=EMPIRICAL,
                        alternatives=[3.0, 5.0, 8.0, 10.0, 15.0, 20.0, 30.0],
                        conditions='same cup type (COC/ASTM D92 or PMCC/ASTM D93) printed or implied by the method on both sides',
                        zero='absolute difference only', missing_metadata='cup type not known on both sides: pending'),
    'pour_point': dict(group='pour point', canonical_unit='°C', kind='absolute', threshold=3.0, basis=EMPIRICAL,
                       alternatives=[0.0, 3.0, 6.0, 9.0],
                       conditions='both point values of the same kind',
                       zero='absolute difference only (0 °C is a valid value)', missing_metadata='method not printed: allowed and flagged'),
    'noack_volatility': dict(group='volatility', canonical_unit='mass %', kind=None, threshold=None, basis='no threshold proposed',
                             alternatives=[], conditions='same method and procedure', zero='absolute only',
                             missing_metadata='one case only; no project basis yet: pending'),
    'tbn': dict(group='TBN', canonical_unit='mg KOH/g', kind=None, threshold=None, basis='no threshold proposed', alternatives=[],
                conditions='same method (ASTM D2896 and D4739 differ)', zero='absolute only', missing_metadata='pending'),
}


def screen(prop, comparability, rel_pct, abs_diff, bound_satisfied, within_rounding, threshold=None):
    """Proposed screening outcome for one inventory row. `threshold` overrides the proposed value (sensitivity only)."""
    if comparability == 'bound check only':
        if bound_satisfied == 'true':
            return BOUND_OK
        if bound_satisfied == 'false':
            return BOUND_BAD
        return 'pending: two bounds or an unparsed bound'
    if comparability != 'comparable':
        return 'pending: ' + comparability
    if within_rounding == 'true':
        return ROUNDING
    r = RULES.get(prop)
    if not r or r['kind'] is None:
        return 'pending: no threshold proposed'
    d = rel_pct if r['kind'] == 'relative' else abs_diff
    if d in (None, ''):
        return 'pending: relative difference undefined (TDS value 0)'
    t = r['threshold'] if threshold is None else threshold
    return BELOW if float(d) < t - 1e-12 else ABOVE


def sensitivity(rows):
    """[(property, threshold, n_below, n_at_or_above, products_at_or_above)] for the comparable, non-rounding pairs."""
    out = []
    for prop, r in RULES.items():
        if r['kind'] is None:
            continue
        pairs = [x for x in rows if x['property'] == prop and x['comparability'] == 'comparable' and x['within_rounding'] != 'true']
        for t in r['alternatives']:
            res = [screen(prop, x['comparability'], x['rel_diff_pct'], x['abs_diff'], '', x['within_rounding'], t) for x in pairs]
            above = sorted({x['product'] for x, s in zip(pairs, res) if s == ABOVE})
            out.append((prop, t, res.count(BELOW), res.count(ABOVE), above, t == r['threshold']))
    return out
