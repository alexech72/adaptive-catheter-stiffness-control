# V1 Digital Twin Model Specification

## 1. Purpose

This document defines the minimum computational model required for V1 of
the Adaptive Catheter Stiffness Control project.

V1 is intended to reproduce qualitative engineering relationships observed
in the literature without claiming to be a validated clinical or
finite-element model.

The primary goal is to create a controlled simulation environment in which
fixed and adaptive catheter stiffness strategies can be compared.


# 2. Modeling Philosophy

The V1 model will be a reduced-order, two-dimensional simulation.

It will prioritize:

- Interpretability
- Reproducibility
- Engineering plausibility
- Controlled experimentation
- Clear separation between simulated ground truth and sensor feedback

It will not attempt to reproduce complete catheter mechanics or patient anatomy.


# 3. Primary Simulation State

At every simulation time step, the digital twin will maintain the following
internal state variables.

## Position

`s`

Current catheter-tip position along the vessel centerline.

## Advancement Velocity

`v`

Current forward catheter advancement velocity.

## Vessel Curvature

`kappa`

Local curvature of the vessel at the catheter tip.

## Catheter Stiffness

`S`

Current distal catheter stiffness command.

For initial development:

    0.0 = minimum stiffness
    1.0 = maximum stiffness

A later model may map normalized stiffness to physical bending stiffness EI.

## Friction

`mu`

Simplified coefficient representing catheter/guidewire/vessel contact
resistance.

## Proximal Pushing Force

`F_push`

Simulated pushing force required to advance the catheter.

V1 may initially express this as a normalized force value rather than
Newtons until the model is calibrated against experimental literature.

## Guidewire Kickback

`x_kickback`

Simulated displacement of the guidewire caused by difficult catheter
advancement.

## Buckling State

`buckled`

Boolean or risk value indicating whether ineffective force transmission
or a simulated buckling condition has occurred.


# 4. Vessel Geometry

The vascular pathway will be represented as a two-dimensional centerline.

The vessel will be defined using ordered coordinates:

    x(s), y(s)

where `s` represents distance along the pathway.

Initial vessel geometries will include:

1. Straight pathway
2. Moderate single curve
3. Severe single curve
4. Multiple-curve tortuous pathway
5. Randomly generated tortuous pathway

Local curvature will be calculated from the vessel centerline.

For a two-dimensional curve:

    kappa =
    |x' y'' - y' x''| /
    (x'^2 + y'^2)^(3/2)

Higher `kappa` represents a sharper local bend.


# 5. Catheter Stiffness Representation

For V1, stiffness will initially be represented using a normalized value:

    0 <= S <= 1

The software architecture shall allow this variable to later be replaced
with physical bending stiffness:

    B = EI

where:

- E = effective elastic modulus
- I = area moment of inertia
- EI = flexural rigidity

The purpose of V1 is to investigate stiffness selection rather than to
accurately reproduce the construction of a specific commercial catheter.


# 6. Expected Mechanical Relationships

The simulation shall enforce the following qualitative relationships.

## MR-001 — Curvature

Increasing vessel curvature shall increase navigation difficulty.

## MR-002 — Friction

Increasing friction shall increase resistance to catheter advancement.

## MR-003 — High Stiffness in Curves

Increasing catheter stiffness in highly curved regions shall increase the
mechanical penalty associated with following the pathway.

## MR-004 — Low Stiffness and Pushability

Very low catheter stiffness shall reduce the efficiency with which
proximal pushing produces distal advancement.

## MR-005 — Mechanical Support

Increasing stiffness shall improve resistance to simulated buckling under
appropriate conditions.

## MR-006 — Force and Advancement

Navigation difficulty may be represented by a state in which proximal
pushing force increases while forward advancement velocity decreases.

## MR-007 — Kickback

Guidewire kickback shall increase under conditions of high navigation
resistance and poor forward advancement.


# 7. V1 Resistance Model

Rather than immediately claiming a clinically accurate force equation,
V1 will calculate an intermediate quantity:

    Navigation Resistance Score, R

R will depend on:

    vessel curvature
    friction
    catheter stiffness
    insertion state

Conceptually:

    R = f(kappa, mu, S, navigation state)

The exact mathematical relationship will be selected during implementation
and documented as a modeling assumption.

The relationship must satisfy controlled unit tests.

