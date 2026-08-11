"""
Optimal Stiffness Mapping
-------------------------

Determines the stiffness that minimizes navigation resistance at each
position along a tortuous vessel.

This represents an idealized reference solution. The future controller
will not have direct access to this optimal answer.

Instead, adaptive controllers will attempt to select appropriate stiffness
using simulated sensor feedback.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from simulation.vessel_geometry import (
    generate_tortuous_vessel,
    calculate_curvature,
)

from simulation.catheter_model import calculate_navigation_resistance

from simulation.navigation_simulator import calculate_arc_length


def find_optimal_stiffness(
    curvature,
    friction=0.20,
    stiffness_values=None,
):
    """
    Find the stiffness producing the lowest resistance
    for one local vessel condition.
    """

    if stiffness_values is None:
        stiffness_values = np.linspace(
            0.10,
            0.90,
            81
        )

    best_stiffness = None
    best_resistance = float("inf")

    for stiffness in stiffness_values:

        resistance = calculate_navigation_resistance(
            curvature=curvature,
            friction=friction,
            stiffness=stiffness,
        )

        if resistance < best_resistance:
            best_resistance = resistance
            best_stiffness = stiffness

    return best_stiffness, best_resistance


def generate_optimal_stiffness_map():
    """
    Determine optimal stiffness along the entire vessel.
    """

    x, y = generate_tortuous_vessel()

    curvature = calculate_curvature(
        x,
        y
    )

    position = calculate_arc_length(
        x,
        y
    )

    optimal_stiffness = []
    optimal_resistance = []

    for local_curvature in curvature:

        stiffness, resistance = find_optimal_stiffness(
            curvature=local_curvature,
            friction=0.20,
        )

        optimal_stiffness.append(
            stiffness
        )

        optimal_resistance.append(
            resistance
        )

    results = pd.DataFrame({
        "position": position,
        "x": x,
        "y": y,
        "curvature": curvature,
        "optimal_stiffness": optimal_stiffness,
        "optimal_resistance": optimal_resistance,
    })

    return results


def print_summary(results):
    """
    Print basic optimal-stiffness statistics.
    """

    print()
    print("Optimal Stiffness Mapping")
    print("-------------------------")

    print(
        f"Minimum selected stiffness: "
        f"{results['optimal_stiffness'].min():.2f}"
    )

    print(
        f"Maximum selected stiffness: "
        f"{results['optimal_stiffness'].max():.2f}"
    )

    print(
        f"Mean selected stiffness: "
        f"{results['optimal_stiffness'].mean():.2f}"
    )


def plot_optimal_stiffness(results):
    """
    Visualize vessel curvature and ideal stiffness.
    """

    fig, axes = plt.subplots(
        3,
        1,
        figsize=(11, 10)
    )

    # Vessel
    axes[0].plot(
        results["x"],
        results["y"]
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

    # Optimal stiffness
    axes[2].plot(
        results["position"],
        results["optimal_stiffness"]
    )

    axes[2].set_title(
        "Resistance-Minimizing Catheter Stiffness"
    )

    axes[2].set_xlabel(
        "Distance Along Vessel"
    )

    axes[2].set_ylabel(
        "Optimal Stiffness"
    )

    axes[2].set_ylim(
        0,
        1
    )

    axes[2].grid(True)

    fig.tight_layout(
        h_pad=2.5
    )

    plt.show()


def main():

    results = generate_optimal_stiffness_map()

    print_summary(results)

    results.to_csv(
        "results/optimal_stiffness_map.csv",
        index=False
    )

    plot_optimal_stiffness(
        results
    )


if __name__ == "__main__":
    main()