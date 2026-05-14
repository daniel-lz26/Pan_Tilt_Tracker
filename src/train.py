"""
Fine-tune YOLOv8n on the Kaggle Drone Detection dataset.

Usage (run from project root):
    python src/train.py

Prerequisites:
    1. Download dataset from https://www.kaggle.com/datasets/sshikamaru/drone-detection
    2. Place dataset at dataset/ with structure:
           dataset/images/train/  dataset/images/val/
           dataset/labels/train/  dataset/labels/val/
    3. dataset/data.yaml must exist (already provided)

Output:
    runs/detect/drone_finetune/weights/best.pt   <- use this for evaluate.py
    runs/detect/drone_finetune/weights/last.pt
"""

import os
from pathlib import Path
from ultralytics import YOLO


DATA_YAML = "dataset/data.yaml"
BASE_MODEL = "yolov8n.pt"
EPOCHS = 50
IMG_SIZE = 640
BATCH = 32
RUN_NAME = "drone_finetune"


def main():
    # Verify dataset exists before starting
    data_path = Path(DATA_YAML)
    if not data_path.exists():
        raise FileNotFoundError(f"data.yaml not found at {DATA_YAML}. "
                                "Did you set up the dataset/ directory?")

    train_imgs = Path("dataset/train/images")
    if not train_imgs.exists() or not any(train_imgs.iterdir()):
        raise FileNotFoundError(
            "No training images found at dataset/train/images/. "
            "Download the Kaggle drone dataset first."
        )

    print(f"Starting fine-tuning: {BASE_MODEL} -> drone_finetune")
    print(f"Epochs: {EPOCHS}  |  Image size: {IMG_SIZE}  |  Batch: {BATCH}")
    print("-" * 60)

    model = YOLO(BASE_MODEL)
    model.train(
        data=DATA_YAML,
        epochs=EPOCHS,
        imgsz=IMG_SIZE,
        batch=BATCH,
        name=RUN_NAME,
        project="runs/detect",
        exist_ok=True,
        verbose=True,
        workers=4,
    )

    best_weights = Path(f"runs/detect/{RUN_NAME}/weights/best.pt")
    print("\n" + "=" * 60)
    print("Training complete!")
    print(f"Best weights saved to: {best_weights}")
    print("Next step: python src/evaluate.py")


if __name__ == "__main__":
    main()
