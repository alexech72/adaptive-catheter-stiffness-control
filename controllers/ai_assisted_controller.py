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
        Evaluate all candidate stiffness values and
        choose the one with the lowest predicted risk.
        """

        candidate_results = []
        model_inputs = []

        # Calculate mechanical response for every
        # candidate stiffness.
        for candidate_stiffness in self.candidate_stiffnesses:

            local_result = simulate_local_navigation(
                curvature=curvature,
                friction=friction,
                stiffness=candidate_stiffness,
                commanded_velocity=commanded_velocity,
                base_force=base_force,
            )

            candidate_results.append({
                "stiffness": float(candidate_stiffness),
                "predicted_resistance":
                    local_result["resistance"],
                "predicted_push_force":
                    local_result["push_force"],
                "predicted_velocity":
                    local_result["velocity"],
            })

            model_inputs.append({
                "curvature":
                    curvature,
                "current_stiffness":
                    candidate_stiffness,
                "push_force":
                    local_result["push_force"],
                "velocity":
                    local_result["velocity"],
            })

        # Predict risk for ALL stiffness candidates
        # with one Random Forest call.
        predicted_risks = (
            self.risk_predictor.predict_batch(
                model_inputs
            )
        )

        for result, predicted_risk in zip(
            candidate_results,
            predicted_risks,
        ):
            result["predicted_risk"] = float(
                predicted_risk
            )

        # Pick candidate with lowest predicted risk.
        best_result = min(
            candidate_results,
            key=lambda result:
                result["predicted_risk"],
        )

        return (
            best_result["stiffness"],
            best_result["predicted_risk"],
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