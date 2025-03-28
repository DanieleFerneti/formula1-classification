import cv2
import argparse
import numpy as np

# Percorso del video di input
INPUT_VIDEO_FILE_PATH = "media/"

# Percorso del video di output
OUTPUT_VIDEO_FILE_PATH = "media/224_canny"

# Create the parser
parser = argparse.ArgumentParser()
parser.add_argument('--i', type=str, required=True)
parser.add_argument('--o', type=str, required=True)
args = parser.parse_args()

INPUT_VIDEO_FILE_PATH = "media/" + args.i
OUTPUT_VIDEO_FILE_PATH = "media/224_canny/" + args.o

print('* input file: ' + INPUT_VIDEO_FILE_PATH)
print('** output file: ' + OUTPUT_VIDEO_FILE_PATH)


OUTPUT_RESOLUTION = (224, 224)

# Crea un oggetto VideoCapture per leggere il video
cap = cv2.VideoCapture(INPUT_VIDEO_FILE_PATH)

# Verifica se il video è stato aperto correttamente
if not cap.isOpened():
    print("Errore nell'apertura del file video")
    exit()


original_fps = int(cap.get(cv2.CAP_PROP_FPS))
print(f'original fps: {original_fps}')
if(original_fps < 49):
    frame_scaler = 1
else:
    frame_scaler = 2

# Crea un oggetto VideoWriter per salvare il video con i nuovi FPS
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(OUTPUT_VIDEO_FILE_PATH, fourcc, 25.0, OUTPUT_RESOLUTION, isColor = True)

frame_count = 0


cockpit = np.array([[0,224],[16,140],[55,101],[190,103],[224,140],[224,224]])
sky = np.array([[0,0],[0,40],[224,40],[224,0]])
aoi = np.array([[0,224],[224,224],[224,78],[160,48],[100,48],[0,132]])

while True:
    # Leggi un frame dal video
    ret, frame = cap.read()

    # Se il frame non è stato letto correttamente, esci dal ciclo
    if not ret:
        break

    # Seleziona i frame necessari in base all'intervallo calcolato
    if (frame_count % frame_scaler) == 0:
        image = cv2.resize(frame, OUTPUT_RESOLUTION)

        edges = cv2.Canny(image,100,200) 
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        final_image = cv2.addWeighted(image, 1, edges, 1, 0)

        cv2.fillPoly(final_image, [cockpit], 0)
        cv2.fillPoly(final_image, [sky], 0)
        out.write(final_image)

    frame_count += 1

# Rilascia gli oggetti VideoCapture e VideoWriter
cap.release()
out.release()

print("*** Video processed ...")


