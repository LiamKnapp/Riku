from ultralytics import YOLO

# Load the pre-trained YOLOv10-N model
model = YOLO("yolov10n.pt")

results = model.predict(0, save=True, show=True, conf=0.15)