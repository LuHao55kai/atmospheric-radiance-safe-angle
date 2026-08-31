"""Minimal end-to-end safe-angle query."""

import numpy as np

from atmospheric_safe_angle import (
    environment_radiance_upper_bound,
    minimum_safe_angle,
)


theta = np.arange(15.0, 180.0, 0.1)
curve = environment_radiance_upper_bound(
    theta,
    visibility_km=15.0,
    band="vis",
    scene="rural",
)

# Replace this illustrative value with an instrument-calibrated limit.
radiance_limit = float(np.median(curve))
theta_min = minimum_safe_angle(
    radiance_limit,
    visibility_km=15.0,
    band="vis",
    scene="rural",
    safety_factor=1.0,
)

print(f"Illustrative radiance limit: {radiance_limit:.6f} W m^-2 sr^-1")
print(f"Minimum safe Sun-target separation: {theta_min:.1f} deg")
