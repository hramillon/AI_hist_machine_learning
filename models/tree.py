import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

# Charger le dataset
iris_data = pd.read_csv('../dataset/Iris.csv')

# Sélectionner uniquement PetalLengthCm et PetalWidthCm
X = iris_data[['PetalLengthCm', 'PetalWidthCm']]
y = iris_data['Species']

# Encoder la cible
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Entraîner l'arbre de décision
clf = DecisionTreeClassifier(criterion='gini', max_depth=3, random_state=42)
clf.fit(X, y_encoded)

# Créer un maillage pour les frontières de décision
x_min, x_max = X['PetalLengthCm'].min() - 0.5, X['PetalLengthCm'].max() + 0.5
y_min, y_max = X['PetalWidthCm'].min() - 0.5, X['PetalWidthCm'].max() + 0.5
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.01),
                     np.arange(y_min, y_max, 0.01))

# Prédire les classes pour chaque point du maillage
Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

# Tracer les frontières de décision
plt.figure(figsize=(10, 6))
plt.contourf(xx, yy, Z, alpha=0.4, colors=['red', 'green', 'blue'])

# Tracer les points du dataset
scatter = plt.scatter(X['PetalLengthCm'], X['PetalWidthCm'], c=y_encoded, 
                      cmap='viridis', edgecolor='k', s=50)

# Ajouter des labels et une légende
plt.xlabel('Petal Length (cm)')
plt.ylabel('Petal Width (cm)')
plt.title('Frontières de décision - Arbre de décision (Iris Dataset)')

# Légende pour les espèces
legend_labels = label_encoder.classes_
handles, _ = scatter.legend_elements()
plt.legend(handles, legend_labels, title='Species')

# Afficher le graphique
plt.grid(True)
plt.savefig('decision_boundaries_iris.png', dpi=300, bbox_inches='tight')
print("Le graphique a été sauvegardé dans 'decision_boundaries_iris.png' !")