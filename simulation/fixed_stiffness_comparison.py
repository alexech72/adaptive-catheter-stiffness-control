"""
Fixed-Stiffness Comparison
--------------------------

Compares three fixed catheter stiffness configurations through the
same tortuous vessel:

- Flexible: stiffness = 0.25
- Medium:   stiffness = 0.50
- Stiff:    stiffness = 0.75

All other simulation conditions are held constant.

The goal is to determine whether one fixed stiffness performs best
throughout the entire vessel or whether performance depends on local
vessel geometry.
"""

import pandas as pd
import matplotlib.pyplot as plt

from simulation.navigation_simulator import run_navigation_simulation


def run_fixed_stiffness_comparison():
    """
    Run the same navigation experiment at three fixed stiffness levels.
    """

    stiffness_cases = {
        "Flexible": 0.25,
        "Medium": 0.50,
        "Stiff": 0.75,
    }

    results = {}

    for name, stiffness in stiffness_cases.items():

        results[name] = run_navigation_simulation(
            stiffness=stiffness,
            friction=0.20,
            commanded_velocity=4.0,
            base_force=0.1,
        )

    return results


def create_summary_table(results):
    """
    Calculate summary metrics for each stiffness configuration.
    """

    summary = []

    for name, data in results.items():

        summary.append({
            "configuration": name,
            "stiffness": data["stiffness"].iloc[0],
            "peak_resistance": data["resistance"].max(),
            "mean_resistance": data["resistance"].mean(),
            "peak_push_force": data["push_force"].max(),
            "mean_push_force": data["push_force"].mean(),
            "minimum_velocity": data["velocity"].min(),
            "mean_velocity": data["velocity"].mean(),
        })

    return pd.DataFrame(summary)


def print_summary(summary):
    """
    Print engineering comparison table.
    """

    print()
    print("Fixed-Stiffness Comparison")
    print("--------------------------")

    print(
        summary.to_string(
            index=False,
            float_format=lambda value: f"{value:.4f}"
        )
    )


def plot_comparison(results):
    """
    Plot resistance, push force, and velocity for all stiffness cases.
    """

    fig, axes = plt.subplots(
        3,
        1,
        figsize=(11, 10)
    )

    # Navigation resistance
    for name, data in results.items():

        axes[0].plot(
            data["position"],
            data["resistance"],
            label=name
        )

    axes[0].set_title(
        "Navigation Resistance by Fixed Catheter Stiffness"
    )

    axes[0].set_xlabel(
        "Distance Along Vessel"
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
            label=name
        )

    axes[1].set_title(
        "Proximal Push Force by Fixed Catheter Stiffness"
    )

    axes[1].set_xlabel(
        "Distance Along Vessel"
    )

    axes[1].set_ylabel(
        "Push Force"
    )

    axes[1].legend()
    axes[1].grid(True)

    # Advancement velocity
    for name, data in results.items():

        axes[2].plot(
            data["position"],
            data["velocity"],
            label=name
        )

    axes[2].set_title(
        "Advancement Velocity by Fixed Catheter Stiffness"
    )

    axes[2].set_xlabel(
        "Distance Along Vessel"
    )

    axes[2].set_ylabel(
        "Velocity"
    )

    axes[2].legend()
    axes[2].grid(True)

    fig.tight_layout(h_pad=2.5)

    plt.show()


def main():

    results = run_fixed_stiffness_comparison()

    summary = create_summary_table(results)

    print_summary(summary)

    # Save summary results
    summary.to_csv(
        "results/fixed_stiffness_summary.csv",
        index=False
    )

    # Save full point-by-point results
    for name, data in results.items():

        filename = (
            f"results/fixed_{name.lower()}_tortuous.csv"
        )

        data.to_csv(
            filename,
            index=False
        )

    plot_comparison(results)


if __name__ == "__main__":
    main()