For example:

    Increasing friction while holding all other variables constant
    must increase R.

    Increasing curvature while holding all other variables constant
    must increase R.

    Stiffness shall have different effects depending on curvature.


# 8. Pushability Model

The model shall represent the ability of proximal pushing to produce
distal advancement.

A highly effective state should look like:

    moderate pushing force
    +
    normal forward velocity

A poor pushability state may look like:

    increasing pushing force
    +
    low forward velocity

This relationship will later be used as one of the primary indicators of
developing navigation difficulty.


# 9. Buckling Model

V1 will initially use a simplified buckling-risk model rather than
claiming to reproduce physical catheter buckling exactly.

Buckling risk shall increase when:

- proximal pushing force increases
- forward advancement decreases
- stiffness is insufficient for the current loading condition

The system will record both:

    buckling_risk

and, when a defined simulation threshold is exceeded:

    buckled = True


# 10. Guidewire Kickback Model

Guidewire kickback will initially be treated as a performance metric.

Kickback shall increase when:

- navigation resistance is high
- pushing force is high
- forward catheter advancement is low

The output will be:

    x_kickback

V1 values may initially be normalized until a defensible physical
calibration is established.


# 11. Virtual Sensor Layer

The controller shall not access the internal simulation state directly.

The virtual sensor layer will expose:

    measured_force
    measured_curvature
    measured_velocity
    current_stiffness

For example:

TRUE SIMULATION STATE

    force = 0.438
    curvature = 0.710
    velocity = 2.35

VIRTUAL SENSOR OUTPUT

    measured_force = 0.451
    measured_curvature = 0.694
    measured_velocity = 2.29

Sensor noise will initially be optional and disabled during basic model
development.


# 12. Controller Boundary

The controller receives:

    measured_force
    measured_curvature
    measured_velocity
    current_stiffness

The controller does NOT receive:

    true friction
    future vessel geometry unless supplied through imaging
    future failure state
    ground-truth buckling label
    true kickback risk

This prevents unrealistic information leakage into the controller.


# 13. Controller Output

The controller shall produce one primary command:

    desired_stiffness

where:

    0 <= desired_stiffness <= 1

Example:

INPUT

    measured_force = high
    measured_curvature = high
    measured_velocity = decreasing
    current_stiffness = 0.75

OUTPUT

    desired_stiffness = 0.50


# 14. Initial Experimental Comparison

The V1 digital twin will eventually compare:

## Fixed Flexible

    S = 0.25

## Fixed Medium

    S = 0.50

## Fixed Stiff

    S = 0.75

## Rule-Based Adaptive

    S changes using predefined engineering rules.

## AI-Assisted Adaptive

    Navigation risk is estimated using machine learning and passed to a
    deterministic stiffness controller.


# 15. Primary Outputs

Every simulation trial shall produce:

- Navigation success
- Peak pushing force
- Mean pushing force
- Navigation time
- Buckling events
- Maximum guidewire kickback
- Stiffness history
- Force history
- Curvature history
- Velocity history


# 16. Model Validation Strategy

Before adaptive control or AI is implemented, the mechanical simulation
will undergo basic behavior testing.

The model should demonstrate:

### Test A

Same catheter + increasing curvature
→ increasing navigation resistance

### Test B

Same catheter + increasing friction
→ increasing navigation resistance

### Test C

Low stiffness + low curvature
→ acceptable trackability but reduced pushability

### Test D

High stiffness + low curvature
→ improved pushability

### Test E

High stiffness + severe curvature
→ increased curvature-related resistance

### Test F

High pushing force + reduced advancement
→ increased buckling/kickback risk

If the simulation cannot reproduce these intended qualitative behaviors,
adaptive-control development will not proceed.


# 17. Important Modeling Limitation

Relationships implemented in V1 will be simplified engineering models.

Any relationship not directly derived from published experimental data
will be explicitly labeled as a modeling assumption.

Normalized outputs shall not be presented as clinical measurements.

The model may later be calibrated using published experimental data.


# 18. Development Order

The digital twin will be implemented in the following order:

1. Vessel geometry generator
2. Curvature calculation
3. Catheter state representation
4. Resistance model
5. Advancement model
6. Virtual force measurement
7. Buckling-risk model
8. Guidewire-kickback model
9. Virtual sensor layer
10. Fixed-stiffness experiments
11. Rule-based controller
12. Machine-learning risk estimator
13. AI-assisted controller
