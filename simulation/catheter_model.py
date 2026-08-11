"""
Catheter Mechanics Model
------------------------

Reduced-order V1 model for catheter navigation.

The model investigates qualitative relationships between:

- vessel curvature
- friction
- catheter stiffness
- navigation resistance
- advancement velocity
- proximal pushing force

IMPORTANT:
The equations in this V1 model are simplified engineering assumptions.
Outputs are comparative simulation values and are not validated clinical
measurements.
"""


def calculate_navigation_resistance(
    curvature,
    friction,
    stiffness,
):
    """
    Calculate a simplified navigation resistance score.

    Parameters
    ----------
    curvature : float
        Local vessel curvature.

    friction : float
        Simplified friction coefficient.

    stiffness : float
        Normalized catheter stiffness from 0 to 1.

        0 = very flexible
        1 = very stiff

    Returns
    -------
    float
        Dimensionless navigation resistance score.
    """

    if not 0 <= stiffness <= 1:
        raise ValueError("Stiffness must be between 0 and 1.")

    if curvature < 0:
        raise ValueError("Curvature cannot be negative.")

    if friction < 0:
        raise ValueError("Friction cannot be negative.")

    # Friction always increases navigation resistance.
    friction_penalty = friction

    # A stiff catheter is penalized more strongly
    # when navigating high-curvature geometry.
    curvature_penalty = (
        10
        * curvature
        * (0.5 + stiffness)
    )

    # An extremely flexible catheter has reduced pushability.
    low_stiffness_penalty = (
        0.2
        * (1 - stiffness) ** 2
    )

    total_resistance = (
        friction_penalty
        + curvature_penalty
        + low_stiffness_penalty
    )

    return total_resistance


def calculate_advancement_velocity(
    commanded_velocity,
    resistance,
):
    """
    Estimate actual catheter advancement velocity.

    Higher resistance reduces forward advancement.
    """

    actual_velocity = (
        commanded_velocity
        / (1 + resistance)
    )

    return actual_velocity


def calculate_push_force(
    base_force,
    resistance,
):
    """
    Estimate proximal pushing force.

    Higher navigation resistance requires more proximal force.
    """

    push_force = (
        base_force
        * (1 + resistance)
    )

    return push_force


def simulate_local_navigation(
    curvature,
    friction,
    stiffness,
    commanded_velocity=4.0,
    base_force=0.1,
):
    """
    Simulate catheter behavior at one local vessel position.
    """

    resistance = calculate_navigation_resistance(
        curvature,
        friction,
        stiffness,
    )

    velocity = calculate_advancement_velocity(
        commanded_velocity,
        resistance,
    )

    force = calculate_push_force(
        base_force,
        resistance,
    )

    return {
        "curvature": curvature,
        "friction": friction,
        "stiffness": stiffness,
        "resistance": resistance,
        "velocity": velocity,
        "push_force": force,
    }


def main():
    """
    Run several simple catheter-mechanics examples.
    """

    print("Catheter Mechanics Model")
    print("------------------------")

    scenarios = [
        {
            "name": "Flexible catheter - straight region",
            "curvature": 0.0,
            "friction": 0.2,
            "stiffness": 0.25,
        },
        {
            "name": "Stiff catheter - straight region",
            "curvature": 0.0,
            "friction": 0.2,
            "stiffness": 0.75,
        },
        {
            "name": "Flexible catheter - sharp curve",
            "curvature": 0.10,
            "friction": 0.2,
            "stiffness": 0.25,
        },
        {
            "name": "Stiff catheter - sharp curve",
            "curvature": 0.10,
            "friction": 0.2,
            "stiffness": 0.75,
        },
    ]

    for scenario in scenarios:

        result = simulate_local_navigation(
            curvature=scenario["curvature"],
            friction=scenario["friction"],
            stiffness=scenario["stiffness"],
        )

        print()
        print(scenario["name"])

        print(
            f"Resistance: {result['resistance']:.3f}"
        )

        print(
            f"Velocity:   {result['velocity']:.3f}"
        )

        print(
            f"Push force: {result['push_force']:.3f}"
        )


if __name__ == "__main__":
    main()