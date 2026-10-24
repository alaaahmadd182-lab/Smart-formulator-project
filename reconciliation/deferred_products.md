# Deferred products (2026-10-24)

The 190 inventory materials without a product JSON are listed, one row each, in
`deferred_products.csv`. None of them has a supplier datasheet of its own in
`Manual + Data to share.zip`, so no JSON was created for them: an empty or placeholder record
would carry no source-reported data. They stay in the inventory for discussion with the professor.

| Reason code | Base oils | Additive packages | Additive components | Total |
|---|---|---|---|---|
| `C-MENTION-ONLY`: named only inside another product's datasheet | 0 | 2 | 18 | **20** |
| `D-WEB-LEAD-ONLY`: no archived source; only unverified Richful web-feed records | 0 | 26 | 26 | **52** |
| `D-IDENTITY-UNRESOLVED`: no archived source; possible alias or placeholder/generic name | 12 | 0 | 1 | **13** |
| `D-NO-SOURCE`: no archived source located | 10 | 24 | 71 | **105** |
| **Total** | **22** | **52** | **116** | **190** |

## How this was checked

- Every archive document with a text layer (346 files) was searched for each material's product
  name and product code. All matches were reviewed: none is a datasheet of the material itself.
  The category C mentions give only a role or a dose in another product's route (for example
  "Formulated and approved in combination with Lubrizol® 7077 performance polymer", "VI Improver
  (VII) PARATONE® 8006", "4.1%+1.9%RF0206"); the remaining matches are false positives (generic
  codes such as 150N or 1000, a REACH registration number, a copyright year).
- The 16 image-only archive documents that no JSON cites were checked visually. They are further
  copies or editions of products that already have JSON (the aramcoPRIMA brochure table, the FPCC
  GII 70N/150N/500N table, SpectraSyn 2-10 cSt and 40/100 cSt family sheets, the S-OIL Ultra-S web
  table).
- The other 74 uncited archive documents (with text) are SDSs or further editions of products that
  already have JSON; none belongs to a material in this list.

## Open points for discussion

- `D-IDENTITY-UNRESOLVED`: Luberef 110HC / 230HC / 500HC (`identity_review.md` ID-02), XOM APE 150 / 600
  (ID-03), the ExxonMobil "per filename" names (ID-06) and the generic or unattributed materials
  (ID-07). None is assumed to be an existing record.
- `D-WEB-LEAD-ONLY`: the Richful web-feed records could support records if they are accepted as a
  source; under the current assessment they are not.
- `C-MENTION-ONLY`: these components (and the HiTEC 12204Y / 12252 premixes) need their own
  supplier datasheets.
