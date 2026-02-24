# Pan_Tilt_Tracker
I love working with PCBs and AI so I wanted to combine them into a single project. With an arduino, Pi, and Servos  I will make a pan tilt tracker that will follow objects. Once completed, I also want to implement a drone tracking model.

# Project Context: Edge AI Pan-Tilt Tracking System

## Overview

I am building a real-time embedded AI system that performs object detection and physically tracks a moving target using a camera mounted on a pan-tilt mechanism. The system integrates machine learning, embedded systems, and hardware control.

This project is intended for:

* Machine Learning coursework
* Resume building for software engineering, embedded systems, and defense internships

---

## Core Objective

Develop a system that:

1. Captures video input using a Raspberry Pi camera
2. Runs real-time object detection (YOLO or TensorFlow Lite)
3. Determines object position relative to the frame
4. Sends control signals to an Arduino
5. Adjusts servo motors (pan and tilt) to track the object
6. Optionally uses an ultrasonic sensor for distance awareness

---

## System Architecture

Camera → Raspberry Pi (ML and logic) → Serial Communication → Arduino → Servos (Pan-Tilt)

Additional sensor:
Ultrasonic → Arduino → influences movement decisions

---

## Hardware Components

### Currently Owned:

* Raspberry Pi 4
* Arduino R4 WiFi

### Ordered or Planned:

* Raspberry Pi Camera Module (preferably Camera Module 3)
* 2 SG90 (180°) servos
* Breadboard and jumper wires
* LEDs and resistors
* Ultrasonic sensor (HC-SR04)
* 3D printed pan-tilt mount

---

## Hardware Decisions Made

* Avoid using a prebuilt drone as the core system, only as a possible extension
* Avoid using the Lorex camera system due to security risks and limited flexibility
* Use a Raspberry Pi camera for full control and better integration
* Use SG90 180° servos instead of 90° alternatives

---

## Software Stack

### Development (Laptop First)

* Python
* OpenCV
* YOLO (Ultralytics)
* NumPy
* PySerial

### Deployment (Raspberry Pi)

* TensorFlow Lite or lightweight YOLO
* Optimized inference for edge device constraints

---

## System Flow

1. Capture frame
2. Run object detection
3. Extract bounding box
4. Compute object center
5. Compare with frame center
6. Generate directional command (LEFT, RIGHT, UP, DOWN)
7. Send command via serial to Arduino
8. Arduino adjusts servo angles

---

## Control Logic (Planned)

* Threshold-based tracking (initial implementation)
* Add smoothing to reduce jitter
* Potential upgrade to PID control for improved stability

---

## Performance Metrics (Required)

* Frames per second (FPS)
* Inference latency
* CPU usage (optional)

---

## Key Features for Resume

* Real-time object tracking
* Embedded system communication (Raspberry Pi to Arduino)
* Closed-loop control system
* Hardware and software integration
* Performance optimization under constraints

---

## Machine Learning Component

* Use a pretrained model initially (YOLOv8n or MobileNet)
* Possible extensions:

  * Train on a custom dataset
  * Compare multiple models
  * Analyze accuracy versus speed tradeoffs

---

## Mechanical Component (3D Printing)

* Pan-tilt mount for two servos
* Camera holder
* Optional base for Arduino and breadboard

---

## Constraints and Rules

* Do not build a detection-only system
* Must include:

  * decision logic
  * servo actuation
  * real-time behavior
* Avoid unnecessary complexity in early stages

---

## Development Plan

### Phase 1 (Pre-Hardware)

* Set up object detection on laptop
* Implement decision logic
* Simulate command outputs

### Phase 2 (Initial Integration)

* Set up Raspberry Pi camera
* Run detection on Raspberry Pi
* Establish serial communication

### Phase 3 (Actuation)

* Control one servo
* Expand to pan-tilt with two servos

### Phase 4 (Enhancement)

* Add ultrasonic sensor
* Implement smoothing or PID control
* Optimize performance

---

## End Goal

A fully functional real-time embedded AI tracking system with physical actuation that demonstrates:

* embedded systems knowledge
* machine learning application
* control systems understanding

---

## Resume Positioning

This project should be framed as:

* an embedded AI system
* a real-time control system
* a hardware-software integration project

It should not be framed as a simple object detection demo

---

## Stretch Goals (Optional)

* Multi-object tracking
* Distance-aware tracking using ultrasonic sensor
* Object following behavior
* Drone integration as a later stage

---

## Current Status

* Hardware has not yet arrived
* Preparing software and architecture in advance
* Building detection and decision logic on laptop first

---

## Next Areas of Focus

* Implementing detection and decision logic cleanly
* Structuring the codebase properly
* Transitioning from laptop to Raspberry Pi
* Arduino communication and servo control
* Adding smoothing or PID control

---
