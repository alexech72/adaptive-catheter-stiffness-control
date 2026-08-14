"""
Rate-Limited AI-Assisted Stiffness Controller
---------------------------------------------

Adds a physically motivated rate constraint to the existing
AI-assisted model-based controller.

The unconstrained AI may select any stiffness from 0.10 to 0.90.

This controller restricts the next command so stiffness may change
by no more than a specified amount per simulation step.

Default maximum change:
    0.05 stiffness units per step

This is a computational R&D model and is not clinically validated.
"""

from controllers.ai_assisted_controller import (
    AIAssistedController,
)


class RateLimitedAIController:
    """
    AI-assisted controller with a stiffness-change constraint.
    """

    def __init__(
        self,
        maximum_stiffness_change=0.10,
    ):

        self.maximum_stiffness_change = (
            maximum_stiffness_change
        )

        # Reuse the already-developed AI controller.
        self.base_controller = (
            AIAssistedController()
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
        Select the lowest predicted-risk stiffness that is reachable
        from the current stiffness during this control step.

        Returns
        -------
        selected_stiffness : float
            Rate-limited stiffness command.

        predicted_risk : float
            AI-predicted risk for the selected command.

        unconstrained_stiffness : float
            Stiffness the AI would have selected without a rate limit.

        candidate_results : list
            All candidate evaluations from the original AI controller.
        """

        (
            unconstrained_stiffness,
            unconstrained_risk,
            candidate_results,
        ) = self.base_controller.select_stiffness(
            curvature=curvature,
            friction=friction,
            current_stiffness=current_stiffness,
            commanded_velocity=commanded_velocity,
            base_force=base_force,
        )

        # -----------------------------------------------------
        # Determine which candidate stiffness values are
        # reachable during this step.
        # -----------------------------------------------------

        minimum_reachable = (
            current_stiffness
            - self.maximum_stiffness_change
        )

        maximum_reachable = (
            current_stiffness
            + self.maximum_stiffness_change
        )

        reachable_candidates = [
            result
            for result in candidate_results
            if (
                result["stiffness"]
                >= minimum_reachable - 1e-9
                and
                result["stiffness"]
                <= maximum_reachable + 1e-9
            )
        ]

        # Safety check.
        if not reachable_candidates:

            raise RuntimeError(
                "No reachable stiffness candidates were found."
            )

        # -----------------------------------------------------
        # Among physically reachable commands, choose the one
        # with the lowest AI-predicted risk.
        # -----------------------------------------------------

        best_reachable = min(
            reachable_candidates,
            key=lambda result:
                result["predicted_risk"],
        )

        selected_stiffness = (
            best_reachable["stiffness"]
        )

        selected_risk = (
            best_reachable["predicted_risk"]
        )

        return (
            selected_stiffness,
            selected_risk,
            unconstrained_stiffness,
            candidate_results,
        )


def main():

    controller = RateLimitedAIController(
        maximum_stiffness_change=0.05
    )

    # Deliberately start stiff in a severe bend.
    #
    # The unconstrained AI should want to become much more
    # flexible, but the rate limit should prevent an
    # instantaneous large stiffness change.

    (
        selected_stiffness,
        selected_risk,
        unconstrained_stiffness,
        candidate_results,
    ) = controller.select_stiffness(
        curvature=0.150,
        friction=0.20,
        current_stiffness=0.90,
        commanded_velocity=4.0,
        base_force=0.10,
    )

    print()
    print("Rate-Limited AI Controller Test")
    print("===============================")

    print(
        f"Current stiffness: "
        f"{0.90:.2f}"
    )

    print(
        f"Unconstrained AI choice: "
        f"{unconstrained_stiffness:.2f}"
    )

    print(
        f"Rate-limited choice: "
        f"{selected_stiffness:.2f}"
    )

    print(
        f"Maximum allowed change: "
        f"{controller.maximum_stiffness_change:.2f}"
    )

    print(
        f"Predicted risk after limited command: "
        f"{selected_risk:.4f}"
    )


if __name__ == "__main__":
    main()