
# LLBP-X Research Project — Viva Questions and Answers

## Section 1: Branch Prediction and Architecture

### Q1. What is branch prediction?

Branch prediction is a processor technique
that predicts the direction of a branch
before its actual outcome is known.

It helps maintain instruction pipeline flow.

### Q2. Why is branch prediction important?

Correct predictions allow speculative
execution to proceed along the expected path.

Incorrect predictions can cause pipeline
flushes and wasted execution cycles.

### Q3. What is TAGE-SC-L?

TAGE-SC-L combines:

- TAGE: Tagged Geometric History Length prediction
- SC: Statistical Corrector
- L: Loop prediction

These mechanisms provide complementary
information for branch prediction.

### Q4. What is LLBP?

LLBP stands for Last-Level Branch Predictor.

It supplements the base predictor with
additional prediction information intended
to help with difficult-to-predict branches.

### Q5. What is LLBP-X?

LLBP-X is an approach that extends
last-level branch prediction with
adaptive behavior.

Our project evaluates its prediction
accuracy against LLBP and TAGE-SC-L.

### Q6. What is the role of context tracking?

Context tracking maintains information
about execution situations associated
with branch behavior.

This can help distinguish different
outcome patterns for a branch.

### Q7. What is pattern storage?

Pattern storage maintains prediction-related
information associated with execution contexts.

The last-level predictor can use this
information to support predictions.

### Q8. What is the pattern buffer?

The pattern buffer is a limited-capacity
structure for holding pattern information.

In our simulator configuration, it has
64 entries and associativity 4.

Its exact lookup and replacement behavior
should be described from the source code.

### Q9. What is adaptive prediction logic?

Adaptive prediction logic allows the
last-level predictor configuration
to change according to observed behavior.

In our project, we also evaluated
the effect of changing an adaptation
threshold from 7 to 9.

### Q10. How does LLBP-X differ from LLBP?

In our studied configurations,
LLBP uses a fixed W value of 8.

LLBP-X uses adaptive W settings
with values of 2 and 64.

The precise meaning of W and the
adaptation conditions must be verified
against the simulator implementation.

### Q11. How do the components work together?

TAGE-SC-L provides base prediction information.

The last-level mechanism uses context
and pattern-related information.

The implemented prediction logic determines
how this information contributes to the
final prediction.

After branch resolution, relevant
predictor structures are updated.

### Q12. Does every branch use the
last-level prediction structures?

Not necessarily.

The precise conditions for accessing
the last-level predictor depend on
the implementation's control logic.

We should not assume that every branch
uses every structure.

### Q13. What is the main architectural
advantage of LLBP-X?

It provides additional context-based
prediction information and adaptive behavior
beyond the base prediction system.

The goal is to reduce mispredictions
on difficult branches.

### Q14. What is a branch misprediction?

A branch misprediction occurs when
the predicted branch direction differs
from the actual branch outcome.

### Q15. What is MPKI?

MPKI stands for Mispredictions Per
Kilo Instructions.

MPKI = (Number of mispredictions /
        Number of executed instructions) * 1000

Lower MPKI indicates fewer mispredictions
per thousand executed instructions.


## Section 2: Experimental Methodology

### Q16. Why did you use simulation instead of real hardware?

The research evaluates branch predictor designs
using a simulator that supports multiple
predictor configurations.

Simulation allows us to compare predictors
under controlled experimental conditions
without modifying physical processor hardware.

### Q17. What is the difference between warmup and measurement?

During warmup, the simulator processes
instructions to establish predictor state.

During measurement, we collect the statistics
used for experimental evaluation.

We used 100 million warmup instructions
for both experiment groups.

### Q18. Why did you choose three workloads?

We selected Kafka, BenchBase TPCC,
and NodeApp to perform a manageable
partial reproduction of the published work.

The original evaluation used 14 workloads.

Therefore, our findings are limited
to the three selected traces.

### Q19. What is a branch trace?

A branch trace records information
about branch behavior during execution.

It allows a branch predictor simulator
to replay branch events and evaluate
prediction accuracy.

