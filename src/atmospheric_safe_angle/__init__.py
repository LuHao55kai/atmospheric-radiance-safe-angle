"""Atmospheric background-radiance upper bounds and safe-angle queries."""

from .model import (
    ANGLE_DOMAIN_DEG,
    BAND_RANGES_UM,
    VISIBILITY_DOMAIN_KM,
    ParameterRow,
    available_configurations,
    environment_radiance_upper_bound,
    get_parameters,
    minimum_safe_angle,
    safe_radiance_upper_bound,
)

__all__ = [
    "ANGLE_DOMAIN_DEG",
    "BAND_RANGES_UM",
    "VISIBILITY_DOMAIN_KM",
    "ParameterRow",
    "available_configurations",
    "environment_radiance_upper_bound",
    "get_parameters",
    "minimum_safe_angle",
    "safe_radiance_upper_bound",
]

__version__ = "0.1.0"
