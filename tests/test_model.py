import numpy as np
import pytest

from atmospheric_safe_angle import (
    available_configurations,
    environment_radiance_upper_bound,
    get_parameters,
    minimum_safe_angle,
    safe_radiance_upper_bound,
)


ANGLES = np.array([15.0, 30.0, 60.0, 90.0, 120.0, 150.0, 179.9])


@pytest.mark.parametrize(
    ("band", "scene", "visibility_km", "expected"),
    [
        (
            "vis",
            "rural",
            15.0,
            [
                135.650896887052,
                97.0937504935931,
                48.0014993132803,
                33.5757120918662,
                31.8998454931351,
                28.8745615543898,
                0.0627033693025665,
            ],
        ),
        (
            "nir",
            "desert",
            5.0,
            [
                40.4600046770897,
                28.3648809300329,
                16.40966675976,
                13.0216498984598,
                11.003131154123,
                7.82485706353444,
                0.0271108812677133,
            ],
        ),
        (
            "mwir",
            "rural",
            30.0,
            [
                1.01724412973222,
                0.515402596377301,
                0.243697543208872,
                0.206749086843202,
                0.203890113606596,
                0.206000592427935,
                4.23669349810665e-06,
            ],
        ),
    ],
)
def test_frozen_formula_matches_reference(band, scene, visibility_km, expected):
    actual = environment_radiance_upper_bound(
        ANGLES,
        visibility_km,
        band,
        scene,
    )
    np.testing.assert_allclose(actual, expected, rtol=2e-13, atol=1e-12)


def test_all_nine_parameter_rows_are_packaged():
    assert len(available_configurations()) == 9
    assert ("vis", "maritime") in available_configurations()


def test_ocean_alias_matches_canonical_maritime_scene():
    ocean = environment_radiance_upper_bound(60.0, 22.0, "vis", "ocean")
    maritime = environment_radiance_upper_bound(60.0, 22.0, "VIS", "maritime")
    assert ocean == pytest.approx(maritime, rel=0.0, abs=0.0)
    assert get_parameters("visible", "ocean").scene == "maritime"


def test_safety_factor_scales_only_the_frozen_curve():
    base = environment_radiance_upper_bound(75.0, 10.0, "vis", "desert")
    safe = safe_radiance_upper_bound(
        75.0,
        10.0,
        "vis",
        "desert",
        safety_factor=1.25,
    )
    assert safe == pytest.approx(1.25 * base)


def test_reference_safe_angle_query():
    theta_min = minimum_safe_angle(
        32.540004502658135,
        15.0,
        "vis",
        "rural",
    )
    assert theta_min == pytest.approx(97.5)


def test_safe_angle_boundary_cases():
    assert minimum_safe_angle(1e9, 15.0, "vis", "rural") == 15.0
    assert minimum_safe_angle(0.0, 15.0, "vis", "rural") is None


@pytest.mark.parametrize(
    "call",
    [
        lambda: environment_radiance_upper_bound(14.9, 15.0, "vis", "rural"),
        lambda: environment_radiance_upper_bound(180.0, 15.0, "vis", "rural"),
        lambda: environment_radiance_upper_bound(30.0, 1.9, "vis", "rural"),
        lambda: environment_radiance_upper_bound(30.0, 30.1, "vis", "rural"),
        lambda: safe_radiance_upper_bound(
            30.0, 15.0, "vis", "rural", safety_factor=0.99
        ),
        lambda: minimum_safe_angle(-1.0, 15.0, "vis", "rural"),
    ],
)
def test_invalid_inputs_fail_closed(call):
    with pytest.raises(ValueError):
        call()
