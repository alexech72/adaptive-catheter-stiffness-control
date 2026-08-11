"""
Navigation Failure Model
------------------------

Provides simplified V1 estimates of:

- buckling risk
- guidewire kickback

These outputs are comparative simulation metrics and are not
validated clinical measurements.

The purpose is to evaluate whether different catheter stiffness
strategies reduce mechanically unfavorable navigation states.
"""


def clamp(value, minimum=0.0, maximum=1.0):
    """
    Restrict a value to a specified range.
    """

    return max(
        minimum,
        min(value, maximum)
    )


def calculate_buckling_risk(
    push_force,
    velocity,
    stiffness,
):
    """
    Estimate normalized catheter buckling risk.

    Buckling risk increases when:
    - pushing force is elevated
    - forward advancement is reduced
    - catheter stiffness is low

    Returns
    -------
    float
        Risk score between 0 and 1.
    """

    force_component = push_force / 0.30

    low_velocity_component = (
        max(0.0, 4.0 - velocity) / 4.0
    )

    flexibility_component = (
        1.0 - stiffness
    )

    risk = (
        0.40 * force_component
        + 0.35 * low_velocity_component
        + 0.25 * flexibility_component
    )

    return clamp(risk)


def calculate_kickback(
    push_force,
    velocity,
    resistance,
):
    """
    Estimate normalized guidewire kickback.

    Kickback increases when:
    - pushing force is high
    - navigation resistance is high
    - forward advancement is poor

    Returns
    -------
    float
        Normalized kickback score.
    """

    force_component = push_force / 0.30

    resistance_component = resistance / 2.0

    low_velocity_component = (
        max(0.0, 4.0 - velocity) / 4.0
    )

    kickback = (
        0.40 * force_component
        + 0.35 * resistance_component
        + 0.25 * low_velocity_component
    )

    return clamp(kickback)