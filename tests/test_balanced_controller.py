from controllers.balanced_controller import (
    select_balanced_stiffness,
)


def test_severe_curvature_reduces_high_stiffness():

    new_stiffness, action, _ = select_balanced_stiffness(
        curvature=0.10,
        push_force=0.22,
        velocity=1.8,
        current_stiffness=0.70,
    )

    assert new_stiffness < 0.70
    assert action == "DECREASE"


def test_severe_curve_preserves_minimum_support():

    new_stiffness, action, _ = select_balanced_stiffness(
        curvature=0.10,
        push_force=0.22,
        velocity=1.8,
        current_stiffness=0.35,
    )

    assert new_stiffness >= 0.35
    assert action == "HOLD"


def test_straight_region_increases_stiffness():

    new_stiffness, action, _ = select_balanced_stiffness(
        curvature=0.01,
        push_force=0.14,
        velocity=2.8,
        current_stiffness=0.50,
    )

    assert new_stiffness > 0.50
    assert action == "INCREASE"


def test_controller_respects_lower_limit():

    new_stiffness, _, _ = select_balanced_stiffness(
        curvature=0.10,
        push_force=0.25,
        velocity=1.5,
        current_stiffness=0.20,
    )

    assert new_stiffness >= 0.20


def test_controller_respects_upper_limit():

    new_stiffness, _, _ = select_balanced_stiffness(
        curvature=0.0,
        push_force=0.15,
        velocity=2.5,
        current_stiffness=0.85,
    )

    assert new_stiffness <= 0.85