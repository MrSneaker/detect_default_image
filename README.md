# Ouverture à la recherche - Détection et classification automatique des défauts dans une image thermique en se basant sur les méthodes d’apprentissage profond

## Installation

1. Assurez-vous d'avoir Python installé sur votre système. Si ce n'est pas le cas, vous pouvez le télécharger depuis [python.org](https://www.python.org/).

2. Clonez ce dépôt GitHub sur votre machine locale en utilisant la commande suivante dans votre terminal :

    ```bash
    git clone https://forge.univ-lyon1.fr/p2002495/ouverture-a-la-recherche.git
    ```

3. Accédez au répertoire du projet :

    ```bash
    cd ouverture-a-la-recherche
    ```

4. Installez les dépendances requises en exécutant la commande suivante :

    ```bash
    pip install -r requirements.txt
    ```

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

## Auteurs

Ce projet a été développé par MUNOZ Matéo, numéro d'étudiant : 12002495.
