import numpy as np

from simulation.vessel_geometry import (
    generate_random_tortuous_vessel,
    calculate_curvature,
)


def test_same_seed_produces_same_vessel():
    """
    Using the same random seed should reproduce
    exactly the same vessel geometry.
    """

    x1, y1 = generate_random_tortuous_vessel(
        seed=42
    )

    x2, y2 = generate_random_tortuous_vessel(
        seed=42
    )

    assert np.array_equal(x1, x2)
    assert np.array_equal(y1, y2)


def test_different_seeds_produce_different_vessels():
    """
    Different seeds should generate different
    vessel geometries.
    """

    _, y1 = generate_random_tortuous_vessel(
        seed=42
    )

    _, y2 = generate_random_tortuous_vessel(
        seed=43
    )

    assert not np.array_equal(y1, y2)


def test_random_vessel_has_valid_curvature():
    """
    Random vessel curvature should contain valid,
    finite, nonnegative values.
    """

    x, y = generate_random_tortuous_vessel(
        seed=100
    )

    curvature = calculate_curvature(
        x,
        y
    )

    assert len(curvature) == len(x)

    assert np.all(
        np.isfinite(curvature)
    )

    assert np.all(
        curvature >= 0
    )