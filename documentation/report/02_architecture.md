# Chapter 2: System Architecture and Implementation

## 2.1 Introduction

This chapter describes the branch prediction architectures evaluated in the project, including TAGE-SC-L, Last-Level Branch Prediction (LLBP), and LLBP-X.

The implementation is based on the publicly available LLBP-X simulator associated with the research paper *The Last-Level Branch Predictor Revisited*.

The project evaluates the original predictor configurations and an experimental modification of the LLBP-X adaptation threshold.

## 2.2 TAGE-SC-L Branch Predictor

TAGE-SC-L combines multiple branch prediction mechanisms.

**TAGE (TAgged GEometric history length):** Uses tagged prediction tables with different history lengths to capture branch correlations.

**Statistical Corrector (SC):** Provides additional prediction information to improve decisions made by the primary predictor.

**Loop Predictor (L):** Exploits repetitive branch behavior associated with loops.

Together, these mechanisms form the TAGE-SC-L prediction architecture used as a baseline in this project.

The evaluated baseline model is `tage64kscl`.

## 2.3 Last-Level Branch Prediction (LLBP)

LLBP extends conventional branch prediction by introducing additional structures for exploiting longer-range execution context.

The objective is to improve predictions for branches that remain difficult for the underlying predictor.

The project evaluates LLBP using the simulator configurations `llbp` and `llbp-timing`.

The timing-aware configuration is used to evaluate prediction accuracy while accounting for the simulator's modeled timing effects.

## 2.4 LLBP-X Architecture

LLBP-X extends the LLBP design with adaptive prediction behavior.

The simulator configuration examined in this project includes the following parameters:

| Parameter | Configuration |
|---|---|
| Base predictor | TAGE-SC-L 64K |
| Statistical corrector | Enabled |
| Loop predictor | Enabled |
| Context tracking table entries | 6,144 |
| Context tracking associativity | 6 |
| Number of patterns | 16 |
| Configured contexts | 14,336 |
| Pattern buffer size | 64 |
| Pattern buffer associativity | 4 |
| Default adaptation threshold | 7 |
| Experimental adaptation threshold | 9 |

These values describe the configuration investigated in this project. The corresponding source-code declarations should be used when discussing the exact implementation.

### 2.4.1 Context Tracking

Context tracking maintains information used to associate branch behavior with execution context.

This allows the predictor to exploit contextual information beyond the correlations represented by the base prediction mechanism.

### 2.4.2 Pattern Storage

The pattern-related structures maintain information used by the last-level prediction mechanism.

The evaluated configuration includes a pattern buffer and multiple configured prediction contexts.

### 2.4.3 Adaptive Prediction

LLBP-X supports adaptive prediction behavior instead of relying exclusively on a fixed prediction configuration.

The adaptation mechanism is intended to adjust predictor behavior based on information available during execution.

The original LLBP configuration uses a fixed prediction width of 8, while the LLBP-X design supports adaptive widths of 2 and 64 in the configuration studied.

### 2.4.4 Prediction Integration

The base TAGE-SC-L predictor and the last-level prediction mechanism work together to produce branch predictions.

The exact decision logic and update ordering are implemented in the simulator source code.

## 2.5 Experimental Adaptation-Threshold Modification

An additional predictor configuration, `llbpx-threshold9`, was introduced to investigate adaptation-threshold sensitivity.

The original LLBP-X configuration uses:

`adaptThreshold = 7`

The experimental configuration changes this value to:

`adaptThreshold = 9`

The experimental class is named `LLBPXTSCL64kThreshold9` and derives from `LLBPX`.

The class was added to:

`bpmodels/llbpx/llbpx.h`

The model name was registered in:

`bpmodels/base_predictor.cc`

This modification preserves the main LLBP-X architecture while changing the configured adaptation threshold.

## 2.6 Simulator Implementation

The implementation and experiments were performed using the publicly available LLBP-X repository.

The development environment includes:

- Ubuntu 22.04 under WSL2
- GCC 11.4
- CMake 3.22
- Python 3.10
- NumPy and Matplotlib for result analysis

The simulator was compiled using CMake in Release mode.

The resulting executable is:

`build/predictor`

The simulator processes benchmark traces and records branch prediction statistics.

## 2.7 Evaluated Predictor Configurations

The following configurations were evaluated:

| Predictor | Purpose |
|---|---|
| `tage64kscl` | TAGE-SC-L baseline |
| `llbp` | Original LLBP configuration |
| `llbpx` | LLBP-X configuration |
| `llbpx-threshold9` | Experimental adaptation-threshold variant |
| `llbp-timing` | Timing-aware LLBP |
| `llbpx-timing` | Timing-aware LLBP-X |

The zero-latency and timing-aware experiments were conducted separately using different measurement lengths.

## 2.8 Summary

This chapter introduced the predictor architectures and implementation configurations evaluated in the project.

The principal experimental contribution is the comparative evaluation of LLBP-X against LLBP and TAGE-SC-L, together with an adaptation-threshold sensitivity experiment.

The next chapter will describe the benchmark traces, simulation methodology, and evaluation metrics.
