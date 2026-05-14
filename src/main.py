# src/main.py
import cv2
import time

SIMULATE_SERIAL = True   # Set False when Arduino is connected
USE_TFLITE = False        # Set True on Raspberry Pi

if USE_TFLITE:
    from detector_tflite import ObjectDetector
else:
    from detector import ObjectDetector
from controller import PanTiltController

def main():
    cap = cv2.VideoCapture(0)
    frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    detector = ObjectDetector(model_path="runs/detect/drone_finetune/weights/best.pt", target_class="Drone")
    controller = PanTiltController(frame_w, frame_h, threshold=40)

    # Serial setup (skip in simulation)
    ser = None
    if not SIMULATE_SERIAL:
        from serial_comm import SerialComm
        ser = SerialComm()  # auto-detects port; pass port="COM4" to override
        ser.connect()

    prev_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        detection = detector.detect(frame)
        frame = detector.draw(frame, detection)

        command = None
        if detection:
            cx, cy, _ = detection
            command = controller.compute_command(cx, cy)
            dx, dy = controller.get_error(cx, cy)

            # Display info on frame
            cv2.putText(frame, f"CMD: {command}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            cv2.putText(frame, f"Error X:{dx} Y:{dy}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 0), 1)

            if ser:
                ser.send(command)
            else:
                print(f"[SIM] Sending: {command}")

        # Draw frame center crosshair
        cv2.drawMarker(frame, (frame_w // 2, frame_h // 2),
                       (255, 0, 0), cv2.MARKER_CROSS, 20, 2)

        # FPS
        fps = 1 / (time.time() - prev_time)
        prev_time = time.time()
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, frame_h - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        cv2.imshow("Pan-Tilt Tracker", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    if ser:
        ser.close()

if __name__ == "__main__":
    main()