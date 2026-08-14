"""
Tests for AI-assisted catheter stiffness controllers.

These tests verify software/controller behavior only.
They do not constitute physical or clinical validation.
"""

import pytest

from controllers.ai_assisted_controller import (
    AIAssistedController,
)

from controllers.rate_limited_ai_controller import (
    RateLimitedAIController,
)


def test_ai_controller_prefers_stiff_setting_in_straight_region():
    """
    A nearly straight vessel should favor a relatively
    stiff catheter under the reference conditions.
    """

    controller = AIAssistedController()

    (
        selected_stiffness,
        predicted_risk,
        candidate_results,
    ) = controller.select_stiffness(
        curvature=0.005,
        friction=0.20,
        current_stiffness=0.50,
        commanded_velocity=4.0,
        base_force=0.10,
    )

    assert selected_stiffness == pytest.approx(
        0.90
    )

    assert 0.0 <= predicted_risk <= 1.0


def test_ai_controller_prefers_flexible_setting_in_severe_bend():
    """
    A severe bend should favor a flexible catheter
    under the reference conditions.
    """

    controller = AIAssistedController()

    (
        selected_stiffness,
        predicted_risk,
        candidate_results,
    ) = controller.select_stiffness(
        curvature=0.150,
        friction=0.20,
        current_stiffness=0.50,
        commanded_velocity=4.0,
        base_force=0.10,
    )

    assert selected_stiffness == pytest.approx(
        0.10
    )

    assert 0.0 <= predicted_risk <= 1.0


def test_ai_controller_evaluates_full_candidate_range():
    """
    The unconstrained AI controller should evaluate
    all stiffness candidates from 0.10 through 0.90
    in increments of 0.05.
    """

    controller = AIAssistedController()

    (
        selected_stiffness,
        predicted_risk,
        candidate_results,
    ) = controller.select_stiffness(
        curvature=0.050,
        friction=0.20,
        current_stiffness=0.50,
        commanded_velocity=4.0,
        base_force=0.10,
    )

    assert len(candidate_results) == 17

    stiffness_values = [
        result["stiffness"]
        for result in candidate_results
    ]

    assert min(stiffness_values) == pytest.approx(
        0.10
    )

    assert max(stiffness_values) == pytest.approx(
        0.90
    )


def test_rate_limited_controller_obeys_final_rate_limit():
    """
    The final controller must never change stiffness
    by more than 0.10 during one simulation step.
    """

    maximum_change = 0.10

    controller = RateLimitedAIController(
        maximum_stiffness_change=maximum_change
    )

    current_stiffness = 0.90

    (
        selected_stiffness,
        predicted_risk,
        unconstrained_stiffness,
        candidate_results,
    ) = controller.select_stiffness(
        curvature=0.150,
        friction=0.20,
        current_stiffness=current_stiffness,
        commanded_velocity=4.0,
        base_force=0.10,
    )

    actual_change = abs(
        selected_stiffness
        - current_stiffness
    )

    assert actual_change <= (
        maximum_change + 1e-9
    )

    # The severe bend should make the unconstrained
    # controller want substantially more flexibility.
    assert unconstrained_stiffness < (
        current_stiffness
    )


def test_rate_limited_controller_stays_inside_global_bounds():
    """
    Final commands must stay inside the permitted
    stiffness range of 0.10 to 0.90.
    """

    controller = RateLimitedAIController(
        maximum_stiffness_change=0.10
    )

    for curvature in [
        0.005,
        0.050,
        0.150,
    ]:

        (
            selected_stiffness,
            predicted_risk,
            unconstrained_stiffness,
            candidate_results,
        ) = controller.select_stiffness(
            curvature=curvature,
            friction=0.20,
            current_stiffness=0.50,
            commanded_velocity=4.0,
            base_force=0.10,
        )

        assert (
            0.10
            <= selected_stiffness
            <= 0.90
        )