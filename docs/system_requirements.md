# System Requirements

## 1. Purpose

This document defines the initial engineering requirements for the
Adaptive Catheter Stiffness Control digital-twin project.

The requirements are derived from the project problem statement and the
engineering findings identified during the initial literature review.

The system is intended to investigate whether measurable navigation
feedback can be used to dynamically select catheter stiffness during
simulated navigation through tortuous vascular pathways.

This is an educational computational engineering study and is not a
validated clinical model or medical device.


# 2. User Needs

## UN-001 — Controlled Advancement

The operator needs a catheter system capable of maintaining controlled
advancement through varying vascular geometries.

## UN-002 — Reduced Navigation Difficulty

The operator needs the catheter system to minimize mechanical conditions
associated with difficult advancement, including excessive pushing force,
buckling, and guidewire kickback.

## UN-003 — Adaptive Mechanical Behavior

The operator needs the catheter system to accommodate different mechanical
requirements as vascular geometry changes during navigation.

## UN-004 — Interpretable Feedback

The operator or engineer needs measurable information describing catheter
navigation performance and the reason for stiffness-control decisions.


# 3. System-Level Requirements

## SYS-001 — Vessel Simulation

The system shall simulate catheter navigation through two-dimensional
vascular pathways with variable curvature and tortuosity.

## SYS-002 — Catheter Representation

The system shall contain a simplified computational representation of a
catheter with adjustable distal bending stiffness.

## SYS-003 — Navigation Simulation

The system shall simulate progressive catheter advancement through a
vascular pathway over discrete time steps.

## SYS-004 — Variable Stiffness

The system shall allow catheter stiffness to change during navigation.

## SYS-005 — Navigation State

The system shall maintain an internal simulation state containing the
variables necessary to calculate catheter navigation behavior.

## SYS-006 — Repeatable Testing

The system shall allow identical vascular and mechanical test conditions
to be repeated across different stiffness-control strategies.


# 4. Virtual Sensor Requirements

The controller shall not receive perfect knowledge of the simulation.

Instead, a virtual sensing layer shall provide information representing
measurements that could plausibly be obtained in a physical system.

## SENS-001 — Proximal Pushing Force

The system shall generate a simulated measurement of proximal catheter
pushing force during navigation.

**Literature basis:** Proximal pushing force has been experimentally
measured during catheter advancement through tortuous vascular models.

## SENS-002 — Curvature

The system shall provide an estimate of local catheter or vascular
curvature relevant to the current navigation state.

## SENS-003 — Advancement Velocity

The system shall provide a measurement of catheter advancement velocity.

## SENS-004 — Current Stiffness

The control system shall have access to the current commanded catheter
stiffness.

## SENS-005 — Sensor Imperfection

The virtual sensing layer shall support the addition of measurement noise
or uncertainty during robustness testing.


# 5. Hidden Simulation Variables

The following information may exist internally as simulation ground truth
but shall not be directly provided to the adaptive controller:

- Future navigation outcome
- Exact future failure state
- Perfect guidewire kickback prediction
- Exact friction coefficient unless explicitly modeled as measurable
- Perfect distal wall-contact force unless explicitly modeled as measurable
- Ground-truth failure labels

This separation is intended to prevent the controller from using
information that would not realistically be available during navigation.


# 6. Mechanical Model Requirements

## MECH-001 — Stiffness

The catheter model shall include a parameter representing bending
stiffness.

The initial implementation may use normalized stiffness for development,
but the model should be structured so that stiffness can later be
represented using a physical quantity such as flexural rigidity, EI.

## MECH-002 — Curvature Dependence

The mechanical response of the simulated catheter shall depend on vascular
curvature or tortuosity.

## MECH-003 — Friction

The simulation shall include a simplified representation of friction or
contact resistance.

## MECH-004 — Pushability

The simulation shall represent the relationship between proximal loading
and forward catheter advancement.

## MECH-005 — Buckling Behavior

The simulation shall contain a defined condition representing catheter
buckling or ineffective force transmission.

## MECH-006 — Guidewire Kickback

The simulation shall contain a simplified model or performance metric for
guidewire kickback during difficult catheter advancement.


# 7. Controller Requirements

Three control strategies shall be implemented and compared.

## CTRL-001 — Fixed-Stiffness Baseline

The system shall support catheter navigation using a constant stiffness
throughout the entire pathway.

Multiple fixed-stiffness configurations shall be testable.

## CTRL-002 — Rule-Based Adaptive Controller

The system shall support a deterministic controller that adjusts catheter
stiffness according to predefined engineering rules using measurable
navigation feedback.

## CTRL-003 — AI-Assisted Adaptive Controller

The system shall support an adaptive controller incorporating
machine-learning-based navigation-risk estimation.

## CTRL-004 — Bounded Stiffness Commands

