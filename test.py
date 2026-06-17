import cv2
from ultralytics import YOLO

model = YOLO("runs/detect/train/weights/best.pt")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Не удалось открыть камеру")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Не удалось получить кадр")
        break

    results = model.predict(frame, verbose=False)
    annotated = results[0].plot()

    cv2.imshow("Camera", annotated)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == 27:
        break

cap.release()
cv2.destroyAllWindows()
print("Камера закрыта")

