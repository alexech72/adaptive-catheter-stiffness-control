from controllers.rule_based_controller import select_stiffness


def test_high_curvature_reduces_stiffness():
    """
    High curvature and elevated force should reduce stiffness.
    """

    new_stiffness, action, _ = select_stiffness(
        curvature=0.10,
        push_force=0.22,
        velocity=2.0,
        current_stiffness=0.70,
    )

    assert new_stiffness < 0.70
    assert action == "DECREASE"


def test_low_curvature_can_increase_stiffness():
    """
    Low curvature with poor advancement should increase stiffness.
    """

    new_stiffness, action, _ = select_stiffness(
        curvature=0.01,
        push_force=0.13,
        velocity=2.8,
        current_stiffness=0.50,
    )

    assert new_stiffness > 0.50
    assert action == "INCREASE"


def test_stiffness_does_not_exceed_maximum():
    """
    Controller must respect the upper stiffness limit.
    """

    new_stiffness, _, _ = select_stiffness(
        curvature=0.0,
        push_force=0.10,
        velocity=2.8,
        current_stiffness=0.90,
    )

    assert new_stiffness <= 0.90


def test_stiffness_does_not_drop_below_minimum():
    """
    Controller must respect the lower stiffness limit.
    """

    new_stiffness, _, _ = select_stiffness(
        curvature=0.10,
        push_force=0.25,
        velocity=1.5,
        current_stiffness=0.10,
    )

    assert new_stiffness >= 0.10