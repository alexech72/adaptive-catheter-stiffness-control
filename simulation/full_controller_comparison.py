"""
Full Controller Comparison
--------------------------

Compares:

- Fixed Flexible
- Fixed Medium
- Fixed Stiff
- Adaptive V1
- Balanced Adaptive V2

All strategies use identical vessel and simulation conditions.
"""

import pandas as pd
import matplotlib.pyplot as plt

from simulation.navigation_simulator import (
    run_navigation_simulation,
)

from simulation.adaptive_navigation_simulator import (
    run_adaptive_navigation,
)

from simulation.balanced_adaptive_navigation_simulator import (
    run_balanced_adaptive_navigation,
)


def run_all_controllers():

    results = {}

    results["Fixed Flexible"] = run_navigation_simulation(
        stiffness=0.25,
        friction=0.20,
    )

    results["Fixed Medium"] = run_navigation_simulation(
        stiffness=0.50,
        friction=0.20,
    )

    results["Fixed Stiff"] = run_navigation_simulation(
        stiffness=0.75,
        friction=0.20,
    )

    results["Adaptive V1"] = run_adaptive_navigation(
        initial_stiffness=0.50,
        friction=0.20,
    )

    results["Balanced V2"] = run_balanced_adaptive_navigation(
        initial_stiffness=0.50,
        friction=0.20,
    )

    return results


def create_summary(results):

    summary = []

    for name, data in results.items():

        summary.append({
            "configuration": name,

            "peak_resistance":
                data["resistance"].max(),

            "mean_resistance":
                data["resistance"].mean(),

            "peak_push_force":
                data["push_force"].max(),

            "mean_push_force":
                data["push_force"].mean(),

            "minimum_velocity":
                data["velocity"].min(),

            "mean_velocity":
                data["velocity"].mean(),

            "peak_buckling_risk":
                data["buckling_risk"].max(),

            "mean_buckling_risk":
                data["buckling_risk"].mean(),

            "peak_kickback":
                data["kickback_score"].max(),

            "mean_kickback":
                data["kickback_score"].mean(),
        })

    return pd.DataFrame(summary)


def print_summary(summary):

    print()
    print("Full Controller Comparison")
    print("--------------------------")

    print(
        summary.to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}"
        )
    )


def plot_controller_comparison(results):

    fig, axes = plt.subplots(
        4,
        1,
        figsize=(11, 13),
        constrained_layout=True,
    )

    # Resistance
    for name, data in results.items():
        axes[0].plot(
            data["position"],
            data["resistance"],
            label=name,
        )

    axes[0].set_title(
        "Navigation Resistance"
    )

    axes[0].set_ylabel(
        "Resistance Score"
    )

    axes[0].legend()
    axes[0].grid(True)

    # Push force
    for name, data in results.items():
        axes[1].plot(
            data["position"],
            data["push_force"],
            label=name,
        )

    axes[1].set_title(
        "Proximal Push Force"
    )

    axes[1].set_ylabel(
        "Push Force"
    )

    axes[1].legend()
    axes[1].grid(True)

    # Buckling risk
    for name, data in results.items():
        axes[2].plot(
            data["position"],
            data["buckling_risk"],
            label=name,
        )

    axes[2].set_title(
        "Simulated Buckling Risk"
    )

    axes[2].set_ylabel(
        "Normalized Risk"
    )

    axes[2].set_ylim(0, 1)
    axes[2].legend()
    axes[2].grid(True)

    # Kickback
    for name, data in results.items():
        axes[3].plot(
            data["position"],
            data["kickback_score"],
            label=name,
        )

    axes[3].set_title(
        "Simulated Guidewire Kickback"
    )

    axes[3].set_xlabel(
        "Distance Along Vessel"
    )

    axes[3].set_ylabel(
        "Normalized Score"
    )

    axes[3].set_ylim(0, 1)
    axes[3].legend()
    axes[3].grid(True)

    plt.show()


def main():

    results = run_all_controllers()

    summary = create_summary(
        results
    )

    print_summary(
        summary
    )

    summary.to_csv(
        "results/full_controller_comparison.csv",
        index=False,
    )

    plot_controller_comparison(
        results
    )


if __name__ == "__main__":
    main()