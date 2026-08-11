"""
Navigation Simulator
--------------------

Connects the vessel geometry model with the catheter mechanics model.

The simulator moves through a vessel centerline point-by-point and
calculates:

- local vessel curvature
- navigation resistance
- catheter advancement velocity
- proximal pushing force

V1 uses a fixed catheter stiffness so that baseline behavior can be
established before adaptive control is introduced.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from simulation.vessel_geometry import (
    generate_tortuous_vessel,
    calculate_curvature,
)

from simulation.catheter_model import simulate_local_navigation


def calculate_arc_length(x, y):
    """
    Calculate cumulative distance along the vessel centerline.
    """

    dx = np.diff(x)
    dy = np.diff(y)

    segment_lengths = np.sqrt(dx**2 + dy**2)

    arc_length = np.concatenate(
        ([0], np.cumsum(segment_lengths))
    )

    return arc_length


def run_navigation_simulation(
    stiffness=0.50,
    friction=0.20,
    commanded_velocity=4.0,
    base_force=0.1,
):
    """
    Run a fixed-stiffness catheter through a tortuous vessel.
    """

    # Generate vascular pathway
    x, y = generate_tortuous_vessel()

    # Calculate curvature along vessel
    curvature = calculate_curvature(x, y)

    # Calculate true distance traveled along vessel
    position = calculate_arc_length(x, y)

    results = []

    # Evaluate catheter behavior at every vessel point
    for i in range(len(x)):

        local_result = simulate_local_navigation(
            curvature=curvature[i],
            friction=friction,
            stiffness=stiffness,
            commanded_velocity=commanded_velocity,
            base_force=base_force,
        )

        results.append({
            "position": position[i],
            "x": x[i],
            "y": y[i],
            "curvature": curvature[i],
            "stiffness": stiffness,
            "friction": friction,
            "resistance": local_result["resistance"],
            "velocity": local_result["velocity"],
            "push_force": local_result["push_force"],
        })

    return pd.DataFrame(results)


def print_summary(results):
    """
    Print important engineering metrics from the simulation.
    """

    print()
    print("Navigation Simulation Summary")
    print("-----------------------------")

    print(
        f"Navigation distance: "
        f"{results['position'].iloc[-1]:.2f}"
    )

    print(
        f"Maximum curvature: "
        f"{results['curvature'].max():.4f}"
    )

    print(
        f"Maximum resistance: "
        f"{results['resistance'].max():.4f}"
    )

    print(
        f"Peak pushing force: "
        f"{results['push_force'].max():.4f}"
    )

    print(
        f"Mean pushing force: "
        f"{results['push_force'].mean():.4f}"
    )

    print(
        f"Minimum advancement velocity: "
        f"{results['velocity'].min():.4f}"
    )


def plot_simulation(results):
    """
    Display vessel geometry and catheter navigation behavior.
    """

    fig, axes = plt.subplots(
        4,
        1,
        figsize=(10, 12)
    )

    # Vessel geometry
    axes[0].plot(
        results["x"],
        results["y"],
        linewidth=2
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
        results["curvature"]
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

    # Resistance
    axes[2].plot(
        results["position"],
        results["resistance"]
    )

    axes[2].set_title(
        "Navigation Resistance"
    )

    axes[2].set_xlabel(
        "Distance Along Vessel"
    )

    axes[2].set_ylabel(
        "Resistance Score"
    )

    axes[2].grid(True)

    # Force and velocity
    force_axis = axes[3]

    velocity_axis = force_axis.twinx()

    force_axis.plot(
        results["position"],
        results["push_force"],
        label="Push Force"
    )

    velocity_axis.plot(
        results["position"],
        results["velocity"],
        linestyle="--",
        label="Velocity"
    )

    force_axis.set_title(
        "Push Force and Advancement Velocity"
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

    fig.tight_layout(h_pad=2.5)

    plt.show()


def main():

    # Baseline fixed-medium-stiffness catheter
    results = run_navigation_simulation(
        stiffness=0.50,
        friction=0.20,
    )

    print_summary(results)

    # Save simulation results
    results.to_csv(
        "results/fixed_medium_tortuous.csv",
        index=False
    )

    plot_simulation(results)


if __name__ == "__main__":
    main()