"""
Rule-Based Adaptive Stiffness Controller
----------------------------------------

Selects catheter stiffness using only simulated measurable feedback:

- local curvature
- proximal pushing force
- advancement velocity
- current stiffness

The controller does NOT know the optimal stiffness calculated by the
optimal-stiffness map.

V1 rules are engineering heuristics used to establish an adaptive-control
baseline before machine learning is introduced.
"""


def clamp(value, minimum, maximum):
    """
    Restrict a value to a defined range.
    """

    return max(
        minimum,
        min(value, maximum)
    )


def select_stiffness(
    curvature,
    push_force,
    velocity,
    current_stiffness,
    minimum_stiffness=0.10,
    maximum_stiffness=0.90,
    stiffness_step=0.05,
):
    """
    Select the next catheter stiffness using rule-based feedback.

    Returns
    -------
    new_stiffness : float
        Updated stiffness command.

    action : str
        INCREASE, DECREASE, or HOLD.

    reason : str
        Explanation for the controller decision.
    """

    new_stiffness = current_stiffness
    action = "HOLD"
    reason = "Navigation state acceptable"

    # ---------------------------------------------------------
    # RULE 1:
    # High curvature + high force indicates difficult tracking.
    # Reduce stiffness to improve flexibility.
    # ---------------------------------------------------------

    if curvature >= 0.06 and push_force >= 0.16:

        new_stiffness -= stiffness_step

        action = "DECREASE"

        reason = (
            "High curvature and elevated pushing force"
        )

    # ---------------------------------------------------------
    # RULE 2:
    # High curvature + slow advancement also suggests that the
    # catheter is struggling to follow the vessel.
    # ---------------------------------------------------------

    elif curvature >= 0.06 and velocity <= 2.5:

        new_stiffness -= stiffness_step

        action = "DECREASE"

        reason = (
            "High curvature and reduced advancement velocity"
        )

    # ---------------------------------------------------------
    # RULE 3:
    # In a relatively straight region, poor advancement may
    # indicate insufficient pushability.
    # Increase stiffness.
    # ---------------------------------------------------------

    elif curvature <= 0.02 and velocity < 3.2:

        new_stiffness += stiffness_step

        action = "INCREASE"

        reason = (
            "Low curvature with reduced advancement velocity"
        )

    # ---------------------------------------------------------
    # RULE 4:
    # In very straight regions, gradually restore stiffness
    # to improve mechanical support.
    # ---------------------------------------------------------

    elif curvature <= 0.01 and current_stiffness < 0.75:

        new_stiffness += stiffness_step

        action = "INCREASE"

        reason = (
            "Low-curvature region permits greater support"
        )

    # Keep stiffness inside allowable limits.

    new_stiffness = clamp(
        new_stiffness,
        minimum_stiffness,
        maximum_stiffness,
    )

    return new_stiffness, action, reason