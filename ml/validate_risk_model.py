"""
Random Forest Risk Model Validation
-----------------------------------

Performs detailed validation of the selected Random Forest risk estimator.

The model is trained using training vessels and evaluated only on
validation vessels.

The final test dataset is intentionally not used in this script.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)


DATA_DIRECTORY = Path("data")
RESULTS_DIRECTORY = Path("results")

FEATURES = [
    "curvature",
    "current_stiffness",
    "push_force",
    "velocity",
]

TARGET = "combined_risk"


def load_data():

    train = pd.read_csv(
        DATA_DIRECTORY / "train_navigation.csv"
    )

    validation = pd.read_csv(
        DATA_DIRECTORY / "validation_navigation.csv"
    )

    return train, validation


def train_model(train):

    x_train = train[FEATURES]
    y_train = train[TARGET]

    model = RandomForestRegressor(
        n_estimators=150,
        max_depth=12,
        min_samples_leaf=5,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(
        x_train,
        y_train,
    )

    return model


def create_predictions(
    model,
    validation,
):

    x_validation = validation[FEATURES]

    predictions = model.predict(
        x_validation
    )

    results = validation.copy()

    results["predicted_risk"] = predictions

    results["residual"] = (
        results[TARGET]
        - results["predicted_risk"]
    )

    results["absolute_error"] = (
        np.abs(
            results["residual"]
        )
    )

    return results


def print_overall_metrics(results):

    actual = results[TARGET]
    predicted = results["predicted_risk"]

    mae = mean_absolute_error(
        actual,
        predicted,
    )

    rmse = mean_squared_error(
        actual,
        predicted,
    ) ** 0.5

    r2 = r2_score(
        actual,
        predicted,
    )

    print()
    print("Random Forest Validation Diagnostics")
    print("------------------------------------")

    print(
        f"MAE:  {mae:.4f}"
    )

    print(
        f"RMSE: {rmse:.4f}"
    )

    print(
        f"R²:   {r2:.4f}"
    )


def print_difficulty_metrics(results):

    print()
    print("Performance by Vessel Difficulty")
    print("--------------------------------")

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

        actual = subset[TARGET]
        predicted = subset["predicted_risk"]

        rows.append({
            "difficulty": difficulty,

            "samples": len(subset),

            "mae": mean_absolute_error(
                actual,
                predicted,
            ),

            "rmse": (
                mean_squared_error(
                    actual,
                    predicted,
                )
                ** 0.5
            ),

            "r2": r2_score(
                actual,
                predicted,
            ),
        })

    table = pd.DataFrame(
        rows
    )

    print(
        table.to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}",
        )
    )


def print_worst_vessels(results):

    vessel_errors = (
        results.groupby(
            [
                "vessel_id",
                "difficulty",
            ]
        )["absolute_error"]
        .mean()
        .reset_index()
    )

    vessel_errors = vessel_errors.sort_values(
        "absolute_error",
        ascending=False,
    )

    print()
    print("10 Validation Vessels With Highest Mean Error")
    print("---------------------------------------------")

    print(
        vessel_errors.head(10).to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}",
        )
    )


def print_ceiling_analysis(results):

    ceiling = results[
        results[TARGET] >= 0.9999
    ]

    print()
    print("Risk-Ceiling Analysis")
    print("---------------------")

    print(
        f"Validation samples at actual risk 1.0: "
        f"{len(ceiling):,}"
    )

    if len(ceiling) > 0:

        ceiling_mae = mean_absolute_error(
            ceiling[TARGET],
            ceiling["predicted_risk"],
        )

        print(
            f"MAE for risk-ceiling samples: "
            f"{ceiling_mae:.4f}"
        )

        print(
            f"Mean prediction at ceiling: "
            f"{ceiling['predicted_risk'].mean():.4f}"
        )


def plot_validation(results):

    fig, axes = plt.subplots(
        2,
        2,
        figsize=(12, 10),
        constrained_layout=True,
    )

    # -----------------------------------------
    # Actual vs predicted risk
    # -----------------------------------------

    sample = results.sample(
        n=min(
            5000,
            len(results)
        ),
        random_state=42,
    )

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
        "Actual vs Predicted Simulated Risk"
    )

    axes[0, 0].set_xlabel(
        "Actual Risk"
    )

    axes[0, 0].set_ylabel(
        "Predicted Risk"
    )

    axes[0, 0].set_xlim(
        0,
        1.02
    )

    axes[0, 0].set_ylim(
        0,
        1.02
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
        "Prediction Residuals"
    )

    axes[0, 1].set_xlabel(
        "Actual Risk"
    )

    axes[0, 1].set_ylabel(
        "Actual - Predicted"
    )

    # -----------------------------------------
    # Absolute error by difficulty
    # -----------------------------------------

    difficulty_data = [
        results[
            results["difficulty"] == difficulty
        ]["absolute_error"]
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
        "Absolute Prediction Error by Difficulty"
    )

    axes[1, 0].set_ylabel(
        "Absolute Error"
    )

    # -----------------------------------------
    # Error distribution
    # -----------------------------------------

    axes[1, 1].hist(
        results["residual"],
        bins=50,
    )

    axes[1, 1].set_title(
        "Residual Error Distribution"
    )

    axes[1, 1].set_xlabel(
        "Actual - Predicted"
    )

    axes[1, 1].set_ylabel(
        "Samples"
    )

    plt.show()


def save_results(results):

    RESULTS_DIRECTORY.mkdir(
        exist_ok=True
    )

    results.to_csv(
        RESULTS_DIRECTORY
        / "validation_risk_predictions.csv",
        index=False,
    )


def main():

    train, validation = load_data()

    model = train_model(
        train
    )

    results = create_predictions(
        model,
        validation,
    )

    print_overall_metrics(
        results
    )

    print_difficulty_metrics(
        results
    )

    print_worst_vessels(
        results
    )

    print_ceiling_analysis(
        results
    )

    save_results(
        results
    )

    plot_validation(
        results
    )


if __name__ == "__main__":
    main()