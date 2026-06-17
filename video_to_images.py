import cv2
import os

video_path = "Video/VID_20260508_190527.mp4"
output_folder = "new_images_4"

os.makedirs(output_folder, exist_ok=True)

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Не удалось открыть видео")
    exit()

frame_count = 0
saved_count = 0

save_every = 6 

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame_count += 1

    if frame_count % save_every == 0:
        filename = os.path.join(output_folder, f"frame_{saved_count:05d}.jpg")
        cv2.imwrite(filename, frame)
        saved_count += 1

cap.release()

print("Готово")
print("Всего кадров в видео:", frame_count)
print("Сохранено изображений:", saved_count)