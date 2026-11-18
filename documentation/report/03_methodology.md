# Chapter 3: Experimental Setup and Methodology

## 3.1 Introduction

This chapter describes the experimental methodology used to evaluate the LLBP-X branch predictor.

The evaluation focuses on comparing branch prediction accuracy across TAGE-SC-L, LLBP, LLBP-X, and an experimental adaptation-threshold configuration.

Two sets of experiments were conducted: zero-latency predictor experiments and timing-aware predictor experiments.

## 3.2 Experimental Environment

The experiments were conducted using the publicly available LLBP-X simulator.

The software environment consisted of:

| Component | Configuration |
|---|---|
| Operating system | Ubuntu 22.04.5 LTS (WSL2) |
| Compiler | GCC 11.4.0 |
| Build system | CMake 3.22.1 |
| Programming language | C++ |
| Analysis language | Python 3.10.12 |
| Libraries | NumPy, Matplotlib |
| Simulator executable | `build/predictor` |

The simulator was compiled in Release mode using CMake.

## 3.3 Benchmark Selection

Five benchmark traces were selected from the publicly available
trace dataset associated with the LLBP-X research project.

| Benchmark | Trace filename |
|---|---|
| DaCapo Kafka | `dacapo-kafka.champsim.trace.gz` |
| BenchBase TPCC | `benchbase-tpcc.champsim.trace.gz` |
| NodeApp | `nodeapp-nodeapp.champsim.trace.gz` |
| DaCapo Spring | `dacapo-spring.champsim.trace.gz` |
| DaCapo Tomcat | `dacapo-tomcat.champsim.trace.gz` |

Kafka, TPCC, and NodeApp formed the initial evaluation set.
Spring and Tomcat were added to expand benchmark coverage.

All five benchmarks were evaluated using both zero-latency
and timing-aware predictor configurations.

The original research paper evaluates 14 workloads.
This project evaluates five selected workloads and therefore
represents a partial reproduction of the published study.

## 3.4 Evaluated Branch Predictors

### 3.4.1 TAGE-SC-L

The `tage64kscl` configuration serves as a conventional branch prediction baseline.

### 3.4.2 LLBP

The `llbp` configuration represents the earlier last-level branch prediction design.

### 3.4.3 LLBP-X

The `llbpx` configuration represents the proposed predictor evaluated in this project.

### 3.4.4 Modified LLBP-X

The `llbpx-threshold9` configuration was introduced to evaluate the sensitivity of LLBP-X to its adaptation threshold.

The default threshold is 7, while the modified configuration uses 9.

### 3.4.5 Timing-Aware Configurations

The `llbp-timing` and `llbpx-timing` configurations were evaluated separately to account for modeled timing effects.

## 3.5 Zero-Latency Experiments

The first experiment set compares four predictor configurations:

1. `tage64kscl`
2. `llbp`
3. `llbpx`
4. `llbpx-threshold9`

Each configuration was evaluated on five benchmark traces.

The simulation parameters were:

- Warmup instructions: 100,000,000
- Measurement instructions: 100,000,000
- BTB simulation: Enabled

The total number of experiments was:

4 predictor configurations × 5 benchmarks = 20 simulations.

### Example Simulation Command

```bash
./build/predictor \
  -b llbpx \
  -i traces/dacapo-kafka.champsim.trace.gz \
  -o results/step7/kafka/llbpx.log \
  --simulate-btb \
  -w 100000000 \
  -n 100000000
```

Equivalent simulations were performed for the remaining predictor configurations and benchmark traces.

## 3.6 Timing-Aware Experiments

The second experiment set compares:

1. `llbp-timing`
2. `llbpx-timing`

The simulation parameters were:

- Warmup instructions: 100,000,000
- Measurement instructions: 200,000,000
- BTB simulation: Enabled

The total number of experiments was:

2 predictor configurations × 5 benchmarks = 10 simulations.

### Example Simulation Command

```bash
./build/predictor \
  -b llbpx-timing \
  -i traces/dacapo-kafka.champsim.trace.gz \
  -o results/step8/timing/kafka/llbpx-timing.log \
  --simulate-btb \
  -w 100000000 \
  -n 200000000
```

The timing-aware experiments used a longer measurement interval than the zero-latency experiments.

Consequently, differences between these experiment sets cannot be attributed solely to timing effects.

## 3.7 Evaluation Metric

Branch prediction accuracy was evaluated using **Mispredictions Per Thousand Instructions (MPKI)**.

The metric is defined as:

\[
\text{MPKI} =
\frac{\text{Number of Branch Mispredictions}}
{\text{Number of Instructions}}
\times 1000
\]

Lower MPKI indicates fewer branch mispredictions relative to the number of executed instructions.

The simulator reports separate statistics for the measurement region, referred to as the Region of Interest (ROI).

The experiments use the following output fields:

- `ROI INSTRUCTIONS`
- `ROI MISPREDICTIONS`
- `ROI MPKI`

Intermediate diagnostic statistics were not used as the primary evaluation metric.

## 3.8 Percentage MPKI Reduction

The percentage improvement of a proposed predictor over a baseline predictor is calculated using:

\[
\text{MPKI Reduction (\%)} =
\frac{\text{Baseline MPKI} - \text{Proposed MPKI}}
{\text{Baseline MPKI}}
\times 100
\]

A positive value indicates that the proposed predictor achieves a lower MPKI.

For the timing-aware experiments, LLBP is used as the baseline and LLBP-X as the proposed predictor.

## 3.9 Result Extraction and Visualization

The simulation logs were processed using Python scripts.

The zero-latency results were extracted using:

`analysis/extract_roi.py`

The timing-aware results were extracted using:

`analysis/extract_timing_roi.py`

The extracted data were stored in:

- `analysis/data/roi_results.csv`
- `analysis/data/timing_roi_results.csv`

The expanded five-benchmark datasets are:

- `analysis/data/roi_results_5bench.csv`
- `analysis/data/timing_roi_results_5bench.csv`

The expanded results were visualized using `analysis/plot_5bench.py` and `analysis/plot_timing_5bench.py`, producing six additional graphs (Graphs 7–12) for the five-benchmark evaluation.

The results were visualized using Matplotlib.

The generated graphs include:

1. Zero-latency ROI MPKI comparison.
2. LLBP-X improvement over the evaluated baselines.
3. Adaptation-threshold sensitivity.
4. Timing-aware ROI MPKI comparison.
5. Timing-aware percentage improvement.
6. Timing-aware branch mispredictions avoided.

## 3.10 Experimental Limitations

The following limitations apply to the evaluation:

1. Only five benchmark traces were evaluated, compared with the larger benchmark suite used in the original research.
2. The experiments were conducted using a simulator rather than physical processor hardware.
3. The zero-latency and timing-aware experiments used different measurement lengths.
4. The adaptation-threshold study evaluated only one alternative threshold value.
5. The evaluation primarily measures branch prediction accuracy rather than complete processor performance.

These limitations are considered when interpreting the experimental results.

## 3.11 Summary

This chapter described the experimental environment, benchmark traces, predictor configurations, simulation parameters, evaluation metrics, and data-analysis procedure.

A total of 30 simulations were conducted across the two experiment sets.

The following chapter presents the experimental results and discusses the observed differences between the predictors.
