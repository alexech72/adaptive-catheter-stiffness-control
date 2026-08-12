"""
Machine Learning Dataset Analysis
---------------------------------

Examines the generated catheter-navigation dataset before
machine-learning model development.

Checks include:

- split integrity
- curvature distribution
- simulated-risk distribution
- difficulty balance
- feature ranges
- risk-score saturation
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


DATA_PATH = Path(
    "data/navigation_dataset.csv"
)


def load_dataset():

    dataset = pd.read_csv(
        DATA_PATH
    )

    return dataset


def verify_split_integrity(dataset):
    """
    Verify that no vessel appears in more than one split.
    """

    train_vessels = set(
        dataset[
            dataset["split"] == "train"
        ]["vessel_id"]
    )

    validation_vessels = set(
        dataset[
            dataset["split"] == "validation"
        ]["vessel_id"]
    )

    test_vessels = set(
        dataset[
            dataset["split"] == "test"
        ]["vessel_id"]
    )

    assert train_vessels.isdisjoint(
        validation_vessels
    )

    assert train_vessels.isdisjoint(
        test_vessels
    )

    assert validation_vessels.isdisjoint(
        test_vessels
    )

    print(
        "Vessel split leakage check: PASSED"
    )


def print_summary(dataset):

    print()
    print("Dataset Analysis")
    print("----------------")

    print(
        f"Rows: {len(dataset):,}"
    )

    print(
        f"Unique vessels: "
        f"{dataset['vessel_id'].nunique()}"
    )

    print()

    print("Feature ranges:")

    features = [
        "curvature",
        "current_stiffness",
        "friction",
        "velocity",
        "push_force",
        "resistance",
        "buckling_risk",
        "kickback_score",
        "combined_risk",
    ]

    print(
        dataset[features]
        .describe()
        .T
        .to_string(
            float_format=lambda x: f"{x:.4f}"
        )
    )

    print()
    print("Mean combined risk by difficulty:")

    print(
        dataset.groupby(
            "difficulty"
        )["combined_risk"]
        .mean()
        .to_string()
    )

    print()
    print("Mean combined risk by split:")

    print(
        dataset.groupby(
            "split"
        )["combined_risk"]
        .mean()
        .to_string()
    )

    # Check how many values hit the upper clamp.

    saturated = (
        dataset["combined_risk"]
        >= 0.9999
    )

    saturated_count = saturated.sum()

    saturated_percent = (
        100
        * saturated_count
        / len(dataset)
    )

    print()
    print(
        f"Samples at risk ceiling (1.0): "
        f"{saturated_count:,}"
    )

    print(
        f"Percent at risk ceiling: "
        f"{saturated_percent:.2f}%"
    )


def plot_distributions(dataset):

    fig, axes = plt.subplots(
        2,
        2,
        figsize=(12, 9),
        constrained_layout=True,
    )

    # -----------------------------------------
    # Curvature by vessel difficulty
    # -----------------------------------------

    for difficulty in [
        "easy",
        "moderate",
        "severe",
    ]:

        subset = dataset[
            dataset["difficulty"]
            == difficulty
        ]

        axes[0, 0].hist(
            subset["curvature"],
            bins=40,
            alpha=0.5,
            label=difficulty.capitalize(),
        )

    axes[0, 0].set_title(
        "Curvature Distribution by Difficulty"
    )

    axes[0, 0].set_xlabel(
        "Curvature"
    )

    axes[0, 0].set_ylabel(
        "Samples"
    )

    axes[0, 0].legend()

    # -----------------------------------------
    # Combined risk by difficulty
    # -----------------------------------------

    for difficulty in [
        "easy",
        "moderate",
        "severe",
    ]:

        subset = dataset[
            dataset["difficulty"]
            == difficulty
        ]

        axes[0, 1].hist(
            subset["combined_risk"],
            bins=40,
            alpha=0.5,
            label=difficulty.capitalize(),
        )

    axes[0, 1].set_title(
        "Combined Risk by Vessel Difficulty"
    )

    axes[0, 1].set_xlabel(
        "Combined Risk"
    )

    axes[0, 1].set_ylabel(
        "Samples"
    )

    axes[0, 1].legend()

    # -----------------------------------------
    # Risk distribution by dataset split
    # -----------------------------------------

    for split in [
        "train",
        "validation",
        "test",
    ]:

        subset = dataset[
            dataset["split"] == split
        ]

        axes[1, 0].hist(
            subset["combined_risk"],
            bins=40,
            alpha=0.5,
            label=split.capitalize(),
            density=True,
        )

    axes[1, 0].set_title(
        "Combined Risk by Dataset Split"
    )

    axes[1, 0].set_xlabel(
        "Combined Risk"
    )

    axes[1, 0].set_ylabel(
        "Density"
    )

    axes[1, 0].legend()

    # -----------------------------------------
    # Push force vs combined risk
    # -----------------------------------------

    sample = dataset.sample(
        n=min(
            5000,
            len(dataset)
        ),
        random_state=42,
    )

    axes[1, 1].scatter(
        sample["push_force"],
        sample["combined_risk"],
        alpha=0.25,
        s=8,
    )

    axes[1, 1].set_title(
        "Push Force vs Combined Risk"
    )

    axes[1, 1].set_xlabel(
        "Push Force"
    )

    axes[1, 1].set_ylabel(
        "Combined Risk"
    )

    plt.show()


def main():

    dataset = load_dataset()

    verify_split_integrity(
        dataset
    )

    print_summary(
        dataset
    )

    plot_distributions(
        dataset
    )


if __name__ == "__main__":
    main()