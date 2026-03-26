# ========== INICIO CODIGO MEDIA PIPE MASCARA FACIAL ==========

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import time


start_time = time.time()

def draw_landmarks_on_image(rgb_image, detection_result):
  face_landmarks_list = detection_result.face_landmarks
  annotated_image = np.copy(rgb_image)

  # Loop through the detected faces to visualize.
  for idx in range(len(face_landmarks_list)):
    face_landmarks = face_landmarks_list[idx]

    # Draw the face landmarks.
    face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    face_landmarks_proto.landmark.extend([
      landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in face_landmarks
    ])

    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp.solutions.drawing_styles
        .get_default_face_mesh_tesselation_style())
    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp.solutions.drawing_styles
        .get_default_face_mesh_contours_style())
    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=mp.solutions.face_mesh.FACEMESH_IRISES,
          landmark_drawing_spec=None,
          connection_drawing_spec=mp.solutions.drawing_styles
          .get_default_face_mesh_iris_connections_style())

  return annotated_image

# STEP 1: Import the necessary modules.
# COPIEI ACIMA PARA IMPORTAR TUDO JUNTO E EVITAR REPETICOES

# STEP 2: Create an FaceLandmarker object.
base_options = python.BaseOptions(model_asset_path='face_landmarker_v2_with_blendshapes.task')
options = vision.FaceLandmarkerOptions(base_options=base_options,
                                       output_face_blendshapes=True,
                                       output_facial_transformation_matrixes=True,
                                       num_faces=1)
detector = vision.FaceLandmarker.create_from_options(options)

# STEP 3: Load the input image.
bgr_img = cv2.imread('/Users/jararacaurbana/PycharmProjects/DeepFace_MediaPipe/foto.jpg')
image = mp.Image(image_format=mp.ImageFormat.SRGB, data=bgr_img)

# STEP 4: Detect face landmarks from the input image.
detection_result = detector.detect(image)

# Criar uma imagem em branco com as mesmas dimensões da imagem original
blank_image = np.full((image.height, image.width, 3), 255, dtype=np.uint8)  # Fundo branco

# Desenhar os landmarks na imagem em branco com cor preta
annotated_blank_image = draw_landmarks_on_image(blank_image, detection_result)

# Criar uma máscara com os landmarks em preto
mask = np.zeros((image.height, image.width, 3), dtype=np.uint8)
annotated_mask = draw_landmarks_on_image(mask, detection_result)

# Converter a cor dos landmarks para preto na imagem em branco
annotated_blank_image = cv2.bitwise_and(annotated_blank_image, cv2.bitwise_not(annotated_mask))

# Get the coordinates of the face landmarks
face_landmarks_list = detection_result.face_landmarks
if face_landmarks_list:
  face_landmarks = face_landmarks_list[0]
  # Find the bounding box of the face landmarks
  x_coords = [landmark.x for landmark in face_landmarks]
  y_coords = [landmark.y for landmark in face_landmarks]
  min_x = min(x_coords)
  min_y = min(y_coords)
  max_x = max(x_coords)
  max_y = max(y_coords)

  # Crop the image based on the bounding box
  image_width, image_height = image.width, image.height
  x1 = int((min_x * image_width)-10)
  y1 = int((min_y * image_height)-10)
  x2 = int((max_x * image_width)+10)
  y2 = int((max_y * image_height)+10)

  cropped_image = annotated_blank_image[y1:y2, x1:x2]
  cv2.imwrite('mascara_facial.jpg', cv2.cvtColor(cropped_image, cv2.COLOR_RGB2BGR))

#cv2.imwrite('mascara_facial.jpg', cv2.cvtColor(annotated_blank_image, cv2.COLOR_RGB2BGR))

end_time = time.time()
total_time = end_time - start_time
print(total_time)

# ========== FIM CODIGO MEDIA PIPE MASCARA FACIAL ==========

#IMPRIME MASCARA FACIAL
import subprocess
subprocess.Popen(['lpr', 'mascara_facial.jpg'])

# ===== apaga a foto =====
import os

def apagar():
  try:
    os.remove('/Users/jararacaurbana/PycharmProjects/DeepFace_MediaPipe/foto.jpg')
    print("\nFoto deletada.")
  except FileNotFoundError:
    print("\nArquivos não encontrados.")
  except Exception as e:
    print(f"\nErro ao deletar o arquivo: {e}")

apagar()