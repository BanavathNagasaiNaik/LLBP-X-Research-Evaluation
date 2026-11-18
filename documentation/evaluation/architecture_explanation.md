
# LLBP-X Architecture — Evaluation Preparation

## 1. Overview

LLBP-X is a branch prediction approach evaluated in
"The Last-Level Branch Predictor Revisited" (HPCA 2026).

It builds on a TAGE-SC-L prediction system and adds
a last-level prediction mechanism designed to help
with difficult-to-predict branches.

The architecture includes several interacting
components:

1. TAGE-SC-L base predictor
2. Context tracking
3. Pattern storage
4. Pattern buffer
5. Adaptive prediction logic

The objective is to improve prediction accuracy
by exploiting additional execution-context
information.

## 2. TAGE-SC-L Base Predictor

TAGE-SC-L combines three prediction mechanisms:

- TAGE: Tagged Geometric History Length predictor
- SC: Statistical Corrector
- L: Loop predictor

TAGE uses branch history information at
different history lengths.

The statistical corrector helps refine predictions.

The loop predictor helps recognize branches
associated with repetitive loop behavior.

Together, these mechanisms provide a strong
baseline for evaluating LLBP and LLBP-X.

## 3. Why an Additional Last-Level Predictor?

Some branches remain difficult to predict
using conventional history-based mechanisms.

A last-level predictor provides an additional
source of prediction information for such branches.

LLBP-X uses context-related information and
stored patterns to supplement the base predictor.

The aim is to reduce mispredictions when the
additional information is useful.


## 4. Context Tracking

Context tracking is an important part of the
last-level branch prediction mechanism.

A context represents information associated
with previous branch execution behavior.

The predictor uses context-related information
to distinguish situations in which a branch
may exhibit different outcomes.

In our simulator configuration, context-related
structures are maintained alongside the
TAGE-SC-L base predictor.

The purpose of context tracking is to help
identify useful relationships between
execution history and branch outcomes.

### Evaluation Question

Q: Why is context tracking useful?

A: The same branch may behave differently
under different execution contexts.
Tracking context can provide additional
information for predicting such branches.

## 5. Pattern Storage

Pattern storage maintains prediction-related
information associated with execution contexts.

The last-level predictor can use this
information when generating predictions
for difficult branches.

Our LLBP-X configuration includes
pattern-related storage structures.

The simulator also includes a pattern buffer,
which we will discuss in the next section.

Pattern storage supports reuse of previously
observed prediction information.

### Evaluation Question

Q: What is the difference between context
tracking and pattern storage?

A: Context tracking identifies or maintains
information about execution situations,
whereas pattern storage maintains
prediction-related information associated
with those situations.


## 6. Pattern Buffer

The pattern buffer is part of the last-level
branch prediction mechanism.

It provides a limited-capacity structure
for holding prediction-related pattern information.

In our simulator configuration, the pattern
buffer has the following parameters:

- Pattern buffer size: 64 entries
- Pattern buffer associativity: 4

The pattern buffer is separate from the
larger pattern and context storage structures.

Its role is to support access to
prediction-related information used by
the last-level predictor.

### Evaluation Question

Q: Why is a pattern buffer needed?

A: A pattern buffer provides a smaller
storage structure for pattern information
used by the last-level predictor.

The exact lookup and replacement behavior
should be explained using the simulator
implementation rather than assumed.

## 7. Adaptive Prediction Logic

An important difference between LLBP
and LLBP-X is the adaptive configuration
of the last-level prediction mechanism.

In the configurations studied in this
project, LLBP uses a fixed W value of 8.

LLBP-X uses adaptive W settings,
with values of 2 and 64.

The LLBP-X configuration also includes
an adaptation threshold.

We evaluated two threshold settings:

- Default LLBP-X: threshold 7
- Modified LLBP-X: threshold 9

The purpose of our threshold experiment
was to determine whether changing this
parameter affects prediction accuracy.

In our three zero-latency workloads,
threshold 9 produced slightly higher
ROI MPKI than the default threshold.

### Evaluation Question

Q: What did your adaptation-threshold
experiment demonstrate?

A: Increasing the threshold from 7 to 9
did not improve prediction accuracy on
Kafka, TPCC, or NodeApp.

This result is limited to the three
evaluated workloads and two threshold
configurations.

### Important Technical Note

The exact meaning of W, the threshold
comparison, and the conditions that
trigger adaptation must be explained
from the implementation code.

Do not describe W as a specific hardware
quantity without verifying its definition.


## 8. Interaction Between Architecture Components

LLBP-X combines a TAGE-SC-L base predictor
with additional last-level prediction structures.

The main components are:

1. TAGE-SC-L base predictor
2. Context tracking
3. Pattern storage
4. Pattern buffer
5. Adaptive prediction logic

### Conceptual Prediction Sequence

Step 1: A branch instruction is encountered.

The predictor receives the branch address
and relevant branch history information.

Step 2: The base predictor is consulted.

TAGE-SC-L generates prediction information
using its history-based mechanisms.

Step 3: Last-level prediction information
is considered.

The last-level mechanism uses context
information and available pattern data.

Step 4: Prediction selection occurs.

The predictor combines or selects
prediction information according to
its implemented control logic.

Step 5: A final branch prediction is produced.

The processor or simulator uses this
prediction to select the speculative path.

### Conceptual Update Sequence

Step 6: The actual branch outcome becomes known.

The simulator determines whether
the prediction was correct.

Step 7: Prediction structures are updated.

The base predictor and relevant last-level
structures update their state according
to their implemented training rules.

Step 8: Adaptive state may change.

LLBP-X may adjust its configuration
according to the conditions implemented
in its adaptation logic.

### Simplified Conceptual Flow

Branch address and history
    |
    v
TAGE-SC-L base prediction
    |
    v
Last-level context and pattern information
    |
    v
Prediction selection logic
    |
    v
Final prediction
    |
    v
Actual branch outcome
    |
    v
Predictor state updates and adaptation

### Evaluation Question

Q: How does LLBP-X differ from a
standalone TAGE-SC-L predictor?

A: LLBP-X supplements the TAGE-SC-L
prediction system with additional
context- and pattern-related prediction
structures and adaptive behavior.

### Important Clarification

This is a conceptual explanation,
not an exact source-code call graph.

The actual order of lookups, prediction
selection, updates, and adaptation must
be verified against the simulator code.

The diagram does not imply that every
branch accesses every last-level structure.
