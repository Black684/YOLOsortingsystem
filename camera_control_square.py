from ultralytics import YOLO
import cv2
import serial
import time

try:
    arduino = serial.Serial(port="COM5", baudrate=9600, timeout=1)
    time.sleep(2)
except Exception as e:
    print("Ошибка подключения к Arduino:", e)
    arduino = None

model = YOLO("runs/detect/train2/weights/best.pt")
print("Классы модели:", model.names)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Не удалось открыть камеру")
    if arduino:
        arduino.close()
    exit()

print("Камера запущена. Нажми esc чтобы выйти.")

last_sent = None
current_object = None
same_count = 0
required_same_frames = 2

pending_commands = []

delay_servo1 = 0.9

while True:
    ret, frame = cap.read()

    if not ret:
        print("Не удалось получить кадр")
        break

    results = model.predict(frame, conf=0.25, verbose=False)
    annotated = results[0].plot()

    detected_object = None

    if len(results) > 0 and results[0].boxes is not None and len(results[0].boxes) > 0:
        boxes = results[0].boxes

        best_index = boxes.conf.argmax().item()
        cls_id = int(boxes.cls[best_index].item())
        conf = float(boxes.conf[best_index].item())

        detected_object = model.names[cls_id]

        print("Класс:", detected_object, "Уверенность:", round(conf, 2))

    if detected_object == current_object and detected_object is not None:
        same_count += 1
    else:
        current_object = detected_object
        same_count = 1 if detected_object is not None else 0

    if detected_object is not None and same_count >= required_same_frames:

        if detected_object != last_sent:

            print("Обнаружено:", detected_object)

            if detected_object in ["square", "Square", "квадрат"]:
                send_time = time.time() + delay_servo1
                pending_commands.append((send_time, 1))

                print("Квадрат обнаружен. Команда для servo1 добавлена: 1")
            else:
                print("Объект пропускается:", detected_object)

            last_sent = detected_object

    if detected_object is None:
        current_object = None
        same_count = 0
        last_sent = None

    current_time = time.time()

    for item in pending_commands[:]:
        send_time, cmd = item

        if current_time >= send_time:
            print("Отправка команды в Arduino:", cmd)

            if arduino:
                arduino.write((str(cmd) + "\n").encode())
                arduino.flush()

            pending_commands.remove(item)

    cv2.imshow("YOLO Conveyor", annotated)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q") or key == 27:
        break

cap.release()
cv2.destroyAllWindows()

if arduino:
    arduino.close()