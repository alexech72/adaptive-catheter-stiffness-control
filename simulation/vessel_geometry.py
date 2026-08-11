"""
Vessel Geometry Module
----------------------

Creates simplified 2D vascular pathways for the adaptive catheter
stiffness-control digital twin.

V1 includes:
1. Straight vessel
2. Moderate curved vessel
3. Tortuous vessel

The module also calculates local vessel curvature.
"""

import numpy as np
import matplotlib.pyplot as plt


def calculate_curvature(x, y):
    """
    Calculate local curvature along a 2D vessel centerline.

    Parameters
    ----------
    x : numpy.ndarray
        X-coordinates of the vessel centerline.
    y : numpy.ndarray
        Y-coordinates of the vessel centerline.

    Returns
    -------
    numpy.ndarray
        Curvature at every point along the vessel.
    """

    # First derivatives
    dx = np.gradient(x)
    dy = np.gradient(y)

    # Second derivatives
    ddx = np.gradient(dx)
    ddy = np.gradient(dy)

    # 2D curvature equation
    numerator = np.abs(dx * ddy - dy * ddx)
    denominator = (dx**2 + dy**2) ** 1.5

    # Prevent division by zero
    curvature = np.divide(
        numerator,
        denominator,
        out=np.zeros_like(numerator),
        where=denominator > 1e-12
    )

    return curvature


def generate_straight_vessel(length=100, n_points=500):
    """
    Generate a straight vessel centerline.
    """

    x = np.linspace(0, length, n_points)
    y = np.zeros(n_points)

    return x, y


def generate_curved_vessel(length=100, amplitude=12, n_points=500):
    """
    Generate a vessel containing one smooth curve.
    """

    x = np.linspace(0, length, n_points)

    # One smooth sinusoidal bend
    y = amplitude * np.sin(np.pi * x / length)

    return x, y


def generate_tortuous_vessel(length=100, amplitude=10, n_points=500):
    """
    Generate a more tortuous vessel containing multiple bends.
    """

    x = np.linspace(0, length, n_points)

    # Combine two sinusoidal components to create variable curvature
    y = (
        amplitude * np.sin(2 * np.pi * x / length)
        + 0.4 * amplitude * np.sin(5 * np.pi * x / length)
    )

    return x, y
def generate_random_tortuous_vessel(
    length=100,
    n_points=500,
    seed=None,
    difficulty="moderate",
):
    """
    Generate a randomized 2D synthetic vessel centerline.

    Three geometric difficulty levels are supported:

    easy:
        Broad, gradual bends with relatively low curvature.

    moderate:
        Multiple bends with intermediate curvature and tortuosity.

    severe:
        More frequent bends, tighter local changes in direction,
        and higher expected curvature.

    The geometry is intended for computational testing and does not
    represent patient-specific anatomy.

    Parameters
    ----------
    length : float
        Longitudinal vessel length.

    n_points : int
        Number of sampled centerline points.

    seed : int or None
        Random seed for reproducible geometry generation.

    difficulty : str
        "easy", "moderate", or "severe".

    Returns
    -------
    x : numpy.ndarray
        Longitudinal coordinates.

    y : numpy.ndarray
        Lateral coordinates.
    """

    rng = np.random.default_rng(seed)

    x = np.linspace(
        0,
        length,
        n_points,
    )

    # Normalized position from 0 to 1.
    t = x / length

    y = np.zeros_like(x)

    # ---------------------------------------------------------
    # Difficulty-dependent geometry settings
    # ---------------------------------------------------------

    if difficulty == "easy":

        n_components = rng.integers(1, 3)

        amplitude_range = (1.5, 4.0)
        frequency_range = (0.4, 1.2)

        n_local_bends = rng.integers(0, 2)

        local_amplitude_range = (1.0, 2.5)
        local_width_range = (0.12, 0.20)

    elif difficulty == "moderate":

        n_components = rng.integers(2, 5)

        amplitude_range = (2.5, 6.0)
        frequency_range = (0.8, 1.8)

        n_local_bends = rng.integers(1, 3)

        local_amplitude_range = (1.5, 4.0)
        local_width_range = (0.08, 0.15)

    elif difficulty == "severe":

        n_components = rng.integers(3, 6)

        amplitude_range = (3.5, 8.0)
        frequency_range = (1.2, 2.4)

        n_local_bends = rng.integers(2, 5)

        local_amplitude_range = (2.5, 6.0)
        local_width_range = (0.05, 0.10)

    else:

        raise ValueError(
            "difficulty must be 'easy', 'moderate', or 'severe'"
        )

    # ---------------------------------------------------------
    # Broad vessel curvature
    # ---------------------------------------------------------

    for _ in range(n_components):

        amplitude = rng.uniform(
            *amplitude_range
        )

        frequency = rng.uniform(
            *frequency_range
        )

        phase = rng.uniform(
            0,
            2 * np.pi
        )

        y += (
            amplitude
            * np.sin(
                2
                * np.pi
                * frequency
                * t
                + phase
            )
        )

    # ---------------------------------------------------------
    # Localized bends
    #
    # These create tighter S-shaped regions instead of making
    # every vessel look like only a large sine wave.
    # ---------------------------------------------------------

    for _ in range(n_local_bends):

        center = rng.uniform(
            0.15,
            0.85
        )

        width = rng.uniform(
            *local_width_range
        )

        amplitude = rng.uniform(
            *local_amplitude_range
        )

        direction = rng.choice(
            [-1.0, 1.0]
        )

        z = (
            (t - center)
            / width
        )

        local_bend = (
            direction
            * amplitude
            * z
            * np.exp(
                -0.5 * z**2
            )
        )

        y += local_bend

    # Shift entire vessel so that it begins at y = 0.
    y = y - y[0]

    return x, y

