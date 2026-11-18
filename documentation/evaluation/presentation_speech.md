
# LLBP-X Research Project — Presentation Speech

## Slide 1: Title Slide

Good morning, respected faculty members and evaluators.

Today, I am presenting my research project titled
"Reproduction and Experimental Evaluation of LLBP-X."

This project is based on the research paper
"The Last-Level Branch Predictor Revisited,"
published at HPCA 2026.

The main objective of this project is to study
advanced branch prediction techniques and evaluate
the effectiveness of LLBP-X using simulation experiments.

We implemented and evaluated multiple predictor
configurations and compared their prediction accuracy.

## Slide 2: Introduction

Modern processors use pipelining to execute multiple
instructions efficiently.

However, conditional branch instructions introduce
uncertainty because the processor must determine
which instruction to execute next.

To avoid waiting for the branch outcome, processors
use branch predictors.

When a prediction is incorrect, the processor may
need to discard speculative work and restart execution
from the correct path.

This can reduce processor performance.

Our project focuses on improving branch prediction
accuracy using the LLBP-X approach.

## Slide 3: Problem Statement

Although modern branch predictors are highly
effective, some branches remain difficult to predict.

These branches may depend on complex execution
histories or long-range correlations.

Conventional prediction mechanisms may not capture
all such relationships effectively.

The research problem is to determine whether
LLBP-X can reduce branch mispredictions compared
with established prediction approaches.

We evaluate this by comparing LLBP-X with
TAGE-SC-L and LLBP using branch prediction
simulation results.

The main evaluation metric is MPKI,
which stands for Mispredictions Per Kilo Instructions.


## Slide 4: Research Objectives

The primary objective of this project is to
reproduce and experimentally evaluate the
LLBP-X branch prediction approach.

We have four major objectives.

First, understand the architecture and working
principles of TAGE-SC-L, LLBP, and LLBP-X.

Second, build and execute the publicly available
LLBP-X simulator.

Third, compare prediction accuracy using
Region of Interest MPKI.

Finally, investigate how changing the adaptation
threshold affects prediction accuracy.

These objectives help us evaluate the proposed
approach and understand its practical behavior.

## Slide 5: Literature Review

Our study focuses on three branch prediction
approaches.

The first is TAGE-SC-L, which combines
tagged geometric history prediction,
statistical correction, and loop prediction.

The second is LLBP, or Last-Level Branch Predictor,
which extends the prediction system with
additional information for difficult branches.

The third is LLBP-X, which introduces adaptive
behavior into the last-level prediction approach.

Our reference paper is
"The Last-Level Branch Predictor Revisited,"
published at HPCA 2026.

We use these approaches to understand how
advanced prediction mechanisms can improve
prediction accuracy.

## Slide 6: LLBP-X System Architecture

This slide presents the major architectural
components of LLBP-X.

The system uses TAGE-SC-L as its base predictor.

It also maintains context-tracking information
to recognize execution patterns.

Pattern storage preserves prediction-related
information associated with these contexts.

A pattern buffer supports access to the
stored prediction information.

The adaptation mechanism controls how the
last-level prediction configuration responds
to observed branch behavior.

Together, these components support prediction
of branches that may be difficult for the
base predictor alone.

In the next slide, I will explain the
working mechanism step by step.


## Slide 7: LLBP-X Working Mechanism

This slide explains how LLBP-X generates
and updates branch predictions.

First, the predictor receives information
about the current branch and its execution history.

The TAGE-SC-L base predictor generates
an initial prediction.

Next, the last-level prediction mechanism
uses context information and stored patterns
to provide additional prediction information.

LLBP-X uses adaptive configuration logic
to respond to observed branch behavior.

The predictor then produces its final prediction.

After the actual branch outcome becomes known,
the relevant prediction structures are updated.

This process allows the predictor to learn
from previous branch behavior.

## Slide 8: Implementation

For implementation, we used the publicly
available LLBP-X simulator.

The simulator is written in C++ and uses
CMake as its build system.

We compiled and executed the simulator
in an Ubuntu environment using WSL2.

The project includes multiple predictor models,
including TAGE-SC-L, LLBP, and LLBP-X.

We also introduced an experimental
LLBP-X configuration named
llbpx-threshold9.

The default adaptation threshold is 7,
while our experimental configuration uses 9.

This modification allows us to examine
whether changing the adaptation threshold
affects prediction accuracy.

## Slide 9: Experimental Setup

For our experimental evaluation,
we selected three workloads:

Kafka, BenchBase TPCC, and NodeApp.

We performed two sets of experiments.

The first set used zero-latency
predictor configurations.

It included four models across
three workloads, giving 12 simulations.

Each simulation used 100 million
warmup instructions and approximately
100 million measurement instructions.

The second set used timing-aware
predictor configurations.

It included LLBP and LLBP-X across
the same three workloads,
giving six additional simulations.

These runs used 100 million warmup
instructions and approximately
200 million measurement instructions.

We enabled BTB simulation in both sets.

Our primary evaluation metric is
Region of Interest MPKI.

MPKI is calculated as:

MPKI = (Branch Mispredictions /
        Executed Instructions) * 1000

A lower MPKI indicates better
branch prediction accuracy.

We use this metric to compare
the different predictor configurations.


