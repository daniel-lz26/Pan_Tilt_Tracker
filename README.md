# Pan-Tilt Tracker — Edge AI Aerial Object Detection

A real-time object detection and tracking system that fine-tunes YOLOv8n on a custom drone dataset (Drones, Airplanes, Helicopters) and compares it against the COCO baseline model. Built for CPSC 483.

The system uses a webcam, runs inference locally, and outputs directional servo commands (pan/tilt). No Arduino hardware is required to run the ML experiment — serial communication is simulated by default.

---

## Required Libraries

```
ultralytics
opencv-python
numpy
pyserial
matplotlib
```

All exact pinned versions are listed in `requirements.txt`.

---

## Installation

**Step 1 — Create a virtual environment**

```bash
python -m venv venv
```

**Step 2 — Activate the virtual environment**

Windows:
```bash
venv\Scripts\activate
```

Mac / Linux:
```bash
source venv/bin/activate
```

**Step 3 — Install all dependencies**

```bash
pip install -r requirements.txt
```

---

## Dataset Setup

The dataset is too large to include in the repository and must be downloaded manually.

**Source:** https://www.kaggle.com/datasets/sshikamaru/drone-detection

**Download steps:**
1. Create a free Kaggle account if you do not have one
2. Go to the URL above and click **Download**
3. Extract the zip file

**Required folder structure** (place files inside the existing `dataset/` folder):

```
dataset/
├── data.yaml              ← already provided in the repo, do not replace
├── train/
│   ├── images/            ← place training .jpg images here
│   └── labels/            ← place training .txt label files here
├── valid/
│   ├── images/
│   └── labels/
└── test/
    ├── images/
    └── labels/
```

**Contents of `dataset/data.yaml`** (already included — shown here for reference):

```yaml
train: ../dataset/train/images
val:   ../dataset/valid/images
test:  ../dataset/test/images

nc: 3
names: ['AirPlane', 'Drone', 'Helicopter']
```

> The dataset is only required to run `train.py` or `evaluate.py`. The live demo (`main.py`) works without it because the trained weights are already included.

---

## How to Run

All commands are run from the **project root directory** (the folder containing `src/`, `dataset/`, etc.).

### 1. Fine-tune the model

```bash
python src/train.py
```

- Fine-tunes YOLOv8n on the drone dataset for 50 epochs
- Requires the dataset to be set up first (see Dataset Setup above)
- Takes approximately 10–30 minutes depending on hardware
- Saves weights to `runs/detect/drone_finetune/weights/best.pt`

### 2. Evaluate and compare models

```bash
python src/evaluate.py
```

- Requires the dataset and `runs/detect/drone_finetune/weights/best.pt`
- Compares the COCO baseline model vs the fine-tuned drone model
- Saves results to the `results/` folder:
  - `results/results_table.csv` — all metrics
  - `results/metrics_comparison.png` — mAP50, Precision, Recall bar chart
  - `results/latency_comparison.png` — inference speed bar chart

### 3. Run the live detection demo

```bash
python src/main.py
```

- Opens your webcam and runs the fine-tuned drone detector in real time
- Draws bounding boxes around detected objects
- Prints simulated servo commands to the terminal
- Shows live FPS in the video window
- Press **Q** to quit

> The pre-trained weights (`runs/detect/drone_finetune/weights/best.pt`) are included in the repository. You do not need to run `train.py` before running the demo.

---

## Project Structure

```
Pan_Tilt_Tracker/
├── src/
│   ├── main.py            # Live tracker — webcam + detection + servo commands
│   ├── train.py           # Fine-tunes YOLOv8n on the drone dataset
│   ├── evaluate.py        # Model comparison — outputs metrics and charts
│   ├── detector.py        # YOLOv8 inference wrapper
│   ├── controller.py      # Pan-tilt deadzone and angle logic
│   └── serial_comm.py     # Arduino serial communication (unused in sim mode)
├── arduino/
│   ├── tracker.ino        # Arduino firmware for servo control
│   └── test.ino           # Servo test sketch
├── dataset/
│   ├── data.yaml          # Dataset config (included)
│   ├── train/             # Training split (download separately)
│   ├── valid/             # Validation split (download separately)
│   └── test/              # Test split (download separately)
├── runs/
│   └── detect/drone_finetune/weights/
│       └── best.pt        # Trained model weights (included)
├── results/
│   ├── results_table.csv
│   ├── metrics_comparison.png
│   └── latency_comparison.png
└── requirements.txt
```

---

## Simulation Mode

Serial communication is disabled by default so the code runs on any machine without an Arduino.

In `src/main.py`, line 5:

```python
SIMULATE_SERIAL = True   # Set to False only when Arduino is physically connected
```

When `True`, servo commands are printed to the terminal instead of sent over USB. The ML experiment (train + evaluate) is entirely unaffected by this flag.

---

## ML Experiment Results

| Model | mAP50 | Precision | Recall | Latency (ms) | FPS |
|---|---|---|---|---|---|
| YOLOv8n (COCO baseline) | 0.0141 | 0.0274 | 0.0110 | 8.92 ms | 112.1 |
| YOLOv8n (Fine-tuned drone) | **0.9668** | **0.9249** | **0.9504** | 8.55 ms | 116.9 |

Fine-tuning on the drone-specific dataset improved mAP50 by **68.5×** with no increase in inference latency.

---

## Troubleshooting

**Webcam not found / black screen:**
- Make sure a webcam is connected and not open in another application
- If the default camera index does not work, change `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)` in `src/main.py` line 16

**`ModuleNotFoundError` on any import:**
- Confirm the virtual environment is activated (you should see `(venv)` in your prompt)
- Re-run `pip install -r requirements.txt`

**`FileNotFoundError: best.pt not found`:**
- The weights file should be at `runs/detect/drone_finetune/weights/best.pt`
- If it is missing, run `python src/train.py` (dataset required)

**`FileNotFoundError: data.yaml not found` or no training images:**
- Complete the Dataset Setup section above before running `train.py` or `evaluate.py`

**PyTorch fails to install:**
- Use Python 3.10 or 3.11 — PyTorch may not support Python 3.12+ on all platforms

**`UserWarning: CUDA not available` — inference is slow:**
- This is normal on a machine without a GPU
- CPU inference still runs at ~9 ms per frame (≈112 FPS) on the test results

---

## References

1. Jocher, G., et al. (2023). *Ultralytics YOLOv8*. https://github.com/ultralytics/ultralytics
2. Redmon, J., & Farhadi, A. (2018). *YOLOv3: An Incremental Improvement*. arXiv:1804.02767.
3. Kaggle Dataset: *Drone Detection* by sshikamaru. https://www.kaggle.com/datasets/sshikamaru/drone-detection
4. Bradski, G. (2000). *The OpenCV Library*. Dr. Dobb's Journal of Software Tools.