All controllers shall be restricted to predefined minimum and maximum
stiffness limits.

## CTRL-005 — Decision Logging

Each adaptive stiffness change shall be recorded along with the navigation
state that caused the decision.


# 8. AI Requirements

## AI-001 — Sensor-Based Inputs

The machine-learning model shall use only information available through
the defined virtual sensing layer.

Initial candidate inputs are:

- Proximal pushing force
- Local curvature
- Advancement velocity
- Current catheter stiffness
- Recent measurement history

## AI-002 — Risk Estimation

The initial AI model shall estimate navigation risk rather than directly
controlling catheter stiffness.

Candidate predicted risks include:

- Buckling risk
- Excessive-force risk
- Guidewire-kickback risk

## AI-003 — Separate Engineering Controller

AI risk predictions shall be passed to a deterministic engineering
controller responsible for selecting the final stiffness command.

## AI-004 — Unseen Test Conditions

The AI model shall be evaluated using vascular geometries or simulation
conditions not included in model training.

## AI-005 — Performance Evaluation

AI performance shall be evaluated using appropriate classification
metrics, including:

- Precision
- Recall
- F1 score
- Confusion matrix

Additional metrics may be added when appropriate.

## AI-006 — Failure Analysis

False-negative risk predictions shall be specifically evaluated because
failure to identify a developing navigation problem may be more important
than unnecessary intervention.


# 9. Navigation Performance Metrics

The simulation shall record the following outcomes for each navigation
trial.

## PERF-001 — Navigation Success

Whether the catheter successfully reaches the defined target.

## PERF-002 — Peak Pushing Force

Maximum simulated proximal pushing force observed during navigation.

## PERF-003 — Mean Pushing Force

Mean simulated pushing force during the navigation trial.

## PERF-004 — Buckling

Occurrence and frequency of simulated buckling events.

## PERF-005 — Guidewire Kickback

Maximum simulated guidewire kickback during navigation.

## PERF-006 — Navigation Time

Time required to successfully reach the target or terminate the trial.

## PERF-007 — Stiffness Adjustments

Number and magnitude of stiffness changes made during navigation.


# 10. Verification Requirements

## VER-001 — Baseline Comparison

Fixed-stiffness, rule-based adaptive, and AI-assisted adaptive strategies
shall be evaluated under identical test conditions.

## VER-002 — Multiple Vessel Geometries

Controller performance shall be evaluated across multiple vascular
geometries representing different levels of curvature and tortuosity.

## VER-003 — Repeated Trials

Simulation experiments shall support repeated trials to quantify
performance variability.

## VER-004 — Robustness Testing

The adaptive system shall be evaluated under simulated measurement
uncertainty.

Candidate conditions include:

- Force-sensor noise
- Curvature-estimation error
- Velocity-measurement error
- Sensor delay

## VER-005 — Failure Conditions

Verification testing shall intentionally include conditions capable of
producing navigation failure.

The system shall not be evaluated only under favorable conditions.


# 11. Initial Acceptance Criteria

Quantitative clinical acceptance thresholds have not yet been established.

Therefore, V1 will initially evaluate performance comparatively rather
than claiming clinically acceptable values.

The primary comparison will determine whether adaptive control improves
navigation metrics relative to fixed-stiffness baselines under identical
simulation conditions.

Examples include:

- Reduced peak pushing force
- Reduced buckling incidence
- Reduced guidewire kickback
- Increased navigation success

Numerical acceptance thresholds will only be introduced when supported by
literature, model calibration, or clearly documented engineering
assumptions.


# 12. Design Constraints

## CON-001

V1 shall use a two-dimensional vascular model.

## CON-002

V1 shall not attempt full finite-element simulation.

## CON-003

V1 shall not model clinical decision-making.

## CON-004

V1 shall not autonomously steer the catheter into vascular branches.

## CON-005

V1 shall focus on stiffness selection rather than development of a
physical variable-stiffness actuator.

## CON-006

All results shall be identified as computational simulation results and
shall not be presented as experimental or clinical findings.


# 13. Initial System Architecture

The intended system architecture is:

    Vessel Geometry
          ↓
    Catheter Mechanical Model
          ↓
    Virtual Sensors
       ├── Proximal Force
       ├── Curvature
       └── Advancement Velocity
          ↓
    Navigation Risk Estimator
          ↓
    Stiffness Controller
          ↓
    Desired Distal Stiffness
          ↓
    Catheter Mechanical Model
          ↺


# 14. Next Development Stage

Before implementation begins, the requirements in this document will be
translated into:

1. Simulation variables
2. Engineering assumptions
3. Mathematical relationships
4. Verification tests
5. Requirements traceability

The next design task is to define the system architecture and determine
the minimum mathematical model required for the V1 digital twin.
