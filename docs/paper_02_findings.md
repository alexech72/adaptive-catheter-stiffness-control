# Paper 02 Findings

## Paper

**Title:** Numerical Methodology to Evaluate Trackability and Pushability of PTCA Balloon Catheter

**Authors:** Martin L. Sirivella, Ganesh B. Rahinj, Harshit S. Chauhan,
Menta V. Satyanarayana, and Laxminarayanan Ramanan

**Year:** 2023

**Journal:** Cardiovascular Engineering and Technology

**DOI:** 10.1007/s13239-022-00653-z

## Why This Paper Matters

This study develops a numerical model for catheter navigation through
coronary vessel geometries.

It is relevant to this project because it demonstrates that catheter
navigation can be studied computationally and identifies several
engineering variables that influence catheter deliverability.

The paper focuses on two important catheter-navigation characteristics:

- Trackability
- Pushability

## Objective

The objective of the study was to develop a numerical model for analyzing
PTCA balloon catheter navigation through coronary vessels.

## Important Navigation Concepts

### Trackability

Trackability describes the ability of a catheter system to follow a
vascular pathway during advancement.

### Pushability

Pushability describes the ability of an applied proximal force to produce
forward advancement of the catheter system.

These characteristics are important when evaluating catheter
deliverability.

## Factors Affecting Navigation

The study identifies several factors that influence trackability and
pushability:

- Vessel tortuosity
- Contact interactions
- Catheter design
- Guidewire-catheter interaction
- Friction

These factors support the idea that catheter navigation performance
depends on both device properties and the surrounding pathway.

## Computational Approach

The researchers developed a finite-element-analysis model to evaluate
catheter trackability and pushability.

Two different vessel geometries were evaluated.

Interactions among the catheter, guidewire, and vessel were included in
the analysis.

The numerical results were compared with in-vitro experimental data.

## Important Findings

The study found that contact interactions and the coefficient of friction
between the guidewire and catheter were important for obtaining numerical
results comparable with experimental measurements.

The researchers also performed a parametric study investigating catheter
shaft dimensions.

Changes in distal and proximal shaft diameter affected simulated
trackability and pushability.

## Relevance to Adaptive-Stiffness Project

This paper supports several important design decisions for the digital
twin.

### Vessel Geometry Must Matter

Navigation behavior should change as vessel geometry becomes more
tortuous or curved.

A model in which catheter performance is independent of geometry would
not represent the behavior described in the literature.

### Friction Must Be Represented

Contact and friction between components affect catheter navigation.

The first version of this project should therefore include a simplified
friction parameter.

### Device Mechanical Properties Must Matter

Changes in catheter design parameters can influence trackability and
pushability.

This supports representing catheter mechanical properties as adjustable
parameters in the digital twin.

### Computational Testing Is Appropriate

The study demonstrates that numerical modeling can be used to investigate
catheter navigation and compare design parameters.

This supports the use of a digital-twin approach for the current project.

## Initial Engineering Assumptions

### EA-005 — Vessel Tortuosity

Increasing vessel tortuosity or curvature should influence catheter
navigation resistance and trackability.

**Basis:** Vessel tortuosity was identified as a factor affecting PTCA
catheter navigation.

### EA-006 — Friction

Catheter navigation force should depend in part on friction and contact
between components.

**Basis:** Guidewire-catheter friction and contact interaction were
important parameters in the numerical model.

### EA-007 — Device Design

Catheter mechanical and geometric properties should influence simulated
pushability and trackability.

**Basis:** Parametric changes to catheter shaft dimensions produced
changes in simulated navigation performance.

### EA-008 — Geometry-Specific Performance

A catheter design should not necessarily perform identically across
different vessel geometries.

**Basis:** The study evaluated navigation using multiple vessel
geometries and identified vessel tortuosity as an important navigation
factor.

## What This Paper Does NOT Yet Tell Us

Based on the currently accessible information, this paper does not provide
enough detail for this project to directly reproduce its finite-element
model.

We have not yet established:

- A mathematical equation relating curvature to pushing force
- A mathematical equation relating stiffness to trackability
- Exact friction coefficients appropriate for our model
- A quantitative buckling threshold
- A quantitative guidewire kickback model

These values should not be inferred from this paper without additional
literature or clearly stated modeling assumptions.

## Takeaway for Project Development

The digital twin should eventually represent at least four interacting
categories:

1. Vessel geometry
2. Catheter mechanical properties
3. Friction/contact
4. Catheter advancement behavior

The next literature-review step should investigate variable-stiffness
catheter systems to determine when increased versus decreased stiffness
is mechanically beneficial.
