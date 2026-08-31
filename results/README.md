# Frozen aggregate results

All files in this directory are derived or aggregate outputs. They contain no
raw DSL-1 spectra, no raw AERONET measurements, and no MODTRAN software assets.

| File | Contents |
|:---|:---|
| <code>band_summary.csv</code> | In-domain simulation metrics aggregated over 39 cases per band |
| <code>scene_summary.csv</code> | In-domain simulation metrics aggregated over 39 cases per scene |
| <code>scenario_metrics.csv</code> | Metrics for all 117 band-scene-visibility cases |
| <code>validation_summary.csv</code> | Compact cross-evidence headline statistics and interpretation levels |
| <code>field_validation_summary.csv</code> | Aggregate statistics for the two accepted DSL-1 VIS datasets |
| <code>aeronet_station_summary.csv</code> | Three representative public-scan station diagnostics |
| <code>safe_angle_benchmark.json</code> | Reported local formula-plus-search timing |

Simulation $R^2$ and NRMSE values evaluate extracted envelope points. Raw-point
coverage evaluates full-geometry records with separation at least 15 degrees
and excludes the artificial 180 degree endpoint. The AERONET and field tables
have the limitations stated in <code>../docs/validation.md</code>.
