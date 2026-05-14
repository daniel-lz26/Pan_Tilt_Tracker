"""
Model comparison: COCO baseline YOLOv8n vs fine-tuned drone model.

Usage (run from project root after training):
    python src/evaluate.py

Outputs to results/:
    results_table.csv          - all 5 metrics for both models
    metrics_comparison.png     - grouped bar chart (mAP50, Precision, Recall)
    latency_comparison.png     - bar chart (latency ms and FPS)
"""

import os
import csv
import time
from pathlib import Path

import numpy as np
import cv2
import matplotlib.pyplot as plt
from ultralytics import YOLO


DATA_YAML = "dataset/data.yaml"
BASELINE_MODEL = "src/yolov8n.pt"
FINETUNED_MODEL = "runs/detect/drone_finetune/weights/best.pt"
RESULTS_DIR = Path("results")
LATENCY_WARMUP = 10
LATENCY_RUNS = 100


def measure_latency(model, val_image_path):
    """Run inference LATENCY_RUNS times on one image; return (mean_ms, fps)."""
    img = cv2.imread(str(val_image_path))
    if img is None:
        raise ValueError(f"Could not load image: {val_image_path}")

    # Warmup
    for _ in range(LATENCY_WARMUP):
        model(img, verbose=False)

    times = []
    for _ in range(LATENCY_RUNS):
        start = time.perf_counter()
        model(img, verbose=False)
        times.append((time.perf_counter() - start) * 1000)  # ms

    mean_ms = float(np.mean(times))
    fps = 1000.0 / mean_ms
    return round(mean_ms, 2), round(fps, 1)


def get_val_image(val_dir):
    """Return path to first image in the val set for latency testing."""
    val_path = Path(val_dir)
    for ext in ("*.jpg", "*.jpeg", "*.png"):
        images = list(val_path.glob(ext))
        if images:
            return images[0]
    raise FileNotFoundError(f"No images found in {val_dir}")


def evaluate_model(name, model_path, val_image_path):
    """Run val + latency for one model. Returns dict of metrics."""
    print(f"\n{'='*60}")
    print(f"Evaluating: {name}")
    print(f"  Model:  {model_path}")

    model = YOLO(model_path)

    # Accuracy metrics from validation set
    print("  Running validation...")
    metrics = model.val(data=DATA_YAML, verbose=False)
    map50 = round(float(metrics.box.map50), 4)
    precision = round(float(metrics.box.p.mean()), 4)
    recall = round(float(metrics.box.r.mean()), 4)

    # Latency
    print(f"  Measuring latency ({LATENCY_RUNS} runs)...")
    latency_ms, fps = measure_latency(model, val_image_path)

    results = {
        "Model": name,
        "mAP50": map50,
        "Precision": precision,
        "Recall": recall,
        "Latency_ms": latency_ms,
        "FPS": fps,
    }

    print(f"  mAP50={map50:.4f}  Precision={precision:.4f}  Recall={recall:.4f}")
    print(f"  Latency={latency_ms}ms  FPS={fps}")
    return results


def save_csv(all_results):
    path = RESULTS_DIR / "results_table.csv"
    fields = ["Model", "mAP50", "Precision", "Recall", "Latency_ms", "FPS"]
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(all_results)
    print(f"\nSaved: {path}")


def plot_accuracy(all_results):
    models = [r["Model"] for r in all_results]
    metrics = ["mAP50", "Precision", "Recall"]
    x = np.arange(len(metrics))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 5))
    for i, result in enumerate(all_results):
        values = [result[m] for m in metrics]
        bars = ax.bar(x + i * width, values, width, label=result["Model"])
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                    f"{val:.3f}", ha="center", va="bottom", fontsize=9)

    ax.set_xlabel("Metric")
    ax.set_ylabel("Score (0–1)")
    ax.set_title("Model Comparison: Accuracy Metrics")
    ax.set_xticks(x + width / 2)
    ax.set_xticklabels(metrics)
    ax.set_ylim(0, 1.15)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)

    path = RESULTS_DIR / "metrics_comparison.png"
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved: {path}")


def plot_latency(all_results):
    models = [r["Model"] for r in all_results]
    latencies = [r["Latency_ms"] for r in all_results]
    fpss = [r["FPS"] for r in all_results]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    colors = ["#4C72B0", "#DD8452"]

    bars1 = ax1.bar(models, latencies, color=colors)
    for bar, val in zip(bars1, latencies):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                 f"{val}ms", ha="center", va="bottom", fontsize=10)
    ax1.set_ylabel("Latency (ms)")
    ax1.set_title("Inference Latency")
    ax1.grid(axis="y", alpha=0.3)

    bars2 = ax2.bar(models, fpss, color=colors)
    for bar, val in zip(bars2, fpss):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                 f"{val} FPS", ha="center", va="bottom", fontsize=10)
    ax2.set_ylabel("FPS")
    ax2.set_title("Frames Per Second")
    ax2.grid(axis="y", alpha=0.3)

    fig.suptitle("Model Comparison: Speed")
    path = RESULTS_DIR / "latency_comparison.png"
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved: {path}")


def print_table(all_results):
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    header = f"{'Model':<25} {'mAP50':>7} {'Prec':>7} {'Recall':>7} {'Lat(ms)':>9} {'FPS':>6}"
    print(header)
    print("-" * 60)
    for r in all_results:
        print(f"{r['Model']:<25} {r['mAP50']:>7.4f} {r['Precision']:>7.4f} "
              f"{r['Recall']:>7.4f} {r['Latency_ms']:>9.1f} {r['FPS']:>6.1f}")
    print("=" * 60)


def main():
    RESULTS_DIR.mkdir(exist_ok=True)

    # Verify models exist
    if not Path(BASELINE_MODEL).exists():
        raise FileNotFoundError(f"Baseline model not found: {BASELINE_MODEL}")
    if not Path(FINETUNED_MODEL).exists():
        raise FileNotFoundError(
            f"Fine-tuned model not found: {FINETUNED_MODEL}\n"
            "Run python src/train.py first."
        )

    # Get a val image for latency testing
    val_image = get_val_image("dataset/valid/images")
    print(f"Using val image for latency: {val_image}")

    all_results = []
    all_results.append(evaluate_model("YOLOv8n (COCO baseline)", BASELINE_MODEL, val_image))
    all_results.append(evaluate_model("YOLOv8n (Fine-tuned drone)", FINETUNED_MODEL, val_image))

    print_table(all_results)
    save_csv(all_results)
    plot_accuracy(all_results)
    plot_latency(all_results)

    print("\nDone. Check results/ for outputs.")


if __name__ == "__main__":
    main()
