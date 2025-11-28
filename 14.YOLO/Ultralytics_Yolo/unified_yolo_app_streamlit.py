import streamlit as st
import cv2
from ultralytics import YOLO
import numpy as np
from collections import defaultdict
import time
import tempfile
import os

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #1E1E1E;
    }
    .stButton > button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 10px;
        border-radius: 5px;
        border: none;
        margin: 5px 0;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    .stSelectbox {
        background-color: #2E2E2E;
        color: white;
        border-radius: 5px;
    }
    .stats-box {
        background-color: #2E2E2E;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .title {
        color: #4CAF50;
        text-align: center;
        padding: 20px;
        font-size: 2.5em;
        font-weight: bold;
    }
    .subtitle {
        color: #9E9E9E;
        text-align: center;
        margin-bottom: 30px;
    }
    .result-text {
        color: #4CAF50;
        font-size: 1.2em;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

class UnifiedYOLOApp:
    def __init__(self):
        # Initialize YOLO models
        self.object_model = YOLO('yolov8n.pt')
        self.pose_model = YOLO('yolov8n-pose.pt')
        self.segment_model = YOLO('yolov8n-seg.pt')
        self.track_model = YOLO('yolov8n.pt')
        
        # Initialize object counter
        self.object_counter = defaultdict(int)
        self.counting_line_position = 0.5
        self.tracked_objects = {}

    def draw_counting_line(self, frame):
        height, width = frame.shape[:2]
        line_y = int(height * self.counting_line_position)
        cv2.line(frame, (0, line_y), (width, line_y), (0, 255, 0), 2)
        return line_y

    def count_objects(self, frame, results):
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
                    if (prev_center_y < line_y and center_y >= line_y) or \
                       (prev_center_y > line_y and center_y <= line_y):
                        cls = int(box.cls[0])
                        self.object_counter[cls] += 1

                self.tracked_objects[track_id] = center_y

    def draw_boxes(self, frame, results, task_type):
        annotated_frame = frame.copy()
        
        if task_type == "segment":
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
                
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                label = f"{self.object_model.names[cls]} {conf:.2f}"
                if task_type == "tracking":
                    track_id = box.id
                    if track_id is not None:
                        label += f" ID:{int(track_id)}"
                
                cv2.putText(annotated_frame, label, (x1, y1 - 10), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                if task_type == "pose" and hasattr(r, 'keypoints'):
                    keypoints = r.keypoints
                    if keypoints is not None:
                        for kp in keypoints:
                            for x, y, conf in kp:
                                if conf > 0:
                                    cv2.circle(annotated_frame, (int(x), int(y)), 4, (0, 255, 0), -1)
        
        if task_type == "counting":
            y_offset = 30
            for cls, count in self.object_counter.items():
                text = f"{self.object_model.names[cls]}: {count}"
                cv2.putText(annotated_frame, text, (10, y_offset), 
                          cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                y_offset += 30
                
        return annotated_frame

    def process_frame(self, frame, task_type):
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

def main():
    st.markdown("<h1 class='title'>Unified YOLO Detection App</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Object Detection, Tracking, Pose Estimation, Segmentation, and Counting</p>", unsafe_allow_html=True)

    app = UnifiedYOLOApp()

    # Sidebar
    st.sidebar.markdown("<h2 style='text-align: center; color: #4CAF50;'>Settings</h2>", unsafe_allow_html=True)
    
    task_type = st.sidebar.selectbox(
        "Select Detection Mode",
        ["detection", "tracking", "pose", "segment", "counting"],
        format_func=lambda x: x.capitalize()
    )

    input_source = st.sidebar.radio("Select Input Source", ["Webcam", "Upload Video"])

    if input_source == "Upload Video":
        video_file = st.sidebar.file_uploader("Upload a video", type=['mp4', 'avi', 'mov'])
    
    # Main content
    if st.sidebar.button("Start Detection"):
        if input_source == "Webcam":
            cap = cv2.VideoCapture(0)
        else:
            if video_file is not None:
                # Save uploaded file temporarily
                tfile = tempfile.NamedTemporaryFile(delete=False)
                tfile.write(video_file.read())
                cap = cv2.VideoCapture(tfile.name)
            else:
                st.error("Please upload a video file!")
                return

        # Create a placeholder for the video feed
        video_placeholder = st.empty()
        stats_placeholder = st.empty()
        
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                # Process frame
                annotated_frame, results = app.process_frame(frame, task_type)
                
                # Convert BGR to RGB
                annotated_frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                
                # Display the frame
                video_placeholder.image(annotated_frame_rgb)
                
                # Display stats
                if task_type == "counting":
                    with stats_placeholder:
                        st.markdown("<div class='stats-box'>", unsafe_allow_html=True)
                        for cls, count in app.object_counter.items():
                            st.markdown(
                                f"<p class='result-text'>{app.object_model.names[cls]}: {count}</p>",
                                unsafe_allow_html=True
                            )
                        st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {str(e)}")
        finally:
            cap.release()
            if input_source == "Upload Video":
                os.unlink(tfile.name)

    # Instructions
    with st.expander("Instructions"):
        st.markdown("""
        1. Select the detection mode from the sidebar
        2. Choose your input source (Webcam or Upload Video)
        3. Click 'Start Detection' to begin
        4. Press 'Stop' in Streamlit to end the detection
        
        **Detection Modes:**
        - Detection: Basic object detection
        - Tracking: Object tracking with unique IDs
        - Pose: Human pose estimation
        - Segment: Instance segmentation
        - Counting: Object counting with line crossing detection
        """)

if __name__ == "__main__":
    main()