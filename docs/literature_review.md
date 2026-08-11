# Literature Review

## Purpose

The purpose of this literature review is to identify the mechanical principles,
device technologies, and measurable variables needed to develop a simplified
digital-twin model of adaptive catheter stiffness control.

The review focuses on:

1. Catheter and guidewire stiffness
2. Pushability and trackability
3. Vascular tortuosity
4. Insertion/pushing force
5. Guidewire kickback
6. Buckling
7. Variable-stiffness catheter technologies
8. Feedback and closed-loop control

9. ## Paper 1: Microguidewire Stiffness and Catheter Delivery

### Questions
- How is pushing force measured?
- How is guidewire kickback measured?
- How does guidewire stiffness affect catheter advancement?
- Does greater stiffness always improve navigation?
- What experimental variables are controlled?
- What outcomes are used to define better or worse performance?

### Relevance to Project
This paper provides experimental evidence for the relationship between
guidewire stiffness, pushing force, kickback, and catheter navigation through
tortuous vascular geometry.

## Paper 2: Numerical Modeling of Catheter Navigation

### Questions
- How are pushability and trackability defined?
- Which physical variables are included in the numerical model?
- How is friction represented?
- How is vessel curvature represented?
- Which catheter dimensions significantly affect navigation?
- How was the simulation compared with physical testing?

### Relevance to Project
This paper will help guide the development of the simplified catheter mechanics
model and identify which variables should be included in the digital twin.

## Paper 3: Variable-Stiffness Guidewire

### Questions
- How is stiffness physically changed?
- What parameter represents stiffness?
- How is desired stiffness controlled?
- What feedback information is used?
- Why are different stiffness levels useful in different anatomies?
- What limitations does the current controller have?

### Relevance to Project
This paper demonstrates that controllable stiffness and closed-loop feedback
are technically feasible in small endovascular devices.

## Paper 4: Programmable-Stiffness Microcatheter

### Questions
- When is high stiffness beneficial?
- When is low stiffness beneficial?
- What failures occur when stiffness is inappropriate?
- How many stiffness states are used?
- How quickly can stiffness be changed?
- How is the catheter observed during navigation?

### Relevance to Project
This paper provides direct evidence that optimal catheter stiffness can change
during a procedure, depending on the current mechanical task.


# Preliminary Engineering Findings

The literature suggests the following relationships should be investigated in
the digital twin:

1. Increased stiffness can improve structural support and resistance to buckling.
2. Excessive stiffness can reduce flexibility and make navigation through
   highly curved regions more difficult.
3. Lower stiffness can improve steering and trackability through curved regions.
4. Insufficient stiffness can reduce pushability and increase buckling risk.
5. Vessel tortuosity and friction influence catheter advancement forces.
6. Pushing force and guidewire displacement are measurable indicators of
   navigation performance.
7. Variable-stiffness endovascular devices are technically feasible.
8. Closed-loop stiffness control using sensing or imaging feedback is technically
   feasible.

These relationships will be translated into engineering assumptions and
mathematical models in the next phase.
