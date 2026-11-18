import csv
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

source = Path("analysis/data/timing_roi_results_5bench.csv")
output = Path("analysis/graphs")
output.mkdir(parents=True, exist_ok=True)

benchmarks = ["Kafka", "TPCC", "NodeApp", "Spring", "Tomcat"]

data = {}

with source.open(newline="") as f:
    for row in csv.DictReader(f):
        data[(row["Benchmark"], row["Model"])] = {
            "mpki": float(row["ROI MPKI"]),
            "misses": int(row["ROI Mispredictions"])
        }

llbp = np.array([
    data[(b, "llbp-timing")]["mpki"]
    for b in benchmarks
])

llbpx = np.array([
    data[(b, "llbpx-timing")]["mpki"]
    for b in benchmarks
])

improvements = 100 * (llbp - llbpx) / llbp

misses_saved = np.array([
    data[(b, "llbp-timing")]["misses"]
    - data[(b, "llbpx-timing")]["misses"]
    for b in benchmarks
])

# Graph 10: Timing-aware MPKI comparison
x = np.arange(len(benchmarks))
width = 0.35

fig, ax = plt.subplots(figsize=(11, 6))

ax.bar(x - width / 2, llbp, width, label="LLBP")
ax.bar(x + width / 2, llbpx, width, label="LLBP-X")

ax.set_xticks(x)
ax.set_xticklabels(benchmarks)
ax.set_ylabel("ROI MPKI (lower is better)")
ax.set_title("Five-Benchmark Timing-Aware MPKI Comparison")
ax.legend()
ax.grid(axis="y", alpha=0.25)

fig.tight_layout()
fig.savefig(
    output / "graph10_5bench_timing_mpki.png",
    dpi=200
)
plt.close(fig)

# Graph 11: Timing-aware improvement
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
ax.set_title("Timing-Aware LLBP-X Improvement over LLBP")
ax.grid(axis="y", alpha=0.25)

fig.tight_layout()
fig.savefig(
    output / "graph11_5bench_timing_improvement.png",
    dpi=200
)
plt.close(fig)

# Graph 12: Mispredictions avoided
fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.bar(benchmarks, misses_saved)

for bar, value in zip(bars, misses_saved):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1500,
        f"{value:,}",
        ha="center"
    )

ax.set_ylim(0, max(misses_saved) * 1.2)
ax.set_ylabel("Branch mispredictions avoided")
ax.set_title("Timing-Aware Mispredictions Avoided by LLBP-X")
ax.grid(axis="y", alpha=0.25)

fig.tight_layout()
fig.savefig(
    output / "graph12_5bench_timing_misses_saved.png",
    dpi=200
)
plt.close(fig)

print("Generated 3 timing-aware graphs.")
print(f"Average MPKI improvement: {np.mean(improvements):.2f}%")
print(f"Total mispredictions avoided: {sum(misses_saved):,}")
