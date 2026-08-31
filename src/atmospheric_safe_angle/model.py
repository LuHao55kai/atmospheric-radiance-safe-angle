"""Frozen analytical model used by the atmospheric safe-angle study."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from functools import lru_cache
from importlib.resources import files
from typing import TypeAlias

import numpy as np
from numpy.typing import ArrayLike, NDArray


FloatResult: TypeAlias = float | NDArray[np.float64]

ANGLE_DOMAIN_DEG = (15.0, 180.0)
VISIBILITY_DOMAIN_KM = (2.0, 30.0)
BAND_RANGES_UM = {
    "vis": (0.40, 0.75),
    "nir": (1.10, 1.70),
    "mwir": (3.70, 4.20),
}

_BAND_ALIASES = {
    "vis": "vis",
    "visible": "vis",
    "nir": "nir",
    "near-infrared": "nir",
    "near_infrared": "nir",
    "mwir": "mwir",
    "mid-wave-infrared": "mwir",
    "mid_wave_infrared": "mwir",
}
_SCENE_ALIASES = {
    "desert": "desert",
    "maritime": "maritime",
    "ocean": "maritime",
    "rural": "rural",
}


@dataclass(frozen=True)
class ParameterRow:
    """One frozen band-scene parameter row."""

    band: str
    band_center_um: float
    scene: str
    w0: float
    w1: float
    d0: float
    d1: float
    g: float
    s0: float
    s1: float
    a: float
    tau_base0: float
    tau_base1: float
    tau_shoulder0: float
    tau_shoulder1: float
    p: float


def _canonical_band(band: str) -> str:
    key = str(band).strip().lower()
    try:
        return _BAND_ALIASES[key]
    except KeyError as exc:
        choices = ", ".join(BAND_RANGES_UM)
        raise ValueError(f"unknown band {band!r}; expected one of: {choices}") from exc


def _canonical_scene(scene: str) -> str:
    key = str(scene).strip().lower()
    try:
        return _SCENE_ALIASES[key]
    except KeyError as exc:
        raise ValueError(
            f"unknown scene {scene!r}; expected desert, maritime, or rural"
        ) from exc


@lru_cache(maxsize=1)
def _parameter_map() -> dict[tuple[str, str], ParameterRow]:
    parameter_file = files(__package__).joinpath("parameters.csv")
    rows: dict[tuple[str, str], ParameterRow] = {}
    with parameter_file.open("r", encoding="utf-8", newline="") as stream:
        for raw in csv.DictReader(stream):
            row = ParameterRow(
                band=raw["band"],
                band_center_um=float(raw["band_center_um"]),
                scene=raw["scene"],
                w0=float(raw["w0"]),
                w1=float(raw["w1"]),
                d0=float(raw["d0"]),
                d1=float(raw["d1"]),
                g=float(raw["g"]),
                s0=float(raw["s0"]),
                s1=float(raw["s1"]),
                a=float(raw["a"]),
                tau_base0=float(raw["tau_base0"]),
                tau_base1=float(raw["tau_base1"]),
                tau_shoulder0=float(raw["tau_shoulder0"]),
                tau_shoulder1=float(raw["tau_shoulder1"]),
                p=float(raw["p"]),
            )
            rows[(row.band, row.scene)] = row
    return rows


def available_configurations() -> tuple[tuple[str, str], ...]:
    """Return the nine supported canonical (band, scene) combinations."""

    return tuple(sorted(_parameter_map()))


def get_parameters(band: str, scene: str) -> ParameterRow:
    """Return the frozen parameter row for a band and atmospheric scene."""

    canonical = (_canonical_band(band), _canonical_scene(scene))
    return _parameter_map()[canonical]


def _sigmoid(value: NDArray[np.float64]) -> NDArray[np.float64]:
    return 1.0 / (1.0 + np.exp(-np.clip(value, -60.0, 60.0)))


def _validate_model_domain(
    theta_deg: NDArray[np.float64], visibility_km: NDArray[np.float64]
) -> None:
    if not np.all(np.isfinite(theta_deg)):
        raise ValueError("theta_deg must contain only finite values")
    if not np.all(np.isfinite(visibility_km)):
        raise ValueError("visibility_km must contain only finite values")
    theta_min, theta_max = ANGLE_DOMAIN_DEG
    if np.any(theta_deg < theta_min) or np.any(theta_deg >= theta_max):
        raise ValueError(
            f"theta_deg must satisfy {theta_min} <= theta_deg < {theta_max}"
        )
    visibility_min, visibility_max = VISIBILITY_DOMAIN_KM
    if np.any(visibility_km < visibility_min) or np.any(
        visibility_km > visibility_max
    ):
        raise ValueError(
            "visibility_km must satisfy "
            f"{visibility_min} <= visibility_km <= {visibility_max}"
        )


def _as_result(value: NDArray[np.float64]) -> FloatResult:
    if value.ndim == 0:
        return float(value)
    return value


def environment_radiance_upper_bound(
    theta_deg: ArrayLike,
    visibility_km: ArrayLike,
    band: str,
    scene: str,
) -> FloatResult:
    """Evaluate the base engineering upper-bound curve L_env.

    Parameters are valid only over 15 <= theta < 180 degrees and visibility
    from 2 to 30 km. The output is band-integrated radiance in W m^-2 sr^-1.
    NumPy broadcasting applies to theta_deg and visibility_km.
    """

    theta = np.asarray(theta_deg, dtype=float)
    visibility = np.asarray(visibility_km, dtype=float)
    _validate_model_domain(theta, visibility)
    row = get_parameters(band, scene)

    theta_rad = np.deg2rad(theta)
    cosine = np.cos(theta_rad)
    x = np.clip((1.0 - cosine) / 2.0, 1e-12, None)
    y = np.clip((1.0 + cosine) / 2.0, 1e-12, None)
    ln_v = np.log(visibility)

    w = np.exp(np.clip(row.w0 - row.w1 * ln_v, -60.0, 60.0))
    d = np.exp(np.clip(row.d0 - row.d1 * ln_v, -60.0, 60.0))
    shoulder_scale = np.exp(
        np.clip(row.s0 - row.s1 * ln_v, -60.0, 60.0)
    )
    phase = (1.0 - row.g**2) / np.power(
        1.0 + row.g**2 - 2.0 * row.g * cosine,
        1.5,
    )

    tau_base = np.clip(
        _sigmoid(np.asarray(row.tau_base0 + row.tau_base1 * ln_v)),
        1e-4,
        0.95,
    )
    tau_shoulder = np.clip(
        _sigmoid(np.asarray(row.tau_shoulder0 + row.tau_shoulder1 * ln_v)),
        1e-4,
        0.95,
    )
    taper_base = 1.0 - np.exp(
        -np.exp(np.clip(row.p * np.log(y / tau_base), -60.0, 60.0))
    )
    taper_shoulder = 1.0 - np.exp(
        -np.exp(np.clip(row.p * np.log(y / tau_shoulder), -60.0, 60.0))
    )

    core = (w * phase + d) * taper_base
    shoulder = (
        shoulder_scale
        * np.exp(np.clip(row.a * np.log(x), -60.0, 60.0))
        * taper_shoulder
    )
    result = np.maximum(core + shoulder, 1e-9)
    return _as_result(np.asarray(result, dtype=float))


def safe_radiance_upper_bound(
    theta_deg: ArrayLike,
    visibility_km: ArrayLike,
    band: str,
    scene: str,
    *,
    safety_factor: float = 1.0,
) -> FloatResult:
    """Evaluate L_safe = K_q L_env for an independently chosen K_q."""

    if not np.isfinite(safety_factor) or safety_factor < 1.0:
        raise ValueError("safety_factor must be finite and at least 1.0")
    base = environment_radiance_upper_bound(
        theta_deg,
        visibility_km,
        band,
        scene,
    )
    scaled = np.asarray(base, dtype=float) * float(safety_factor)
    return _as_result(scaled)


def minimum_safe_angle(
    radiance_limit: float,
    visibility_km: float,
    band: str,
    scene: str,
    *,
    safety_factor: float = 1.0,
    min_angle_deg: float = 15.0,
    max_angle_deg: float = 179.9,
    step_deg: float = 0.1,
) -> float | None:
    """Return the first grid angle after which every larger angle is admissible.

    The suffix-safe rule remains robust to small non-monotonic numerical
    variations. None is returned when no angle on the requested grid is safe.
    No interpolation between grid nodes is performed.
    """

    if not np.isfinite(radiance_limit) or radiance_limit < 0.0:
        raise ValueError("radiance_limit must be finite and non-negative")
    if not np.isfinite(step_deg) or step_deg <= 0.0:
        raise ValueError("step_deg must be finite and positive")
    if not np.isfinite(min_angle_deg) or not np.isfinite(max_angle_deg):
        raise ValueError("angle limits must be finite")
    if min_angle_deg > max_angle_deg:
        raise ValueError("min_angle_deg must not exceed max_angle_deg")
    theta_min, theta_max = ANGLE_DOMAIN_DEG
    if min_angle_deg < theta_min or max_angle_deg >= theta_max:
        raise ValueError(
            f"search grid must remain within [{theta_min}, {theta_max}) degrees"
        )

    theta = np.arange(
        min_angle_deg,
        max_angle_deg + 0.5 * step_deg,
        step_deg,
        dtype=float,
    )
    theta = theta[theta <= max_angle_deg + 1e-10]
    radiance = np.asarray(
        safe_radiance_upper_bound(
            theta,
            visibility_km,
            band,
            scene,
            safety_factor=safety_factor,
        ),
        dtype=float,
    )
    safe = radiance <= float(radiance_limit)
    suffix_safe = np.logical_and.accumulate(safe[::-1])[::-1]
    indices = np.flatnonzero(suffix_safe)
    if indices.size == 0:
        return None
    return float(np.round(theta[indices[0]], 12))
