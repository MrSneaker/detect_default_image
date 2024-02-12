# https://github.com/jakkcoder/Training_Yolo_Custom_Object_Detection_files/blob/main/creating-train-and-test-txt-files.py
import os
import shutil

full_path_to_images = '/home/mateo/M1/ouverture-a-la-recherche/DATASET_Sujet2/Defaut'

train_dir = os.path.join(full_path_to_images, 'train_images')
test_dir = os.path.join(full_path_to_images, 'test_images')

os.makedirs(train_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

image_paths = []

for current_dir, dirs, files in os.walk(full_path_to_images):
    for f in files:
        if f.endswith('.png'):
            image_paths.append(os.path.join(current_dir, f))

test_image_paths = image_paths[:int(len(image_paths) * 0.15)]
train_image_paths = image_paths[int(len(image_paths) * 0.15):]

for image_path in train_image_paths:
    shutil.copy(image_path, train_dir)

for image_path in test_image_paths:
    shutil.copy(image_path, test_dir)

train_txt_path = os.path.join(full_path_to_images, 'train.txt')
test_txt_path = os.path.join(full_path_to_images, 'test.txt')

with open(train_txt_path, 'w') as train_txt:
    for image_path in train_image_paths:
        train_txt.write(image_path + '\n')

with open(test_txt_path, 'w') as test_txt:
    for image_path in test_image_paths:
        test_txt.write(image_path + '\n')

print("Le processus est terminé avec succès.")
