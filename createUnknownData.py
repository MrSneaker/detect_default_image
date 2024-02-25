import os
import shutil
import cv2
import numpy as np
import random

shutil.rmtree('nouveau_dossier_test')

# Chemins des dossiers contenant les images
chemin_defaut = 'DATASET_Sujet2/Defaut'
chemin_sans_defaut = 'DATASET_Sujet2/Sans_Defaut'

# Chemin du nouveau dossier de test
chemin_nouveau_dossier_test = 'nouveau_dossier_test'

# Nombre maximal d'images à sélectionner au hasard
nb_max_images = 50

# Création du nouveau dossier de test s'il n'existe pas déjà
if not os.path.exists(chemin_nouveau_dossier_test):
    os.makedirs(chemin_nouveau_dossier_test)

# Fonction pour copier un nombre maximal d'images au hasard d'un dossier source vers le nouveau dossier de test avec des transformations
def copier_images_avec_transformation(source, destination, nb_max):
    # Liste des noms de fichiers dans le dossier source
    fichiers = os.listdir(source)
    # Mélanger la liste de noms de fichiers de manière aléatoire
    random.shuffle(fichiers)
    # Sélectionner les nb_max premiers fichiers
    fichiers_selectionnes = fichiers[:nb_max]
    for filename in fichiers_selectionnes:
        # Lire l'image
        image = cv2.imread(os.path.join(source, filename))
        if image is not None:
            angle = random.randint(-10, 10)
            hauteur, largeur = image.shape[:2]
            rotation_matrix = cv2.getRotationMatrix2D((largeur / 2, hauteur / 2), angle, 1)
            image_rotate = cv2.warpAffine(image, rotation_matrix, (largeur, hauteur))

            blur_val = random.randint(0,4) * 2 + 1
            image_blur = cv2.GaussianBlur(image_rotate, (blur_val, blur_val), 0)

            cv2.imwrite(os.path.join(destination, filename), image_blur)

copier_images_avec_transformation(chemin_defaut, chemin_nouveau_dossier_test, nb_max_images)
copier_images_avec_transformation(chemin_sans_defaut, chemin_nouveau_dossier_test, nb_max_images)

print("Images copiées avec succès vers le nouveau dossier de test avec des transformations.")
