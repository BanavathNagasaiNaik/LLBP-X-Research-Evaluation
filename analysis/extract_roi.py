import csv
import re
from pathlib import Path

root = Path("results/step7")
output = Path("analysis/data/roi_results.csv")

benchmarks = {
    "Kafka": "kafka",
    "TPCC": "benchbase-tpcc",
    "NodeApp": "nodeapp-nodeapp",
}

models = [
    "tage64kscl",
    "llbp",
    "llbpx",
    "llbpx-threshold9",
]

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

        rows.append([
            benchmark,
            model,
            instructions,
            mispredictions,
            round(mispredictions * 1000 / instructions, 6),
        ])

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
