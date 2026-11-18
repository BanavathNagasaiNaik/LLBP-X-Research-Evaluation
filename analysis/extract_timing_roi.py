import csv
import re
from pathlib import Path

root = Path("results/step8/timing")
output = Path("analysis/data/timing_roi_results.csv")

benchmarks = {
    "Kafka": "kafka",
    "TPCC": "tpcc",
    "NodeApp": "nodeapp",
}

models = ["llbp-timing", "llbpx-timing"]

rows = []

for benchmark, folder in benchmarks.items():
    for model in models:
        log = root / folder / f"{model}.log"
        content = log.read_text()

        values = {}

        for label in [
            "ROI INSTRUCTIONS",
            "ROI MISPREDICTIONS",
            "ROI MPKI",
        ]:
            matches = re.findall(
                rf"^\s*{label}\s*:\s*([\d.]+)",
                content,
                re.MULTILINE,
            )
            if not matches:
                raise ValueError(f"Missing {label} in {log}")

            values[label] = matches[-1]

        instructions = int(values["ROI INSTRUCTIONS"])
        mispredictions = int(values["ROI MISPREDICTIONS"])
        mpki = mispredictions * 1000 / instructions

        rows.append([
            benchmark,
            model,
            instructions,
            mispredictions,
            round(mpki, 6),
        ])

output.parent.mkdir(parents=True, exist_ok=True)

with output.open("w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Benchmark",
        "Model",
        "ROI Instructions",
        "ROI Mispredictions",
        "ROI MPKI",
    ])
    writer.writerows(rows)

print(f"Successfully saved {len(rows)} results to {output}")
