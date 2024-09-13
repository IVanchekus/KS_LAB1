from pathlib import Path
from deepface import DeepFace
import os

import tensorflow as tf

class DeepFaceController:
    def face_verify(self, image1_path, image2_path):
        result = DeepFace.verify(img1_path = image1_path, img2_path = image2_path)
        return result
    
    def face_find(self, image_path, folder_path):
        try:
            result_find = DeepFace.find(img_path=image_path, db_path=folder_path, silent=True)

            result = []
            for value in result_find:
                print(value)
                for i in range(len(value.identity)):
                    if (value.identity[i] == image_path): continue
                    result.append({
                        "photo_path": value.identity[i],
                        "diff": round(((1 - value.distance[i]) * 100), 2)
                    })

            result = sorted(result, key=lambda x: x['diff'], reverse=True)
            result = result[:3]
            return result
        except Exception as ex:
            raise Exception("Не могу найти лиц")
    
    def face_analyze(self, image_path):
        result = DeepFace.analyze(img_path = image_path, actions = ['age', 'gender', 'race', 'emotion'])
        return result

# controller = DeepFaceController()
# iam = "../../saved_photos/WIN_20210831_21_53_37_Pro.jpg"
# test = "../../saved_photos/"

# ct = DeepFaceController()
# res = ct.face_find(iam, test)
# print(res)

