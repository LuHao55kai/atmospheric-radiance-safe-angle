# Validation scope and interpretation

## Reference grid

The frozen reference audit contains:

- three band-integrated ranges: VIS 0.40-0.75 um, NIR 1.10-1.70 um, and MWIR
  3.70-4.20 um;
- three atmospheric scene classes: maritime, desert, and rural;
- 13 visibility levels: 2, 4, 5, 7.5, 10, 12, 15, 18, 20, 22, 25, 28, and
  30 km;
- 117 complete band-scene-visibility cases;
- 17,161 geometrically valid directional records per case and 2,007,837
  records in total.

For each case, maxima in 5 degree separation-angle bins were followed by
non-increasing isotonic regression. A zero-valued point at exactly 180 degrees
was included only as a fitting regularizer. It is excluded from raw-point
coverage and from the callable model domain.

## Frozen simulation metrics

| Band | Cases | Mean $R^2$ | Mean NRMSE | 120-180 degree NRMSE | 150-180 degree NRMSE | Mean raw-point coverage |
|:---|---:|---:|---:|---:|---:|---:|
| VIS | 39 | 0.9958 | 0.0121 | 0.0198 | 0.0305 | 99.62% |
| NIR | 39 | 0.9970 | 0.0114 | 0.0443 | 0.0680 | 99.80% |
| MWIR | 39 | 0.9892 | 0.0162 | 0.0326 | 0.0437 | 99.51% |

The 39-fold VIS leave-one-scenario-out procedure withheld one complete
scene-visibility case, refit the remaining 38 cases, and evaluated the held-out
case. It produced mean $R^2=0.9945$, mean NRMSE 0.0136, 120-180 degree NRMSE
0.0232, 150-180 degree NRMSE 0.0330, and minimum held-out $R^2=0.9755$.

The reduced structural baseline retained a forward lobe and pedestal but
omitted the shoulder and dual endpoint tapers. Across VIS, the unified model
reduced 120-180 degree NRMSE from 0.1471 to 0.0198 and 150-180 degree NRMSE
from 0.2358 to 0.0305, reductions of 86.5% and 87.1%.

The NIR and MWIR rows demonstrate adaptation of the common formula across the
complete simulation grid. They are not NIR or MWIR field validation.

## AERONET public-scan diagnostic

AERONET principal-plane sky radiances at 440 and 675 nm were combined into an
engineering VIS proxy:

$$
L_{\mathrm{VIS,proxy}}
=0.01(1.575L_{440}+1.925L_{675}).
$$

The screened diagnostic set contained 9,907 scan curves and 161,367 angular
samples. Base-curve engineering coverage was 87.91%. Three high-coverage
station examples were:

| Scene | Station | Matched visibility | Samples | Base coverage | Same-site multiplier at 99% |
|:---|:---|---:|---:|---:|---:|
| Maritime | Ascension Island | 22 km | 9,791 | 98.48% | 1.056 |
| Desert | SEDE BOKER | 30 km | 15,542 | 98.13% | 1.095 |
| Rural | BONDVILLE | 18 km | 1,604 | 94.95% | 1.295 |

This is not a broadband absolute-radiance blind test. It uses two narrowband
samples, effective visibility matching, and site-scale processing. Same-site
multipliers are diagnostics and are not independent deployment factors.

## DSL-1 field VIS evaluation

Two accepted datasets from one rural/farmland site and one instrument
contained 17,458 strictly screened 400-750 nm samples. The base formula was
frozen before field evaluation. A nearby public meteorological station,
approximately 145 km from the site, supplied an external visibility proxy;
that proxy is not a synchronous on-site MOR measurement.

| Date | Sessions | Points | Median visibility proxy | Pointwise coverage | Session-bootstrap 95% CI | 2 degree-bin q95 coverage |
|:---|---:|---:|---:|---:|:---|---:|
| 2023-12-20 | 27 | 8,843 | 5.13 km | 98.98% | 98.55%-99.40% | 94.52% |
| 2023-12-27 | 28 | 8,615 | 3.56 km | 99.88% | 99.78%-99.97% | 100.00% |
| Combined | 55 | 17,458 | Not pooled | 99.43% | Not pooled | Not pooled |

These are repeated measurements at one site during one season, not multisite
or annual validation. Raw spectra are not public because of data-ownership
restrictions.

## Runtime benchmark

The reported benchmark evaluated one VIS-rural curve and a suffix-safe search
on a 0.1 degree grid from 15.0 to 179.9 degrees, totaling 1,650 nodes. A
single-process Python/NumPy implementation on an Apple M1 CPU produced a median
of 0.136 ms per query after warm-up. This is an illustrative implementation
benchmark, not a certified real-time bound and not a same-platform speed
comparison with MODTRAN.

## Claims supported by this release

The strongest current evidence supports the frozen VIS formula over the stated
angle, visibility, and scene-class domain, with one-site field evidence and a
public-scan angular-trend diagnostic. Multiband simulation results support the
adaptability of the same analytical structure. They do not establish universal
coverage across arbitrary sites, seasons, instruments, clouds, unmodeled
aerosols, wavelengths, or visibility outside 2-30 km.
