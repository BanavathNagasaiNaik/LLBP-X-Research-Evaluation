import csv
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

source = Path("analysis/data/roi_results_5bench.csv")
out = Path("analysis/graphs")
out.mkdir(parents=True, exist_ok=True)

benchmarks = ["Kafka", "TPCC", "NodeApp", "Spring", "Tomcat"]

models = [
    "tage64kscl",
    "llbp",
    "llbpx",
    "llbpx-threshold9"
]

labels = [
    "TAGE-SC-L",
    "LLBP",
    "LLBP-X",
    "LLBP-X Threshold 9"
]

data = {}

with source.open(newline="") as f:
    for row in csv.DictReader(f):
        data[(row["Benchmark"], row["Model"])] = float(
            row["ROI MPKI"]
        )

# Graph 1: ROI MPKI comparison
x = np.arange(len(benchmarks))
width = 0.19

fig, ax = plt.subplots(figsize=(12, 6))

for i, model in enumerate(models):
    values = [data[(b, model)] for b in benchmarks]
    ax.bar(
        x + (i - 1.5) * width,
        values,
        width,
        label=labels[i]
    )

ax.set_xticks(x)
ax.set_xticklabels(benchmarks)
ax.set_ylabel("ROI MPKI (lower is better)")
ax.set_title("Five-Benchmark Branch Predictor Comparison")
ax.legend()
ax.grid(axis="y", alpha=0.25)

fig.tight_layout()
fig.savefig(
    out / "graph7_5bench_roi_mpki.png",
    dpi=200
)
plt.close(fig)

# Graph 2: Improvement over LLBP
improvements = [
    100 * (
        data[(b, "llbp")] - data[(b, "llbpx")]
    ) / data[(b, "llbp")]
    for b in benchmarks
]

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(benchmarks, improvements)

for bar, value in zip(bars, improvements):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.15,
        f"{value:.2f}%",
        ha="center"
    )

ax.set_ylim(0, max(improvements) * 1.2)
ax.set_ylabel("MPKI reduction (%)")
ax.set_title("LLBP-X Improvement over LLBP")
ax.grid(axis="y", alpha=0.25)

fig.tight_layout()
fig.savefig(
    out / "graph8_5bench_improvement.png",
    dpi=200
)
plt.close(fig)

# Graph 3: Threshold sensitivity
fig, ax = plt.subplots(figsize=(12, 6))

for i, model in enumerate(["llbpx", "llbpx-threshold9"]):
    values = [data[(b, model)] for b in benchmarks]
    ax.bar(
        x + (i - 0.5) * 0.35,
        values,
        0.35,
        label=["Default LLBP-X", "Threshold 9"][i]
    )

ax.set_xticks(x)
ax.set_xticklabels(benchmarks)
ax.set_ylabel("ROI MPKI (lower is better)")
ax.set_title("LLBP-X Adaptation Threshold Sensitivity")
ax.legend()
ax.grid(axis="y", alpha=0.25)

fig.tight_layout()
fig.savefig(
    out / "graph9_5bench_threshold.png",
    dpi=200
)
plt.close(fig)

print("Generated 3 five-benchmark graphs.")
print(f"Average improvement over LLBP: {np.mean(improvements):.2f}%")
