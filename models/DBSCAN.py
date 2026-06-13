import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris

def dbscan(X, eps, min_samples):
    # -1 = Bruit, 0 = Non visité
    labels = np.zeros(X.shape[0], dtype=int) 
    cluster_id = 0
    
    for i in range(X.shape[0]):
        if labels[i] != 0:
            continue
            
        # si on visité alors on cherche voisins
        distances = np.linalg.norm(X - X[i], axis=1)
        voisins = np.where(distances <= eps)[0]
        
        if len(voisins) < min_samples:
            labels[i] = -1
        else:
            cluster_id += 1
            labels[i] = cluster_id
            
            graine = list(voisins)
            while len(graine) > 0:
                actuel = graine.pop(0)
                
                if labels[actuel] == -1:
                    labels[actuel] = cluster_id
                if labels[actuel] != 0:
                    continue
                    
                labels[actuel] = cluster_id
                dist_actuel = np.linalg.norm(X - X[actuel], axis=1)
                voisins_actuel = np.where(dist_actuel <= eps)[0]
                
                if len(voisins_actuel) >= min_samples:
                    graine.extend(voisins_actuel)
                    
    return labels

# Données
iris = load_iris()
X = iris.data[:, [2, 3]]   
y = iris.target
noms_features = [iris.feature_names[2], iris.feature_names[3]]

labels_dbscan = dbscan(X, eps=0.4, min_samples=5)
fig, axes = plt.subplots(1, 2, figsize=(10, 5))

axes[0].scatter(X[:, 0], X[:, 1], c=y, cmap="viridis", edgecolor="k")
axes[0].set_title("Vraies espèces (y)")
axes[0].set_xlabel(noms_features[0])
axes[0].set_ylabel(noms_features[1])

# DBSCAN
axes[1].scatter(X[:, 0], X[:, 1], c=labels_dbscan, cmap="tab10", edgecolor="k")
axes[1].set_title("DBSCAN from scratch")
axes[1].set_xlabel(noms_features[0])
axes[1].set_ylabel(noms_features[1])

plt.tight_layout()
plt.savefig("dbscan_iris.png", dpi=120)