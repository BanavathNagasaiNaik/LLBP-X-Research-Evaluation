# LLBP-X Experimental Reproducibility Guide

## Scope and attribution

This project is a **partial reproduction and experimental extension** of *The Last-Level Branch Predictor Revisited* (HPCA 2026), using the publicly available [LLBP-X simulator](https://github.com/dhschall/LLBP-X). The original implementation and upstream scripts belong to their respective authors; preserve their copyright and license notices.

The project evaluates five traces, four zero-latency predictor configurations, and two timing-aware configurations. It does **not** reproduce all 14 workloads in the published study or demonstrate full-system speedup.

## Tested environment

- Ubuntu 22.04.5 under WSL2
- GCC 11.4, CMake 3.22, Python 3.10
- C++ predictor simulator: `build/predictor`
- Plotting dependencies: NumPy and Matplotlib
- Presentation dependency: python-pptx

These are the tested versions, not necessarily minimum requirements.

## Build

From the repository root:

```bash
cmake -S . -B build
cmake --build build --target predictor -j "$(nproc)"
```

The executable should be available at `build/predictor`.

## Obtain traces

Download the following `.champsim.trace.gz` files from [Zenodo record 13133243](https://zenodo.org/records/13133243) into the `traces/` directory:

| Benchmark | Trace filename |
|---|---|
| Kafka | `dacapo-kafka.champsim.trace.gz` |
| TPCC | `benchbase-tpcc.champsim.trace.gz` |
| NodeApp | `nodeapp-nodeapp.champsim.trace.gz` |
| Spring | `dacapo-spring.champsim.trace.gz` |
| Tomcat | `dacapo-tomcat.champsim.trace.gz` |

The upstream `scripts/download_traces.sh` downloads a **larger, 14-trace suite**, not just these five. The trace archives are large and should not be committed to Git.

## Zero-latency experiments

Models: `tage64kscl`, `llbp`, `llbpx`, `llbpx-threshold9`.

- Warmup: 100,000,000 instructions
- Measurement: 100,000,000 instructions
- BTB simulation: enabled
- Five traces × four models = **20 runs**

Example for Kafka / LLBP-X (create the output directory first):

```bash
mkdir -p results/reproduction/kafka
./build/predictor \
  -b llbpx \
  -i traces/dacapo-kafka.champsim.trace.gz \
  -o results/reproduction/kafka/llbpx \
  --simulate-btb \
  -w 100000000 -n 100000000 \
  > results/reproduction/kafka/llbpx.log 2>&1
```

Repeat for each of the five trace filenames and four model names, changing the output paths accordingly. `scripts/run_step7_remaining.sh` is a historical helper for **TPCC and NodeApp only**, not a complete five-benchmark runner.

## Timing-aware experiments

Models: `llbp-timing`, `llbpx-timing`.

- Warmup: 100,000,000 instructions
- Measurement: 200,000,000 instructions
- BTB simulation: enabled
- Five traces × two models = **10 runs**

Example for Kafka / timing-aware LLBP-X:

```bash
mkdir -p results/reproduction/timing/kafka
./build/predictor \
  -b llbpx-timing \
  -i traces/dacapo-kafka.champsim.trace.gz \
  -o results/reproduction/timing/kafka/llbpx-timing \
  --simulate-btb \
  -w 100000000 -n 200000000 \
  > results/reproduction/timing/kafka/llbpx-timing.log 2>&1
```

Repeat for the five traces and two timing-aware models. **Do not interpret differences between the 100M and 200M measurement windows as isolated timing effects.**

## Results, extraction and figures

Consolidated data used by the five-benchmark figures and report:

- `analysis/data/roi_results_5bench.csv` (20 model–benchmark rows)
- `analysis/data/timing_roi_results_5bench.csv` (10 model–benchmark rows)

Each row contains `Benchmark`, `Model`, `ROI Instructions`, `ROI Mispredictions`, and `ROI MPKI`.

**Extraction limitation:** `analysis/extract_roi.py` and `analysis/extract_timing_roi.py` currently process only Kafka, TPCC and NodeApp and output separate three-benchmark CSVs. They do **not** regenerate the five-benchmark CSVs. The five-benchmark CSVs should be retained as experimental artifacts until a consolidated extractor is implemented and validated against all run logs. The original run logs are distributed across `results/step7`, `results/step8/timing`, and `results/step10`.

Regenerate the six expanded figures from the consolidated CSVs:

```bash
python3 -m pip install numpy matplotlib
python3 analysis/plot_5bench.py
python3 analysis/plot_timing_5bench.py
```

The output files are `analysis/graphs/graph7_5bench_roi_mpki.png` through `graph12_5bench_timing_misses_saved.png` (six figures, numbered 7–12).

Regenerate the presentation:

```bash
python3 -m pip install python-pptx
python3 documentation/presentation/create_presentation.py
```

The presentation generator produces `documentation/presentation/LLBPX_Research_Presentation.pptx` with 15 slides and six embedded graphs.

## Reported findings

Arithmetic mean of **per-workload** MPKI reductions across five workloads:

| Comparison | Mean MPKI reduction |
|---|---:|
| Zero-latency LLBP-X vs LLBP | 5.36% |
| Zero-latency LLBP-X vs TAGE-SC-L | 16.95% |
| Timing-aware LLBP-X vs LLBP | 5.25% |

The five timing-aware LLBP-X runs collectively recorded **145,125 fewer ROI branch mispredictions** than the corresponding LLBP runs. The default adaptation threshold 7 had lower MPKI than threshold 9 for each of the five tested traces.

These are simulated branch-prediction metrics, **not** CPU performance or energy improvements. The original-paper Table I reference values used in `documentation/report/04_results.md` must be verified against the source paper before submission.

## Reproduction caveats

- Only five of the original study's 14 benchmarks are included.
- The two experiment sets have different measurement lengths.
- Published and locally measured MPKI may differ because of setup and measurement details.
- Upstream `scripts/eval_all.sh` and `scripts/eval_benchmarks.sh` target the broader upstream workflow, not exactly this project's 30-run matrix.
- Preserve upstream attribution and licenses when publishing; do not upload large traces, build artifacts, or temporary backups.
