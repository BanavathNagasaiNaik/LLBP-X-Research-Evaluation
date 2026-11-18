
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

ROOT = Path(__file__).resolve().parent
FIGURES = ROOT.parent.parent / "analysis" / "graphs"
OUTPUT = ROOT / "LLBPX_Research_Presentation.pptx"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

NAVY = RGBColor(20, 35, 65)
BLUE = RGBColor(35, 95, 175)
DARK = RGBColor(45, 50, 60)

def add_text(slide, x, y, w, h, content, size=20, color=DARK):
    box = slide.shapes.add_textbox(
        Inches(x), Inches(y), Inches(w), Inches(h)
    )
    tf = box.text_frame
    tf.word_wrap = True
    for i, line in enumerate(content.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.font.size = Pt(size)
        p.font.color.rgb = color
        p.space_after = Pt(12)
    return box

def new_slide(title, body=None, image=None):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_text(slide, 0.7, 0.35, 12, 0.65, title, 30, NAVY)

    if body:
        add_text(slide, 0.85, 1.35, 11.7, 5.6, body, 20)

    if image:
        path = FIGURES / image
        if not path.is_file():
            raise FileNotFoundError(f"Missing graph: {path}")
        slide.shapes.add_picture(
            str(path), Inches(1.25), Inches(1.35),
            width=Inches(10.8), height=Inches(5.35)
        )

    return slide


def add_extra_graph(slide, filename, x, y, w, h):
    path = FIGURES / filename

    if not path.is_file():
        raise FileNotFoundError(f"Missing graph: {path}")

    slide.shapes.add_picture(
        str(path),
        Inches(x),
        Inches(y),
        width=Inches(w),
        height=Inches(h)
    )


new_slide(
    "Reproduction and Experimental Evaluation of LLBP-X",
    "Final-Year Research Project\n"
    "Computer Science and Engineering\n"
    "The Last-Level Branch Predictor Revisited"
)

new_slide(
    "Introduction",
    "Modern processors use branch prediction to reduce pipeline stalls.\n"
    "Incorrect predictions waste execution cycles.\n"
    "TAGE-SC-L provides a strong conventional baseline.\n"
    "LLBP-X targets difficult-to-predict branches."
)

new_slide(
    "Problem Statement",
    "Some branches depend on complex execution histories.\n"
    "Conventional predictors may not capture all correlations.\n"
    "Research question: Can LLBP-X reduce mispredictions?"
)

new_slide(
    "Research Objectives",
    "Study TAGE-SC-L, LLBP and LLBP-X.\n"
    "Build and evaluate the public LLBP-X simulator.\n"
    "Compare prediction accuracy using ROI MPKI.\n"
    "Investigate adaptation-threshold sensitivity."
)

new_slide(
    "Literature Review",
    "TAGE-SC-L: Tagged history, statistical correction, loops.\n"
    "LLBP: Additional long-range prediction mechanism.\n"
    "LLBP-X: Adaptive last-level branch prediction.\n"
    "Reference: The Last-Level Branch Predictor Revisited."
)

new_slide(
    "LLBP-X System Architecture",
    "TAGE-SC-L base predictor.\n"
    "Context tracking structures.\n"
    "Pattern storage and pattern buffer.\n"
    "Adaptive prediction configuration.\n"
    "Integration with final branch prediction."
)

new_slide(
    "Working Mechanism",
    "1. Receive branch address and execution history.\n"
    "2. Generate base prediction.\n"
    "3. Consult context-based prediction information.\n"
    "4. Apply predictor selection and adaptation logic.\n"
    "5. Update predictor state after branch resolution."
)

new_slide(
    "Implementation",
    "Language: C++ | Build: CMake | Platform: Ubuntu WSL2.\n"
    "Simulator executable: build/predictor.\n"
    "Custom model: llbpx-threshold9.\n"
    "Default adaptation threshold: 7.\n"
    "Experimental adaptation threshold: 9."
)

new_slide(
    "Experimental Setup",
    "Benchmarks: Kafka, TPCC, NodeApp, Spring, Tomcat.\n"
    "Zero-latency: 20 simulations, 100M measurement instructions.\n"
    "Timing-aware: 10 simulations, 200M measurement instructions.\n"
    "Warmup: 100M instructions in both sets.\n"
    "Metric: Region of Interest MPKI."
)

new_slide(
    "Zero-Latency ROI MPKI",
    image="graph7_5bench_roi_mpki.png"
)

new_slide(
    "Adaptation-Threshold Analysis",
    image="graph9_5bench_threshold.png"
)

new_slide(
    "Timing-Aware ROI MPKI",
    image="graph10_5bench_timing_mpki.png"
)

new_slide(
    "Performance Analysis",
    "Timing-aware MPKI reduction over LLBP:\n"
    "Kafka: 4.43% | TPCC: 4.15% | NodeApp: 3.09%.\n"
    "Spring: 12.65% | Tomcat: 1.93%.\n"
    "Mean timing-aware reduction: 5.25%.\n"
    "Mean zero-latency reduction: 5.36%.\n"
    "Total timing-aware mispredictions avoided: 145,125."
)

new_slide(
    "Limitations and Future Work",
    "Evaluated 5 of the 14 benchmark workloads.\n"
    "Results measure simulated prediction accuracy.\n"
    "Different measurement lengths across experiment sets.\n"
    "Future work: full benchmark suite and threshold sweeps."
)

new_slide(
    "Conclusion and References",
    "LLBP-X achieved lower ROI MPKI than LLBP on all 5 workloads.\n"
    "Threshold 9 did not outperform default threshold 7.\n"
    "This is a partial reproduction of the published evaluation.\n\n"
    "Paper: The Last-Level Branch Predictor Revisited (HPCA 2026).\n"
    "Repository: github.com/dhschall/LLBP-X"
)


# Layout adjustments for the additional graphs

# Slide 10: Resize the existing MPKI graph to the left half.
slide10 = prs.slides[9]

for shape in slide10.shapes:
    if shape.shape_type == 13:
        shape.left = Inches(0.5)
        shape.top = Inches(1.5)
        shape.width = Inches(6.1)
        shape.height = Inches(4.7)

# Slide 13: Move the existing text above the graphs.
slide13 = prs.slides[12]

for shape in slide13.shapes:
    if shape.has_text_frame:
        if shape.top > Inches(1.0):
            shape.left = Inches(0.8)
            shape.top = Inches(1.2)
            shape.width = Inches(11.8)
            shape.height = Inches(2.1)


# Slide 10: Additional zero-latency improvement graph
add_extra_graph(
    prs.slides[9],
    "graph8_5bench_improvement.png",
    6.8, 1.5, 6.0, 4.7
)


# Slide 13: Timing-aware percentage improvement
add_extra_graph(
    prs.slides[12],
    "graph11_5bench_timing_improvement.png",
    0.7, 3.6, 5.8, 3.0
)

# Slide 13: Timing-aware mispredictions avoided
add_extra_graph(
    prs.slides[12],
    "graph12_5bench_timing_misses_saved.png",
    6.8, 3.6, 5.8, 3.0
)


assert len(prs.slides) == 15
prs.save(OUTPUT)

print(f"Presentation created: {OUTPUT}")
print(f"Total slides: {len(prs.slides)}")
