import matplotlib.pyplot as plt
import numpy as np

# Données pour les ensembles de données de test et d'entraînement
test_data = {
    "ST_Inf_OU_Sup": {"ap": 80.21, "precision": 0.83, "recall": 0.80, "f1_score": 0.81},
    "SL_Pli": {"ap": 87.01, "precision": 0.83, "recall": 0.80, "f1_score": 0.81},
    "ST_Point": {"ap": 58.93, "precision": 0.83, "recall": 0.80, "f1_score": 0.81},
    "ST_Sup_Pli": {"ap": 57.38, "precision": 0.83, "recall": 0.80, "f1_score": 0.81},
    "Normal": {"ap": 97.39, "precision": 0.83, "recall": 0.80, "f1_score": 0.81}
}

train_data = {
    "ST_Inf_OU_Sup": {"ap": 95.98, "precision": 0.91, "recall": 0.87, "f1_score": 0.89},
    "SL_Pli": {"ap": 98.54, "precision": 0.91, "recall": 0.87, "f1_score": 0.89},
    "ST_Point": {"ap": 82.69, "precision": 0.91, "recall": 0.87, "f1_score": 0.89},
    "ST_Sup_Pli": {"ap": 61.01, "precision": 0.91, "recall": 0.87, "f1_score": 0.89},
    "Normal": {"ap": 97.69, "precision": 0.91, "recall": 0.87, "f1_score": 0.89}
}

# Comparaison des valeurs d'AP par classe
classes = list(test_data.keys())
ap_test = [test_data[c]["ap"] for c in classes]
ap_train = [train_data[c]["ap"] for c in classes]

plt.figure(figsize=(10, 6))
plt.bar(classes, ap_test, color='blue', alpha=0.5, label='Test Data')
plt.bar(classes, ap_train, color='red', alpha=0.5, label='Train Data')
plt.xlabel('Classes')
plt.ylabel('Average Precision (AP)')
plt.title('Comparison of AP by Class')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Comparaison des métriques globales
metrics = ['precision', 'recall', 'f1_score']
metrics_test = [sum(test_data[c][m] for c in classes) / len(classes) for m in metrics]
metrics_train = [sum(train_data[c][m] for c in classes) / len(classes) for m in metrics]

plt.figure(figsize=(8, 6))
plt.plot(metrics, metrics_test, marker='o', color='blue', label='Test Data')
plt.plot(metrics, metrics_train, marker='o', color='red', label='Train Data')
plt.xlabel('Metrics')
plt.ylabel('Value')
plt.title('Comparison of Global Metrics')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Comparaison de la mAP@0.5
mAP_test = sum(test_data[c]["ap"] for c in classes) / len(classes)
mAP_train = sum(train_data[c]["ap"] for c in classes) / len(classes)

plt.figure(figsize=(6, 4))
plt.bar(['Test Data', 'Train Data'], [mAP_test, mAP_train], color=['blue', 'red'], alpha=0.5)
plt.xlabel('Datasets')
plt.ylabel('mAP@0.5')
plt.title('Comparison of mAP@0.5')
plt.tight_layout()
plt.show()

# Données des ensembles de test
classes = ["ST_Inf_OU_Sup", "SL_Pli", "ST_Point", "ST_Sup_Pli", "Normal"]
tp_test = [231, 123, 55, 56, 57]
fp_test = [30, 18, 23, 32, 4]

# Données des ensembles d'entraînement
tp_train = [1419, 769, 371, 372, 189]
fp_train = [39, 10, 81, 172, 16]

# Conversion en nombres de FP et de TP pour 100 détections
total_detections_test = np.array(tp_test) + np.array(fp_test)
total_detections_train = np.array(tp_train) + np.array(fp_train)

tp_test_per_100 = np.array(tp_test) / total_detections_test * 100
fp_test_per_100 = np.array(fp_test) / total_detections_test * 100

tp_train_per_100 = np.array(tp_train) / total_detections_train * 100
fp_train_per_100 = np.array(fp_train) / total_detections_train * 100

# Création des positions des barres
bar_width = 0.35
index = np.arange(len(classes))

# Création du graphique
plt.figure(figsize=(12, 6))

plt.bar(index, tp_test_per_100, bar_width, color='skyblue', label='TP (Test)')
plt.bar(index, fp_test_per_100, bar_width, color='salmon', label='FP (Test)', bottom=tp_test_per_100)

plt.bar(index + bar_width, tp_train_per_100, bar_width, color='dodgerblue', label='TP (Entraînement)')
plt.bar(index + bar_width, fp_train_per_100, bar_width, color='tomato', label='FP (Entraînement)', bottom=tp_train_per_100)

plt.xlabel('Classes')
plt.ylabel('Pourcentage de détections')
plt.title('Comparaison des TP et FP pour chaque classe (pour 100 détections)')
plt.xticks(index + bar_width / 2, classes)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()

# Données
classes = ['Normal', 'ST_Inf_OU_Sup', 'SL_Pli', 'ST_Point', 'ST_Sup_Pli']
TP = [1, 23, 7, 4, 5]
FP = [0, 0, 2, 0, 5]
FN = [41, 2, 2, 1, 5]

# Calcul de la précision et du rappel par classe
precision = [tp / (tp + fp) for tp, fp in zip(TP, FP)]
recall = [tp / (tp + fn) for tp, fn in zip(TP, FN)]

# Calcul du F1-score par classe
f1_score = [2 * (p * r) / (p + r) if p + r != 0 else 0 for p, r in zip(precision, recall)]

# Création du graphe
plt.figure(figsize=(10, 6))

# Création des barres
plt.bar(classes, f1_score, color='b', edgecolor='grey')

# Ajout de titres et de libellés
plt.xlabel('Classes', fontweight='bold')
plt.ylabel('F1-score', fontweight='bold')
plt.title('F1-score par classe')
plt.ylim(0, 1)

# Affichage du graphe
plt.show()




