"""
Machine Learning Dataset Generator
----------------------------------

Generates synthetic catheter-navigation data across:

- Easy vessel geometries
- Moderate vessel geometries
- Severe vessel geometries
- Different catheter stiffness values
- Different friction conditions
- Different commanded velocities
- Different baseline force conditions

IMPORTANT:

Entire vessel geometries are separated between training,
validation, and test sets.

The final test vessels are therefore geometries that the
machine-learning model has never seen during training.

All values are simulation outputs and are not validated
clinical measurements.
"""

from pathlib import Path

import numpy as np
import pandas as pd

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

from simulation.navigation_simulator import (
    calculate_arc_length,
)


# ---------------------------------------------------------
# Dataset design
#
# For EACH difficulty:
#
# 70 vessels -> training
# 15 vessels -> validation
# 15 vessels -> testing
#
# Total:
#
# 100 easy
# 100 moderate
# 100 severe
# = 300 vessels
# ---------------------------------------------------------


DIFFICULTY_SEED_BASES = {
    "easy": 0,
    "moderate": 10_000,
    "severe": 20_000,
}


def get_split(index_within_difficulty):
    """
    Assign vessels to train, validation, or test.

    The split occurs at the whole-vessel level.
    """

    if index_within_difficulty < 70:
        return "train"

    if index_within_difficulty < 85:
        return "validation"

    return "test"


