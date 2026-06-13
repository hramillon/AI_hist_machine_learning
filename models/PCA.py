import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Nécessaire pour les graphiques 3D

# Génération de données aléatoires pour l'exemple (5D)
np.random.seed(42)
X = np.random.rand(100, 3)  # 100 échantillons, 5 dimensions

# Étape 1 : Centrer la matrice autour de l'origine
X_centered = X - np.mean(X, axis=0)

# Étape 2 : Appliquer la SVD
U, S, Vt = np.linalg.svd(X_centered, full_matrices=False)

# Étape 3 : Extraire les composantes principales
# Pour la projection en 2D
components_2d = Vt[:2]
X_pca_2d = X_centered @ components_2d.T

# image 2D
plt.figure(figsize=(8, 6))
plt.scatter(X_pca_2d[:, 0], X_pca_2d[:, 1], alpha=0.7, label='Données projetées (PCA)')
plt.title("Projection des données en 2D avec PCA (SVD)")
plt.xlabel("Composante Principale 1")
plt.ylabel("Composante Principale 2")
plt.grid(True)
plt.legend()
plt.savefig("scene_24_pca_svd_2d.png", dpi=200, bbox_inches='tight')
plt.close()

# image 3D
fig_3d = plt.figure(figsize=(8, 6))
ax_3d = fig_3d.add_subplot(111, projection='3d')  # Crée un sous-graphe 3D
ax_3d.scatter(
    X_centered[:, 0],
    X_centered[:, 1],
    X_centered[:, 2],
    alpha=0.7,
    label='Données projetées en 3D (PCA)'
)
ax_3d.set_title("Données en 3D")
ax_3d.set_xlabel("x")
ax_3d.set_ylabel("y")
ax_3d.set_zlabel("z")
ax_3d.grid(True)
ax_3d.legend()
plt.savefig("scene_24_pca_svd_3d.png", dpi=200, bbox_inches='tight')
plt.close()