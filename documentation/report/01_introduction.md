# Chapter 1: Introduction

## 1.1 Background

Modern high-performance processors employ sophisticated branch prediction mechanisms to improve instruction-level parallelism and maintain efficient instruction pipeline utilization. Conditional branch instructions introduce control dependencies, making it difficult for processors to determine the correct sequence of instructions before the branch outcome is known.

Branch predictors estimate the direction of conditional branches using information from previously executed instructions. Accurate predictions allow processors to continue speculative execution, while incorrect predictions may result in pipeline flushing, wasted execution cycles, and reduced performance.

TAGE (TAgged GEometric history length) predictors are widely studied because they combine multiple prediction tables indexed using different branch history lengths. However, accurately predicting branches with complex or long-range correlations remains challenging.

Last-Level Branch Prediction (LLBP) provides an additional prediction mechanism for difficult branches by exploiting longer-range execution context. LLBP-X extends this approach with adaptive prediction mechanisms intended to improve prediction accuracy and resource utilization.

This project investigates the implementation and experimental behavior of LLBP-X using the publicly available simulator associated with the research paper *The Last-Level Branch Predictor Revisited*.

## 1.2 Problem Statement

Despite advances in branch prediction, modern predictors may struggle with branches whose outcomes depend on complex execution histories or contextual information.

The central problem investigated in this project is:

**How effectively does LLBP-X reduce branch mispredictions compared with conventional TAGE-based prediction and the earlier LLBP design under selected benchmark workloads?**

The project also investigates how modifying an adaptation threshold influences LLBP-X prediction accuracy.

## 1.3 Project Objectives

The primary objectives are:

1. Study the architecture and working principles of TAGE-based prediction, LLBP, and LLBP-X.
2. Obtain, configure, and compile the publicly available LLBP-X simulator.
3. Understand the implementation of adaptive prediction and context-based prediction mechanisms.
4. Implement an experimental LLBP-X configuration with a modified adaptation threshold.
5. Execute baseline and proposed predictors using representative benchmark traces.
6. Evaluate prediction accuracy using branch mispredictions per thousand instructions (MPKI).
7. Compare zero-latency and timing-aware predictor configurations under their respective experimental settings.
8. Generate graphs and analyze the performance differences between predictor configurations.
9. Assess how the reproduced results relate to the evaluation methodology presented in the research paper.

## 1.4 Scope of the Project

The project focuses on simulation-based evaluation rather than physical processor implementation.

Three benchmark traces are evaluated:

- DaCapo Kafka
- BenchBase TPCC
- NodeApp

The predictor configurations include TAGE-SC-L, LLBP, LLBP-X, and an experimental LLBP-X adaptation-threshold variant. Additional timing-aware simulations compare LLBP and LLBP-X.

The zero-latency experiments use 100 million warmup instructions and approximately 100 million measurement instructions. The timing-aware experiments use 100 million warmup instructions and approximately 200 million measurement instructions.

The study evaluates a subset of the benchmark suite rather than reproducing the complete 14-benchmark evaluation.

## 1.5 Expected Contributions

The expected contributions of this project are:

- A reproducible simulation environment for evaluating LLBP-X.
- A comparative analysis of branch prediction accuracy across selected workloads.
- An experimental study of an adaptation-threshold modification.
- Timing-aware performance comparisons between LLBP and LLBP-X.
- Experimental graphs, datasets, and documented evaluation procedures.

## 1.6 Organization of the Report

The remaining chapters will cover the research background, branch predictor architecture, implementation methodology, experimental setup, performance evaluation, conclusions, and future work.
