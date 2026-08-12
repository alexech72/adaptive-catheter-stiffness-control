"""
Vessel Difficulty Distribution Analysis
---------------------------------------

Evaluates the synthetic easy, moderate, and severe vessel generators
across many reproducible vessel seeds.

The purpose is to verify that the three geometric difficulty groups
produce meaningfully different curvature distributions before they
are used for machine-learning dataset generation.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from simulation.vessel_geometry import (
    generate_random_tortuous_vessel,
    calculate_curvature,
)


def analyze_difficulty(
    difficulty,
    n_vessels=100,
):
    """
    Generate multiple vessels for one difficulty level and
    calculate curvature statistics for each vessel.
    """

    rows = []

    for seed in range(n_vessels):

        x, y = generate_random_tortuous_vessel(
            seed=seed,
            difficulty=difficulty,
        )

        curvature = calculate_curvature(
            x,
            y,
        )

        rows.append({
            "difficulty": difficulty,
            "seed": seed,
            "max_curvature": curvature.max(),
            "mean_curvature": curvature.mean(),
            "median_curvature": np.median(curvature),
            "p95_curvature": np.percentile(
                curvature,
                95
            ),
        })

    return pd.DataFrame(rows)


def generate_analysis():

    datasets = []

    for difficulty in [
        "easy",
        "moderate",
        "severe",
    ]:

        print(
            f"Analyzing {difficulty} vessels..."
        )

        data = analyze_difficulty(
            difficulty=difficulty,
            n_vessels=100,
        )

        datasets.append(
            data
        )

    results = pd.concat(
        datasets,
        ignore_index=True,
    )

    return results


def print_summary(results):
    """
    Print curvature statistics by difficulty group.
    """

    summary = (
        results
        .groupby("difficulty")
        .agg(
            vessels=("seed", "count"),

            mean_max_curvature=(
                "max_curvature",
                "mean"
            ),

            median_max_curvature=(
                "max_curvature",
                "median"
            ),

            minimum_max_curvature=(
                "max_curvature",
                "min"
            ),

            maximum_max_curvature=(
                "max_curvature",
                "max"
            ),

            mean_p95_curvature=(
                "p95_curvature",
                "mean"
            ),
        )
    )

    print()
    print("Vessel Difficulty Curvature Summary")
    print("-----------------------------------")

    print(
        summary.to_string(
            float_format=lambda value: f"{value:.4f}"
        )
    )


def plot_distributions(results):
    """
    Plot the maximum-curvature distributions for each
    vessel difficulty level.
    """

    difficulties = [
        "easy",
        "moderate",
        "severe",
    ]

    data = [
        results[
            results["difficulty"] == difficulty
        ]["max_curvature"]
        for difficulty in difficulties
    ]

    fig, axes = plt.subplots(
        2,
        1,
        figsize=(10, 9),
        constrained_layout=True,
    )

    # Boxplot comparison
    axes[0].boxplot(
        data,
        tick_labels=[
            "Easy",
            "Moderate",
            "Severe",
        ],
    )

    axes[0].set_title(
        "Maximum Curvature by Synthetic Vessel Difficulty"
    )

    axes[0].set_ylabel(
        "Maximum Curvature"
    )

    axes[0].grid(True)

    # Distribution histograms
    for difficulty in difficulties:

        subset = results[
            results["difficulty"] == difficulty
        ]

        axes[1].hist(
            subset["max_curvature"],
            bins=20,
            alpha=0.5,
            label=difficulty.capitalize(),
        )

    axes[1].set_title(
        "Distribution of Maximum Vessel Curvature"
    )

    axes[1].set_xlabel(
        "Maximum Curvature"
    )

    axes[1].set_ylabel(
        "Number of Vessels"
    )

    axes[1].legend()
    axes[1].grid(True)

    plt.show()


def main():

    results = generate_analysis()

    print_summary(
        results
    )

    results.to_csv(
        "results/vessel_difficulty_analysis.csv",
        index=False,
    )

    plot_distributions(
        results
    )


if __name__ == "__main__":
    main()