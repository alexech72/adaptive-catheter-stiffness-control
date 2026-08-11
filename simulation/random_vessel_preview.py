"""
Random Vessel Difficulty Preview
--------------------------------

Visualizes synthetic vessels across easy, moderate, and severe
geometric difficulty levels before dataset generation.
"""

import matplotlib.pyplot as plt

from simulation.vessel_geometry import (
    generate_random_tortuous_vessel,
    calculate_curvature,
)


def main():

    cases = [
        ("Easy", "easy", 42),
        ("Easy", "easy", 43),

        ("Moderate", "moderate", 42),
        ("Moderate", "moderate", 43),

        ("Severe", "severe", 42),
        ("Severe", "severe", 43),
    ]

    fig, axes = plt.subplots(
        3,
        2,
        figsize=(12, 10),
        constrained_layout=True,
    )

    axes = axes.flatten()

    for axis, (label, difficulty, seed) in zip(
        axes,
        cases,
    ):

        x, y = generate_random_tortuous_vessel(
            seed=seed,
            difficulty=difficulty,
        )

        curvature = calculate_curvature(
            x,
            y,
        )

        axis.plot(
            x,
            y,
            linewidth=2,
        )

        axis.set_title(
            f"{label} | Seed {seed}\n"
            f"Max Curvature = {curvature.max():.4f}"
        )

        axis.set_xlabel(
            "Longitudinal Position"
        )

        axis.set_ylabel(
            "Lateral Position"
        )

        axis.grid(True)

    plt.show()


if __name__ == "__main__":
    main()