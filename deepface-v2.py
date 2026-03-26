import numpy as np
import matplotlib.pyplot as plt

import cv2

cam = cv2.VideoCapture(0)
cv2.namedWindow("test")

#img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("Erro na captura da foto.")
        break
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Fechando...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "foto.jpg" #.format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} capturada!".format(img_name))
        #img_counter += 1

cam.release()
cv2.destroyAllWindows()

# ========== FIM CODIGO CAMERA ==========

# ========== INICIO CODIGO DEEPFACE ==========
import os
from deepface import DeepFace
import time

#tradução do output

gender = {"Woman": "Feminino",
          "Man": "Masculino"}

emotion = {"angry": "Irritação",
           "disgust": "Aversão",
           "fear": "Medo",
           "happy": "Felicidade",
           "sad": "Tristeza",
           "surprise": "Surpresa",
           "neutral": "Neutra"}

race = {"asian": "Asiático",
        "indian": "Indiano",
        "black": "Negro",
        "white": "Branco",
        "middle eastern": "Oriente médio",
        "latino hispanic": "Latino"}

def analise():
  try:
    global dados
    analysis = DeepFace.analyze(img_path ='foto.jpg', actions = ["age", "emotion", "race", "gender"], enforce_detection=False)
    dados = analysis
    print('Análise concluída')
  except ValueError:
    print("Não foi possível detectar um rosto na imagem.")

start_time = time.time()

analise()
#print(dados)
#formata dados e salva em arquivo .txt

def salvar():
    text_lines = []  # Initialize an empty list to store lines of text
    try:
        text_lines.append("\n.\n.\n.")
        text_lines.append("\n Festa da Vilinha\n")
        text_lines.append("   12/10/2025\n")
        text_lines.append("\n   BOTA A CARA")
        text_lines.append("\nReconhecimento")
        text_lines.append("facial: pensando")
        text_lines.append("   nos riscos")
        text_lines.append("\n")
        text_lines.append(f"\nIdade: {dados[0]['age']} anos")
        text_lines.append("\n=== Gênero ===")
        for key, value in dados[0]['gender'].items():
            if key in gender:
                text_lines.append(f"{gender[key]}: {value:.0f}%")

        text_lines.append("\n=== Emoções ===")
        for key, value in dados[0]['emotion'].items():
            if key in emotion:
                text_lines.append(f"{emotion[key]}: {value:.0f}%")
            else:
                text_lines.append(f"{key}: {value:.0f}%")

        text_lines.append('\n === Etnias === ')
        for key, value in dados[0]['race'].items():
            if key in race:
                text_lines.append(f"{race[key]}: {value:.0f}%")
            else:
                text_lines.append(f"{key}: {value:.0f}%")
        text_lines.append('\nPROEXT-PG - CAPES\n ')
        #print(text_lines)
    except ValueError:
        print('Erro')

    # Join the lines of text into a single string
    global output_string
    output_string = "\n".join(text_lines)
    #global relatorio
    #relatorio = output_string

    # Return the string
    return output_string

salvar()

with open('relatorio.txt', 'w') as f:
    f.write(output_string)

end_time = time.time()
total_time = end_time - start_time
print(total_time)



# MUDEI PARA O MEDIA PIPE ===== apaga a foto =====
'''
def apagar():
  try:
    os.remove('foto.jpg')
    print("\nFoto deletada.")
  except FileNotFoundError:
    print("\nArquivos não encontrados.")
  except Exception as e:
    print(f"\nErro ao deletar o arquivo: {e}")
'''
#apagar()

import subprocess
subprocess.Popen(['lpr', 'relatorio.txt'])