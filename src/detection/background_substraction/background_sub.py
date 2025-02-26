import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

import cv2
import numpy as np
from src.config.config_loader import load_config, get_video_path
from src.detection.light.lowlight_test import enhance_image



def draw_parallelogram(image, pts, color, thickness):
    pts = np.array(pts, np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.polylines(image, [pts], isClosed=True, color=color, thickness=thickness)



def background_substraction(video_ref_dir, video_ref_name, video_test_dir, video_test_name, frame_tested):
    # Charger la configuration
    config = load_config()
    video_path = get_video_path(config)

    # Charger la vidéo de référence (sans objet)
    cap_ref = cv2.VideoCapture(os.path.join(video_path, video_ref_dir, video_ref_name))

    # Charger la vidéo actuelle (avec objets ajoutés)
    cap_current = cv2.VideoCapture(os.path.join(video_path, video_test_dir, video_test_name))


    # Aller chercher la 100ᵉ frame de la vidéo de référence
    cap_ref.set(cv2.CAP_PROP_POS_FRAMES, 100)
    ret_ref, frame_ref = cap_ref.read()
    if not ret_ref:
        print("Erreur : Impossible de lire la vidéo de référence à la frame 100")
        cap_ref.release()
        cap_current.release()
        exit()

    # Traitement luminosité
    frame_ref_light = enhance_image(frame_ref)

    # Aller chercher la nᵉ frame de la vidéo avec objet
    cap_current.set(cv2.CAP_PROP_POS_FRAMES, frame_tested)
    ret_cur, frame_cur = cap_current.read()
    if not ret_cur:
        print("Erreur : Impossible de lire la vidéo actuelle à la frame 200")
        cap_ref.release()
        cap_current.release()
        exit()

    # Traitement luminosité
    frame_cur_light = enhance_image(frame_cur)

    # --- AJOUTER UN RECTANGLE BLEU POUR LES ZONES À EXCLURE ---
    x1, y1, x2, y2 = 770, 90, 1040, 100
    x3, y3, x4, y4 = 1125, 120, 1265, 147
    x5, y5, x6, y6 = 425, 75, 730, 75

    # Définir les points des parallélogrammes

    #pour fonction occlusion
    parallelogram1 = np.array([[x1, y1], [x2, y2], [x2 + 0, y2 + 295], [x1 + 0, y1 + 200]], np.int32)
    parallelogram2 = np.array([[x3, y3], [x4, y4], [x4 + 0, y4 + 378], [x3 + 0, y3 + 350]], np.int32)
    parallelogram3 = np.array([[x5, y5], [x6, y6], [x6 + 0, y6 + 100], [x5 + 0, y5 + 100]], np.int32)

    #pour affichage graphique
    parallelo1 = [(x1, y1), (x2, y2), (x2 + 0, y2 + 295), (x1 + 0, y1 + 200)] 
    parallelo2 = [(x3, y3), (x4, y4), (x4 + 0, y4 + 378), (x3 + 0, y3 + 350)]
    parallelo3 = [(x5, y5), (x6, y6), (x6 + 0, y6 + 50), (x5 + 0, y5 + 55)]


    # --- EXCLURE LES ZONES DES VITRES ---

    #  Convertir en niveaux de gris pour la soustraction
    gray_ref = cv2.cvtColor(frame_ref_light, cv2.COLOR_BGR2GRAY)
    gray_cur = cv2.cvtColor(frame_cur_light, cv2.COLOR_BGR2GRAY)

    #  Appliquer la soustraction d'image
    diff = cv2.absdiff(gray_ref, gray_cur)

    #  Seuillage pour détecter les différences importantes (objets ajoutés)
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

    # Supprimer les zones des vitres (mettre à zéro les pixels dans cette région)
    cv2.fillPoly(thresh, [parallelogram1], 0) 
    cv2.fillPoly(thresh, [parallelogram2], 0) 
    cv2.fillPoly(thresh, [parallelogram3], 0) 

    #  Appliquer des opérations morphologiques pour réduire le bruit
    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    #  Détecter les contours des objets présents
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #  Filtrer les objets trop petits
    min_size = 25  # Ajuster selon la résolution (taille minimum en pixels)
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_size**2]

    #  Dessiner les objets détectés sur l'image actuelle
    output = frame_cur.copy()
    for cnt in filtered_contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)


    # Dessiner un rectangle bleu sur l'image pour visualiser la zone d'exclusion
    
    draw_parallelogram(output, parallelo1, (255, 0, 0), 2)
    draw_parallelogram(output, parallelo2, (255, 0, 0), 2)
    draw_parallelogram(output, parallelo3, (255, 0, 0), 2)

    #  Afficher le résultat
    cv2.imshow("Objets detectes", output)
    cv2.waitKey(0)

    #  Libérer les ressources
    cap_ref.release()
    cap_current.release()
    cv2.destroyAllWindows()



background_substraction("prise_0", "vlc-record-2025-01-23-14h53m24s-rtsp___10.129.52.34_live_ID-STREAM-CAM7H-VID1-.mp4", "prise_16", "vlc-record-2025-01-23-16h05m02s-rtsp___10.129.52.34_live_ID-STREAM-CAM7H-VID1-.mp4", 3600)