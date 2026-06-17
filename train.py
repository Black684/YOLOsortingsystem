from ultralytics import YOLO

def main():
    model = YOLO("yolov8n.pt")

    model.train(
    data="dataset/data.yaml",

    epochs=100,
    patience=20,

    imgsz=512,
    batch=4,
    device=0,

    optimizer="AdamW",
    lr0=0.001,

    augment=True,

    freeze=10,        
    dropout=0.1      
)

if __name__ == "__main__":
    main()


