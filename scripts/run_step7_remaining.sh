
#!/bin/bash

set -euo pipefail

TRACES=(
    "benchbase-tpcc"
    "nodeapp-nodeapp"
)

MODELS=(
    "tage64kscl"
    "llbp"
    "llbpx"
    "llbpx-threshold9"
)

WARMUP=100000000
SIMULATE=100000000

for trace in "${TRACES[@]}"; do

    TRACE_FILE="traces/${trace}.champsim.trace.gz"
    OUTDIR="results/step7/${trace}"

    if [ ! -s "$TRACE_FILE" ]; then
        echo "ERROR: Missing trace $TRACE_FILE"
        exit 1
    fi

    mkdir -p "$OUTDIR"

    for model in "${MODELS[@]}"; do

        echo "======================================"
        echo "Benchmark: $trace"
        echo "Predictor: $model"
        echo "======================================"

        ./build/predictor \
            -b "$model" \
            -i "$TRACE_FILE" \
            --simulate-btb \
            -w "$WARMUP" \
            -n "$SIMULATE" \
            -o "$OUTDIR/$model" \
            > "$OUTDIR/$model.log" 2>&1

        echo "Completed: $trace / $model"

        grep 'MPKI:: TAGE:' "$OUTDIR/$model.log" | tail -1

    done
done

echo "ALL EXPERIMENTS COMPLETED"
