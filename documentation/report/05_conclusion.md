# Chapter 5: Conclusions and Future Work

## 5.1 Introduction

This chapter summarizes the findings of the project, *Reproduction and Experimental Evaluation of the LLBP-X Branch Predictor*.

The project investigated the architecture and prediction accuracy of LLBP-X using the publicly available simulator associated with the research paper *The Last-Level Branch Predictor Revisited*.

The experimental evaluation compared TAGE-SC-L, LLBP, LLBP-X, and a modified adaptation-threshold configuration using five benchmark traces.

## 5.2 Summary of Work Completed

The following activities were completed during the project:

1. Studied the fundamentals of branch prediction and the architectures of TAGE-SC-L, LLBP, and LLBP-X.
2. Obtained and successfully compiled the publicly available LLBP-X simulator.
3. Examined the predictor configuration and implementation files.
4. Implemented an experimental LLBP-X configuration with an adaptation threshold of 9 instead of the default value of 7.
5. Obtained five benchmark traces: DaCapo Kafka, BenchBase TPCC, NodeApp, DaCapo Spring, and DaCapo Tomcat.
6. Conducted 20 zero-latency predictor simulations.
7. Conducted 10 timing-aware predictor simulations.
8. Extracted ROI branch prediction statistics from the simulation logs.
9. Generated twelve experimental graphs for performance comparison.
10. Analyzed prediction accuracy, adaptation-threshold sensitivity, and experimental limitations.

## 5.3 Major Experimental Findings

### 5.3.1 Zero-Latency Prediction Accuracy

The zero-latency experiments demonstrated that LLBP-X achieved lower ROI MPKI than both LLBP and the evaluated TAGE-SC-L baseline for all five workloads.

Compared with LLBP, the percentage MPKI reductions achieved by LLBP-X were:

| Benchmark | MPKI Reduction |
|---|---:|
| Kafka | 5.62% |
| TPCC | 2.69% |
| NodeApp | 2.66% |
| Spring | 14.25% |
| Tomcat | 1.59% |

The arithmetic mean of these workload-specific reductions was approximately **5.36%**.

These results demonstrate a consistent prediction-accuracy advantage for LLBP-X under the evaluated configurations.

### 5.3.2 Timing-Aware Prediction Accuracy

The timing-aware experiments compared LLBP and LLBP-X using approximately 200 million measurement instructions per workload.

The observed improvements were:

| Benchmark | MPKI Reduction |
|---|---:|
| Kafka | 4.43% |
| TPCC | 4.15% |
| NodeApp | 3.09% |
| Spring | 12.65% |
| Tomcat | 1.93% |

The arithmetic mean of the five workload-specific reductions was approximately **5.25%**.

Across the five timing-aware benchmark pairs, LLBP-X recorded **145,125 fewer branch mispredictions** than LLBP.

### 5.3.3 Adaptation-Threshold Sensitivity

The experimental LLBP-X configuration modified the adaptation threshold from 7 to 9.

The threshold-9 configuration produced slightly higher ROI MPKI than the default threshold-7 configuration for Kafka, TPCC, NodeApp, Spring, and Tomcat.

Therefore, increasing the threshold from 7 to 9 did not improve prediction accuracy in the evaluated experiments.

This observation does not establish that threshold 7 is optimal across all possible workloads or parameter values.

## 5.4 Research Contributions

The primary contributions of this project are:

1. **Simulator reproduction:** Establishing a working simulation environment for the publicly available LLBP-X implementation.

2. **Comparative evaluation:** Measuring branch prediction accuracy across selected workloads using multiple predictor configurations.

3. **Experimental modification:** Implementing an additional LLBP-X configuration to investigate adaptation-threshold sensitivity.

4. **Timing-aware analysis:** Comparing LLBP and LLBP-X using timing-aware simulator configurations.

5. **Reproducible analysis:** Organizing simulation logs, ROI datasets, analysis scripts, and graphs to support verification and future experiments.

The adaptation-threshold experiment represents a small configuration-level extension rather than a new branch prediction architecture.

## 5.5 Limitations

Although the experiments produced consistent results, the study has several limitations.

### 5.5.1 Limited Benchmark Coverage

Only five benchmark traces were evaluated.

The broader research evaluation considers fourteen benchmark workloads. Consequently, the findings cannot be generalized to the complete workload suite.

### 5.5.2 Simulation-Based Evaluation

The evaluation was performed using a branch predictor simulator rather than physical processor hardware.

Therefore, the results demonstrate simulated prediction accuracy rather than measured processor execution speedup.

### 5.5.3 Different Measurement Intervals

The zero-latency experiments used approximately 100 million measurement instructions, whereas the timing-aware experiments used approximately 200 million.

Because the measurement intervals differ, the two experiment sets cannot be directly compared to isolate the effects of predictor timing.

### 5.5.4 Limited Parameter Exploration

The adaptation-threshold study considered only values 7 and 9.

A wider parameter sweep would be necessary to investigate the relationship between adaptation thresholds and prediction accuracy.

### 5.5.5 Limited Performance Metrics

The primary evaluation metric was ROI MPKI.

Additional metrics, such as predictor storage requirements, modeled latency, energy consumption, and full-system performance, would provide a broader understanding of design trade-offs.

## 5.6 Future Work

Several extensions could improve the completeness and depth of this research.

### 5.6.1 Evaluate the Complete Benchmark Suite

Future experiments could include all fourteen workloads used in the broader research evaluation.

This would allow a more comprehensive comparison with the published results.

### 5.6.2 Perform Adaptation-Threshold Sweeps

The experimental threshold could be varied systematically across multiple values.

For example, future experiments could evaluate thresholds 5, 7, 9, and 11 while keeping other simulation parameters constant.

This would help identify whether different workloads benefit from different adaptation settings.

### 5.6.3 Standardize Measurement Intervals

Zero-latency and timing-aware configurations could be evaluated using identical warmup and measurement intervals.

This would support more controlled comparisons of timing-related effects.

### 5.6.4 Investigate Predictor Resource Trade-offs

Future studies could examine how changing pattern-buffer capacity, context tracking resources, or prediction configuration affects accuracy.

Such experiments could help characterize the trade-off between prediction accuracy and predictor resource usage.

### 5.6.5 Analyze Workload-Specific Behavior

Additional analysis could investigate why the magnitude of MPKI reduction differs across Kafka, TPCC, NodeApp, Spring, and Tomcat.

This may involve examining branch characteristics, execution-history correlations, and predictor utilization statistics where available.

### 5.6.6 Evaluate Full-System Performance

A future extension could integrate the predictor with a suitable processor performance simulation environment.

This would allow investigation of whether improved branch prediction accuracy translates into overall performance improvements under controlled system assumptions.

## 5.7 Final Conclusion

This project successfully reproduced and evaluated selected configurations of the LLBP-X branch predictor using a publicly available simulation framework.

Across five benchmark workloads, LLBP-X consistently achieved lower ROI MPKI than the evaluated LLBP configuration.

In the timing-aware experiments, LLBP-X achieved an arithmetic mean workload-specific MPKI reduction of approximately 5.25% and avoided 145,125 branch mispredictions across five benchmark pairs.

The additional adaptation-threshold experiment showed that changing the default threshold from 7 to 9 did not improve prediction accuracy under the selected conditions.

Overall, the results support the effectiveness of LLBP-X for improving simulated branch prediction accuracy on the evaluated workloads.

The study provides a foundation for broader benchmark evaluation, more extensive parameter exploration, and future investigation of branch prediction performance trade-offs.
