# src/detector.py
import cv2
from ultralytics import YOLO

class ObjectDetector:
    def __init__(self, model_path="yolov8n.pt", target_class="person", conf=0.5):
        self.model = YOLO(model_path)
        self.target_class = target_class
        self.conf = conf

    def detect(self, frame):
        """
        Returns (cx, cy, bbox) of best detection, or None.
        cx, cy = center of bounding box
        bbox = (x1, y1, x2, y2)
        """
        results = self.model(frame, conf=self.conf, verbose=False)[0]

        best = None
        best_conf = 0

        for box in results.boxes:
            cls_name = self.model.names[int(box.cls)]
            if cls_name != self.target_class:
                continue
            conf = float(box.conf)
            if conf > best_conf:
                best_conf = conf
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2
                best = (cx, cy, (x1, y1, x2, y2))

        return best

    def draw(self, frame, detection):
        if detection is None:
            return frame
        cx, cy, (x1, y1, x2, y2) = detection
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
        return frame