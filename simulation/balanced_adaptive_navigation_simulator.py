"""
Balanced Adaptive Navigation Simulator - V2
-------------------------------------------

Runs the catheter through the tortuous vessel while dynamically
adjusting stiffness using the balanced V2 controller.

V2 attempts to balance:

- trackability
- pushability
- buckling susceptibility
- guidewire kickback

The V1 simulator remains unchanged so both controllers can later
be compared under identical conditions.
"""

import pandas as pd
import matplotlib.pyplot as plt

from simulation.vessel_geometry import (
    generate_tortuous_vessel,
    calculate_curvature,
)

from simulation.catheter_model import (
    simulate_local_navigation,
)

from simulation.navigation_simulator import (
    calculate_arc_length,
)

from simulation.failure_model import (
    calculate_buckling_risk,
    calculate_kickback,
)

from controllers.balanced_controller import (
    select_balanced_stiffness,
)


def run_balanced_adaptive_navigation(
    initial_stiffness=0.50,
    friction=0.20,
    commanded_velocity=4.0,
    base_force=0.1,
):
    """
    Run the V2 balanced adaptive controller through
    the tortuous vessel.
    """

    # Generate vessel geometry
    x, y = generate_tortuous_vessel()

    # Calculate curvature
    curvature = calculate_curvature(
        x,
        y,
    )

    # Calculate distance along vessel
    position = calculate_arc_length(
        x,
        y,
    )

    results = []

    current_stiffness = initial_stiffness

    for i in range(len(x)):

        # Simulate current catheter behavior
        local_result = simulate_local_navigation(
            curvature=curvature[i],
            friction=friction,
            stiffness=current_stiffness,
            commanded_velocity=commanded_velocity,
            base_force=base_force,
        )

        # Calculate failure-related metrics
        buckling_risk = calculate_buckling_risk(
            push_force=local_result["push_force"],
            velocity=local_result["velocity"],
            stiffness=current_stiffness,
        )

        kickback_score = calculate_kickback(
            push_force=local_result["push_force"],
            velocity=local_result["velocity"],
            resistance=local_result["resistance"],
        )

        # V2 controller chooses stiffness for next step
        next_stiffness, action, reason = (
            select_balanced_stiffness(
                curvature=curvature[i],
                push_force=local_result["push_force"],
                velocity=local_result["velocity"],
                current_stiffness=current_stiffness,
            )
        )

        # Record current state
        results.append({
            "position": position[i],
            "x": x[i],
            "y": y[i],
            "curvature": curvature[i],
            "friction": friction,
            "stiffness": current_stiffness,
            "next_stiffness": next_stiffness,
            "resistance": local_result["resistance"],
            "velocity": local_result["velocity"],
            "push_force": local_result["push_force"],
            "buckling_risk": buckling_risk,
            "kickback_score": kickback_score,
            "controller_action": action,
            "controller_reason": reason,
        })

        # Apply command for next position
        current_stiffness = next_stiffness

    return pd.DataFrame(results)


def print_summary(results):
    """
    Print V2 navigation metrics.
    """

    changes = (
        results["controller_action"] != "HOLD"
    ).sum()

    print()
    print("Balanced Adaptive Navigation - V2")
    print("---------------------------------")

    print(
        f"Minimum stiffness used: "
        f"{results['stiffness'].min():.2f}"
    )

    print(
        f"Maximum stiffness used: "
        f"{results['stiffness'].max():.2f}"
    )

    print(
        f"Peak resistance: "
        f"{results['resistance'].max():.4f}"
    )

    print(
        f"Mean resistance: "
        f"{results['resistance'].mean():.4f}"
    )

    print(
        f"Peak pushing force: "
        f"{results['push_force'].max():.4f}"
    )

    print(
        f"Minimum velocity: "
        f"{results['velocity'].min():.4f}"
    )

    print(
        f"Peak buckling risk: "
        f"{results['buckling_risk'].max():.4f}"
    )

    print(
        f"Mean buckling risk: "
        f"{results['buckling_risk'].mean():.4f}"
    )

    print(
        f"Peak kickback score: "
        f"{results['kickback_score'].max():.4f}"
    )

    print(
        f"Mean kickback score: "
        f"{results['kickback_score'].mean():.4f}"
    )

    print(
        f"Total stiffness changes: "
        f"{changes}"
    )


def plot_balanced_navigation(results):
    """
    Plot V2 controller behavior.
    """

    fig, axes = plt.subplots(
        4,
        1,
        figsize=(11, 12),
        constrained_layout=True,
    )

    # Vessel
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

    axes[0].axis("equal")
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

    # V2 stiffness
    axes[2].plot(
        results["position"],
        results["stiffness"],
    )

    axes[2].set_title(
        "Balanced Adaptive Catheter Stiffness - V2"
    )

    axes[2].set_xlabel(
        "Distance Along Vessel"
    )

    axes[2].set_ylabel(
        "Stiffness"
    )

    axes[2].set_ylim(
        0,
        1
    )

    axes[2].grid(True)

    # Failure metrics
    axes[3].plot(
        results["position"],
        results["buckling_risk"],
        label="Buckling Risk",
    )

    axes[3].plot(
        results["position"],
        results["kickback_score"],
        label="Kickback",
    )

    axes[3].set_title(
        "V2 Failure-Related Metrics"
    )

    axes[3].set_xlabel(
        "Distance Along Vessel"
    )

    axes[3].set_ylabel(
        "Normalized Score"
    )

    axes[3].set_ylim(
        0,
        1
    )

    axes[3].legend()
    axes[3].grid(True)

    plt.show()


def main():

    results = run_balanced_adaptive_navigation(
        initial_stiffness=0.50,
        friction=0.20,
    )

    print_summary(
        results
    )

    results.to_csv(
        "results/balanced_adaptive_v2_tortuous.csv",
        index=False,
    )

    plot_balanced_navigation(
        results
    )


if __name__ == "__main__":
    main()