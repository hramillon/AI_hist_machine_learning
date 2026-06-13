import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans as KMeansSklearn

def initialiser_centroides(X, k, random_state=42):
    rng = np.random.default_rng(random_state)
    #choisit k points aléatoires
    indices = rng.choice(X.shape[0], size=k, replace=False)
    return X[indices].copy()


def assigner_clusters(X, centroides):
    # calcul de la distance euclidienne avec chaque centroïde
    distances = np.linalg.norm(X[:, np.newaxis, :] - centroides[np.newaxis, :, :], axis=2)
    return np.argmin(distances, axis=1)


def mettre_a_jour_centroides(X, labels, k, anciens_centroides):
    # calcul le point "moyen" pour chaque cluster afin de remplacer ce point par le centroïde
    n_features = X.shape[1]
    nouveaux = np.zeros((k, n_features))
    for i in range(k):
        points_du_cluster = X[labels == i]
        if len(points_du_cluster) > 0:
            nouveaux[i] = points_du_cluster.mean(axis=0)
        else:
            nouveaux[i] = anciens_centroides[i]
    return nouveaux


def inertie(X, labels, centroides):
    # résultat à minimiser
    return np.sum((X - centroides[labels]) ** 2)


def kmeans(X, k, max_iter=300, tol=1e-4, random_state=42):
    centroides = initialiser_centroides(X, k, random_state)

    for iteration in range(1, max_iter + 1):
        labels = assigner_clusters(X, centroides)
        nouveaux_centroides = mettre_a_jour_centroides(X, labels, k, centroides)

        deplacement = np.linalg.norm(nouveaux_centroides - centroides)
        centroides = nouveaux_centroides

        if deplacement < tol:
            break

    labels = assigner_clusters(X, centroides)
    return labels, centroides, iteration, inertie(X, labels, centroides)



iris = load_iris()
X = iris.data[:, [2, 3]]   
y = iris.target
noms_features = [iris.feature_names[2], iris.feature_names[3]]

k = 3

labels_scratch, centroides_scratch, n_iter, inertie_scratch = kmeans(X, k)

fig, axes = plt.subplots(1, 2, figsize=(10, 5))

# Vraies classes
axes[0].scatter(X[:, 0], X[:, 1], c=y, cmap="viridis", edgecolor="k")
axes[0].set_title("Vraies espèces (y)")
axes[0].set_xlabel(noms_features[0])
axes[0].set_ylabel(noms_features[1])

# K-means from scratch
axes[1].scatter(X[:, 0], X[:, 1], c=labels_scratch, cmap="viridis", edgecolor="k")
axes[1].scatter(centroides_scratch[:, 0], centroides_scratch[:, 1],
                c="red", marker="X", s=200, label="Centroïdes")
axes[1].set_title(f"K-means from scratch (k={k})")
axes[1].set_xlabel(noms_features[0])
axes[1].set_ylabel(noms_features[1])
axes[1].legend()

plt.tight_layout()
plt.savefig("kmeans_iris.png", dpi=120)