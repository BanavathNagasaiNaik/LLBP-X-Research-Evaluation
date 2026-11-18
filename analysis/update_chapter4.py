from pathlib import Path
import csv, re, shutil
from datetime import datetime

ROOT = Path.cwd()
REPORT = ROOT / 'documentation/report/04_results.md'
ZERO = ROOT / 'analysis/data/roi_results_5bench.csv'
TIMING = ROOT / 'analysis/data/timing_roi_results_5bench.csv'
GRAPHS = ROOT / 'analysis/graphs'
ORDER = ['Kafka', 'TPCC', 'NodeApp', 'Spring', 'Tomcat']
ZERO_MODELS = ['tage64kscl', 'llbp', 'llbpx', 'llbpx-threshold9']
TIMING_MODELS = ['llbp-timing', 'llbpx-timing']
FIGURES = ['graph7_5bench_roi_mpki.png','graph8_5bench_improvement.png','graph9_5bench_threshold.png','graph10_5bench_timing_mpki.png','graph11_5bench_timing_improvement.png','graph12_5bench_timing_misses_saved.png']
PAPER_TAGE = {'Kafka':0.26,'TPCC':3.74,'NodeApp':4.43,'Spring':3.58,'Tomcat':3.40}

def load(path, models):
    with path.open(newline='', encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == len(ORDER)*len(models), f'Unexpected row count in {path}'
    data = {}
    for row in rows:
        bench = row['Benchmark'].strip()
        model = row['Model'].strip()
        assert bench in ORDER and model in models, f'Unexpected benchmark/model: {bench}/{model}'
        key = (bench, model)
        assert key not in data, f'Duplicate row: {key}'
        data[key] = {'mpki':float(row['ROI MPKI']), 'misses':int(float(row['ROI Mispredictions'])), 'instructions':int(float(row['ROI Instructions']))}
    assert all((b,m) in data for b in ORDER for m in models), 'Missing benchmark/model pair'
    return data

def reduction(baseline, proposed):
    return 100*(baseline-proposed)/baseline

def mean(values):
    return sum(values)/len(values)

def table(headers, rows):
    return '\n'.join(['| ' + ' | '.join(headers) + ' |', '|' + '|'.join(['---' if i == 0 else '---:' for i in range(len(headers))]) + '|'] + ['| ' + ' | '.join(map(str, row)) + ' |' for row in rows])

def image(number, name, title):
    return f'![Figure 4.{number}: {title}](../../analysis/graphs/{name})\n\n**Figure 4.{number}:** {title}.'

zero = load(ZERO, ZERO_MODELS)
timing = load(TIMING, TIMING_MODELS)
assert REPORT.is_file(), 'Chapter 4 report missing'
for graph in FIGURES:
    assert (GRAPHS/graph).is_file(), f'Missing graph: {graph}'
assert all(v['instructions'] > 0 for v in [*zero.values(), *timing.values()])

zimp = {b:reduction(zero[b,'llbp']['mpki'],zero[b,'llbpx']['mpki']) for b in ORDER}
timp = {b:reduction(timing[b,'llbp-timing']['mpki'],timing[b,'llbpx-timing']['mpki']) for b in ORDER}
tageimp = {b:reduction(zero[b,'tage64kscl']['mpki'],zero[b,'llbpx']['mpki']) for b in ORDER}
saved = {b:timing[b,'llbp-timing']['misses']-timing[b,'llbpx-timing']['misses'] for b in ORDER}

# Verify the previously reported benchmark outcomes before replacing any text.
assert all(zero[b,'llbpx']['mpki'] < zero[b,m]['mpki'] for b in ORDER for m in ['tage64kscl','llbp','llbpx-threshold9'])
assert all(timing[b,'llbpx-timing']['mpki'] < timing[b,'llbp-timing']['mpki'] for b in ORDER)
assert sum(saved.values()) == 145125, f'Unexpected total misses saved: {sum(saved.values())}'

sections = {}
sections['4.1'] = '''## 4.1 Introduction

This chapter presents the five-benchmark experimental evaluation of TAGE-SC-L, LLBP, LLBP-X, and the modified LLBP-X adaptation-threshold configuration. The evaluation comprises **20 zero-latency** and **10 timing-aware** simulations on Kafka, BenchBase TPCC, NodeApp, DaCapo Spring, and DaCapo Tomcat: **30 simulations in total**.

The primary accuracy metric is Region of Interest (ROI) mispredictions per thousand instructions (MPKI). Lower MPKI indicates fewer branch mispredictions per thousand instructions. Results are reported for the simulator's measured ROI, not its warmup period.
'''
sections['4.2'] = '''## 4.2 Zero-Latency Predictor Results

The four zero-latency predictor configurations were evaluated with 100 million warmup instructions, 100 million requested measurement instructions, and BTB simulation enabled.

**Table 4.1: Zero-Latency ROI MPKI Comparison**

'''+table(['Benchmark','TAGE-SC-L','LLBP','LLBP-X','LLBP-X Threshold-9'],[[b]+[f"{zero[b,m]['mpki']:.5f}" for m in ZERO_MODELS] for b in ORDER])+'''

'''+image(1,FIGURES[0],'Zero-latency ROI MPKI comparison across five benchmarks')+'''

### 4.2.1 Observations

LLBP-X has the lowest measured ROI MPKI among all four configurations on **all five benchmarks**. The largest relative improvement over LLBP occurs on Spring; Tomcat shows the smallest relative improvement. The direction of the result is consistent across Kafka, TPCC, NodeApp, Spring, and Tomcat.
'''
sections['4.3'] = '''## 4.3 Zero-Latency Percentage Improvement

For each workload, percentage MPKI reduction is computed as `(Baseline MPKI - LLBP-X MPKI) / Baseline MPKI × 100`. The reported average is the arithmetic mean of the five workload-level percentages, not the percentage change between average MPKI values.

**Table 4.2: LLBP-X MPKI Reduction Relative to LLBP**

'''+table(['Benchmark','MPKI Reduction'],[[b,f'{zimp[b]:.2f}%'] for b in ORDER]+[['Arithmetic mean of workload reductions',f'{mean(list(zimp.values())):.2f}%']])+'''

'''+image(2,FIGURES[1],'Zero-latency LLBP-X MPKI reduction relative to LLBP')+'''

**Table 4.2a: LLBP-X MPKI Reduction Relative to TAGE-SC-L**

'''+table(['Benchmark','MPKI Reduction'],[[b,f'{tageimp[b]:.2f}%'] for b in ORDER]+[['Arithmetic mean of workload reductions',f'{mean(list(tageimp.values())):.2f}%']])+'''

The largest relative reduction against LLBP occurs on Spring. LLBP-X also reduces MPKI against TAGE-SC-L on every evaluated workload.
'''
sections['4.4'] = '''## 4.4 Adaptation-Threshold Sensitivity

The experimental `llbpx-threshold9` configuration increases the adaptation threshold from the default value of 7 to 9 while retaining the same zero-latency simulation parameters.

**Table 4.3: Adaptation-Threshold Comparison**

'''+table(['Benchmark','Default Threshold-7 MPKI','Modified Threshold-9 MPKI'],[[b,f"{zero[b,'llbpx']['mpki']:.5f}",f"{zero[b,'llbpx-threshold9']['mpki']:.5f}"] for b in ORDER])+'''

'''+image(3,FIGURES[2],'Adaptation-threshold sensitivity across five benchmarks')+'''

The threshold-9 variant has slightly higher MPKI than the default threshold-7 configuration on **all five workloads**. This experiment does not establish that threshold 7 is globally optimal; only one alternative threshold was evaluated.
'''
sections['4.5'] = '''## 4.5 Timing-Aware Predictor Results

The timing-aware configurations `llbp-timing` and `llbpx-timing` were evaluated using 100 million warmup instructions, 200 million requested measurement instructions, and BTB simulation enabled.

**Table 4.4: Timing-Aware ROI MPKI Comparison**

'''+table(['Benchmark','LLBP MPKI','LLBP-X MPKI'],[[b,f"{timing[b,'llbp-timing']['mpki']:.6f}",f"{timing[b,'llbpx-timing']['mpki']:.6f}"] for b in ORDER])+'''

'''+image(4,FIGURES[3],'Timing-aware ROI MPKI comparison across five benchmarks')+'''

LLBP-X records lower timing-aware ROI MPKI than LLBP on every evaluated workload. The zero-latency and timing-aware experiments use different measurement intervals, so their absolute MPKI values should not be compared to isolate a timing effect.
'''
sections['4.6'] = '''## 4.6 Timing-Aware Percentage Improvement

**Table 4.5: Timing-Aware MPKI Reduction Relative to LLBP**

'''+table(['Benchmark','LLBP-X Improvement'],[[b,f'{timp[b]:.2f}%'] for b in ORDER]+[['Arithmetic mean of workload reductions',f'{mean(list(timp.values())):.2f}%']])+'''

'''+image(5,FIGURES[4],'Timing-aware LLBP-X MPKI reduction relative to LLBP')+'''

The arithmetic mean of the five workload-level reductions is **'''+f'{mean(list(timp.values())):.2f}%'+'''**. This workload-average percentage is not equivalent to the reduction computed from the mean of raw MPKI values; the latter weights the workloads differently.
'''
sections['4.7'] = '''## 4.7 Reduction in Branch Mispredictions

**Table 4.6: Timing-Aware ROI Mispredictions**

'''+table(['Benchmark','LLBP Mispredictions','LLBP-X Mispredictions','Mispredictions Avoided'],[[b,f"{timing[b,'llbp-timing']['misses']:,}",f"{timing[b,'llbpx-timing']['misses']:,}",f'{saved[b]:,}'] for b in ORDER]+[['Total',f"{sum(timing[b,'llbp-timing']['misses'] for b in ORDER):,}",f"{sum(timing[b,'llbpx-timing']['misses'] for b in ORDER):,}",f'{sum(saved.values()):,}']])+'''

'''+image(6,FIGURES[5],'Timing-aware branch mispredictions avoided across five benchmarks')+'''

Across the five separately simulated workloads, LLBP-X records **'''+f'{sum(saved.values()):,}'+''' fewer ROI branch mispredictions than LLBP. This total sums five independent benchmark runs; it is not a single application-level speedup measurement.
'''
sections['4.8'] = '''## 4.8 Discussion and Comparison with the Original Paper

The experimental trend supports the paper's central finding that LLBP-X can improve branch prediction accuracy over LLBP and a TAGE-SC-L baseline. Across the five selected workloads, LLBP-X improves zero-latency MPKI over LLBP by an arithmetic mean of **'''+f'{mean(list(zimp.values())):.2f}%'+'''** and over TAGE-SC-L by **'''+f'{mean(list(tageimp.values())):.2f}%'+'''**. The timing-aware reduction over LLBP averages **'''+f'{mean(list(timp.values())):.2f}%'+'''**.

**Table 4.7: Published TAGE-SC-L MPKI Reference Values Versus This Project**

'''+table(['Benchmark','Paper TAGE-SC-L MPKI','Project TAGE-SC-L MPKI','Project vs. Paper'],[[b,f'{PAPER_TAGE[b]:.2f}',f"{zero[b,'tage64kscl']['mpki']:.5f}",f"{reduction(PAPER_TAGE[b],zero[b,'tage64kscl']['mpki'])*-1:+.1f}%"] for b in ORDER])+'''

*Paper values in Table 4.7 are reference values transcribed during the project review from Table I of the original research paper. Verify the transcription against the paper before final submission. The difference column is `(Project - Paper) / Paper × 100`; it is a comparison of measured MPKI, not a speedup.*

The published study evaluates **14 workloads** and reports broader aggregate results. This project covers **five** of those workloads, and the zero-latency measurement window used here is **100 million instructions**, rather than the **200 million ROI instructions** used in the paper's reported evaluation. Consequently, the two studies' absolute MPKI and aggregate improvement figures are not directly interchangeable. Differences may arise from ROI selection, trace processing, simulator settings, and the smaller benchmark subset. The project reproduces a consistent improvement trend, not an exact numerical replication of the full paper.

The results do not isolate the contribution of individual internal LLBP-X mechanisms, and no full-system IPC or execution-time speedup was measured.
'''
sections['4.9'] = '''## 4.9 Limitations of the Results

1. Only **five of the original fourteen workloads** were evaluated.
2. Results come from branch predictor simulations rather than full-system processor performance measurements.
3. Zero-latency and timing-aware experiments use different ROI lengths (100 million versus 200 million requested instructions), so differences between the two sets cannot be attributed solely to timing effects.
4. The adaptation-threshold experiment compares only thresholds 7 and 9.
5. Absolute MPKI comparisons with the paper are affected by differences in experimental windows and potentially other settings.
6. The evaluation reports branch prediction accuracy; it does not establish processor speedup, energy efficiency, or silicon area.

Accordingly, this is a partial reproduction and focused experimental evaluation, not a complete replication of the published study.
'''
sections['4.10'] = '''## 4.10 Summary

The 30 simulations cover five benchmarks and six predictor configurations across two experiment sets. LLBP-X improves zero-latency ROI MPKI over LLBP by an arithmetic mean of **'''+f'{mean(list(zimp.values())):.2f}%'+'''**, and timing-aware ROI MPKI by **'''+f'{mean(list(timp.values())):.2f}%'+'''**. The threshold-9 variant does not outperform the default threshold-7 configuration on any of the five benchmarks. The timing-aware LLBP-X runs record **'''+f'{sum(saved.values()):,}'+''' fewer mispredictions in total than the corresponding LLBP runs.

The improvements are consistent with the direction of the original paper's findings, while the smaller benchmark set and different experimental windows limit direct numerical comparisons. Chapter 5 presents conclusions and future work.
'''

original = REPORT.read_text(encoding='utf-8')
for num in sections:
    assert len(re.findall(rf'^## {re.escape(num)}\b', original, flags=re.M)) == 1, f'Missing or duplicate heading {num}'
assert len(re.findall(r'^## 4\.\d+\b', original, flags=re.M)) == 10, 'Unexpected Chapter 4 structure'
updated = '# Chapter 4: Experimental Results and Discussion\n\n'+'\n'.join(sections[num].rstrip() for num in sections)+'\n'
assert updated.count('](../../analysis/graphs/') == 6
for match in re.findall(r'!\[[^\]]+\]\(([^)]+)\)', updated):
    assert (REPORT.parent/match).is_file(), f'Broken figure path: {match}'
backup = REPORT.with_name('04_results_backup_'+datetime.now().strftime('%Y%m%d_%H%M%S')+'.md')
shutil.copy2(REPORT, backup)
REPORT.write_text(updated, encoding='utf-8')
print('SUCCESS: Chapter 4 updated (Sections 4.1–4.10)')
print('Backup:', backup)
print('Verified: 20 zero-latency rows, 10 timing-aware rows, 6 existing figure paths')
print(f'Zero-latency mean MPKI reduction vs LLBP: {mean(list(zimp.values())):.2f}%')
print(f'Zero-latency mean MPKI reduction vs TAGE-SC-L: {mean(list(tageimp.values())):.2f}%')
print(f'Timing-aware mean MPKI reduction vs LLBP: {mean(list(timp.values())):.2f}%')
print(f'Timing-aware mispredictions avoided: {sum(saved.values()):,}')
print('NOTE: Verify original-paper reference values against Table I before final submission.')
