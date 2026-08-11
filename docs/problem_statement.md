# Problem Statement

## Background

Microcatheters navigating tortuous vascular pathways must balance two competing mechanical requirements: sufficient stiffness for pushability and sufficient flexibility for trackability.

A catheter that is too flexible may buckle or fail to efficiently transmit proximal pushing force. A catheter that is too stiff may have difficulty following highly curved vessel geometries, increasing resistance during advancement and potentially contributing to guidewire displacement or excessive mechanical interaction.

Because vascular geometry and mechanical resistance vary throughout catheter advancement, a single fixed stiffness may not provide optimal performance across the entire navigation pathway.

## Problem Statement

This project investigates whether a closed-loop adaptive-stiffness control system can use realistically measurable catheter-navigation feedback to dynamically adjust simulated distal catheter stiffness and improve navigation through tortuous vascular pathways.

## User Need

**UN-001:** The operator needs a catheter system capable of maintaining controlled advancement through varying vascular geometries while minimizing excessive pushing force, buckling, and loss of guidewire position.

## Engineering Question

Can catheter stiffness be dynamically adjusted using proximal pushing force, catheter curvature, and advancement velocity to improve navigation performance compared with a fixed-stiffness catheter?

## Hypothesis

An adaptive-stiffness catheter controller using real-time mechanical feedback will improve simulated navigation performance relative to fixed-stiffness catheter configurations by reducing excessive pushing force, buckling, and guidewire kickback.

## Initial System Inputs

The first version of the system will use three simulated feedback measurements:

1. Proximal pushing force
2. Catheter/local vessel curvature
3. Catheter advancement velocity

The controller will also know the catheter's current stiffness setting.

## Primary Performance Metrics

The system will be evaluated using:

- Navigation success rate
- Maximum pushing force
- Buckling incidence
- Maximum guidewire kickback
- Navigation time

## Systems to Compare

Three catheter-control approaches will eventually be evaluated:

1. Fixed stiffness
2. Rule-based adaptive stiffness
3. AI-assisted adaptive stiffness

## V1 Scope

The initial version of this project will include:

- Two-dimensional vessel geometry
- Simplified catheter mechanics
- Variable distal catheter stiffness
- Simulated sensor feedback
- Fixed-stiffness baseline testing
- Rule-based adaptive control
- Machine-learning-based risk estimation
- Closed-loop stiffness control
- Verification and robustness testing

## Out of Scope for V1

The first version will not attempt to model:

- Real patient anatomy
- Clinical decision-making
- Blood-flow fluid dynamics
- Full finite-element catheter mechanics
- Autonomous catheter steering
- Actual medical-device hardware
- Human or animal testing

## Project Limitation

This project is an educational computational biomedical engineering R&D study. It is intended to investigate engineering concepts related to adaptive catheter stiffness and control and is not a validated clinical model or medical device.