### Q20. Why did you compare TAGE-SC-L,
LLBP, and LLBP-X?

TAGE-SC-L provides the base predictor
reference.

LLBP represents the earlier last-level
prediction approach.

LLBP-X is the proposed approach
whose accuracy we are evaluating.

Comparing them helps identify the
benefit of the last-level mechanism
and its adaptive extension.

### Q21. Why did you enable BTB simulation?

The Branch Target Buffer, or BTB,
provides information related to
branch targets.

We enabled the simulator's BTB option
to use a consistent configuration
across our experimental runs.

Our reported ROI MPKI remains a
prediction-accuracy metric, not
a direct measure of processor speed.

### Q22. What is the difference between
zero-latency and timing-aware experiments?

Zero-latency configurations do not
model the same predictor-access timing
constraints as timing-aware configurations.

Timing-aware configurations include
the simulator's predictor timing behavior.

We evaluated both to compare prediction
accuracy under different model settings.

### Q23. Why did you use different
measurement lengths?

Our zero-latency runs measured
approximately 100 million instructions.

Our timing-aware runs measured
approximately 200 million instructions.

These were the chosen experimental
configurations, but the difference
limits direct comparisons between groups.

We cannot attribute cross-group MPKI
differences solely to predictor timing.

### Q24. How did you ensure a fair comparison?

Within each experiment group,
we used the same workload traces,
warmup length, measurement length,
and BTB setting for the models compared.

This makes within-group comparisons
more meaningful.

We did not perform a full
reproduction of all published workloads.

### Q25. What is ROI MPKI, and why
did you use it?

ROI means Region of Interest.

ROI MPKI measures branch mispredictions
per thousand instructions within
the measured instruction region.

We used it to compare prediction
accuracy consistently within each
experiment group.

MPKI = (ROI mispredictions /
        ROI instructions) * 1000


## Section 3: Results and Numerical Analysis

### Q26. How is MPKI calculated?

MPKI stands for Mispredictions Per Kilo Instructions.

Formula:

MPKI = (Mispredictions / Instructions) * 1000

Example from our timing-aware Kafka experiment:

LLBP mispredictions = 47,203
ROI instructions = 199,999,996

MPKI = (47,203 / 199,999,996) * 1000
     = approximately 0.236015

### Q27. How do you calculate percentage MPKI improvement?

Formula:

Improvement (%) =
    ((Baseline MPKI - Proposed MPKI)
     / Baseline MPKI) * 100

For timing-aware Kafka:

LLBP MPKI = 0.236015
LLBP-X MPKI = 0.225555

Improvement =
    ((0.236015 - 0.225555) / 0.236015) * 100

Improvement = approximately 4.43%

### Q28. Which workload showed the highest
relative improvement in timing-aware experiments?

Kafka showed the highest relative improvement.

Kafka: 4.43%
TPCC: 4.15%
NodeApp: 3.09%

These percentages compare LLBP-X against LLBP.

### Q29. Which workload showed the largest
absolute reduction in mispredictions?

TPCC showed the largest absolute reduction.

LLBP mispredictions = 666,818
LLBP-X mispredictions = 639,151

Mispredictions avoided:

666,818 - 639,151 = 27,667

### Q30. How many mispredictions were avoided
across all timing-aware experiments?

Kafka: 2,092
TPCC: 27,667
NodeApp: 20,611

Total:

2,092 + 27,667 + 20,611 = 50,370

LLBP-X produced 50,370 fewer mispredictions
across the three measured workloads.

### Q31. Why do you report both
3.89% and 3.65% improvement?

They represent different aggregation methods.

3.89% is the arithmetic mean of the
individual workload percentage reductions.

3.65% is calculated by taking the
percentage reduction between the
mean MPKI values of LLBP and LLBP-X.

The two methods assign different
relative importance to workloads.

We must state which method is used.

### Q32. Did threshold 9 outperform threshold 7?

No.

Threshold 9 produced slightly higher
zero-latency ROI MPKI on all three workloads.

Kafka:
Threshold 7 = 0.30452
Threshold 9 = 0.30597

