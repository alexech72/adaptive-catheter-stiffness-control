"""
AI-Assisted Adaptive Navigation Simulator
------------------------------------------

Runs the frozen Random Forest risk estimator inside a
model-based adaptive catheter stiffness controller.

At each vessel location:

1. Evaluate candidate catheter stiffness values.
2. Predict the resulting mechanical response.
3. Use the Random Forest to estimate navigation risk.
4. Select the stiffness with the lowest predicted risk.
5. Simulate the actual digital-twin response.
6. Record predicted and simulated risk.

This is a computational R&D model and is not clinically validated.
"""

import pandas as pd
import matplotlib.pyplot as plt

from controllers.ai_assisted_controller import (
    AIAssistedController,
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


def run_ai_adaptive_navigation(
    initial_stiffness=0.50,
    friction=0.20,
    commanded_velocity=4.0,
    base_force=0.10,
):
    """
    Run AI-assisted adaptive navigation through
    the complete tortuous vessel.
    """

    controller = AIAssistedController()

    # Generate vessel geometry
    x, y = generate_tortuous_vessel()

    curvature = calculate_curvature(
        x,
        y,
    )

    position = calculate_arc_length(
        x,
        y,
    )

    current_stiffness = initial_stiffness

    results = []

    for i in range(len(x)):

        # -------------------------------------------------
        # AI evaluates candidate stiffness values.
        # -------------------------------------------------

        (
            selected_stiffness,
            predicted_risk,
            candidate_results,
        ) = controller.select_stiffness(
            curvature=curvature[i],
            friction=friction,
            current_stiffness=current_stiffness,
            commanded_velocity=commanded_velocity,
            base_force=base_force,
        )

        # -------------------------------------------------
        # Apply selected stiffness to digital twin.
        # -------------------------------------------------

        local_result = simulate_local_navigation(
            curvature=curvature[i],
            friction=friction,
            stiffness=selected_stiffness,
            commanded_velocity=commanded_velocity,
            base_force=base_force,
        )

        # -------------------------------------------------
        # Calculate simulated failure-related metrics.
        # -------------------------------------------------

        buckling_risk = calculate_buckling_risk(
            push_force=local_result["push_force"],
            velocity=local_result["velocity"],
            stiffness=selected_stiffness,
        )

        kickback_score = calculate_kickback(
            push_force=local_result["push_force"],
            velocity=local_result["velocity"],
            resistance=local_result["resistance"],
        )

        simulated_combined_risk = max(
            buckling_risk,
            kickback_score,
        )

        prediction_error = (
            simulated_combined_risk
            - predicted_risk
        )

        # -------------------------------------------------
        # Record navigation state.
        # -------------------------------------------------

        results.append({
            "position": position[i],
            "x": x[i],
            "y": y[i],
            "curvature": curvature[i],

            "stiffness":
                selected_stiffness,

            "resistance":
                local_result["resistance"],

            "push_force":
                local_result["push_force"],

            "velocity":
                local_result["velocity"],

            "buckling_risk":
                buckling_risk,

            "kickback_score":
                kickback_score,

            "predicted_risk":
                predicted_risk,

            "simulated_combined_risk":
                simulated_combined_risk,

            "prediction_error":
                prediction_error,
        })

        current_stiffness = (
            selected_stiffness
        )

    return pd.DataFrame(
        results
    )


def print_summary(results):

    print()
    print("AI-Assisted Navigation Summary")
    print("==============================")

    print(
        f"Minimum stiffness used: "
        f"{results['stiffness'].min():.2f}"
    )

    print(
        f"Maximum stiffness used: "
        f"{results['stiffness'].max():.2f}"
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
        f"Peak simulated combined risk: "
        f"{results['simulated_combined_risk'].max():.4f}"
    )

    print(
        f"Mean simulated combined risk: "
        f"{results['simulated_combined_risk'].mean():.4f}"
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

    # Vessel geometry
    axes[0].plot(
        results["x"],
        results["y"],
    )

    axes[0].set_title(
        "Tortuous Vessel Geometry"
    )

    axes[0].set_xlabel(
        "Longitudinal Position"
    )

    axes[0].set_ylabel(
        "Lateral Position"
    )

    axes[0].grid(True)

    # Curvature
    axes[1].plot(
        results["position"],
        results["curvature"],
    )

    axes[1].set_title(
        "Local Vessel Curvature"
    )

    axes[1].set_xlabel(
        "Distance Along Vessel"
    )

    axes[1].set_ylabel(
        "Curvature"
    )

    axes[1].grid(True)

    # AI-selected stiffness
    axes[2].plot(
        results["position"],
        results["stiffness"],
    )

    axes[2].set_title(
        "AI-Selected Adaptive Catheter Stiffness"
    )

    axes[2].set_xlabel(
        "Distance Along Vessel"
    )

    axes[2].set_ylabel(
        "Stiffness"
    )

    axes[2].set_ylim(
        0,
        1,
    )

    axes[2].grid(True)

    # Predicted vs actual simulated risk
    axes[3].plot(
        results["position"],
        results["predicted_risk"],
        label="AI Predicted Risk",
    )

    axes[3].plot(
        results["position"],
        results["simulated_combined_risk"],
        label="Digital Twin Risk",
        linestyle="--",
    )

    axes[3].set_title(
        "AI Predicted vs Simulated Navigation Risk"
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

    results = run_ai_adaptive_navigation()

    print_summary(
        results
    )

    results.to_csv(
        "results/ai_adaptive_navigation.csv",
        index=False,
    )

    plot_results(
        results
    )


if __name__ == "__main__":
    main()