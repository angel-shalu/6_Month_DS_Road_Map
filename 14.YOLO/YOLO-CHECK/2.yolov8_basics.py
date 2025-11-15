from ultralytics import YOLO
import numpy

# load a pretrained YOLOv8n model
model = YOLO("yolov8n.pt", "v8")  


# predict on an image
detection_output = model.predict(source=r"C:\Users\shali\Desktop\DS_Road_Map\14.YOLO\YOLO-CHECK\sample\1.jpg", conf=0.25, save=True) 

# Display tensor array
print(detection_output)

# Display numpy array
print(detection_output[0].numpy())
