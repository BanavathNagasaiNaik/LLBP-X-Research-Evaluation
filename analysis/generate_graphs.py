
import csv
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent
DATA_DIR = BASE / "data"
GRAPH_DIR = BASE / "graphs"

GRAPH_DIR.mkdir(parents=True, exist_ok=True)

benchmarks = ["Kafka", "TPCC", "NodeApp"]

models = {
    "tage64kscl": "TAGE-SC-L",
    "llbp": "LLBP",
    "llbpx": "LLBP-X",
    "llbpx-threshold9": "LLBP-X Threshold 9",
}

results = {name: {} for name in models.values()}

# Load official ROI data
with open(DATA_DIR / "roi_results.csv", newline="") as f:
    reader = csv.DictReader(f)

    for row in reader:
        model = models[row["Model"]]
        benchmark = row["Benchmark"]
        results[model][benchmark] = float(row["ROI MPKI"])

# Build arrays in benchmark order
values = {
    model: np.array([data[b] for b in benchmarks])
    for model, data in results.items()
}

tage = values["TAGE-SC-L"]
llbp = values["LLBP"]
llbpx = values["LLBP-X"]
threshold9 = values["LLBP-X Threshold 9"]

reduction_llbp = (llbp - llbpx) / llbp * 100
reduction_tage = (tage - llbpx) / tage * 100
threshold_change = (threshold9 - llbpx) / llbpx * 100

# Graph 1: Absolute ROI MPKI
x = np.arange(len(benchmarks))
width = 0.2

fig, ax = plt.subplots(figsize=(11, 6))

for i, (model, data) in enumerate(values.items()):
    ax.bar(
        x + (i - 1.5) * width,
        data,
        width,
        label=model
    )

ax.set_xlabel("Benchmark")
ax.set_ylabel("ROI Branch MPKI (lower is better)")
ax.set_title("Branch Predictor Comparison Using ROI MPKI")
ax.set_xticks(x)
ax.set_xticklabels(benchmarks)
ax.legend()
ax.grid(axis="y", alpha=0.25)

fig.tight_layout()
fig.savefig(
    GRAPH_DIR / "graph1_roi_mpki_comparison.png",
    dpi=300
)
plt.close(fig)

# Graph 2: LLBP-X improvement over LLBP
fig, ax = plt.subplots(figsize=(9, 5))

bars = ax.bar(benchmarks, reduction_llbp)

for bar, value in zip(bars, reduction_llbp):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.05,
        f"{value:.2f}%",
        ha="center"
    )

ax.set_ylabel("ROI MPKI Reduction (%)")
ax.set_title("LLBP-X Improvement Over LLBP")
ax.set_ylim(0, max(reduction_llbp) * 1.2)
ax.grid(axis="y", alpha=0.25)

fig.tight_layout()
fig.savefig(
    GRAPH_DIR / "graph2_roi_llbpx_improvement.png",
    dpi=300
)
plt.close(fig)

# Graph 3: Threshold sensitivity
fig, ax = plt.subplots(figsize=(9, 5))

bars = ax.bar(benchmarks, threshold_change)

for bar, value in zip(bars, threshold_change):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.01,
        f"+{value:.2f}%",
        ha="center"
    )

ax.set_ylabel("ROI MPKI Increase (%)")
ax.set_title("Threshold 9 vs Original LLBP-X")
ax.set_ylim(0, max(threshold_change) * 1.2)
ax.grid(axis="y", alpha=0.25)

fig.tight_layout()
fig.savefig(
    GRAPH_DIR / "graph3_roi_threshold_sensitivity.png",
    dpi=300
)
plt.close(fig)

# Save corrected summary
with open(
    DATA_DIR / "roi_comparison_summary.csv",
    "w",
    newline=""
) as f:
    writer = csv.writer(f)
    writer.writerow([
        "Benchmark",
        "LLBP-X vs LLBP (%)",
        "LLBP-X vs TAGE-SC-L (%)",
        "Threshold9 MPKI Increase (%)"
    ])

    for i, benchmark in enumerate(benchmarks):
        writer.writerow([
            benchmark,
            round(reduction_llbp[i], 4),
            round(reduction_tage[i], 4),
            round(threshold_change[i], 4)
        ])

print("=== Corrected ROI MPKI Results ===")

for i, benchmark in enumerate(benchmarks):
    print(
        f"{benchmark}: "
        f"LLBP-X vs LLBP = {reduction_llbp[i]:.2f}%, "
        f"LLBP-X vs TAGE = {reduction_tage[i]:.2f}%, "
        f"Threshold 9 increase = {threshold_change[i]:.2f}%"
    )

print(
    f"\nAverage LLBP-X improvement vs LLBP: "
    f"{np.mean(reduction_llbp):.2f}%"
)

print("\nROI graphs generated successfully.")
