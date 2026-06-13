import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Génération de points 3D qui suivent approximativement le plan z = 0.5x + 0.5y + 2.5
np.random.seed(42)  # Pour la reproductibilité
n_points = 100
x = np.random.uniform(-10, 10, n_points)
y = np.random.uniform(-10, 10, n_points)
z = 0.5 * x + 0.5 * y + 2.5 + np.random.normal(0, 0.5, n_points)  # Ajout de bruit pour "suivre à peu près"

# Image 1 : Points en 3D uniquement
fig1 = plt.figure(figsize=(8, 6))
ax1 = fig1.add_subplot(111, projection='3d')
ax1.scatter(x, y, z, c='r', marker='o', label='Points 3D')
ax1.set_title("Points 3D")
ax1.set_xlabel("X")
ax1.set_ylabel("Y")
ax1.set_zlabel("Z")
ax1.legend()
plt.savefig("points_3d.png", dpi=200, bbox_inches='tight')
plt.close(fig1)

# Image 2 : Points en 3D + plan 2D (z = 0.5x + 0.5y + 2.5)
fig2 = plt.figure(figsize=(8, 6))
ax2 = fig2.add_subplot(111, projection='3d')

# Affichage des points
ax2.scatter(x, y, z, c='r', marker='o', label='Points 3D')

# Affichage du plan
X_plan, Y_plan = np.meshgrid(np.linspace(-10, 10, 10), np.linspace(-10, 10, 10))
Z_plan = 0.5 * X_plan + 0.5 * Y_plan + 2.5
ax2.plot_surface(X_plan, Y_plan, Z_plan, alpha=0.3, color='b', label='Plan 2D')

ax2.set_title("Points 3D + Plan 2D dans l'espace 3D")
ax2.set_xlabel("X")
ax2.set_ylabel("Y")
ax2.set_zlabel("Z")
ax2.legend()
plt.savefig("points_3d_with_plan.png", dpi=200, bbox_inches='tight')
plt.close(fig2)

# Image 3 : Projection 2D des points (on ignore z)
fig3 = plt.figure(figsize=(8, 6))
ax3 = fig3.add_subplot(111)
ax3.scatter(x, y, c='r', marker='o', label='Projection 2D des points')
ax3.set_title("Projection 2D des points")
ax3.set_xlabel("X")
ax3.set_ylabel("Y")
ax3.legend()
plt.savefig("points_2d_projection.png", dpi=200, bbox_inches='tight')
plt.close(fig3)