def generate_circular_arc(radius=20, angle_degrees=120, n_points=500):
    """
    Generate a circular vessel arc with analytically known curvature.

    For a circle:
        curvature = 1 / radius

    This geometry is primarily used to verify the numerical
    curvature calculation.
    """

    theta = np.linspace(
        0,
        np.deg2rad(angle_degrees),
        n_points
    )

    x = radius * np.cos(theta)
    y = radius * np.sin(theta)

    return x, y

def plot_vessel(x, y, title):
    """
    Plot a vessel centerline.
    """

    plt.figure(figsize=(9, 4))
    plt.plot(x, y, linewidth=2)

    plt.title(title)
    plt.xlabel("Longitudinal Position")
    plt.ylabel("Lateral Position")

    plt.axis("equal")
    plt.grid(True)
    plt.tight_layout()

    plt.show()


def main():

    # Generate vessel geometries
    straight_x, straight_y = generate_straight_vessel()
    curved_x, curved_y = generate_curved_vessel()
    tortuous_x, tortuous_y = generate_tortuous_vessel()
    circle_x, circle_y = generate_circular_arc(radius=20)
    # Calculate curvature
    straight_curvature = calculate_curvature(
        straight_x,
        straight_y
    )

    curved_curvature = calculate_curvature(
        curved_x,
        curved_y
    )

    tortuous_curvature = calculate_curvature(
        tortuous_x,
        tortuous_y
    )

    circle_curvature = calculate_curvature(
        circle_x,
        circle_y
    )
    # Print basic verification information
    print("Vessel Geometry Verification")
    print("----------------------------")

    print(
        f"Straight vessel max curvature: "
        f"{straight_curvature.max():.6f}"
    )

    print(
        f"Curved vessel max curvature: "
        f"{curved_curvature.max():.6f}"
    )

    print(
        f"Tortuous vessel max curvature: "
        f"{tortuous_curvature.max():.6f}"
    )
    # Ignore edge points because numerical differentiation
    # is less accurate at the boundaries
    circle_interior = circle_curvature[10:-10]

    print(
        f"Circular arc expected curvature: "
        f"{1 / 20:.6f}"
    )

    print(
        f"Circular arc calculated curvature: "
        f"{np.mean(circle_interior):.6f}"
    )
    # Visualize vessels
    plot_vessel(
        straight_x,
        straight_y,
        "Straight Vessel"
    )

    plot_vessel(
        curved_x,
        curved_y,
        "Moderately Curved Vessel"
    )

    plot_vessel(
        tortuous_x,
        tortuous_y,
        "Tortuous Vessel"
    )

    plot_vessel(
        circle_x,
        circle_y,
        "Circular Verification Vessel"
    )

if __name__ == "__main__":
    main()