"""
Freeze Navigation Risk Model
----------------------------

Retrains the selected Random Forest configuration using the
combined training + validation datasets and saves the frozen model.

The final test dataset remains untouched.

Selected inputs:
- curvature
- current_stiffness
- push_force
- velocity

Target:
- combined_risk
"""

from pathlib import Path
import json

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestRegressor


DATA_DIRECTORY = Path("data")
MODEL_DIRECTORY = Path("models")

FEATURES = [
    "curvature",
    "current_stiffness",
    "push_force",
    "velocity",
]

TARGET = "combined_risk"


def load_development_data():
    """
    Combine training and validation data after model selection.
    """

    train = pd.read_csv(
        DATA_DIRECTORY / "train_navigation.csv"
    )

    validation = pd.read_csv(
        DATA_DIRECTORY / "validation_navigation.csv"
    )

    development = pd.concat(
        [
            train,
            validation,
        ],
        ignore_index=True,
    )

    return development


def train_final_model(
    development
):
    """
    Train the frozen Random Forest configuration.
    """

    x = development[FEATURES]
    y = development[TARGET]

    model = RandomForestRegressor(
        n_estimators=150,
        max_depth=12,
        min_samples_leaf=5,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(
        x,
        y,
    )

    return model


def save_model(
    model,
    development,
):
    """
    Save trained model and model metadata.
    """

    MODEL_DIRECTORY.mkdir(
        exist_ok=True
    )

    model_path = (
        MODEL_DIRECTORY
        / "navigation_risk_random_forest.joblib"
    )

    joblib.dump(
        model,
        model_path,
    )

    metadata = {
        "model_type": "RandomForestRegressor",

        "features": FEATURES,

        "target": TARGET,

        "training_samples": len(
            development
        ),

        "training_vessels": int(
            development[
                "vessel_id"
            ].nunique()
        ),

        "hyperparameters": {
            "n_estimators": 150,
            "max_depth": 12,
            "min_samples_leaf": 5,
            "random_state": 42,
        },

        "important_note": (
            "Predicts simulated digital-twin risk. "
            "Not clinically validated."
        ),
    }

    metadata_path = (
        MODEL_DIRECTORY
        / "navigation_risk_model_metadata.json"
    )

    with open(
        metadata_path,
        "w",
    ) as file:

        json.dump(
            metadata,
            file,
            indent=4,
        )

    print()
    print(
        f"Saved model to: "
        f"{model_path}"
    )

    print(
        f"Saved metadata to: "
        f"{metadata_path}"
    )


def main():

    development = (
        load_development_data()
    )

    print()
    print("Freezing Navigation Risk Model")
    print("------------------------------")

    print(
        f"Development samples: "
        f"{len(development):,}"
    )

    print(
        f"Development vessels: "
        f"{development['vessel_id'].nunique()}"
    )

    print()
    print(
        "Final test dataset has NOT been loaded."
    )

    model = train_final_model(
        development
    )

    save_model(
        model,
        development,
    )


if __name__ == "__main__":
    main()