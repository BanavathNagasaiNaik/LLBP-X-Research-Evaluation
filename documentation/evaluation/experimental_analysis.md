
# LLBP-X Experimental Analysis — Evaluation Preparation

## 1. Experimental Overview

We evaluated branch prediction accuracy using
three workloads:

- Kafka
- BenchBase TPCC
- NodeApp

The evaluation included two experiment groups:

1. Zero-latency predictor configurations
2. Timing-aware predictor configurations

The primary metric was Region of Interest
Mispredictions Per Kilo Instructions (ROI MPKI).

MPKI = (ROI Mispredictions / ROI Instructions) * 1000

A lower MPKI indicates better prediction accuracy.

## 2. Zero-Latency ROI MPKI Results

We compared four predictor configurations:

- TAGE-SC-L
- LLBP
- LLBP-X
- LLBP-X with adaptation threshold 9

Each experiment used approximately 100 million
measurement instructions after 100 million
warmup instructions.

### Measured Results

| Workload | TAGE-SC-L | LLBP | LLBP-X | Threshold 9 |
|---|---:|---:|---:|---:|
| Kafka | 0.37981 | 0.32264 | 0.30452 | 0.30597 |
| TPCC | 4.30471 | 3.82597 | 3.72292 | 3.72616 |
| NodeApp | 4.40926 | 3.38402 | 3.29396 | 3.29845 |

All values are ROI MPKI.

### LLBP-X Improvement Over LLBP

Percentage reduction is calculated as:

Reduction (%) =
    ((LLBP MPKI - LLBP-X MPKI) / LLBP MPKI) * 100

Results:

- Kafka: approximately 5.62%
- TPCC: approximately 2.69%
- NodeApp: approximately 2.66%

The arithmetic mean of the three workload
percentage reductions is approximately 3.66%.

### Interpretation

LLBP-X achieved lower ROI MPKI than LLBP
for all three evaluated workloads.

It also achieved lower ROI MPKI than
the TAGE-SC-L baseline on these workloads.

The relative improvement varied by workload,
indicating that prediction accuracy depends
on the characteristics of the branch trace.

These results support the effectiveness
of LLBP-X for our selected workloads.

They do not establish identical improvements
for the full published benchmark suite.

### Evaluation Question

Q: Why did you use MPKI rather than
only reporting the number of mispredictions?

A: MPKI normalizes mispredictions by
the number of executed instructions.

This makes prediction accuracy easier
to compare across experiments with
different instruction counts.

Q: Which workload showed the largest
percentage improvement over LLBP?

A: Kafka, with approximately 5.62%
lower ROI MPKI in the zero-latency experiments.

Q: Does lower MPKI prove higher IPC?

A: No. Lower MPKI indicates fewer
branch mispredictions per thousand instructions.

We did not directly measure a corresponding
increase in processor IPC.


## 3. Adaptation-Threshold Analysis

### Objective

The objective of this experiment was to
investigate how changing the LLBP-X
adaptation threshold affects branch
prediction accuracy.

We compared two configurations:

- Default LLBP-X: adaptation threshold 7
- Modified LLBP-X: adaptation threshold 9

Both configurations were evaluated using
the same zero-latency experimental setup.

### Measured Results

| Workload | Threshold 7 MPKI | Threshold 9 MPKI |
|---|---:|---:|
| Kafka | 0.30452 | 0.30597 |
| TPCC | 3.72292 | 3.72616 |
| NodeApp | 3.29396 | 3.29845 |

### Interpretation

Increasing the adaptation threshold
from 7 to 9 resulted in slightly higher
ROI MPKI for all three workloads.

The absolute MPKI increases were:

- Kafka: 0.00145
- TPCC: 0.00324
- NodeApp: 0.00449

Therefore, the modified configuration
did not improve prediction accuracy
on the evaluated workloads.

The experiment demonstrates that
prediction accuracy can be sensitive
to the adaptation-threshold setting.

However, only two threshold values
and three workloads were evaluated.

We cannot conclude that threshold 7
is globally optimal.

### Evaluation Questions

Q: Why did you change the threshold?

A: We wanted to investigate whether
the adaptation parameter affects
LLBP-X prediction accuracy.

Q: Did threshold 9 improve performance?

A: No. Threshold 9 produced slightly
higher ROI MPKI for all three workloads.

Q: Does this prove threshold 7 is optimal?

A: No. We tested only two settings.
A broader parameter sweep would be
needed to identify better settings.

Q: What is the research contribution
of this experiment?

A: We added and evaluated an alternative
LLBP-X configuration, providing a small
sensitivity study beyond the default model.


## 4. Timing-Aware ROI MPKI Analysis

### Objective

The objective of the timing-aware experiments
was to compare LLBP and LLBP-X using simulator
configurations that model predictor timing.

We evaluated three workloads:

- Kafka
- BenchBase TPCC
- NodeApp

Each simulation used:

- 100 million warmup instructions
- Approximately 200 million measurement instructions
- BTB simulation enabled

### Measured Results

| Workload | LLBP MPKI | LLBP-X MPKI |
|---|---:|---:|
| Kafka | 0.236015 | 0.225555 |
| TPCC | 3.334090 | 3.195755 |
| NodeApp | 3.336635 | 3.233580 |

### Percentage Improvement

Percentage MPKI reduction is calculated as:

