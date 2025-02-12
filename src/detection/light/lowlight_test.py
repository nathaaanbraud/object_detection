import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import torch
import torch.nn as nn
import torchvision
import torch.backends.cudnn as cudnn
import torch.optim
import argparse
import time
import my_dataloader
import model
import numpy as np
from torchvision import transforms
from PIL import Image
import glob
import time
import cv2
from src.detection.light import model as light_model

#si cuda
# Vérifier la disponibilité de CUDA
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Initialize the low-light enhancement model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'snapshots', 'epoch99.pth')
DCE_net = light_model.enhance_net_nopool().to(device)
DCE_net.load_state_dict(torch.load(model_path, map_location=device))
DCE_net.eval()


def enhance_image(frame):
    # TODO : Déplacer la fonction dans un autre fichier
    if not isinstance(frame, np.ndarray):
        raise TypeError("Le frame fourni n'est pas un tableau NumPy. Vérifiez la source de l'image.")
    # Convertir le frame en image PIL
    frame_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # Améliorer l'image
    data_lowlight = (np.asarray(frame_image) / 255.0)
    data_lowlight = torch.from_numpy(data_lowlight).float().to(device)
    data_lowlight = data_lowlight.permute(2, 0, 1)
    data_lowlight = data_lowlight.unsqueeze(0)  # Add batch dimension

    with torch.no_grad():
        _, enhanced_image, _ = DCE_net(data_lowlight)
    
    enhanced_image = enhanced_image.squeeze().permute(1, 2, 0).cpu().numpy()
    enhanced_image = (enhanced_image * 255).astype(np.uint8)
    enhanced_frame = Image.fromarray(enhanced_image)

    # Convertir l'image améliorée en frame OpenCV
    enhanced_frame = cv2.cvtColor(np.array(enhanced_frame), cv2.COLOR_RGB2BGR)

    # Traiter l'image et obtenir les résultats
    #detections = process_frame(enhanced_frame) # supprimer cette ligne si tu veux pas calculer sur l'image amélioree

    # Afficher les résultats dans la vidéo #ce paragraphe aussi
    '''for index, row in detections.iterrows():
        x1, y1, x2, y2 = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
        label = row['name']
        confidence = row['confidence']
        color = (0, 255, 0)  # Vert pour les objets détectés
        cv2.rectangle(enhanced_frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(enhanced_frame, f"{label} ({confidence:.2f})", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)'''

    return enhanced_frame
 
def lowlight(image_path):
	os.environ['CUDA_VISIBLE_DEVICES']='0'
	data_lowlight = Image.open(image_path).convert('RGB')

 

	data_lowlight = (np.asarray(data_lowlight)/255.0)

	data_lowlight = torch.from_numpy(data_lowlight).float()
	data_lowlight = data_lowlight.permute(2,0,1)
	data_lowlight = data_lowlight.cuda().unsqueeze(0)

	DCE_net = model.enhance_net_nopool().cuda()
	DCE_net.load_state_dict(torch.load('snapshots/Epoch99.pth'))
	start = time.time()
	_,enhanced_image,_ = DCE_net(data_lowlight)

	end_time = (time.time() - start)
	print(end_time)
	#Met a jour le chemin du resultat
	image_path = image_path.replace('test_data','result')
	result_path = image_path
	print(f"Saving result to: {result_path}")

	if not os.path.exists(image_path.replace('/'+image_path.split("/")[-1],'')):
		os.makedirs(image_path.replace('/'+image_path.split("/")[-1],''))
    
	#verifie que le dossier existe
	os.makedirs(os.path.dirname(result_path), exist_ok=True)
	#enregistre les images qui sont améliorées
	torchvision.utils.save_image(enhanced_image, result_path)
    


if __name__ == '__main__':
# test_images
	with torch.no_grad():
		filePath = 'data/test_data/'
	
		file_list = os.listdir(filePath)

		for file_name in file_list:
			test_list = glob.glob(filePath+file_name+"/*") 
			for image in test_list:
				# image = image
				print(image)
				lowlight(image)
