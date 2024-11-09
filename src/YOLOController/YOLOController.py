import cv2
import torch
import numpy as np
from collections import defaultdict

# Загрузка модели YOLOv5
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

class YOLOController:
    def process_video(self, video_path):
        print("Начало поиска")
        # Открытие видеофайла
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("Ошибка при открытии видеофайла")
            return []
        
        detected_objects = defaultdict(int)
        tracked_objects = {}

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Преобразование кадра в формат, подходящий для YOLO
            results = model(frame)

            # Получение списка обнаруженных объектов
            for obj in results.xyxy[0]:
                x1, y1, x2, y2, conf, cls = obj.tolist()
                label = model.names[int(cls)]

                # Проверка, был ли объект уже отслежен
                is_new_object = True
                for tracked_obj in tracked_objects.values():
                    if self.is_same_object(tracked_obj, (x1, y1, x2, y2)):
                        is_new_object = False
                        break

                if is_new_object:
                    # Добавляем новый объект в список отслеживаемых
                    obj_id = len(tracked_objects) + 1
                    tracked_objects[obj_id] = (x1, y1, x2, y2)
                    detected_objects[label] += 1

        cap.release()
        print("Конец поиска")
        return detected_objects

    def is_same_object(self, obj1, obj2, threshold=0.5):
        """
        Проверяет, являются ли два объекта одним и тем же объектом.
        Используется метод IoU (Intersection over Union).
        """
        x1_1, y1_1, x2_1, y2_1 = obj1
        x1_2, y1_2, x2_2, y2_2 = obj2

        # Вычисление пересечения
        inter_x1 = max(x1_1, x1_2)
        inter_y1 = max(y1_1, y1_2)
        inter_x2 = min(x2_1, x2_2)
        inter_y2 = min(y2_1, y2_2)

        inter_area = max(0, inter_x2 - inter_x1) * max(0, inter_y2 - inter_y1)

        # Вычисление объединения
        area_1 = (x2_1 - x1_1) * (y2_1 - y1_1)
        area_2 = (x2_2 - x1_2) * (y2_2 - y1_2)
        union_area = area_1 + area_2 - inter_area

        # Вычисление IoU
        iou = inter_area / union_area

        return iou > threshold

    def send_detected_objects_message(self, detected_objects):
        message = "Обнаруженные объекты:\n"
        for obj, count in detected_objects.items():
            message += f"- {obj}: {count} шт.\n"
        return message