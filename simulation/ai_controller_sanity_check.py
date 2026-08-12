"""
AI Controller Sanity Check
--------------------------

Tests the AI-assisted stiffness controller under several
representative vessel-curvature conditions before full-vessel
integration.
"""

from controllers.ai_assisted_controller import (
    AIAssistedController,
)


def main():

    controller = AIAssistedController()

    scenarios = [
        {
            "name": "Nearly Straight",
            "curvature": 0.005,
        },
        {
            "name": "Moderate Bend",
            "curvature": 0.050,
        },
        {
            "name": "Severe Bend",
            "curvature": 0.150,
        },
    ]

    print()
    print("AI Controller Sanity Check")
    print("==========================")

    for scenario in scenarios:

        best_stiffness, best_risk, candidates = (
            controller.select_stiffness(
                curvature=scenario["curvature"],
                friction=0.20,
                current_stiffness=0.50,
                commanded_velocity=4.0,
                base_force=0.1,
            )
        )

        print()
        print(
            f"{scenario['name']}"
        )

        print(
            f"Curvature: "
            f"{scenario['curvature']:.3f}"
        )

        print(
            f"Selected stiffness: "
            f"{best_stiffness:.2f}"
        )

        print(
            f"Predicted risk: "
            f"{best_risk:.4f}"
        )

        print("--------------------------")


if __name__ == "__main__":
    main()