# Running This Project — Quick Reference for Graders

This file mirrors the README but is written as a linear checklist. Follow each step in order.

---

## What You Need

- Python **3.10 or 3.11** (not 3.12+)
- A webcam for the live demo (`main.py`)
- ~3 GB free disk space
- Internet access (first run downloads ~6 MB of YOLOv8 base weights)

---

## Checklist

### Environment Setup

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
#    Windows:
venv\Scripts\activate
#    Mac / Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

### To Run the Live Demo Only (no dataset needed)

The trained weights are already included in the repo at `runs/detect/drone_finetune/weights/best.pt`.

```bash
python src/main.py
```

- Opens webcam, detects drones/airplanes/helicopters in real time
- Servo commands print to the terminal (no Arduino required)
- Press **Q** to quit

---

### To Re-run the ML Evaluation (dataset required)

**Step 1 — Download the dataset**

Go to: https://www.kaggle.com/datasets/sshikamaru/drone-detection

Click Download, extract the zip, and place the files so the folder looks like:

```
dataset/
├── data.yaml        ← already in repo, do not replace
├── train/
│   ├── images/      ← put training images here
│   └── labels/
├── valid/
│   ├── images/
│   └── labels/
└── test/
    ├── images/
    └── labels/
```

**Step 2 — (Optional) Re-train the model**

```bash
python src/train.py
```

Takes 10–30 minutes. Skip this if you just want to evaluate — the trained weights are already included.

**Step 3 — Run evaluation**

```bash
python src/evaluate.py
```

Outputs to `results/`:
- `results_table.csv` — mAP50, Precision, Recall, Latency, FPS for both models
- `metrics_comparison.png` — accuracy bar chart
- `latency_comparison.png` — speed bar chart

Pre-computed results are already in `results/` if you do not want to re-run this.

---

## Common Issues

| Problem | Fix |
|---|---|
| `ModuleNotFoundError` | Make sure venv is activated, re-run `pip install -r requirements.txt` |
| Webcam not opening | Change `cv2.VideoCapture(0)` to `(1)` in `src/main.py` line 16 |
| `best.pt` not found | Run `python src/train.py` or restore from git |
| `data.yaml` not found | Complete the dataset setup above before running evaluate/train |
| PyTorch install error | Switch to Python 3.10 or 3.11 |
| CUDA warning | Normal on CPU-only machines — inference is still ~9 ms/frame |