def generate_vessel_trial(
    difficulty,
    vessel_seed,
    vessel_index,
    n_points=200,
):
    """
    Generate one complete catheter-navigation trial.
    """

    # Separate random generator for mechanical conditions.
    #
    # This keeps the experiment reproducible while separating
    # mechanical randomization from vessel geometry generation.

    rng = np.random.default_rng(
        vessel_seed + 50_000
    )

    # Generate synthetic vessel geometry.

    x, y = generate_random_tortuous_vessel(
        seed=vessel_seed,
        difficulty=difficulty,
        n_points=n_points,
    )

    curvature = calculate_curvature(
        x,
        y,
    )

    position = calculate_arc_length(
        x,
        y,
    )

    # ---------------------------------------------------------
    # Randomized catheter / procedural conditions
    # ---------------------------------------------------------

    friction = rng.uniform(
        0.10,
        0.40,
    )

    stiffness = rng.uniform(
        0.10,
        0.90,
    )

    commanded_velocity = rng.uniform(
        3.0,
        5.0,
    )

    base_force = rng.uniform(
        0.08,
        0.12,
    )

    split = get_split(
        vessel_index
    )

    vessel_id = (
        f"{difficulty}_{vessel_seed}"
    )

    rows = []

    # ---------------------------------------------------------
    # Simulate every location along the vessel
    # ---------------------------------------------------------

    for i in range(len(x)):

        local_result = simulate_local_navigation(
            curvature=curvature[i],
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

        # For now, define overall simulated mechanical risk
        # as whichever modeled failure mode is currently greater.
        #
        # This remains a continuous score.
        # We are NOT calling this a clinical probability.

        combined_risk = max(
            buckling_risk,
            kickback_score,
        )

        rows.append({
            # Dataset identifiers
            "split": split,
            "difficulty": difficulty,
            "vessel_id": vessel_id,
            "vessel_seed": vessel_seed,

            # Position
            "position": position[i],
            "x": x[i],
            "y": y[i],

            # Geometry
            "curvature": curvature[i],

            # Catheter / procedure conditions
            "current_stiffness": stiffness,
            "friction": friction,
            "commanded_velocity": commanded_velocity,
            "base_force": base_force,

            # Navigation response
            "resistance": local_result["resistance"],
            "velocity": local_result["velocity"],
            "push_force": local_result["push_force"],

            # Failure-related simulation outputs
            "buckling_risk": buckling_risk,
            "kickback_score": kickback_score,
            "combined_risk": combined_risk,
        })

    return pd.DataFrame(
        rows
    )


def generate_dataset(
    vessels_per_difficulty=100,
    n_points=200,
):
    """
    Generate the complete dataset.
    """

    all_vessels = []

    difficulties = [
        "easy",
        "moderate",
        "severe",
    ]

    for difficulty in difficulties:

        seed_base = (
            DIFFICULTY_SEED_BASES[difficulty]
        )

        print()
        print(
            f"Generating {difficulty} vessels..."
        )

        for vessel_index in range(
            vessels_per_difficulty
        ):

            vessel_seed = (
                seed_base
                + vessel_index
            )

            vessel_data = generate_vessel_trial(
                difficulty=difficulty,
                vessel_seed=vessel_seed,
                vessel_index=vessel_index,
                n_points=n_points,
            )

            all_vessels.append(
                vessel_data
            )

            if (
                vessel_index + 1
            ) % 20 == 0:

                print(
                    f"  Completed "
                    f"{vessel_index + 1}/"
                    f"{vessels_per_difficulty}"
                )

    dataset = pd.concat(
        all_vessels,
        ignore_index=True,
    )

    return dataset


def validate_dataset(dataset):
    """
    Perform basic integrity checks before ML training.
    """

    # All 300 vessels should be present.

    assert (
        dataset["vessel_id"].nunique()
        == 300
    )

    # 100 vessels from each difficulty.

    difficulty_counts = (
        dataset.groupby(
            "difficulty"
        )["vessel_id"]
        .nunique()
    )

    assert (
        difficulty_counts["easy"]
        == 100
    )

    assert (
        difficulty_counts["moderate"]
        == 100
    )

    assert (
        difficulty_counts["severe"]
        == 100
    )

    # No vessel may exist in multiple dataset splits.

    split_counts = (
        dataset.groupby(
            "vessel_id"
        )["split"]
        .nunique()
    )

    assert (
        split_counts.max()
        == 1
    )

    # Risk scores must remain valid.

    assert (
        dataset["buckling_risk"]
        .between(0, 1)
        .all()
    )

    assert (
        dataset["kickback_score"]
        .between(0, 1)
        .all()
    )

    assert (
        dataset["combined_risk"]
        .between(0, 1)
        .all()
    )

    # Numerical columns should contain no missing data.

    assert not (
        dataset.isna()
        .any()
        .any()
    )

    print()
    print(
        "Dataset integrity checks: PASSED"
    )


def print_dataset_summary(dataset):
    """
    Print basic dataset statistics.
    """

    print()
    print("Machine Learning Dataset Summary")
    print("--------------------------------")

    print(
        f"Total rows: "
        f"{len(dataset):,}"
    )

    print(
        f"Unique vessels: "
        f"{dataset['vessel_id'].nunique()}"
    )

    print()

    print(
        "Vessels by difficulty:"
    )

    print(
        dataset.groupby(
            "difficulty"
        )["vessel_id"]
        .nunique()
    )

    print()

    print(
        "Vessels by split:"
    )

    print(
        dataset.groupby(
            "split"
        )["vessel_id"]
        .nunique()
    )

    print()

    print(
        "Rows by split:"
    )

    print(
        dataset[
            "split"
        ].value_counts()
    )

    print()

    print(
        "Combined risk range:"
    )

    print(
        f"{dataset['combined_risk'].min():.4f}"
        f" to "
        f"{dataset['combined_risk'].max():.4f}"
    )


def save_dataset(dataset):
    """
    Save complete and split-specific CSV files.
    """

    data_directory = Path(
        "data"
    )

    data_directory.mkdir(
        exist_ok=True
    )

    dataset.to_csv(
        data_directory
        / "navigation_dataset.csv",
        index=False,
    )

    for split in [
        "train",
        "validation",
        "test",
    ]:

        split_data = dataset[
            dataset["split"] == split
        ]

        split_data.to_csv(
            data_directory
            / f"{split}_navigation.csv",
            index=False,
        )


def main():

    dataset = generate_dataset(
        vessels_per_difficulty=100,
        n_points=200,
    )

    validate_dataset(
        dataset
    )

    print_dataset_summary(
        dataset
    )

    save_dataset(
        dataset
    )

    print()
    print(
        "Dataset files saved in data/"
    )


if __name__ == "__main__":
    main()