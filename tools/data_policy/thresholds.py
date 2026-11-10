"""Rule 2, step C: property-specific TDS-SDS screening rules (PROPOSED, awaiting review; not yet applied to findings).

A screening rule only says whether a numerical TDS-SDS difference between COMPARABLE values is ordinary for typical
values printed in two documents of one product. It never confirms or refutes a scientific contradiction, and it is
not an industry standard. Thresholds are project screening values; their justification is in
docs/data_policy_mandatory_review/threshold_proposal.md.

APPROVAL is 'proposed' until the reviewer approves the table; tools must not reclassify findings while it is 'proposed'.
"""

APPROVAL = 'proposed'
VERSION = 'thresholds-2026-11-10-proposed'

# property -> rule. kind: 'relative' (% of the TDS value), 'absolute' (canonical unit), or None (no threshold: pending)
RULES = {
    'kv40':  dict(group='viscosity', canonical_unit='mm²/s', kind='relative', threshold=3.0,
                  conditions='same test temperature (40 °C); both typical/single point values; kinematic viscosity on both sides',
                  zero='not applicable (viscosity is never 0); a 0 is treated as unparsed and the pair stays pending',
                  missing_metadata='method not printed on one side is allowed (kinematic viscosity at a fixed temperature) and flagged; '
                                   'a label/unit inconsistency keeps the pair pending'),
    'kv100': dict(group='viscosity', canonical_unit='mm²/s', kind='relative', threshold=3.0,
                  conditions='same test temperature (100 °C); both typical/single point values; kinematic viscosity on both sides',
                  zero='as kv40', missing_metadata='as kv40'),
    'density': dict(group='density', canonical_unit='g/cm³', kind='absolute', threshold=0.005,
                    conditions='same reference temperature printed on both sides; density (mass/volume) on both sides',
                    zero='not applicable', missing_metadata='temperature not printed on one side, or a relative-density label with a '
                                                            'density unit, keeps the pair pending'),
    'specific_gravity': dict(group='density', canonical_unit='dimensionless', kind='absolute', threshold=0.005,
                             conditions='same reference-temperature pair (e.g. 15.6/15.6 °C) printed on both sides',
                             zero='not applicable', missing_metadata='reference temperatures not printed on both sides keeps the pair pending'),
    'flash_point': dict(group='flash point', canonical_unit='°C', kind='absolute', threshold=10.0,
                        conditions='same cup type (COC/ASTM D92 or PMCC/ASTM D93) printed or implied by the method on both sides',
                        zero='absolute difference only', missing_metadata='cup type not known on both sides keeps the pair pending'),
    'pour_point': dict(group='pour point', canonical_unit='°C', kind='absolute', threshold=3.0,
                       conditions='both point values; pour point is reported in 3 °C steps (ASTM D97 test interval)',
                       zero='absolute difference only (0 °C is a valid value)', missing_metadata='method not printed is allowed and flagged'),
    'noack_volatility': dict(group='volatility', canonical_unit='mass %', kind=None, threshold=None,
                             conditions='same method and variant (e.g. ASTM D5800 procedure B)', zero='absolute only',
                             missing_metadata='no threshold proposed: one case only, no project basis yet; kept pending'),
    'tbn': dict(group='TBN', canonical_unit='mg KOH/g', kind=None, threshold=None,
                conditions='same method (ASTM D2896 vs D4739 differ)', zero='absolute only',
                missing_metadata='no threshold proposed: kept pending'),
}
# bound and range pairs (no difference is computed):
BOUND_RULE = ('a point value that satisfies the other document\'s bound or range is ordinary (not a contradiction); '
              'a point value outside it is retained for review; two bounds/ranges are reported and kept pending')


def screen(prop, comparability, rel_pct, abs_diff, bound_satisfied, within_rounding):
    """Return the proposed screening outcome for one inventory row (strings, for the review table)."""
    if comparability == 'bound check only':
        if bound_satisfied == 'true':
            return 'ordinary: bound satisfied'
        if bound_satisfied == 'false':
            return 'retain for review: outside bound'
        return 'pending: two bounds or unparsed bound'
    if comparability != 'comparable':
        return 'pending: ' + comparability
    r = RULES.get(prop)
    if within_rounding == 'true':
        return 'ordinary: within print rounding'
    if not r or r['kind'] is None:
        return 'pending: no threshold proposed'
    d = rel_pct if r['kind'] == 'relative' else abs_diff
    if d is None:
        return 'pending: relative difference undefined'
    return 'ordinary: within screening threshold' if d <= r['threshold'] + 1e-12 else 'retain for review: exceeds screening threshold'
