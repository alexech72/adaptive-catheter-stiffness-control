import numpy as np

from simulation.vessel_geometry import (
    calculate_curvature,
    generate_straight_vessel,
    generate_circular_arc,
)


def test_straight_vessel_has_zero_curvature():
    """
    A straight vessel should have essentially zero curvature.
    """

    x, y = generate_straight_vessel()

    curvature = calculate_curvature(x, y)

    assert np.max(np.abs(curvature)) < 1e-8


def test_circular_arc_curvature():
    """
    A circular arc should have curvature approximately equal to 1 / radius.
    """

    radius = 20

    x, y = generate_circular_arc(radius=radius)

    curvature = calculate_curvature(x, y)

    # Ignore boundary points because numerical derivatives are
    # less accurate near the ends of the sampled curve.
    interior_curvature = curvature[10:-10]

    calculated = np.mean(interior_curvature)
    expected = 1 / radius

    assert np.isclose(
        calculated,
        expected,
        rtol=0.02
    )