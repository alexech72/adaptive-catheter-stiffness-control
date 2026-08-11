from simulation.failure_model import (
    calculate_buckling_risk,
    calculate_kickback,
)


def test_higher_force_increases_buckling_risk():
    """
    Higher pushing force should increase buckling risk
    when other conditions are held constant.
    """

    low_force_risk = calculate_buckling_risk(
        push_force=0.12,
        velocity=2.5,
        stiffness=0.40,
    )

    high_force_risk = calculate_buckling_risk(
        push_force=0.24,
        velocity=2.5,
        stiffness=0.40,
    )

    assert high_force_risk > low_force_risk


def test_lower_velocity_increases_buckling_risk():
    """
    Reduced forward advancement should increase buckling risk.
    """

    fast_risk = calculate_buckling_risk(
        push_force=0.18,
        velocity=3.2,
        stiffness=0.40,
    )

    slow_risk = calculate_buckling_risk(
        push_force=0.18,
        velocity=1.6,
        stiffness=0.40,
    )

    assert slow_risk > fast_risk


def test_lower_stiffness_increases_buckling_risk():
    """
    More flexible configurations should have greater
    simulated buckling susceptibility under the same load.
    """

    flexible_risk = calculate_buckling_risk(
        push_force=0.18,
        velocity=2.2,
        stiffness=0.20,
    )

    stiff_risk = calculate_buckling_risk(
        push_force=0.18,
        velocity=2.2,
        stiffness=0.80,
    )

    assert flexible_risk > stiff_risk


def test_higher_resistance_increases_kickback():
    """
    Higher navigation resistance should increase
    simulated guidewire kickback.
    """

    low_resistance = calculate_kickback(
        push_force=0.18,
        velocity=2.2,
        resistance=0.50,
    )

    high_resistance = calculate_kickback(
        push_force=0.18,
        velocity=2.2,
        resistance=1.50,
    )

    assert high_resistance > low_resistance


def test_lower_velocity_increases_kickback():
    """
    Poorer forward advancement should increase kickback.
    """

    fast = calculate_kickback(
        push_force=0.18,
        velocity=3.2,
        resistance=1.0,
    )

    slow = calculate_kickback(
        push_force=0.18,
        velocity=1.6,
        resistance=1.0,
    )

    assert slow > fast


def test_failure_scores_are_bounded():
    """
    Failure metrics should remain between 0 and 1.
    """

    buckling = calculate_buckling_risk(
        push_force=1.0,
        velocity=0.0,
        stiffness=0.0,
    )

    kickback = calculate_kickback(
        push_force=1.0,
        velocity=0.0,
        resistance=5.0,
    )

    assert 0.0 <= buckling <= 1.0
    assert 0.0 <= kickback <= 1.0