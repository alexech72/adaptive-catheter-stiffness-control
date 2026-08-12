"""
AI-Assisted Adaptive Stiffness Controller
-----------------------------------------

Uses the frozen Random Forest navigation-risk estimator together with
the catheter digital twin to select a stiffness command.

For every candidate stiffness:

1. Simulate the local catheter response.
2. Estimate navigation risk using the trained Random Forest.
3. Compare candidate risk predictions.
4. Select the stiffness with the lowest predicted risk.

This is a model-based AI-assisted controller.

The predicted risk is a synthetic digital-twin engineering metric and
is not a clinically validated probability of failure.
"""

import numpy as np

from ml.risk_predictor import (
    NavigationRiskPredictor,
)

from simulation.catheter_model import (
    simulate_local_navigation,
)


class AIAssistedController:
    """
    Select catheter stiffness using predicted navigation risk.
    """

    def __init__(
        self,
        minimum_stiffness=0.10,
        maximum_stiffness=0.90,
        stiffness_step=0.05,
    ):

        self.minimum_stiffness = (
            minimum_stiffness
        )

        self.maximum_stiffness = (
            maximum_stiffness
        )

        self.stiffness_step = (
            stiffness_step
        )

        # Load frozen Random Forest model once.
        self.risk_predictor = (
            NavigationRiskPredictor()
        )

        # Candidate stiffness values:
        # 0.10, 0.15, 0.20 ... 0.90

        self.candidate_stiffnesses = (
            np.arange(
                minimum_stiffness,
                maximum_stiffness
                + stiffness_step / 2,
                stiffness_step,
            )
        )


    def select_stiffness(
        self,
        curvature,
        friction,
        current_stiffness,
        commanded_velocity=4.0,
        base_force=0.1,
    ):
        """
        Evaluate candidate stiffness values and select
        the one with the lowest predicted risk.

        Returns
        -------
        best_stiffness : float
            Selected stiffness command.

        best_predicted_risk : float
            Lowest predicted risk found.

        candidate_results : list
            Results for every stiffness evaluated.
        """

        candidate_results = []

        best_stiffness = None
        best_predicted_risk = float(
            "inf"
        )

        for candidate_stiffness in (
            self.candidate_stiffnesses
        ):

            # -----------------------------------------
            # Predict mechanical response for this
            # candidate stiffness.
            # -----------------------------------------

            local_result = (
                simulate_local_navigation(
                    curvature=curvature,
                    friction=friction,
                    stiffness=candidate_stiffness,
                    commanded_velocity=commanded_velocity,
                    base_force=base_force,
                )
            )

            # -----------------------------------------
            # AI estimates risk from the resulting
            # navigation state.
            # -----------------------------------------

            predicted_risk = (
                self.risk_predictor.predict(
                    curvature=curvature,
                    current_stiffness=(
                        candidate_stiffness
                    ),
                    push_force=(
                        local_result[
                            "push_force"
                        ]
                    ),
                    velocity=(
                        local_result[
                            "velocity"
                        ]
                    ),
                )
            )

            candidate_results.append({
                "stiffness":
                    float(
                        candidate_stiffness
                    ),

                "predicted_risk":
                    predicted_risk,

                "predicted_resistance":
                    local_result[
                        "resistance"
                    ],

                "predicted_push_force":
                    local_result[
                        "push_force"
                    ],

                "predicted_velocity":
                    local_result[
                        "velocity"
                    ],
            })

            # -----------------------------------------
            # Keep lowest-risk candidate.
            # -----------------------------------------

            if (
                predicted_risk
                < best_predicted_risk
            ):

                best_predicted_risk = (
                    predicted_risk
                )

                best_stiffness = float(
                    candidate_stiffness
                )

        return (
            best_stiffness,
            best_predicted_risk,
            candidate_results,
        )


def main():

    controller = (
        AIAssistedController()
    )

    best_stiffness, best_risk, candidates = (
        controller.select_stiffness(
            curvature=0.08,
            friction=0.20,
            current_stiffness=0.50,
            commanded_velocity=4.0,
            base_force=0.1,
        )
    )

    print()
    print("AI-Assisted Stiffness Selection")
    print("-------------------------------")

    print()
    print("Candidate results:")

    for result in candidates:

        print(
            f"Stiffness "
            f"{result['stiffness']:.2f}"
            f" -> predicted risk "
            f"{result['predicted_risk']:.4f}"
        )

    print()

    print(
        f"Selected stiffness: "
        f"{best_stiffness:.2f}"
    )

    print(
        f"Lowest predicted risk: "
        f"{best_risk:.4f}"
    )


if __name__ == "__main__":
    main()