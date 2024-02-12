import cv2
import numpy as np
import os


def rotateImg(imagePath, imageName, outputDir):
    image = cv2.imread(imagePath)
    nbRotate = 0
    maxRotate = (360 / 5) - 1
    angle_rotation = 5
    while nbRotate < maxRotate:
        hauteur, largeur = image.shape[:2]
        centre_image = (largeur / 2, hauteur / 2)
        mat_rotation = cv2.getRotationMatrix2D(centre_image, angle_rotation, 1.0)
        image_rotate = cv2.warpAffine(image, mat_rotation, (largeur, hauteur))
        newName = imageName + '_' + str(nbRotate) + '.png'
        output_path = os.path.join(outputDir, newName)
        cv2.imwrite(output_path, image_rotate)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        nbRotate += 1
        angle_rotation += 5

dossier_images = '/home/mateo/M1/ouverture-a-la-recherche/DATASET_Sujet2/Defaut'

for fichier in os.listdir(dossier_images):
    if fichier.endswith(".png"):
        chemin_image = os.path.join(dossier_images, fichier)
        rotateImg(chemin_image, fichier, dossier_images)

