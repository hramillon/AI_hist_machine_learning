import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
from scipy.linalg import eigh

def make_swiss_roll(n_samples=2000, random_state=42):
    np.random.seed(random_state)
    t = np.random.uniform(1.5 * np.pi, 6 * np.pi, n_samples)
    h = np.random.uniform(-10, 10, n_samples)
    
    X = np.column_stack([t * np.cos(t), t * np.sin(t), h])
    return X, t

X, t = make_swiss_roll(n_samples=2000, random_state=42)
n_neighbors = 15  
n_components = 2
# calculons la matrice des distances
distances = cdist(X, X)

# calcul des poids W
n_samples = X.shape[0]
W = np.zeros((n_samples, n_samples))

for i in range(n_samples):
    dist_i = distances[i, :].copy()
    dist_i[i] = np.inf 
    nearest_indices = np.argsort(dist_i)[:n_neighbors]
 
    Z = X[nearest_indices] - X[i]
    C = Z @ Z.T
    ones = np.ones(n_neighbors)
    C_reg = C + 1e-3 * np.eye(n_neighbors)
    W_i = np.linalg.solve(C_reg, ones)
    W_i /= np.sum(W_i)  
    W[i, nearest_indices] = W_i

# calcul de la matrice M
I = np.eye(n_samples)
M = (I - W).T @ (I - W)

# vecteurs propres de M 
eigenvalues, eigenvectors = eigh(M)

sorted_indices = np.argsort(eigenvalues)
eigenvalues = eigenvalues[sorted_indices]
eigenvectors = eigenvectors[:, sorted_indices]

Y = eigenvectors[:, 1:n_components+1]

# --- Visualisation ---
# Image 1 : Swiss Roll en 3D (couleurs = position t)
fig_3d = plt.figure(figsize=(10, 6))
ax_3d = fig_3d.add_subplot(111, projection='3d')
scatter_3d = ax_3d.scatter(X[:, 0], X[:, 2], X[:, 1], c=t, cmap='viridis', alpha=0.7, s=10)
ax_3d.set_title("Swiss Roll en 3D (couleurs = position le long de la spirale)")
ax_3d.set_xlabel("X")
ax_3d.set_ylabel("Y")
ax_3d.set_zlabel("Z")
plt.colorbar(scatter_3d, ax=ax_3d, label='Position t')
plt.savefig("swiss_roll_3d_corrected_colors.png", dpi=200, bbox_inches='tight')
plt.close(fig_3d)

# Image 2 : Projection LLE en 2D (mêmes couleurs)
plt.figure(figsize=(10, 6))
scatter_2d = plt.scatter(
    Y[:, 0], Y[:, 1],
    c=t,  # Même couleur que en 3D
    cmap='viridis',
    alpha=0.7,
    s=10
)
plt.title("Projection LLE en 2D (Swiss Roll déroulé, couleurs = position t)")
plt.xlabel("Composante 1")
plt.ylabel("Composante 2")
plt.colorbar(scatter_2d, label='Position t')
plt.grid(True)
plt.savefig("swiss_roll_lle_2d_corrected_colors.png", dpi=200, bbox_inches='tight')
plt.close()