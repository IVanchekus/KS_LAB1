from pathlib import Path
from deepface import DeepFace
from state.state import user_state

class DeepFaceController:
    def face_analyze(self, image_path):
        try:
            detector = self.face_detector(image_path)
            if detector > 1:
                raise Exception("На фото больше 1 лица")
            
            result = DeepFace.analyze(img_path = image_path, actions = ['age', 'gender', 'race', 'emotion'])
            return result
        except Exception as ex:
                if ("not be detected" in str(ex)): raise Exception("Не могу найти лиц на фото")
                raise Exception(ex)
    
    def face_detector(self, image_path):
        detected_faces = DeepFace.extract_faces(image_path)

        return len(detected_faces)
        