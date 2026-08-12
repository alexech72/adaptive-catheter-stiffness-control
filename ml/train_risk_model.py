"""
Navigation Risk Model Training
------------------------------

Trains baseline machine-learning models to estimate simulated
combined navigation risk.

Model inputs:
- local vessel curvature
- current catheter stiffness
- proximal push force
- advancement velocity

Target:
- combined_risk

Model selection is performed using the validation vessels.
The final test dataset is intentionally not used here.
"""

from pathlib import Path

import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)


DATA_DIRECTORY = Path("data")

FEATURES = [
    "curvature",
    "current_stiffness",
    "push_force",
    "velocity",
]

TARGET = "combined_risk"


def load_data():
    """
    Load training and validation datasets.
    """

    train = pd.read_csv(
        DATA_DIRECTORY / "train_navigation.csv"
    )

    validation = pd.read_csv(
        DATA_DIRECTORY / "validation_navigation.csv"
    )

    return train, validation


def prepare_xy(dataset):
    """
    Separate model inputs and prediction target.
    """

    x = dataset[FEATURES]
    y = dataset[TARGET]

    return x, y


def evaluate_model(
    name,
    model,
    x_validation,
    y_validation,
):
    """
    Evaluate a trained model on unseen validation vessels.
    """

    predictions = model.predict(
        x_validation
    )

    mae = mean_absolute_error(
        y_validation,
        predictions,
    )

    rmse = mean_squared_error(
        y_validation,
        predictions,
    ) ** 0.5

    r2 = r2_score(
        y_validation,
        predictions,
    )

    print()
    print(name)
    print("-" * len(name))

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
        "model": name,
        "mae": mae,
        "rmse": rmse,
        "r2": r2,
    }


def main():

    train, validation = load_data()

    x_train, y_train = prepare_xy(
        train
    )

    x_validation, y_validation = prepare_xy(
        validation
    )

    print()
    print("Navigation Risk Model Training")
    print("------------------------------")

    print(
        f"Training samples: "
        f"{len(train):,}"
    )

    print(
        f"Validation samples: "
        f"{len(validation):,}"
    )

    print()

    print("Model features:")

    for feature in FEATURES:
        print(
            f"  - {feature}"
        )

    # ---------------------------------------------------------
    # MODEL 1: Linear Regression
    # ---------------------------------------------------------

    linear_model = LinearRegression()

    linear_model.fit(
        x_train,
        y_train,
    )

    linear_results = evaluate_model(
        "Linear Regression",
        linear_model,
        x_validation,
        y_validation,
    )

    # ---------------------------------------------------------
    # MODEL 2: Random Forest
    # ---------------------------------------------------------

    random_forest = RandomForestRegressor(
        n_estimators=150,
        max_depth=12,
        min_samples_leaf=5,
        random_state=42,
        n_jobs=-1,
    )

    random_forest.fit(
        x_train,
        y_train,
    )

    forest_results = evaluate_model(
        "Random Forest",
        random_forest,
        x_validation,
        y_validation,
    )

    # ---------------------------------------------------------
    # Compare models
    # ---------------------------------------------------------

    results = pd.DataFrame([
        linear_results,
        forest_results,
    ])

    print()
    print("Validation Model Comparison")
    print("---------------------------")

    print(
        results.to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}",
        )
    )

    # ---------------------------------------------------------
    # Random Forest feature importance
    # ---------------------------------------------------------

    importance = pd.DataFrame({
        "feature": FEATURES,
        "importance": random_forest.feature_importances_,
    })

    importance = importance.sort_values(
        "importance",
        ascending=False,
    )

    print()
    print("Random Forest Feature Importance")
    print("--------------------------------")

    print(
        importance.to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}",
        )
    )


if __name__ == "__main__":
    main()