from pathlib import Path
from deepface import DeepFace
from state.state import user_state

class DeepFaceController:
    def face_verify(self, image1_path, image2_path):
        result = DeepFace.verify(img1_path = image1_path, img2_path = image2_path)
        return result
    

    def face_find(self, image_path, folder_path):
        try:
            detector = self.face_detector(image_path)
            if detector > 1:
                raise Exception("На фото больше 1 лица")

            result_find = DeepFace.find(img_path=image_path, db_path=folder_path, silent=True)

            result = []
            for value in result_find:
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
            if ("not be detected" in str(ex)): raise Exception("Не могу найти лиц на фото")
            raise Exception(ex)
    

    def face_analyze(self, image_path):
        detector = self.face_detector(image_path)
        if detector > 1:
            raise Exception("На фото больше 1 лица")
        
        result = DeepFace.analyze(img_path = image_path, actions = ['age', 'gender', 'race', 'emotion'])
        return result
    
    def face_detector(self, image_path):
        detected_faces = DeepFace.extract_faces(image_path)

        return len(detected_faces)
        