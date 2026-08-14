"""
Rate-Limited AI Navigation Simulator
------------------------------------

Runs the AI-assisted catheter stiffness controller through a complete
tortuous vessel while limiting stiffness change between consecutive
simulation steps.

At each location:

1. The unconstrained AI identifies its preferred stiffness.
2. The rate-limited controller considers only reachable stiffnesses.
3. The lowest-risk reachable stiffness is selected.
4. The digital twin calculates the resulting mechanical response.
5. Failure-related metrics and AI predictions are recorded.

The stiffness-change limit is a computational control constraint.
It is not yet calibrated to a physical actuator or time constant.

This model is not clinically validated.
"""

import pandas as pd
import matplotlib.pyplot as plt

from controllers.rate_limited_ai_controller import (
    RateLimitedAIController,
)

from simulation.vessel_geometry import (
    generate_tortuous_vessel,
    calculate_curvature,
)

from simulation.navigation_simulator import (
    calculate_arc_length,
)

from simulation.catheter_model import (
    simulate_local_navigation,
)

from simulation.failure_model import (
    calculate_buckling_risk,
    calculate_kickback,
)


def run_rate_limited_ai_navigation(
    initial_stiffness=0.50,
    friction=0.20,
    commanded_velocity=4.0,
    base_force=0.10,
    maximum_stiffness_change=0.10,
):
    """
    Run rate-limited AI-assisted navigation through
    the complete tortuous vessel.
    """

    controller = RateLimitedAIController(
        maximum_stiffness_change=(
            maximum_stiffness_change
        )
    )

    x, y = generate_tortuous_vessel()

    curvature = calculate_curvature(
        x,
        y,
    )

    position = calculate_arc_length(
        x,
        y,
    )

    current_stiffness = (
        initial_stiffness
    )

    results = []

    for i in range(len(x)):

        previous_stiffness = (
            current_stiffness
        )

        (
            selected_stiffness,
            predicted_risk,
            unconstrained_stiffness,
            candidate_results,
        ) = controller.select_stiffness(
            curvature=curvature[i],
            friction=friction,
            current_stiffness=(
                current_stiffness
            ),
            commanded_velocity=(
                commanded_velocity
            ),
            base_force=base_force,
        )

        local_result = (
            simulate_local_navigation(
                curvature=curvature[i],
                friction=friction,
                stiffness=(
                    selected_stiffness
                ),
                commanded_velocity=(
                    commanded_velocity
                ),
                base_force=base_force,
            )
        )

        buckling_risk = (
            calculate_buckling_risk(
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
                stiffness=(
                    selected_stiffness
                ),
            )
        )

        kickback_score = (
            calculate_kickback(
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
                resistance=(
                    local_result[
                        "resistance"
                    ]
                ),
            )
        )

        combined_risk = max(
            buckling_risk,
            kickback_score,
        )

        stiffness_change = (
            selected_stiffness
            - previous_stiffness
        )

        target_gap = abs(
            unconstrained_stiffness
            - selected_stiffness
        )

        rate_limit_active = (
            target_gap > 1e-9
        )

        results.append({
            "position":
                position[i],

            "x":
                x[i],

            "y":
                y[i],

            "curvature":
                curvature[i],

            "previous_stiffness":
                previous_stiffness,

            "unconstrained_stiffness":
                unconstrained_stiffness,

            "stiffness":
                selected_stiffness,

            "stiffness_change":
                stiffness_change,

            "target_gap":
                target_gap,

            "rate_limit_active":
                rate_limit_active,

            "resistance":
                local_result[
                    "resistance"
                ],

            "push_force":
                local_result[
                    "push_force"
                ],

            "velocity":
                local_result[
                    "velocity"
                ],

            "buckling_risk":
                buckling_risk,

            "kickback_score":
                kickback_score,

            "predicted_risk":
                predicted_risk,

            "combined_risk":
                combined_risk,

            "prediction_error":
                (
                    combined_risk
                    - predicted_risk
                ),
        })

        current_stiffness = (
            selected_stiffness
        )

    return pd.DataFrame(
        results
    )


