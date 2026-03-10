# src/controller.py

class PanTiltController:
    def __init__(self, frame_w, frame_h, threshold=30):
        self.frame_w = frame_w
        self.frame_h = frame_h
        self.cx = frame_w // 2   # frame center x
        self.cy = frame_h // 2   # frame center y
        self.threshold = threshold  # deadzone in pixels

        # Servo angles (starts centered)
        self.pan_angle = 90
        self.tilt_angle = 90
        self.step = 3  # degrees per command

    def compute_command(self, obj_cx, obj_cy):
        """
        Returns a command string: 'P90,T90' format for Arduino.
        """
        dx = obj_cx - self.cx   # positive = object is right of center
        dy = obj_cy - self.cy   # positive = object is below center

        if abs(dx) > self.threshold:
            if dx > 0:
                self.pan_angle = max(0, self.pan_angle - self.step)   # pan right
            else:
                self.pan_angle = min(180, self.pan_angle + self.step) # pan left

        if abs(dy) > self.threshold:
            if dy > 0:
                self.tilt_angle = max(0, self.tilt_angle - self.step)   # tilt down
            else:
                self.tilt_angle = min(180, self.tilt_angle + self.step) # tilt up

        return f"P{self.pan_angle},T{self.tilt_angle}"

    def get_error(self, obj_cx, obj_cy):
        return (obj_cx - self.cx, obj_cy - self.cy)