"""
Balanced Adaptive Stiffness Controller - V2
-------------------------------------------

Second-generation rule-based controller intended to balance:

- trackability in curved regions
- pushability in straighter regions
- structural support against excessive flexibility

Unlike Controller V1, V2 avoids driving stiffness to extreme values
unless necessary.

All thresholds are simulation-specific engineering assumptions and are
not clinical limits.
"""


def clamp(value, minimum, maximum):
    """
    Restrict a value to an allowable range.
    """

    return max(
        minimum,
        min(value, maximum)
    )


def select_balanced_stiffness(
    curvature,
    push_force,
    velocity,
    current_stiffness,
    minimum_stiffness=0.20,
    maximum_stiffness=0.85,
):
    """
    Select the next stiffness using a balanced rule set.

    Returns
    -------
    new_stiffness : float
        Updated stiffness command.

    action : str
        INCREASE, DECREASE, or HOLD.

    reason : str
        Explanation for the decision.
    """

    new_stiffness = current_stiffness
    action = "HOLD"
    reason = "Navigation state acceptable"

    # ---------------------------------------------------------
    # RULE 1
    # Severe curvature:
    # become more flexible, but maintain enough stiffness
    # to preserve structural support.
    # ---------------------------------------------------------

    if curvature >= 0.08:

        if current_stiffness > 0.35:

            new_stiffness -= 0.05
            action = "DECREASE"
            reason = "Severe curvature requires greater flexibility"

        else:

            action = "HOLD"
            reason = "Minimum support stiffness maintained in severe curve"

    # ---------------------------------------------------------
    # RULE 2
    # Moderate-high curvature with elevated pushing force:
    # reduce stiffness gradually.
    # ---------------------------------------------------------

    elif curvature >= 0.05 and push_force >= 0.16:

        if current_stiffness > 0.40:

            new_stiffness -= 0.05
            action = "DECREASE"
            reason = "Curvature and pushing force indicate tracking difficulty"

    # ---------------------------------------------------------
    # RULE 3
    # Moderate curvature:
    # steer stiffness toward a middle operating region rather
    # than toward either extreme.
    # ---------------------------------------------------------

    elif 0.02 < curvature < 0.05:

        if current_stiffness > 0.60:

            new_stiffness -= 0.025
            action = "DECREASE"
            reason = "Moderate curvature favors reduced stiffness"

        elif current_stiffness < 0.40:

            new_stiffness += 0.025
            action = "INCREASE"
            reason = "Moderate curvature allows additional support"

    # ---------------------------------------------------------
    # RULE 4
    # Straight region with poor advancement:
    # increase stiffness to improve pushability.
    # ---------------------------------------------------------

    elif curvature <= 0.02 and velocity < 3.2:

        new_stiffness += 0.05
        action = "INCREASE"
        reason = "Low curvature and reduced velocity indicate poor pushability"

    # ---------------------------------------------------------
    # RULE 5
    # Very straight region:
    # gradually restore stiffness.
    # ---------------------------------------------------------

    elif curvature <= 0.01 and current_stiffness < 0.75:

        new_stiffness += 0.025
        action = "INCREASE"
        reason = "Straight region permits increased mechanical support"

    new_stiffness = clamp(
        new_stiffness,
        minimum_stiffness,
        maximum_stiffness,
    )

    return new_stiffness, action, reason