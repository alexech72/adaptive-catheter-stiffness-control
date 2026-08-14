"""
AI Stiffness Rate-Limit Sensitivity Study
-----------------------------------------

Evaluates how the maximum allowable stiffness change per
simulation step affects AI-assisted catheter navigation.

The purpose is to quantify the tradeoff between:

- smoother / slower stiffness commands
- navigation mechanics
- simulated navigation risk

The stiffness-change limits are computational control constraints.
They are not calibrated to a physical actuator or time constant.
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from simulation.rate_limited_ai_navigation_simulator import (
    run_rate_limited_ai_navigation,
)


RESULTS_DIRECTORY = Path("results/final")


RATE_LIMITS = [
    0.05,
    0.10,
    0.15,
    0.20,
    0.80,
]


def analyze_rate_limit(
    rate_limit,
):
    """
    Run one complete vessel simulation for a
    specified stiffness-change limit.
    """

    print(
        f"Running rate limit = "
        f"{rate_limit:.2f}..."
    )

    results = (
        run_rate_limited_ai_navigation(
            maximum_stiffness_change=(
                rate_limit
            )
        )
    )

    active_steps = (
        results[
            "rate_limit_active"
        ].sum()
    )

    percent_limited = (
        100
        * active_steps
        / len(results)
    )

    mean_absolute_change = (
        results[
            "stiffness_change"
        ]
        .abs()
        .mean()
    )

    total_stiffness_variation = (
        results[
            "stiffness_change"
        ]
        .abs()
        .sum()
    )

    return {
        "rate_limit":
            rate_limit,

        "peak_resistance":
            results[
                "resistance"
            ].max(),

        "mean_resistance":
            results[
                "resistance"
            ].mean(),

        "peak_push_force":
            results[
                "push_force"
            ].max(),

        "mean_push_force":
            results[
                "push_force"
            ].mean(),

        "minimum_velocity":
            results[
                "velocity"
            ].min(),

        "mean_velocity":
            results[
                "velocity"
            ].mean(),

        "peak_buckling_risk":
            results[
                "buckling_risk"
            ].max(),

        "mean_buckling_risk":
            results[
                "buckling_risk"
            ].mean(),

        "peak_kickback":
            results[
                "kickback_score"
            ].max(),

        "mean_kickback":
            results[
                "kickback_score"
            ].mean(),

        "peak_combined_risk":
            results[
                "combined_risk"
            ].max(),

        "mean_combined_risk":
            results[
                "combined_risk"
            ].mean(),

        "mean_stiffness_change":
            mean_absolute_change,

        "total_stiffness_variation":
            total_stiffness_variation,

        "percent_steps_limited":
            percent_limited,

        "mean_target_gap":
            results[
                "target_gap"
            ].mean(),
    }


def run_sensitivity_study():
    """
    Run all requested stiffness-change limits.
    """

    rows = []

    print()
    print(
        "AI Rate-Limit Sensitivity Study"
    )

    print(
        "==============================="
    )

    for rate_limit in RATE_LIMITS:

        row = analyze_rate_limit(
            rate_limit
        )

        rows.append(
            row
        )

    summary = pd.DataFrame(
        rows
    )

    return summary


def print_summary(
    summary
):

    print()
    print(
        "RATE-LIMIT SENSITIVITY RESULTS"
    )

    print(
        "=============================="
    )

    selected_columns = [
        "rate_limit",
        "mean_combined_risk",
        "peak_combined_risk",
        "mean_resistance",
        "minimum_velocity",
        "mean_stiffness_change",
        "percent_steps_limited",
    ]

    print(
        summary[
            selected_columns
        ].to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}",
        )
    )


def save_summary(
    summary
):

    RESULTS_DIRECTORY.mkdir(
        exist_ok=True
    )

    summary.to_csv(
        RESULTS_DIRECTORY
        / "rate_limit_sensitivity.csv",
        index=False,
    )


def plot_summary(
    summary
):

    fig, axes = plt.subplots(
        3,
        1,
        figsize=(10, 11),
        constrained_layout=True,
    )

    # -----------------------------------------
    # Risk
    # -----------------------------------------

    axes[0].plot(
        summary["rate_limit"],
        summary[
            "mean_combined_risk"
        ],
        marker="o",
        label="Mean Combined Risk",
    )

    axes[0].plot(
        summary["rate_limit"],
        summary[
            "peak_combined_risk"
        ],
        marker="o",
        label="Peak Combined Risk",
    )

    axes[0].set_title(
        "Navigation Risk vs Stiffness Rate Limit"
    )

    axes[0].set_xlabel(
        "Maximum Stiffness Change per Step"
    )

    axes[0].set_ylabel(
        "Normalized Risk"
    )

    axes[0].legend()
    axes[0].grid(True)

    # -----------------------------------------
    # Mechanical performance
    # -----------------------------------------

    axes[1].plot(
        summary["rate_limit"],
        summary[
            "mean_resistance"
        ],
        marker="o",
        label="Mean Resistance",
    )

    axes[1].plot(
        summary["rate_limit"],
        summary[
            "minimum_velocity"
        ],
        marker="o",
        label="Minimum Velocity",
    )

    axes[1].set_title(
        "Mechanical Performance vs Rate Limit"
    )

    axes[1].set_xlabel(
        "Maximum Stiffness Change per Step"
    )

    axes[1].legend()
    axes[1].grid(True)

    # -----------------------------------------
    # Control activity
    # -----------------------------------------

    axes[2].plot(
        summary["rate_limit"],
        summary[
            "mean_stiffness_change"
        ],
        marker="o",
        label="Mean Stiffness Change",
    )

    axes[2].set_title(
        "Controller Activity vs Rate Limit"
    )

    axes[2].set_xlabel(
        "Maximum Stiffness Change per Step"
    )

    axes[2].set_ylabel(
        "Mean Absolute Stiffness Change"
    )

    axes[2].legend()
    axes[2].grid(True)

    plt.show()


def main():

    summary = (
        run_sensitivity_study()
    )

    print_summary(
        summary
    )

    save_summary(
        summary
    )

    plot_summary(
        summary
    )


if __name__ == "__main__":
    main()