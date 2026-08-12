"""
Final Navigation Risk Model Evaluation
--------------------------------------

Evaluates the frozen Random Forest navigation-risk estimator on the
final held-out test set.

The test vessels were not used for:
- model training
- hyperparameter selection
- model selection
- validation analysis

This script represents the final unbiased ML evaluation.

IMPORTANT:
The predicted target is a simulated digital-twin risk metric.
It is not a clinically validated probability of catheter failure.
"""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)


DATA_DIRECTORY = Path("data")
MODEL_DIRECTORY = Path("models")
RESULTS_DIRECTORY = Path("results")


FEATURES = [
    "curvature",
    "current_stiffness",
    "push_force",
    "velocity",
]

TARGET = "combined_risk"


def load_model():
    """
    Load the frozen Random Forest model.
    """

    model_path = (
        MODEL_DIRECTORY
        / "navigation_risk_random_forest.joblib"
    )

    model = joblib.load(
        model_path
    )

    return model


def load_test_data():
    """
    Load the untouched final test dataset.
    """

    test = pd.read_csv(
        DATA_DIRECTORY
        / "test_navigation.csv"
    )

    return test


def create_predictions(
    model,
    test,
):
    """
    Generate final predictions.
    """

    x_test = test[
        FEATURES
    ]

    predictions = model.predict(
        x_test
    )

    results = test.copy()

    results[
        "predicted_risk"
    ] = predictions

    results[
        "residual"
    ] = (
        results[TARGET]
        - results["predicted_risk"]
    )

    results[
        "absolute_error"
    ] = np.abs(
        results["residual"]
    )

    return results


def print_overall_metrics(
    results
):
    """
    Print final test metrics.
    """

    actual = results[
        TARGET
    ]

    predicted = results[
        "predicted_risk"
    ]

    mae = mean_absolute_error(
        actual,
        predicted,
    )

    rmse = (
        mean_squared_error(
            actual,
            predicted,
        )
        ** 0.5
    )

    r2 = r2_score(
        actual,
        predicted,
    )

    print()
    print("FINAL TEST SET RESULTS")
    print("======================")

    print(
        f"Test samples: "
        f"{len(results):,}"
    )

    print(
        f"Test vessels: "
        f"{results['vessel_id'].nunique()}"
    )

    print()

    print(
        f"MAE:  {mae:.4f}"
    )

    print(
        f"RMSE: {rmse:.4f}"
    )

    print(
        f"R²:   {r2:.4f}"
    )

    return {
        "mae": mae,
        "rmse": rmse,
        "r2": r2,
    }


def print_difficulty_metrics(
    results
):
    """
    Evaluate final performance separately for
    easy, moderate, and severe vessels.
    """

    rows = []

    for difficulty in [
        "easy",
        "moderate",
        "severe",
    ]:

        subset = results[
            results["difficulty"]
            == difficulty
        ]

        actual = subset[
            TARGET
        ]

        predicted = subset[
            "predicted_risk"
        ]

        rows.append({
            "difficulty": difficulty,

            "samples": len(
                subset
            ),

            "vessels": subset[
                "vessel_id"
            ].nunique(),

            "mae":
                mean_absolute_error(
                    actual,
                    predicted,
                ),

            "rmse":
                mean_squared_error(
                    actual,
                    predicted,
                )
                ** 0.5,

            "r2":
                r2_score(
                    actual,
                    predicted,
                ),
        })

    table = pd.DataFrame(
        rows
    )

    print()
    print(
        "Final Performance by Vessel Difficulty"
    )

    print(
        "--------------------------------------"
    )

    print(
        table.to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}",
        )
    )


def print_worst_vessels(
    results
):
    """
    Identify the test vessels with the largest
    mean prediction error.
    """

    vessel_errors = (
        results
        .groupby(
            [
                "vessel_id",
                "difficulty",
            ]
        )[
            "absolute_error"
        ]
        .mean()
        .reset_index()
    )

    vessel_errors = (
        vessel_errors
        .sort_values(
            "absolute_error",
            ascending=False,
        )
    )

    print()
    print(
        "10 Test Vessels With Highest Mean Error"
    )

    print(
        "---------------------------------------"
    )

    print(
        vessel_errors
        .head(10)
        .to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}",
        )
    )