TPCC:
Threshold 7 = 3.72292
Threshold 9 = 3.72616

NodeApp:
Threshold 7 = 3.29396
Threshold 9 = 3.29845

Lower MPKI is better.

### Q33. What is the percentage improvement
of LLBP-X over LLBP for zero-latency Kafka?

LLBP MPKI = 0.32264
LLBP-X MPKI = 0.30452

Improvement =
    ((0.32264 - 0.30452) / 0.32264) * 100

Improvement = approximately 5.62%

### Q34. Does lower MPKI guarantee higher IPC?

No.

Lower MPKI indicates fewer branch
mispredictions per thousand instructions.

IPC also depends on factors such as
memory behavior, pipeline design,
instruction dependencies, and
misprediction recovery costs.

We did not directly establish an IPC gain.

### Q35. Can the results be generalized
to all applications?

Not yet.

We evaluated three workloads,
while the published evaluation used 14.

The results show an accuracy improvement
for our selected traces.

A broader evaluation is required before
making claims about general performance.


## Section 4: Implementation and Research Limitations

### Q36. Did you implement LLBP-X completely from scratch?

No.

We used the publicly available LLBP-X
simulator associated with the research paper.

We built and configured the simulator,
executed experiments, analyzed results,
and added a custom threshold configuration.

Our work is a partial reproduction and
experimental evaluation, not a new
branch predictor designed from scratch.

### Q37. What was your original implementation contribution?

We introduced an additional model named
llbpx-threshold9.

This model changes the adaptation threshold
from the default value of 7 to 9.

We then compared both configurations
using the same zero-latency workloads.

This is a limited parameter-sensitivity
experiment rather than a new architecture.

### Q38. Which programming tools did you use?

We used:

- C++ for the predictor simulator
- CMake for the build process
- Ubuntu on WSL2 for execution
- Python for result extraction and analysis
- Matplotlib for experimental graphs
- python-pptx for presentation generation

### Q39. What is the purpose of CMake?

CMake manages the build configuration.

It helps generate the build files needed
to compile the C++ simulator.

Our compiled executable is located at:

build/predictor

### Q40. How did you introduce the custom predictor?

We added a derived LLBP-X predictor
configuration with adaptation threshold 9.

We registered the configuration under
the model name llbpx-threshold9.

This allowed us to select it using
the simulator's command-line interface.

### Q41. What is the difference between
reproducing a paper and proposing a new method?

Reproduction evaluates whether published
results can be obtained using a specified
implementation and experimental setup.

A new method introduces a distinct
technical approach or algorithm.

Our project primarily reproduces and
evaluates an existing approach.

Our threshold experiment is a small
additional investigation.

### Q42. What is the main limitation
of your experimental evaluation?

We evaluated three workloads rather than
the full 14-workload published suite.

Therefore, we cannot claim that our
results reproduce every published finding.

The experiments also focus on branch
prediction accuracy rather than
full-system processor performance.

### Q43. Why should we trust your results?

We used consistent simulation settings
within each experimental group.

We extracted ROI instruction counts
and misprediction counts from the logs.

We calculated MPKI using these counts
and generated graphs from the results.

The logs and analysis files provide
a basis for checking the calculations.

Independent reproduction would provide
additional confidence.

### Q44. What would you improve if
you had more time?

I would:

1. Evaluate all 14 published workloads.
2. Test additional adaptation thresholds.
3. Use matched measurement regions
   when comparing timing configurations.
4. Investigate IPC and execution-time effects.
5. Study hardware storage and timing costs.

These improvements would make the
evaluation more comprehensive.

### Q45. What is the final conclusion
of your research project?

LLBP-X achieved lower ROI MPKI than
LLBP on all three evaluated workloads
in both experiment groups.

In the timing-aware experiments,
the arithmetic mean of the workload
MPKI reductions was approximately 3.89%.

Our modified threshold 9 configuration
did not outperform the default threshold 7.

These findings support the effectiveness
of LLBP-X on our selected traces,
while remaining a partial reproduction
of the published research.
