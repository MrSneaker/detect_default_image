import os

def extract_label_id(image_name):
    if 'ST_Inf' in image_name:
        return 0
    elif 'ST_Sup' in image_name and not 'ST_Sup_Pli' in image_name:
        return 0
    elif 'SL' in image_name:
        return 1
    elif 'STP' in image_name:
        return 2
    elif 'ST_Sup_Pli' in image_name:
        return 3
    else:
        return 4

def modify_yolo_labels(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt') and file_name != 'classes.txt':
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as file:
                lines = file.readlines()

            if len(lines) > 0:
                # Modifier le premier chiffre (l'ID du label) en fonction du nom de l'image
                image_name = file_name.split('.')[0]  # obtenir le nom de l'image sans extension
                label_id = extract_label_id(image_name)  # obtenir l'ID du label à partir du nom de l'image
                # print(lines)
                lines[0] = f"{label_id} {lines[0].split(' ', 1)[1]}"  # remplacer le premier chiffre

                # Écrire les modifications dans le fichier
                with open(file_path, 'w') as file:
                    file.writelines(lines)

# Chemin du dossier contenant les fichiers texte de rectangle de labelisation YOLO
folder_path = '/home/mateo/COURS/M1/OuvertureRecherche/ouverture-a-la-recherche/data/train_images'
modify_yolo_labels(folder_path)