def print_ceiling_performance(
    results
):
    """
    Analyze samples at the simulated risk ceiling.
    """

    ceiling = results[
        results[TARGET]
        >= 0.9999
    ]

    print()
    print(
        "Test Risk-Ceiling Analysis"
    )

    print(
        "--------------------------"
    )

    print(
        f"Samples at actual risk 1.0: "
        f"{len(ceiling):,}"
    )

    if len(ceiling) > 0:

        ceiling_mae = (
            mean_absolute_error(
                ceiling[TARGET],
                ceiling["predicted_risk"],
            )
        )

        print(
            f"MAE at risk ceiling: "
            f"{ceiling_mae:.4f}"
        )

        print(
            f"Mean prediction at ceiling: "
            f"{ceiling['predicted_risk'].mean():.4f}"
        )


def plot_final_results(
    results
):
    """
    Create final test-set diagnostic plots.
    """

    sample = results.sample(
        n=min(
            5000,
            len(results),
        ),
        random_state=42,
    )

    fig, axes = plt.subplots(
        2,
        2,
        figsize=(12, 10),
        constrained_layout=True,
    )

    # -----------------------------------------
    # Actual vs predicted
    # -----------------------------------------

    axes[0, 0].scatter(
        sample[TARGET],
        sample["predicted_risk"],
        alpha=0.25,
        s=10,
    )

    axes[0, 0].plot(
        [0, 1],
        [0, 1],
        linestyle="--",
    )

    axes[0, 0].set_title(
        "Final Test: Actual vs Predicted Risk"
    )

    axes[0, 0].set_xlabel(
        "Actual Simulated Risk"
    )

    axes[0, 0].set_ylabel(
        "Predicted Risk"
    )

    axes[0, 0].set_xlim(
        0,
        1.02,
    )

    axes[0, 0].set_ylim(
        0,
        1.02,
    )

    # -----------------------------------------
    # Residuals
    # -----------------------------------------

    axes[0, 1].scatter(
        sample[TARGET],
        sample["residual"],
        alpha=0.25,
        s=10,
    )

    axes[0, 1].axhline(
        0,
        linestyle="--",
    )

    axes[0, 1].set_title(
        "Final Test Prediction Residuals"
    )

    axes[0, 1].set_xlabel(
        "Actual Simulated Risk"
    )

    axes[0, 1].set_ylabel(
        "Actual - Predicted"
    )

    # -----------------------------------------
    # Error by difficulty
    # -----------------------------------------

    difficulty_data = [
        results[
            results[
                "difficulty"
            ] == difficulty
        ][
            "absolute_error"
        ]

        for difficulty in [
            "easy",
            "moderate",
            "severe",
        ]
    ]

    axes[1, 0].boxplot(
        difficulty_data,
        tick_labels=[
            "Easy",
            "Moderate",
            "Severe",
        ],
        showfliers=False,
    )

    axes[1, 0].set_title(
        "Final Test Error by Vessel Difficulty"
    )

    axes[1, 0].set_ylabel(
        "Absolute Error"
    )

    # -----------------------------------------
    # Residual histogram
    # -----------------------------------------

    axes[1, 1].hist(
        results[
            "residual"
        ],
        bins=50,
    )

    axes[1, 1].set_title(
        "Final Test Residual Distribution"
    )

    axes[1, 1].set_xlabel(
        "Actual - Predicted"
    )

    axes[1, 1].set_ylabel(
        "Samples"
    )

    plt.show()


def save_results(
    results,
    metrics,
):
    """
    Save final test predictions and metrics.
    """

    RESULTS_DIRECTORY.mkdir(
        exist_ok=True
    )

    results.to_csv(
        RESULTS_DIRECTORY
        / "final_test_risk_predictions.csv",
        index=False,
    )

    metrics_table = pd.DataFrame([
        {
            "model":
                "Random Forest",

            "test_samples":
                len(results),

            "test_vessels":
                results[
                    "vessel_id"
                ].nunique(),

            "mae":
                metrics["mae"],

            "rmse":
                metrics["rmse"],

            "r2":
                metrics["r2"],
        }
    ])

    metrics_table.to_csv(
        RESULTS_DIRECTORY
        / "final_test_metrics.csv",
        index=False,
    )


def main():

    print()
    print(
        "Loading frozen navigation risk model..."
    )

    model = load_model()

    print(
        "Loading final held-out test vessels..."
    )

    test = load_test_data()

    results = create_predictions(
        model,
        test,
    )

    metrics = print_overall_metrics(
        results
    )

    print_difficulty_metrics(
        results
    )

    print_worst_vessels(
        results
    )

    print_ceiling_performance(
        results
    )

    save_results(
        results,
        metrics,
    )

    plot_final_results(
        results
    )


if __name__ == "__main__":
    main()