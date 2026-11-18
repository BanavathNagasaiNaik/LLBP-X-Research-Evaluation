import csv
import re
from pathlib import Path

benchmarks = {
    "Kafka": ("step7/kafka", "step8/timing/kafka"),
    "TPCC": ("step7/benchbase-tpcc", "step8/timing/tpcc"),
    "NodeApp": ("step7/nodeapp-nodeapp", "step8/timing/nodeapp"),
    "Spring": ("step10/spring", "step10/timing/spring"),
    "Tomcat": ("step10/tomcat", "step10/timing/tomcat"),
}

groups = {
    "zero": [
        "tage64kscl", "llbp", "llbpx", "llbpx-threshold9"
    ],
    "timing": ["llbp-timing", "llbpx-timing"],
}

def extract(path):
    content = path.read_text()
    values = {}

    for label in ("ROI INSTRUCTIONS", "ROI MISPREDICTIONS"):
        matches = re.findall(
            rf"^\s*{label}\s*:\s*(\d+)",
            content,
            re.MULTILINE | re.IGNORECASE,
        )
        if not matches:
            raise ValueError(f"Missing {label}: {path}")
        values[label] = int(matches[-1])

    instructions = values["ROI INSTRUCTIONS"]
    misses = values["ROI MISPREDICTIONS"]

    if instructions <= 0:
        raise ValueError(f"Invalid instruction count: {path}")

    return instructions, misses, round(misses * 1000 / instructions, 6)

for group, models in groups.items():
    rows = []

    for benchmark, (zero_dir, timing_dir) in benchmarks.items():
        directory = zero_dir if group == "zero" else timing_dir

        for model in models:
            if benchmark == "Spring" and model == "tage64kscl":
                path = Path("results/step10/spring/tage64kscl_summary.txt")
            elif directory.startswith("step10"):
                path = Path("results") / directory / f"{model}_terminal.log"
            else:
                path = Path("results") / directory / f"{model}.log"

            if not path.exists() or path.stat().st_size == 0:
                print(f"UNVERIFIED: {benchmark} {model} ({path})")
                continue

            instructions, misses, mpki = extract(path)
            rows.append([benchmark, model, instructions, misses, mpki])

    output = Path(f"analysis/data/{group}_5bench_candidate.csv")
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Benchmark", "Model", "ROI Instructions",
            "ROI Mispredictions", "ROI MPKI"
        ])
        writer.writerows(rows)

    print(f"{group}: extracted {len(rows)} rows -> {output}")
