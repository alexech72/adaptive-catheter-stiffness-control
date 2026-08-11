"""
Rule-Based Adaptive Navigation Simulator
----------------------------------------

Runs a catheter through the tortuous vessel while dynamically adjusting
catheter stiffness using measurable navigation feedback.

At each vessel location:

1. The catheter experiences the current geometry.
2. Force and advancement velocity are calculated.
3. The rule-based controller receives:
       - local curvature
       - proximal pushing force
       - advancement velocity
       - current stiffness
4. The controller selects the stiffness for the next navigation step.

This represents the first closed-loop adaptive simulation.
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

from controllers.rule_based_controller import (
    select_stiffness,
)


def run_adaptive_navigation(
    initial_stiffness=0.50,
    friction=0.20,
    commanded_velocity=4.0,
    base_force=0.1,
):
    """
    Run a rule-based adaptive catheter through a tortuous vessel.
    """

    # Generate vessel
    x, y = generate_tortuous_vessel()

    # Calculate local vessel curvature
    curvature = calculate_curvature(
        x,
        y
    )

    # Calculate distance along vessel
    position = calculate_arc_length(
        x,
        y
    )

    results = []

    current_stiffness = initial_stiffness

    for i in range(len(x)):

        # ---------------------------------------------
        # 1. Simulate catheter behavior using the
        #    current stiffness.
        # ---------------------------------------------

        local_result = simulate_local_navigation(
            curvature=curvature[i],
            friction=friction,
            stiffness=current_stiffness,
            commanded_velocity=commanded_velocity,
            base_force=base_force,
        )

        # ---------------------------------------------
        # 2. Send the simulated measurements to
        #    the adaptive controller.
        # ---------------------------------------------

        next_stiffness, action, reason = select_stiffness(
            curvature=curvature[i],
            push_force=local_result["push_force"],
            velocity=local_result["velocity"],
            current_stiffness=current_stiffness,
        )

        # ---------------------------------------------
        # 3. Record the current navigation state.
        # ---------------------------------------------

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
            "controller_action": action,
            "controller_reason": reason,
        })

        # ---------------------------------------------
        # 4. Apply the controller command for the
        #    next vessel location.
        # ---------------------------------------------

        current_stiffness = next_stiffness

    return pd.DataFrame(results)


def print_summary(results):
    """
    Print summary metrics from the adaptive navigation trial.
    """

    stiffness_changes = (
        results["controller_action"] != "HOLD"
    ).sum()

    decreases = (
        results["controller_action"] == "DECREASE"
    ).sum()

    increases = (
        results["controller_action"] == "INCREASE"
    ).sum()

    print()
    print("Rule-Based Adaptive Navigation")
    print("------------------------------")

    print(
        f"Starting stiffness: "
        f"{results['stiffness'].iloc[0]:.2f}"
    )

    print(
        f"Final stiffness: "
        f"{results['next_stiffness'].iloc[-1]:.2f}"
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
        f"Peak resistance: "
        f"{results['resistance'].max():.4f}"
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
        f"Total stiffness changes: "
        f"{stiffness_changes}"
    )

    print(
        f"Stiffness increases: "
        f"{increases}"
    )

    print(
        f"Stiffness decreases: "
        f"{decreases}"
    )


def plot_adaptive_navigation(results):
    """
    Plot geometry, curvature, stiffness, and mechanical response.
    """

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
        linewidth=2,
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

    # Vessel curvature
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

    # Adaptive stiffness
    axes[2].plot(
        results["position"],
        results["stiffness"],
    )

    axes[2].set_title(
        "Rule-Based Adaptive Catheter Stiffness"
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

    # Push force and velocity
    force_axis = axes[3]

    velocity_axis = force_axis.twinx()

    force_axis.plot(
        results["position"],
        results["push_force"],
        label="Push Force",
    )

    velocity_axis.plot(
        results["position"],
        results["velocity"],
        linestyle="--",
        label="Velocity",
    )

    force_axis.set_title(
        "Mechanical Response During Adaptive Navigation"
    )

    force_axis.set_xlabel(
        "Distance Along Vessel"
    )

    force_axis.set_ylabel(
        "Push Force"
    )

    velocity_axis.set_ylabel(
        "Velocity"
    )

    force_axis.grid(True)

    plt.show()


def main():

    results = run_adaptive_navigation(
        initial_stiffness=0.50,
        friction=0.20,
    )

    print_summary(
        results
    )

    results.to_csv(
        "results/rule_based_adaptive_tortuous.csv",
        index=False,
    )

    plot_adaptive_navigation(
        results
    )


if __name__ == "__main__":
    main()