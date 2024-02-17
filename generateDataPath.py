# https://github.com/jakkcoder/Training_Yolo_Custom_Object_Detection_files/blob/main/creating-train-and-test-txt-files.py
import os
import shutil

full_path_to_images = '/home/mateo/COURS/M1/OuvertureRecherche/ouverture-a-la-recherche/data/test_images'

image_paths = []

for current_dir, dirs, files in os.walk(full_path_to_images):
    for f in files:
        if f.endswith('.png'):
            image_paths.append(os.path.join(current_dir, f))

txt_path = '/home/mateo/COURS/M1/OuvertureRecherche/ouverture-a-la-recherche/data/test.txt'

with open(txt_path, 'w') as train_txt:
    for image_path in image_paths:
        train_txt.write(image_path + '\n')

print("Le processus est terminé avec succès.")
