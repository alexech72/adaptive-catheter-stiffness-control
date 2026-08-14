"""
Multi-Vessel Controller Robustness Study
----------------------------------------

Evaluates three catheter stiffness strategies across 30 previously
unused synthetic vessel geometries:

- 10 easy
- 10 moderate
- 10 severe

Strategies:
1. Fixed Flexible
2. Balanced Rule-Based V2
3. Final Rate-Limited AI

The final AI uses a maximum stiffness change of 0.10 per simulation
step, selected from the rate-limit sensitivity study.

All metrics are synthetic digital-twin outputs and are not clinically
validated.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from simulation.vessel_geometry import (
    generate_random_tortuous_vessel,
    calculate_curvature,
)

from simulation.catheter_model import (
    simulate_local_navigation,
)

from simulation.failure_model import (
    calculate_buckling_risk,
    calculate_kickback,
)

from controllers.balanced_controller import (
    select_balanced_stiffness,
)

from controllers.rate_limited_ai_controller import (
    RateLimitedAIController,
)


RESULTS_DIRECTORY = Path("results")

DIFFICULTIES = [
    "easy",
    "moderate",
    "severe",
]

# These seeds are intentionally outside the seed ranges
# used to create the machine-learning dataset.

SEED_BASES = {
    "easy": 1000,
    "moderate": 11000,
    "severe": 21000,
}

VESSELS_PER_DIFFICULTY = 10

N_POINTS = 200

FINAL_RATE_LIMIT = 0.10


def generate_procedural_conditions(seed):
    """
    Generate reproducible procedural/mechanical conditions
    for one vessel.

    The exact same conditions are used by every controller
    tested on that vessel.
    """

    rng = np.random.default_rng(
        seed + 50_000
    )

    friction = rng.uniform(
        0.10,
        0.40,
    )

    commanded_velocity = rng.uniform(
        3.0,
        5.0,
    )

    base_force = rng.uniform(
        0.08,
        0.12,
    )

    return (
        friction,
        commanded_velocity,
        base_force,
    )


def calculate_local_metrics(
    curvature,
    stiffness,
    friction,
    commanded_velocity,
    base_force,
):
    """
    Run the catheter mechanics and failure models
    for one vessel location.
    """

    local_result = simulate_local_navigation(
        curvature=curvature,
        friction=friction,
        stiffness=stiffness,
        commanded_velocity=commanded_velocity,
        base_force=base_force,
    )

    buckling_risk = calculate_buckling_risk(
        push_force=local_result["push_force"],
        velocity=local_result["velocity"],
        stiffness=stiffness,
    )

    kickback_score = calculate_kickback(
        push_force=local_result["push_force"],
        velocity=local_result["velocity"],
        resistance=local_result["resistance"],
    )

    combined_risk = max(
        buckling_risk,
        kickback_score,
    )

    return {
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

        "combined_risk":
            combined_risk,
    }


def simulate_fixed_flexible(
    curvature,
    friction,
    commanded_velocity,
    base_force,
):
    """
    Run the fixed flexible catheter through one vessel.
    """

    rows = []

    stiffness = 0.25

    for local_curvature in curvature:

        metrics = calculate_local_metrics(
            curvature=local_curvature,
            stiffness=stiffness,
            friction=friction,
            commanded_velocity=commanded_velocity,
            base_force=base_force,
        )

        rows.append(
            metrics
        )

    return pd.DataFrame(
        rows
    )


def simulate_balanced_v2(
    curvature,
    friction,
    commanded_velocity,
    base_force,
):
    """
    Run the Balanced V2 rule-based controller
    through one vessel.
    """

    rows = []

    current_stiffness = 0.50

    for local_curvature in curvature:

        metrics = calculate_local_metrics(
            curvature=local_curvature,
            stiffness=current_stiffness,
            friction=friction,
            commanded_velocity=commanded_velocity,
            base_force=base_force,
        )

        metrics["stiffness"] = (
            current_stiffness
        )

        rows.append(
            metrics
        )

        (
            next_stiffness,
            action,
            reason,
        ) = select_balanced_stiffness(
            curvature=local_curvature,
            push_force=metrics["push_force"],
            velocity=metrics["velocity"],
            current_stiffness=current_stiffness,
        )

        current_stiffness = (
            next_stiffness
        )

    return pd.DataFrame(
        rows
    )


def simulate_final_ai(
    curvature,
    friction,
    commanded_velocity,
    base_force,
):
    """
    Run the final rate-limited AI controller
    through one vessel.
    """

    controller = RateLimitedAIController(
        maximum_stiffness_change=(
            FINAL_RATE_LIMIT
        )
    )

    rows = []

    current_stiffness = 0.50

    for local_curvature in curvature:

        (
            selected_stiffness,
            predicted_risk,
            unconstrained_stiffness,
            candidate_results,
        ) = controller.select_stiffness(
            curvature=local_curvature,
            friction=friction,
            current_stiffness=current_stiffness,
            commanded_velocity=commanded_velocity,
            base_force=base_force,
        )

        metrics = calculate_local_metrics(
            curvature=local_curvature,
            stiffness=selected_stiffness,
            friction=friction,
            commanded_velocity=commanded_velocity,
            base_force=base_force,
        )

        metrics["stiffness"] = (
            selected_stiffness
        )

        metrics["predicted_risk"] = (
            predicted_risk
        )

        rows.append(
            metrics
        )

        current_stiffness = (
            selected_stiffness
        )

    return pd.DataFrame(
        rows
    )


def summarize_trial(
    results,
    difficulty,
    seed,
    strategy,
):
    """
    Convert one complete navigation trial into
    one summary row.
    """

    return {
        "difficulty":
            difficulty,

        "seed":
            seed,

        "strategy":
            strategy,

        "mean_combined_risk":
            results[
                "combined_risk"
            ].mean(),

        "peak_combined_risk":
            results[
                "combined_risk"
            ].max(),

        "mean_resistance":
            results[
                "resistance"
            ].mean(),

        "peak_resistance":
            results[
                "resistance"
            ].max(),

        "mean_push_force":
            results[
                "push_force"
            ].mean(),

        "peak_push_force":
            results[
                "push_force"
            ].max(),

        "minimum_velocity":
            results[
                "velocity"
            ].min(),

        "mean_velocity":
            results[
                "velocity"
            ].mean(),

        "mean_buckling_risk":
            results[
                "buckling_risk"
            ].mean(),

        "peak_buckling_risk":
            results[
                "buckling_risk"
            ].max(),

        "mean_kickback":
            results[
                "kickback_score"
            ].mean(),

        "peak_kickback":
            results[
                "kickback_score"
            ].max(),
    }


def run_robustness_study():
    """
    Run all three strategies on 30 random vessels.
    """

    rows = []

    print()
    print(
        "MULTI-VESSEL ROBUSTNESS STUDY"
    )

    print(
        "============================="
    )

    for difficulty in DIFFICULTIES:

        print()
        print(
            f"Testing {difficulty} vessels..."
        )

        seed_base = (
            SEED_BASES[difficulty]
        )

        for vessel_number in range(
            VESSELS_PER_DIFFICULTY
        ):

            seed = (
                seed_base
                + vessel_number
            )

            print(
                f"  {difficulty} vessel "
                f"{vessel_number + 1}/"
                f"{VESSELS_PER_DIFFICULTY} "
                f"(seed {seed})"
            )

            # -------------------------------------
            # Generate one random vessel.
            # -------------------------------------

            x, y = (
                generate_random_tortuous_vessel(
                    seed=seed,
                    difficulty=difficulty,
                    n_points=N_POINTS,
                )
            )

            curvature = (
                calculate_curvature(
                    x,
                    y,
                )
            )

            # -------------------------------------
            # Generate one set of procedural
            # conditions shared by every strategy.
            # -------------------------------------

            (
                friction,
                commanded_velocity,
                base_force,
            ) = generate_procedural_conditions(
                seed
            )

            # -------------------------------------
            # Fixed Flexible
            # -------------------------------------

            fixed = (
                simulate_fixed_flexible(
                    curvature=curvature,
                    friction=friction,
                    commanded_velocity=(
                        commanded_velocity
                    ),
                    base_force=base_force,
                )
            )

            rows.append(
                summarize_trial(
                    fixed,
                    difficulty,
                    seed,
                    "Fixed Flexible",
                )
            )

            # -------------------------------------
            # Balanced V2
            # -------------------------------------

            v2 = simulate_balanced_v2(
                curvature=curvature,
                friction=friction,
                commanded_velocity=(
                    commanded_velocity
                ),
                base_force=base_force,
            )

            rows.append(
                summarize_trial(
                    v2,
                    difficulty,
                    seed,
                    "Balanced V2",
                )
            )

            # -------------------------------------
            # Final Rate-Limited AI
            # -------------------------------------

            ai = simulate_final_ai(
                curvature=curvature,
                friction=friction,
                commanded_velocity=(
                    commanded_velocity
                ),
                base_force=base_force,
            )

            rows.append(
                summarize_trial(
                    ai,
                    difficulty,
                    seed,
                    "Rate-Limited AI",
                )
            )

    return pd.DataFrame(
        rows
    )


def create_group_summary(
    trials
):
    """
    Average results across vessels for every
    difficulty and controller.
    """

    metrics = [
        "mean_combined_risk",
        "peak_combined_risk",
        "mean_resistance",
        "peak_resistance",
        "mean_push_force",
        "peak_push_force",
        "minimum_velocity",
        "mean_velocity",
        "mean_buckling_risk",
        "peak_buckling_risk",
        "mean_kickback",
        "peak_kickback",
    ]

    summary = (
        trials
        .groupby(
            [
                "difficulty",
                "strategy",
            ]
        )[metrics]
        .mean()
        .reset_index()
    )

    return summary


def print_summary(
    summary
):
    """
    Print the most important robustness metrics.
    """

    print()
    print(
        "ROBUSTNESS SUMMARY"
    )

    print(
        "=================="
    )

    selected_columns = [
        "difficulty",
        "strategy",
        "mean_combined_risk",
        "peak_combined_risk",
        "mean_resistance",
        "minimum_velocity",
    ]

    print(
        summary[
            selected_columns
        ].to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}",
        )
    )


def print_ai_win_rates(
    trials
):
    """
    Calculate how often AI achieves lower mean
    combined risk than each comparator.
    """

    pivot = trials.pivot_table(
        index=[
            "difficulty",
            "seed",
        ],
        columns="strategy",
        values="mean_combined_risk",
    )

    ai = pivot[
        "Rate-Limited AI"
    ]

    print()
    print(
        "AI VESSEL-LEVEL WIN RATES"
    )

    print(
        "========================="
    )

    for comparator in [
        "Fixed Flexible",
        "Balanced V2",
    ]:

        wins = (
            ai
            < pivot[comparator]
        )

        percentage = (
            100
            * wins.mean()
        )

        print(
            f"AI lower mean risk than "
            f"{comparator}: "
            f"{wins.sum()}/"
            f"{len(wins)} vessels "
            f"({percentage:.1f}%)"
        )


def save_results(
    trials,
    summary,
):

    RESULTS_DIRECTORY.mkdir(
        exist_ok=True
    )

    trials.to_csv(
        RESULTS_DIRECTORY
        / "multi_vessel_robustness_trials.csv",
        index=False,
    )

    summary.to_csv(
        RESULTS_DIRECTORY
        / "multi_vessel_robustness_summary.csv",
        index=False,
    )


def plot_results(
    trials
):
    """
    Plot vessel-level controller performance.
    """

    strategies = [
        "Fixed Flexible",
        "Balanced V2",
        "Rate-Limited AI",
    ]

    fig, axes = plt.subplots(
        3,
        1,
        figsize=(11, 12),
        constrained_layout=True,
    )

    for index, difficulty in enumerate(
        DIFFICULTIES
    ):

        subset = trials[
            trials["difficulty"]
            == difficulty
        ]

        data = [
            subset[
                subset["strategy"]
                == strategy
            ]["mean_combined_risk"]
            for strategy in strategies
        ]

        axes[index].boxplot(
            data,
            tick_labels=strategies,
            showfliers=True,
        )

        axes[index].set_title(
            f"{difficulty.title()} Vessels"
        )

        axes[index].set_ylabel(
            "Mean Combined Risk"
        )

        axes[index].set_ylim(
            0,
            1,
        )

        axes[index].grid(
            True,
            axis="y",
        )

    fig.suptitle(
        "Controller Robustness Across 30 Unseen Synthetic Vessels"
    )

    plt.show()


def main():

    trials = run_robustness_study()

    summary = create_group_summary(
        trials
    )

    print_summary(
        summary
    )

    print_ai_win_rates(
        trials
    )

    save_results(
        trials,
        summary,
    )

    plot_results(
        trials
    )


if __name__ == "__main__":
    main()