def print_summary(results):

    print()
    print(
        "Rate-Limited AI Navigation Summary"
    )

    print(
        "=================================="
    )

    print(
        f"Minimum stiffness used: "
        f"{results['stiffness'].min():.2f}"
    )

    print(
        f"Maximum stiffness used: "
        f"{results['stiffness'].max():.2f}"
    )

    print(
        f"Maximum observed stiffness change: "
        f"{results['stiffness_change'].abs().max():.2f}"
    )

    print()

    active_count = (
        results[
            "rate_limit_active"
        ].sum()
    )

    active_percent = (
        100
        * active_count
        / len(results)
    )

    print(
        f"Steps where rate limit was active: "
        f"{active_count}"
    )

    print(
        f"Percent of navigation steps limited: "
        f"{active_percent:.1f}%"
    )

    print(
        f"Mean gap from unconstrained AI target: "
        f"{results['target_gap'].mean():.4f}"
    )

    print()

    print(
        f"Peak resistance: "
        f"{results['resistance'].max():.4f}"
    )

    print(
        f"Mean resistance: "
        f"{results['resistance'].mean():.4f}"
    )

    print(
        f"Peak push force: "
        f"{results['push_force'].max():.4f}"
    )

    print(
        f"Mean push force: "
        f"{results['push_force'].mean():.4f}"
    )

    print(
        f"Minimum velocity: "
        f"{results['velocity'].min():.4f}"
    )

    print(
        f"Mean velocity: "
        f"{results['velocity'].mean():.4f}"
    )

    print()

    print(
        f"Peak buckling risk: "
        f"{results['buckling_risk'].max():.4f}"
    )

    print(
        f"Mean buckling risk: "
        f"{results['buckling_risk'].mean():.4f}"
    )

    print(
        f"Peak kickback: "
        f"{results['kickback_score'].max():.4f}"
    )

    print(
        f"Mean kickback: "
        f"{results['kickback_score'].mean():.4f}"
    )

    print()

    print(
        f"Peak combined risk: "
        f"{results['combined_risk'].max():.4f}"
    )

    print(
        f"Mean combined risk: "
        f"{results['combined_risk'].mean():.4f}"
    )

    print(
        f"Mean absolute AI prediction error: "
        f"{results['prediction_error'].abs().mean():.4f}"
    )


def plot_results(results):

    fig, axes = plt.subplots(
        4,
        1,
        figsize=(11, 12),
        constrained_layout=True,
    )

    # Vessel curvature
    axes[0].plot(
        results["position"],
        results["curvature"],
    )

    axes[0].set_title(
        "Local Vessel Curvature"
    )

    axes[0].set_ylabel(
        "Curvature"
    )

    axes[0].grid(True)

    # Desired vs actual stiffness
    axes[1].plot(
        results["position"],
        results[
            "unconstrained_stiffness"
        ],
        label="Unconstrained AI Target",
        linestyle="--",
    )

    axes[1].plot(
        results["position"],
        results["stiffness"],
        label="Rate-Limited Command",
    )

    axes[1].set_title(
        "AI Target vs Rate-Limited Stiffness"
    )

    axes[1].set_ylabel(
        "Stiffness"
    )

    axes[1].set_ylim(
        0,
        1,
    )

    axes[1].legend()
    axes[1].grid(True)

    # Combined risk
    axes[2].plot(
        results["position"],
        results["combined_risk"],
    )

    axes[2].set_title(
        "Rate-Limited AI Combined Navigation Risk"
    )

    axes[2].set_ylabel(
        "Normalized Risk"
    )

    axes[2].set_ylim(
        0,
        1,
    )

    axes[2].grid(True)

    # Prediction quality
    axes[3].plot(
        results["position"],
        results["predicted_risk"],
        label="AI Predicted Risk",
    )

    axes[3].plot(
        results["position"],
        results["combined_risk"],
        label="Digital Twin Risk",
        linestyle="--",
    )

    axes[3].set_title(
        "AI Prediction During Rate-Limited Navigation"
    )

    axes[3].set_xlabel(
        "Distance Along Vessel"
    )

    axes[3].set_ylabel(
        "Normalized Risk"
    )

    axes[3].set_ylim(
        0,
        1,
    )

    axes[3].legend()
    axes[3].grid(True)

    plt.show()


def main():

    results = (
        run_rate_limited_ai_navigation()
    )

    print_summary(
        results
    )

    results.to_csv(
        "results/"
        "rate_limited_ai_navigation.csv",
        index=False,
    )

    plot_results(
        results
    )


if __name__ == "__main__":
    main()