from simulation.catheter_model import (
    calculate_navigation_resistance,
    calculate_advancement_velocity,
    calculate_push_force,
)


def test_higher_friction_increases_resistance():
    """
    Increasing friction should increase navigation resistance.
    """

    low_friction = calculate_navigation_resistance(
        curvature=0.02,
        friction=0.1,
        stiffness=0.5,
    )

    high_friction = calculate_navigation_resistance(
        curvature=0.02,
        friction=0.4,
        stiffness=0.5,
    )

    assert high_friction > low_friction


def test_stiff_catheter_better_in_straight_region():
    """
    In a low-curvature region, a stiffer catheter should have
    lower resistance than a very flexible catheter.
    """

    flexible = calculate_navigation_resistance(
        curvature=0.0,
        friction=0.2,
        stiffness=0.25,
    )

    stiff = calculate_navigation_resistance(
        curvature=0.0,
        friction=0.2,
        stiffness=0.75,
    )

    assert stiff < flexible


def test_flexible_catheter_better_in_sharp_curve():
    """
    In a high-curvature region, the flexible catheter should
    have lower resistance than the stiff catheter.
    """

    flexible = calculate_navigation_resistance(
        curvature=0.10,
        friction=0.2,
        stiffness=0.25,
    )

    stiff = calculate_navigation_resistance(
        curvature=0.10,
        friction=0.2,
        stiffness=0.75,
    )

    assert flexible < stiff


def test_resistance_reduces_velocity():
    """
    Increasing navigation resistance should decrease
    catheter advancement velocity.
    """

    low_resistance_velocity = calculate_advancement_velocity(
        commanded_velocity=4.0,
        resistance=0.2,
    )

    high_resistance_velocity = calculate_advancement_velocity(
        commanded_velocity=4.0,
        resistance=1.0,
    )

    assert high_resistance_velocity < low_resistance_velocity


def test_resistance_increases_push_force():
    """
    Increasing navigation resistance should increase
    proximal pushing force.
    """

    low_force = calculate_push_force(
        base_force=0.1,
        resistance=0.2,
    )

    high_force = calculate_push_force(
        base_force=0.1,
        resistance=1.0,
    )

    assert high_force > low_force