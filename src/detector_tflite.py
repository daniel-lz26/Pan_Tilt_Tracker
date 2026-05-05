# src/detector_tflite.py
# Pi-compatible object detector using TFLite + MobileNet SSD.
# Same public interface as detector.py so main.py can swap them with USE_TFLITE.
#
# Model download (run once on the Pi):
#   wget https://storage.googleapis.com/download.tensorflow.org/models/tflite/coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip
#   unzip coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip -d src/models/
#
# Install runtime (Pi 4 64-bit Bookworm):
#   pip install tflite-runtime           # or:
#   sudo apt install python3-tflite-runtime

import os
import cv2
import numpy as np

# Try the standalone tflite-runtime package first (smaller install on Pi),
# then fall back to the full TensorFlow package (laptop dev).
try:
    from tflite_runtime.interpreter import Interpreter
except ImportError:
    from tensorflow.lite.python.interpreter import Interpreter

_MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
_DEFAULT_MODEL = os.path.join(_MODEL_DIR, "detect.tflite")
_DEFAULT_LABELS = os.path.join(_MODEL_DIR, "labelmap.txt")


def _load_labels(path: str) -> list[str]:
    with open(path, "r") as f:
        lines = [l.strip() for l in f.readlines()]
    # COCO labelmap files sometimes have a blank first line ("???")
    if lines and lines[0] in ("", "???"):
        lines = lines[1:]
    return lines


class ObjectDetector:
    def __init__(
        self,
        model_path: str = _DEFAULT_MODEL,
        labels_path: str = _DEFAULT_LABELS,
        target_class: str = "person",
        confidence_threshold: float = 0.5,
    ):
        self._threshold = confidence_threshold
        self._target = target_class.lower()

        self._interpreter = Interpreter(model_path=model_path)
        self._interpreter.allocate_tensors()

        self._input  = self._interpreter.get_input_details()[0]
        self._output = self._interpreter.get_output_details()

        # Input tensor shape: [1, height, width, channels]
        _, self._h, self._w, _ = self._input["shape"]

        self._labels = _load_labels(labels_path)

    def detect(self, frame):
        """
        Run inference on a BGR frame.
        Returns (cx, cy, (x1, y1, x2, y2)) for the highest-confidence
        target detection, or None if no target is found.
        """
        img_h, img_w = frame.shape[:2]

        # Resize + convert BGR→RGB
        resized = cv2.resize(frame, (self._w, self._h))
        rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        input_data = np.expand_dims(rgb, axis=0)

        # TFLite quantized models expect uint8
        if self._input["dtype"] == np.uint8:
            input_data = input_data.astype(np.uint8)
        else:
            input_data = input_data.astype(np.float32) / 255.0

        self._interpreter.set_tensor(self._input["index"], input_data)
        self._interpreter.invoke()

        # Output tensors: [boxes, classes, scores, count]
        # boxes  shape [1, N, 4]  — normalized [ymin, xmin, ymax, xmax]
        # classes shape [1, N]
        # scores  shape [1, N]
        boxes   = self._interpreter.get_tensor(self._output[0]["index"])[0]
        classes = self._interpreter.get_tensor(self._output[1]["index"])[0]
        scores  = self._interpreter.get_tensor(self._output[2]["index"])[0]

        best = None
        best_score = 0.0

        for i, score in enumerate(scores):
            if score < self._threshold:
                continue
            label_idx = int(classes[i])
            if label_idx >= len(self._labels):
                continue
            label = self._labels[label_idx].lower()
            if label != self._target:
                continue
            if score > best_score:
                best_score = score
                ymin, xmin, ymax, xmax = boxes[i]
                x1 = int(xmin * img_w)
                y1 = int(ymin * img_h)
                x2 = int(xmax * img_w)
                y2 = int(ymax * img_h)
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2
                best = (cx, cy, (x1, y1, x2, y2))

        return best

    def draw(self, frame, detection):
        """Draw bounding box and center dot. Safe to call with detection=None."""
        if detection is None:
            return frame
        cx, cy, (x1, y1, x2, y2) = detection
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
        return frame
