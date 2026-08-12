"""
Final Controller Comparison
---------------------------

Compares six catheter stiffness strategies under identical
digital-twin navigation conditions:

1. Fixed Flexible
2. Fixed Medium
3. Fixed Stiff
4. Rule-Based Adaptive V1
5. Balanced Adaptive V2
6. AI-Assisted Adaptive

This is a computational R&D comparison using synthetic
digital-twin metrics. It is not clinically validated.
"""

from pathlib import Path

import numpy as np
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

from simulation.ai_adaptive_navigation_simulator import (
    run_ai_adaptive_navigation,
)


RESULTS_DIRECTORY = Path("results")


def add_combined_risk(data):
    """
    Ensure every controller result has the same combined-risk column.
    """

    result = data.copy()

    if "simulated_combined_risk" in result.columns:

        result["combined_risk"] = (
            result["simulated_combined_risk"]
        )

    else:

        result["combined_risk"] = np.maximum(
            result["buckling_risk"],
            result["kickback_score"],
        )

    return result


def run_all_strategies():
    """
    Run all six controller configurations.
    """

    print()
    print("Running Fixed Flexible...")

    fixed_flexible = run_navigation_simulation(
        stiffness=0.25,
        friction=0.20,
    )

    print("Running Fixed Medium...")

    fixed_medium = run_navigation_simulation(
        stiffness=0.50,
        friction=0.20,
    )

    print("Running Fixed Stiff...")

    fixed_stiff = run_navigation_simulation(
        stiffness=0.75,
        friction=0.20,
    )

    print("Running Adaptive V1...")

    adaptive_v1 = run_adaptive_navigation(
        initial_stiffness=0.50,
        friction=0.20,
    )

    print("Running Balanced V2...")

    balanced_v2 = (
        run_balanced_adaptive_navigation(
            initial_stiffness=0.50,
            friction=0.20,
        )
    )

    print("Running AI-Assisted...")

    ai_assisted = (
        run_ai_adaptive_navigation(
            initial_stiffness=0.50,
            friction=0.20,
        )
    )

    results = {
        "Fixed Flexible":
            add_combined_risk(
                fixed_flexible
            ),

        "Fixed Medium":
            add_combined_risk(
                fixed_medium
            ),

        "Fixed Stiff":
            add_combined_risk(
                fixed_stiff
            ),

        "Adaptive V1":
            add_combined_risk(
                adaptive_v1
            ),

        "Balanced V2":
            add_combined_risk(
                balanced_v2
            ),

        "AI-Assisted":
            add_combined_risk(
                ai_assisted
            ),
    }

    return results


def create_summary(results):
    """
    Calculate comparison metrics for every strategy.
    """

    rows = []

    for name, data in results.items():

        rows.append({
            "configuration":
                name,

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

            "peak_combined_risk":
                data["combined_risk"].max(),

            "mean_combined_risk":
                data["combined_risk"].mean(),
        })

    return pd.DataFrame(
        rows
    )


def print_summary(summary):

    print()
    print("FINAL CONTROLLER COMPARISON")
    print("===========================")

    print(
        summary.to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}",
        )
    )


def plot_comparison(results):

    fig, axes = plt.subplots(
        4,
        1,
        figsize=(12, 14),
        constrained_layout=True,
    )

    # -----------------------------------------
    # Resistance
    # -----------------------------------------

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

    # -----------------------------------------
    # Push force
    # -----------------------------------------

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

    # -----------------------------------------
    # Velocity
    # -----------------------------------------

    for name, data in results.items():

        axes[2].plot(
            data["position"],
            data["velocity"],
            label=name,
        )

    axes[2].set_title(
        "Catheter Advancement Velocity"
    )

    axes[2].set_ylabel(
        "Velocity"
    )

    axes[2].legend()
    axes[2].grid(True)

    # -----------------------------------------
    # Combined risk
    # -----------------------------------------

    for name, data in results.items():

        axes[3].plot(
            data["position"],
            data["combined_risk"],
            label=name,
        )

    axes[3].set_title(
        "Simulated Combined Navigation Risk"
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


def save_summary(summary):

    RESULTS_DIRECTORY.mkdir(
        exist_ok=True
    )

    summary.to_csv(
        RESULTS_DIRECTORY
        / "final_controller_comparison.csv",
        index=False,
    )


def main():

    results = run_all_strategies()

    summary = create_summary(
        results
    )

    print_summary(
        summary
    )

    save_summary(
        summary
    )

    plot_comparison(
        results
    )


if __name__ == "__main__":
    main()