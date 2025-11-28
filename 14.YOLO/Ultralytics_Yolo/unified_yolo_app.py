import cv2
from ultralytics import YOLO
import numpy as np
import time
import math
from collections import defaultdict

class UnifiedYOLOApp:
    def __init__(self):
        # Initialize YOLO models
        self.object_model = YOLO('yolov8n.pt')
        self.pose_model = YOLO('yolov8n-pose.pt')
        self.segment_model = YOLO('yolov8n-seg.pt')
        self.track_model = YOLO('yolov8n.pt')
        
        # Initialize object counter
        self.object_counter = defaultdict(int)
        self.counting_line_position = 0.5  # middle of the frame
        self.tracked_objects = {}

    def draw_counting_line(self, frame):
        """Draw counting line on frame"""
        height, width = frame.shape[:2]
        line_y = int(height * self.counting_line_position)
        cv2.line(frame, (0, line_y), (width, line_y), (0, 255, 0), 2)
        return line_y

    def count_objects(self, frame, results):
        """Count objects crossing the line"""
        line_y = self.draw_counting_line(frame)
        
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                track_id = box.id
                if track_id is None:
                    continue
                
                track_id = int(track_id)
                center_y = (y1 + y2) // 2

                if track_id in self.tracked_objects:
                    prev_center_y = self.tracked_objects[track_id]
                    # Check if object crossed the line
                    if (prev_center_y < line_y and center_y >= line_y) or \
                       (prev_center_y > line_y and center_y <= line_y):
                        cls = int(box.cls[0])
                        self.object_counter[cls] += 1

                self.tracked_objects[track_id] = center_y

    def draw_boxes(self, frame, results, task_type):
        """Draw bounding boxes and additional information based on task type"""
        annotated_frame = frame.copy()
        
        if task_type == "segment":
            # Draw segmentation masks
            for r in results:
                masks = r.masks
                if masks is not None:
                    for mask in masks:
                        mask_array = mask.data[0].cpu().numpy()
                        mask_array = mask_array.astype(np.uint8) * 255
                        colored_mask = cv2.applyColorMap(mask_array, cv2.COLORMAP_JET)
                        annotated_frame = cv2.addWeighted(annotated_frame, 0.7, colored_mask, 0.3, 0)
        
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                
                # Draw box
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # Draw label
                label = f"{self.object_model.names[cls]} {conf:.2f}"
                if task_type == "tracking":
                    track_id = box.id
                    if track_id is not None:
                        label += f" ID:{int(track_id)}"
                
                cv2.putText(annotated_frame, label, (x1, y1 - 10), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                # Draw keypoints for pose estimation
                if task_type == "pose" and hasattr(r, 'keypoints'):
                    keypoints = r.keypoints
                    if keypoints is not None:
                        for kp in keypoints:
                            for x, y, conf in kp:
                                if conf > 0:
                                    cv2.circle(annotated_frame, (int(x), int(y)), 4, (0, 255, 0), -1)
        
        # Draw object counts
        if task_type == "counting":
            y_offset = 30
            for cls, count in self.object_counter.items():
                text = f"{self.object_model.names[cls]}: {count}"
                cv2.putText(annotated_frame, text, (10, y_offset), 
                          cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                y_offset += 30
                
        return annotated_frame

    def process_frame(self, frame, task_type):
        """Process frame based on selected task"""
        if task_type == "detection":
            results = self.object_model(frame)
        elif task_type == "pose":
            results = self.pose_model(frame)
        elif task_type == "segment":
            results = self.segment_model(frame)
        elif task_type in ["tracking", "counting"]:
            results = self.track_model.track(frame, persist=True)
        else:
            return frame, []
        
        if task_type == "counting":
            self.count_objects(frame, results)
            
        annotated_frame = self.draw_boxes(frame, results, task_type)
        return annotated_frame, results

    def run(self):
        cap = cv2.VideoCapture(0)  # Use webcam
        if not cap.isOpened():
            print("Error: Could not open webcam")
            return

        # Create window and trackbar
        cv2.namedWindow('Unified YOLO App')
        modes = ['detection', 'tracking', 'pose', 'segment', 'counting']
        current_mode = 0
        cv2.createTrackbar('Mode', 'Unified YOLO App', 0, len(modes)-1, lambda x: None)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Get current mode from trackbar
            current_mode = cv2.getTrackbarPos('Mode', 'Unified YOLO App')
            task_type = modes[current_mode]

            # Process frame
            annotated_frame, _ = self.process_frame(frame, task_type)

            # Add mode text to frame
            cv2.putText(annotated_frame, f"Mode: {task_type}", (10, 30), 
                      cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Show frame
            cv2.imshow('Unified YOLO App', annotated_frame)

            # Break loop on 'q' press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = UnifiedYOLOApp()
    app.run()