# Ouverture à la recherche - Détection et classification automatique des défauts dans une image thermique en se basant sur les méthodes d’apprentissage profond

Ce projet est un projet universitaire de Master 1 qui visait à détecter et classifier des défauts dans des images thermiques de façon automatique grâce à l'apprentissage profond. Le but du projet était de s'ouvrir au domaine de la recherche et donc de réaliser le projet comme un projet de recherche. Pour cette raison, un état de l'art et un rapport respectant le style d'un article de recherche ont été réalisé pour ce projet. Ces documents sont accessibles dans ce dépot à la racine, dans le fichier `Rapport.pdf`.

## Installation

1. Assurez-vous d'avoir Python installé sur votre système. Si ce n'est pas le cas, vous pouvez le télécharger depuis [python.org](https://www.python.org/).

2. Clonez ce dépôt GitHub sur votre machine locale en utilisant la commande suivante dans votre terminal :

    ```bash
    git clone https://github.com/MrSneaker/detect_default_image.git
    ```

3. Accédez au répertoire du projet :

    ```bash
    cd detect_default_image
    ```

4. Installez les dépendances requises en exécutant la commande suivante :

    ```bash
    pip install -r requirements.txt
    ```

5. Télécharger les poids du modèle Yolo du projet dans le répertoire ```detect_default_image``` sur [ce lien](https://mega.nz/file/Fj8njCzZ#_Ukt5qZ42OxeRKcVzZf4ZcXp49FV9Jf8sJXLv0osAu4) (si le lien n'est plus valable me contacter).

## Utilisation

1. Une fois les dépendances installées, lancez l'application en exécutant le fichier `app.py` :

    ```bash
    python3 app.py
    ```

2. L'application devrait démarrer et ouvrir une interface utilisateur.

3. Sélectionnez une image thermique à analyser en utilisant le bouton d'ouverture de fichier. Vous pouvez aussi ouvrir un dossier entier contenant des images avec le bouton dédié(formats des images : png, jpg, bmp).

4. Une fois l'image chargée, vous pouvez lancer la détection de défauts sur l'image affichée.

5. Les défauts détectés seront mis en évidence et classés sur l'image thermique affichée.

6. Vous pouvez alors récupérez l'image générée ou zoomer sur le défaut par exemple.

## Génération de données pour tester le modèle

En executant le script ```createUnknownData.py```, vous pouvez créer dans le dossier ```nouveau_dossier_test``` à la racine du projet un set d'image nouvellement généré. Si vous voulez réduire ou augmenter la difficulté de détection sur le set généré, vous pouvez simplement modifier la force du flou gaussien ligne 40 du script.

## Auteurs

Ce projet a été développé par MUNOZ Matéo, numéro d'étudiant : 12002495.
