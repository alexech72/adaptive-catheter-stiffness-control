"""
Controller Comparison
---------------------

Compares fixed-stiffness catheter configurations with the rule-based
adaptive-stiffness controller under identical vessel and simulation
conditions.

Configurations:
- Fixed Flexible
- Fixed Medium
- Fixed Stiff
- Rule-Based Adaptive
"""

import pandas as pd
import matplotlib.pyplot as plt

from simulation.navigation_simulator import run_navigation_simulation
from simulation.adaptive_navigation_simulator import run_adaptive_navigation


def run_controller_comparison():
    """
    Run all catheter-control strategies under identical conditions.
    """

    results = {}

    # Fixed-stiffness baselines
    results["Fixed Flexible"] = run_navigation_simulation(
        stiffness=0.25,
        friction=0.20,
        commanded_velocity=4.0,
        base_force=0.1,
    )

    results["Fixed Medium"] = run_navigation_simulation(
        stiffness=0.50,
        friction=0.20,
        commanded_velocity=4.0,
        base_force=0.1,
    )

    results["Fixed Stiff"] = run_navigation_simulation(
        stiffness=0.75,
        friction=0.20,
        commanded_velocity=4.0,
        base_force=0.1,
    )

    # Rule-based adaptive system
    results["Rule Adaptive"] = run_adaptive_navigation(
        initial_stiffness=0.50,
        friction=0.20,
        commanded_velocity=4.0,
        base_force=0.1,
    )

    return results


def create_summary(results):
    """
    Generate comparison metrics for each controller.
    """

    summary = []

    for name, data in results.items():

        summary.append({
            "configuration": name,

            "peak_resistance": data["resistance"].max(),
            "mean_resistance": data["resistance"].mean(),

            "peak_push_force": data["push_force"].max(),
            "mean_push_force": data["push_force"].mean(),

            "minimum_velocity": data["velocity"].min(),
            "mean_velocity": data["velocity"].mean(),

            "peak_buckling_risk": data["buckling_risk"].max(),
            "mean_buckling_risk": data["buckling_risk"].mean(),

            "peak_kickback_score": data["kickback_score"].max(),
            "mean_kickback_score": data["kickback_score"].mean(),
        })
    

    return pd.DataFrame(summary)


def print_summary(summary):
    """
    Print the controller comparison table.
    """

    print()
    print("Controller Performance Comparison")
    print("---------------------------------")

    print(
        summary.to_string(
            index=False,
            float_format=lambda value: f"{value:.4f}"
        )
    )


def plot_comparison(results):
    """
    Plot resistance, push force, and velocity for each strategy.
    """

    fig, axes = plt.subplots(
        3,
        1,
        figsize=(11, 10),
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
        "Navigation Resistance: Fixed vs Adaptive"
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
            label=name,
        )

    axes[1].set_title(
        "Push Force: Fixed vs Adaptive"
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
            label=name,
        )

    axes[2].set_title(
        "Advancement Velocity: Fixed vs Adaptive"
    )

    axes[2].set_xlabel(
        "Distance Along Vessel"
    )

    axes[2].set_ylabel(
        "Velocity"
    )

    axes[2].legend()
    axes[2].grid(True)

    plt.show()

def plot_failure_comparison(results):
    """
    Compare simulated buckling risk and guidewire kickback
    across all catheter-control strategies.
    """

    fig, axes = plt.subplots(
        2,
        1,
        figsize=(11, 8),
        constrained_layout=True,
    )

    # Buckling risk
    for name, data in results.items():
        axes[0].plot(
            data["position"],
            data["buckling_risk"],
            label=name,
        )

    axes[0].set_title(
        "Simulated Buckling Risk: Fixed vs Adaptive"
    )

    axes[0].set_xlabel(
        "Distance Along Vessel"
    )

    axes[0].set_ylabel(
        "Normalized Risk Score"
    )

    axes[0].set_ylim(
        0,
        1
    )

    axes[0].legend()
    axes[0].grid(True)

    # Guidewire kickback
    for name, data in results.items():
        axes[1].plot(
            data["position"],
            data["kickback_score"],
            label=name,
        )

    axes[1].set_title(
        "Simulated Guidewire Kickback: Fixed vs Adaptive"
    )

    axes[1].set_xlabel(
        "Distance Along Vessel"
    )

    axes[1].set_ylabel(
        "Normalized Kickback Score"
    )

    axes[1].set_ylim(
        0,
        1
    )

    axes[1].legend()
    axes[1].grid(True)

    plt.show()

def main():

    results = run_controller_comparison()

    summary = create_summary(
        results
    )

    print_summary(
        summary
    )

    summary.to_csv(
        "results/controller_comparison_summary.csv",
        index=False,
    )

    plot_comparison(
        results
    )
    plot_failure_comparison(
        results
    )

if __name__ == "__main__":
    main()