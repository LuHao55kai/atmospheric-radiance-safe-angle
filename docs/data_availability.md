# Data availability and provenance

## Included

This GitHub release includes:

- the frozen full-precision parameter table for all nine band-scene
  configurations;
- executable formula evaluation and suffix-safe angle-search code;
- numerical golden tests against the frozen reference implementation;
- 117 case-level simulation metrics and band- and scene-level summaries;
- aggregate AERONET and DSL-1 validation statistics;
- the reported local query benchmark;
- selected figures used to explain fit quality, multiband structure, field
  comparison, and safe-angle inversion.

These materials are sufficient to evaluate the frozen analytical curve,
reproduce the documented quick-start result, inspect every case-level metric,
and reproduce the threshold-to-angle calculation.

## Not included

The following are intentionally excluded:

- MODTRAN executables, databases, documentation, and license-controlled assets;
- the complete raw full-geometry simulation files and original run logs;
- raw DSL-1 field spectra and instrument-owned source archives;
- raw AERONET files;
- a rejected field dataset and its diagnostic outputs;
- patent application materials, manuscript drafts, comments, temporary
  renderings, and local absolute paths.

Consequently, this release does not reproduce the original radiative-transfer
runs or coefficient optimization from raw inputs. It reproduces use and
numerical evaluation of the frozen model.

## Third-party sources

AERONET measurements should be downloaded from the
[official AERONET service](https://aeronet.gsfc.nasa.gov/) and used under its
current data-use, acknowledgment, and principal-investigator policies. No
AERONET source measurements are relicensed here.

The DSL-1 field spectra are subject to data-owner authorization. Aggregate
statistics and derived figure-level information are provided, but access to
raw spectra must be arranged with the owner.

## Planned archive

The manuscript-associated version will be tagged and archived on Zenodo after
formal author metadata are confirmed. The resulting DOI will identify the
exact immutable release used by the paper. The DOI is intentionally not
invented or reserved in this initial GitHub release.
