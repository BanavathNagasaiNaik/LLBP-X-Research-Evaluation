
import csv
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent
INPUT = BASE / "data/timing_roi_results.csv"
OUTPUT = BASE / "graphs"

OUTPUT.mkdir(parents=True, exist_ok=True)

benchmarks = ["Kafka", "TPCC", "NodeApp"]
results = {}

with INPUT.open(newline="") as f:
    for row in csv.DictReader(f):
        key = (row["Benchmark"], row["Model"])
        results[key] = {
            "instructions": int(row["ROI Instructions"]),
            "misses": int(row["ROI Mispredictions"]),
        }

llbp = []
llbpx = []
improvements = []
misses_saved = []

for benchmark in benchmarks:
    a = results[(benchmark, "llbp-timing")]
    b = results[(benchmark, "llbpx-timing")]

    assert a["instructions"] == b["instructions"]

    mpki_a = a["misses"] * 1000 / a["instructions"]
    mpki_b = b["misses"] * 1000 / b["instructions"]

    llbp.append(mpki_a)
    llbpx.append(mpki_b)
    improvements.append((mpki_a - mpki_b) / mpki_a * 100)
    misses_saved.append(a["misses"] - b["misses"])

x = np.arange(len(benchmarks))
width = 0.35

# Graph 1: Timing-aware MPKI
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(x - width/2, llbp, width, label="LLBP-Timing")
ax.bar(x + width/2, llbpx, width, label="LLBP-X-Timing")

ax.set_xticks(x)
ax.set_xticklabels(benchmarks)
ax.set_ylabel("ROI MPKI (lower is better)")
ax.set_title("Timing-Aware Branch Predictor Comparison")
ax.legend()
ax.grid(axis="y", alpha=0.25)

fig.tight_layout()
fig.savefig(OUTPUT / "graph4_timing_mpki.png", dpi=300)
plt.close(fig)

# Graph 2: Percentage improvement
fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(benchmarks, improvements)

for bar, value in zip(bars, improvements):
    ax.text(
        bar.get_x() + bar.get_width()/2,
        bar.get_height() + 0.05,
        f"{value:.2f}%",
        ha="center"
    )

ax.set_ylabel("ROI MPKI Reduction (%)")
ax.set_title("LLBP-X-Timing Improvement Over LLBP-Timing")
ax.set_ylim(0, max(improvements) * 1.2)
ax.grid(axis="y", alpha=0.25)

fig.tight_layout()
fig.savefig(OUTPUT / "graph5_timing_improvement.png", dpi=300)
plt.close(fig)

# Graph 3: Mispredictions avoided
fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(benchmarks, misses_saved)

for bar, value in zip(bars, misses_saved):
    ax.text(
        bar.get_x() + bar.get_width()/2,
        bar.get_height() + 400,
        f"{value:,}",
        ha="center"
    )

ax.set_ylabel("Mispredictions Avoided")
ax.set_title("Branch Mispredictions Avoided by LLBP-X")
ax.set_ylim(0, max(misses_saved) * 1.2)
ax.grid(axis="y", alpha=0.25)

fig.tight_layout()
fig.savefig(OUTPUT / "graph6_timing_misses_saved.png", dpi=300)
plt.close(fig)

# Save summary
summary = BASE / "data/timing_comparison_summary.csv"

with summary.open("w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Benchmark",
        "LLBP MPKI",
        "LLBP-X MPKI",
        "MPKI Reduction (%)",
        "Mispredictions Avoided",
    ])

    for i, benchmark in enumerate(benchmarks):
        writer.writerow([
            benchmark,
            round(llbp[i], 6),
            round(llbpx[i], 6),
            round(improvements[i], 4),
            misses_saved[i],
        ])

print("=== Timing-Aware Results ===")

for i, benchmark in enumerate(benchmarks):
    print(
        f"{benchmark}: "
        f"LLBP={llbp[i]:.4f}, "
        f"LLBP-X={llbpx[i]:.4f}, "
        f"Improvement={improvements[i]:.2f}%, "
        f"Misses Saved={misses_saved[i]:,}"
    )

print(
    f"\nAverage improvement: "
    f"{np.mean(improvements):.2f}%"
)

print("\nThree timing-aware graphs generated successfully.")
