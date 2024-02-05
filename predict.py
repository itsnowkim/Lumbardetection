from ultralytics import YOLO

# Load a pretrained YOLOv8n model
model = YOLO('runs/segment/train/weights/best.pt')

# Define path to directory containing images and videos for inference
source = 'dataset/test/images'

# Run inference on the source
# results = model(source, stream=True)  # generator of Results objects
model.predict(source, save=True, imgsz=640, conf=0.5)
