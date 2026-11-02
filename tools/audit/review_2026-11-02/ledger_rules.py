"""Classification rules of the citation ledger (pure functions, no file access; tested by tests/test_ledger_rules.py).

Categories:
  A  fully verified: automated column/row check   the citation is listed in the explicit column-check set
  B  fully verified: visual check                 explicit verdict "verified" with a visual basis
  C  fully verified: context review               explicit verdict "verified" with a reading basis
  D  automated text presence only                 no verdict; the number was found on the cited page
  E  unresolved                                   verdict "incomplete" or "unavailable", an unknown verdict, or no verdict
                                                  and no number found
  N  not used as evidence                         a source the finding names only to say it was not consulted

Rules that the regression tests hold:
  - only an explicit verdict in VERIFIED_VERDICTS (or column-check membership) makes a citation verified;
  - "incomplete", "unavailable" and any unknown verdict are unresolved, never verified;
  - a citation without a verdict is never verified (D at best);
  - verification is complete only when no citation is in D or E.
"""

VERIFIED_VERDICTS = {'verified', 'verified, qualifier corrected'}
UNRESOLVED_VERDICTS = {'incomplete', 'unavailable'}
NOT_EVIDENCE_VERDICTS = {'not used as evidence'}
VISUAL_WORDS = ('visual', 'render', 'image', 'matrix extraction')
LABEL = {'A': 'fully verified: automated column/row check', 'B': 'fully verified: visual check', 'C': 'fully verified: context review',
         'D': 'automated text presence only', 'E': 'unresolved', 'N': 'not used as evidence (named only as not consulted)'}
VERIFIED_CATS = ('A', 'B', 'C')


def classify_verdict(verdict):
    """Category for an explicit reviewer verdict dict {'verdict', 'basis', ...}; anything not recognised is unresolved."""
    if not isinstance(verdict, dict):
        return 'E'
    v = str(verdict.get('verdict', '')).strip().lower()
    if v in VERIFIED_VERDICTS:
        basis = str(verdict.get('basis', '')).lower()
        if not basis:
            return 'E'  # a verified verdict must say how it was verified
        if basis.startswith('automated'):
            return 'A'
        return 'B' if any(w in basis for w in VISUAL_WORDS) else 'C'
    if v in NOT_EVIDENCE_VERDICTS:
        return 'N'
    return 'E'  # incomplete, unavailable, empty or unknown


def classify_citation(key, number_check, column_checked, verdicts):
    """Category of one value citation.

    key            'CF-xxx#index#file'
    number_check   result of check_sources.py ('on cited page', 'not found', ...)
    column_checked set of keys verified by the automated column/row check
    verdicts       {key: verdict dict} of explicit reviewer verdicts
    """
    if key in verdicts:
        cat = classify_verdict(verdicts[key])
        if cat == 'E' or key not in column_checked:
            return cat  # an explicit unresolved verdict is never overridden by an automated check
    if key in column_checked:
        return 'A'
    if number_check == 'on cited page':
        return 'D'
    return 'E'


def summarize(categories):
    """Counts per category and the completeness flag (complete only when nothing is in D or E)."""
    counts = {c: 0 for c in LABEL}
    for c in categories:
        counts[c] = counts.get(c, 0) + 1
    counts['verified'] = sum(counts[c] for c in VERIFIED_CATS)
    counts['total'] = len(categories)
    counts['complete'] = counts['D'] == 0 and counts['E'] == 0
    return counts