Reduction (%) =
    ((LLBP MPKI - LLBP-X MPKI) / LLBP MPKI) * 100

Results:

- Kafka: approximately 4.43%
- TPCC: approximately 4.15%
- NodeApp: approximately 3.09%

The arithmetic mean of the three workload
percentage reductions is approximately 3.89%.

If we instead calculate the reduction using
the mean MPKI values, it is approximately 3.65%.

These are different aggregation methods.

### Mispredictions Avoided

The measured ROI misprediction counts were:

| Workload | LLBP | LLBP-X | Avoided |
|---|---:|---:|---:|
| Kafka | 47,203 | 45,111 | 2,092 |
| TPCC | 666,818 | 639,151 | 27,667 |
| NodeApp | 667,327 | 646,716 | 20,611 |

Total avoided mispredictions:

2,092 + 27,667 + 20,611 = 50,370

Across the three experiments, LLBP-X
produced 50,370 fewer branch mispredictions.

### Interpretation

LLBP-X achieved lower ROI MPKI than LLBP
on all three timing-aware workloads.

Kafka had the largest relative MPKI
improvement, approximately 4.43%.

TPCC had the largest absolute reduction
in branch mispredictions, with 27,667
fewer mispredictions.

The results demonstrate improved prediction
accuracy for the selected traces.

However, reduced MPKI does not by itself
establish improved processor IPC or runtime.

### Important Experimental Limitation

Our zero-latency experiments used approximately
100 million measurement instructions.

Our timing-aware experiments used approximately
200 million measurement instructions.

Therefore, differences between these experiment
groups cannot be attributed solely to timing.

### Evaluation Questions

Q: What is the main result of your
timing-aware evaluation?

A: LLBP-X achieved lower ROI MPKI than LLBP
on all three workloads, with an arithmetic
mean workload improvement of about 3.89%.

Q: Which workload avoided the most
branch mispredictions?

A: TPCC, with 27,667 fewer mispredictions.

Q: Why do you report both 3.89% and 3.65%?

A: 3.89% is the arithmetic mean of the
three workload percentage reductions.

3.65% is the percentage reduction
calculated from the mean MPKI values.

Q: Can you claim that LLBP-X improved
processor execution speed by 3.89%?

A: No. The 3.89% figure measures MPKI
reduction, not processor speedup.


## 5. Interpretation of the Six Experimental Graphs

### Graph 1: Zero-Latency ROI MPKI Comparison

File: graph1_roi_mpki_comparison.png
Presentation: Slide 10

This graph compares TAGE-SC-L, LLBP,
LLBP-X, and LLBP-X threshold 9.

The X-axis represents the workloads.
The Y-axis represents ROI MPKI.

LLBP-X achieves lower MPKI than LLBP
and TAGE-SC-L on all three workloads.

Key observation:
LLBP-X improves prediction accuracy
across all three evaluated traces.

### Graph 2: Zero-Latency LLBP-X Improvement

File: graph2_roi_llbpx_improvement.png
Presentation: Slide 10

This graph shows the percentage reduction
in ROI MPKI achieved by LLBP-X over LLBP.

Kafka: approximately 5.62%
TPCC: approximately 2.69%
NodeApp: approximately 2.66%

The arithmetic mean workload improvement
is approximately 3.66%.

Key observation:
Kafka shows the largest relative
improvement in this experiment.

### Graph 3: Adaptation-Threshold Sensitivity

File: graph3_roi_threshold_sensitivity.png
Presentation: Slide 11

This graph compares default LLBP-X
with the threshold 9 configuration.

Threshold 7 produces slightly lower
MPKI than threshold 9 for all workloads.

Key observation:
Increasing the adaptation threshold
from 7 to 9 did not improve accuracy
for the three evaluated workloads.

### Graph 4: Timing-Aware ROI MPKI Comparison

File: graph4_timing_mpki.png
Presentation: Slide 12

This graph compares timing-aware
LLBP and LLBP-X configurations.

LLBP-X has lower ROI MPKI on Kafka,
TPCC, and NodeApp.

Key observation:
LLBP-X retains an accuracy advantage
in the timing-aware simulations.

### Graph 5: Timing-Aware MPKI Improvement

File: graph5_timing_improvement.png
Presentation: Slide 13

This graph shows the percentage
reduction in ROI MPKI for LLBP-X
relative to LLBP.

Kafka: approximately 4.43%
TPCC: approximately 4.15%
NodeApp: approximately 3.09%

The arithmetic mean workload
improvement is approximately 3.89%.

Key observation:
All three workloads benefit,
although the improvement varies.

### Graph 6: Timing-Aware Mispredictions Avoided

File: graph6_timing_misses_saved.png
Presentation: Slide 13

This graph shows the absolute number
of branch mispredictions avoided
by LLBP-X compared with LLBP.

Kafka: 2,092
TPCC: 27,667
NodeApp: 20,611

Total: 50,370 fewer mispredictions.

Key observation:
TPCC shows the largest absolute
reduction in misprediction count.

### How to Explain the Graphs During Evaluation

For each graph, explain four things:

1. What is being compared?
2. What do the axes represent?
3. What is the main numerical observation?
4. What conclusion does the observation support?

Do not confuse MPKI reduction with
processor speedup or IPC improvement.

The results represent three workloads,
not the full published benchmark suite.

The zero-latency and timing-aware runs
used different measurement lengths,
so comparisons between these two groups
require caution.
