from ultralytics import YOLO

model = YOLO("yolov8n.pt")

model.train(
    data="dataset_real/data.yaml",
    epochs=50,
    imgsz=640,
    batch=4
)