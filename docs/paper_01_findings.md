# Paper 01 Findings

## Paper

**Title:** Microguidewire stiffness for microcatheter and aspiration catheter navigation in tortuous vessels

**Authors:** Kenichi Sakuta, Yoshiki Hanaoka, Mahsa Ghovvati, et al.

**Year:** 2025

**Journal:** Interventional Neuroradiology

## Why This Paper Matters

This study investigates how microguidewire stiffness affects the ability to advance catheters through tortuous neurovascular pathways.

The study is relevant to this project because it provides experimental evidence connecting mechanical stiffness/support with:

- Catheter pushing force
- Guidewire kickback
- Catheter deliverability
- Navigation through tortuous vascular geometry

Importantly, this paper changes **microguidewire stiffness**, not catheter stiffness. Therefore, its results should not be interpreted as direct evidence that increasing catheter stiffness will produce the same effects.

## Objective

The objective of the study was to determine whether microguidewire stiffness influences microcatheter and aspiration catheter deliverability through highly tortuous vascular pathways.

## Experimental Setup

The researchers used two in-vitro silicone vascular models.

### Experiment 1

A 0.021-inch microcatheter was advanced through an acute-angle M2 branch of a middle cerebral artery model.

### Experiment 2

A 0.071-inch aspiration catheter was advanced through a severely tortuous internal carotid artery model.

Microguidewires of similar construction but different stiffness levels were tested.

The catheter was advanced at a controlled rate of **4 mm/s**.

A digital force gauge was used to measure the force required to advance the catheter.

Video recordings were used to determine microguidewire kickback distance.

## Primary Measurements

The two primary performance measurements were:

1. **Maximum catheter pushing force**
2. **Maximum microguidewire kickback distance**

These measurements provide quantitative indicators of how difficult it is to advance a catheter through a tortuous vascular pathway.

## Main Findings

Stiffer microguidewires generally:

- Required lower pushing force during catheter advancement
- Produced less microguidewire kickback
- Provided greater mechanical support during catheter delivery

The results suggest that the mechanical stiffness and support provided by the guidewire can significantly influence catheter deliverability through tortuous vascular anatomy.

## Mechanical Interpretation

The findings demonstrate an important relationship between:

**Mechanical support → catheter advancement → pushing force → guidewire stability**

When insufficient support is present, more proximal pushing force may be required to advance the catheter and greater guidewire kickback may occur.

This suggests that pushing force and distal advancement behavior may contain useful information about the mechanical state of the catheter-guidewire system.

## Relevance to Adaptive-Stiffness Project

This study supports several elements of the proposed adaptive-stiffness catheter simulation.

### Proximal Force as Feedback

Pushing force can be measured from the proximal end of the catheter system and used as an indicator of navigation difficulty.

This means a future adaptive-stiffness system may not require direct force measurement at the catheter tip.

### Advancement Feedback

Force measurements are more useful when interpreted together with catheter advancement.

For example:

- Low force + normal advancement may indicate normal navigation.
- Increasing force + decreasing advancement may indicate increasing resistance.
- High force + little advancement may indicate a potential mechanical problem.

### Guidewire Kickback

Guidewire kickback provides another measurable outcome for evaluating navigation performance.

An adaptive-stiffness controller could therefore be evaluated by determining whether it reduces simulated kickback compared with fixed-stiffness configurations.

## Initial Engineering Assumptions

### EA-001 — Navigation Resistance

An increase in proximal pushing force accompanied by reduced catheter advancement may indicate increasing mechanical resistance during navigation.

**Basis:** The study demonstrates that pushing force can be quantitatively measured during catheter advancement through tortuous anatomy.

### EA-002 — Guidewire Kickback

Guidewire kickback can be used as an outcome measure for catheter navigation stability.

**Basis:** The study directly measured maximum microguidewire kickback during catheter advancement.

### EA-003 — Mechanical Support

The stiffness and mechanical support of the catheter-guidewire system influence catheter deliverability.

**Basis:** Stiffer microguidewires required lower pushing forces and generally reduced guidewire kickback in the tested vascular models.

### EA-004 — Vessel Geometry

Severe vessel tortuosity and acute branching geometries create challenging conditions for catheter advancement.

**Basis:** The experiments specifically evaluated catheter navigation through acute-angle and severely tortuous vascular models.

## Important Limitation

The experimental variable in this study was **microguidewire stiffness**, not catheter stiffness.

Therefore, this study supports the broader relationship between mechanical support and catheter navigation but does not by itself prove that dynamically changing catheter stiffness will improve navigation.

Additional literature specifically studying variable-stiffness catheters will be required before developing the adaptive-stiffness model.

## Takeaway for Project Development

This paper provides support for using the following variables in the digital twin:

**Potential controller inputs**
- Proximal pushing force
- Catheter advancement velocity

**Performance outputs**
- Maximum pushing force
- Guidewire kickback
- Successful catheter advancement

The next literature review step should determine how catheter stiffness, vessel curvature, friction, and trackability can be represented mathematically.