## Slide 10: Zero-Latency ROI MPKI

This slide presents the results of our
zero-latency branch prediction experiments.

We compare four configurations:
TAGE-SC-L, LLBP, LLBP-X, and
our modified LLBP-X with threshold 9.

The graphs show the Region of Interest MPKI
for three workloads.

For Kafka, LLBP achieved an MPKI of 0.32264,
while LLBP-X achieved 0.30452.

For TPCC, LLBP achieved 3.82597,
while LLBP-X achieved 3.72292.

For NodeApp, LLBP achieved 3.38402,
while LLBP-X achieved 3.29396.

Compared with LLBP, LLBP-X reduced MPKI
by approximately 5.62 percent for Kafka,
2.69 percent for TPCC, and
2.66 percent for NodeApp.

The average of these three percentage
reductions is approximately 3.66 percent.

These results show that LLBP-X improved
prediction accuracy on all three
evaluated workloads.

## Slide 11: Adaptation-Threshold Analysis

This slide investigates how changing
the adaptation threshold affects LLBP-X.

The default LLBP-X configuration
uses an adaptation threshold of 7.

We created an additional configuration
with the threshold increased to 9.

For Kafka, the default configuration
achieved an MPKI of 0.30452,
compared with 0.30597 for threshold 9.

For TPCC, the values were
3.72292 and 3.72616, respectively.

For NodeApp, the values were
3.29396 and 3.29845, respectively.

The threshold 9 configuration produced
slightly higher MPKI on all three workloads.

Therefore, in our experiments,
increasing the threshold from 7 to 9
did not improve prediction accuracy.

However, this comparison covers only
two threshold settings and three workloads.

It does not establish that threshold 7
is optimal for every application.

## Slide 12: Timing-Aware ROI MPKI

This slide presents the results of our
timing-aware branch prediction experiments.

We compared LLBP and LLBP-X
using the same three workloads.

For Kafka, LLBP achieved an MPKI
of approximately 0.23602,
while LLBP-X achieved 0.22556.

For TPCC, LLBP achieved 3.33409,
while LLBP-X achieved 3.19576.

For NodeApp, LLBP achieved 3.33664,
while LLBP-X achieved 3.23358.

The corresponding MPKI reductions
were approximately 4.43 percent,
4.15 percent, and 3.09 percent.

The arithmetic mean of the workload
percentage reductions is 3.89 percent.

These results demonstrate that
LLBP-X maintained lower MPKI than LLBP
across all three timing-aware experiments.

It is important to note that our
zero-latency and timing-aware experiments
used different measurement lengths.

Therefore, we should not attribute
differences between the two experiment
sets solely to predictor timing.


## Slide 13: Performance Analysis

This slide summarizes the performance
improvements achieved by LLBP-X.

The first graph shows the percentage
reduction in MPKI compared with LLBP
under timing-aware simulation.

LLBP-X reduced MPKI by approximately
4.43 percent for Kafka,
4.15 percent for TPCC, and
3.09 percent for NodeApp.

The arithmetic mean of these workload
percentage reductions is 3.89 percent.

When we instead calculate the reduction
using the mean MPKI values,
the improvement is approximately 3.65 percent.

These values differ because they use
different aggregation methods.

The second graph shows the number
of branch mispredictions avoided.

LLBP-X avoided 2,092 mispredictions
for Kafka, 27,667 for TPCC,
and 20,611 for NodeApp.

Across the three measured workloads,
this gives a total of 50,370
fewer branch mispredictions.

These results support our conclusion
that LLBP-X provides better prediction
accuracy than LLBP for the evaluated traces.

## Slide 14: Limitations and Future Work

Although our results are encouraging,
the project has several limitations.

First, the published evaluation considers
14 workloads, whereas our experiments
cover only three workloads.

Therefore, this project represents
a partial reproduction of the research.

Second, we primarily evaluated branch
prediction accuracy using ROI MPKI.

We did not establish full processor
performance improvements using
metrics such as execution time or IPC.

Third, our zero-latency and timing-aware
experiments used different measurement
lengths, so direct comparisons between
these sets require caution.

Finally, our threshold experiment
compared only two configurations:
the default threshold of 7
and a modified threshold of 9.

In future work, we can evaluate
the complete benchmark suite,
test additional threshold values,
and investigate more detailed
performance and hardware trade-offs.

## Slide 15: Conclusion and References

To conclude, this project studied
and experimentally evaluated LLBP-X,
an advanced branch prediction approach.

We successfully built the publicly
available simulator and executed
18 simulation experiments across
three workloads.

Our zero-latency and timing-aware
results consistently showed lower
ROI MPKI for LLBP-X than for LLBP.

In the timing-aware experiments,
LLBP-X achieved an average workload
MPKI reduction of approximately
3.89 percent.

We also investigated the effect
of changing the adaptation threshold.

Increasing the threshold from 7 to 9
did not improve prediction accuracy
for our three evaluated workloads.

Overall, our work demonstrates
a partial experimental reproduction
of the LLBP-X research results.

Our main reference is the paper
"The Last-Level Branch Predictor Revisited,"
published at HPCA 2026.

We also used its publicly available
LLBP-X simulator repository.

Thank you for your attention.

I am ready to answer your questions.
