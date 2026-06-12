from manim import *
import numpy as np

class Projection3D(ThreeDScene):
    def construct(self):
        # 1. Configuration de la scène et de la caméra
        axes = ThreeDAxes(
            x_range=[-5, 5, 1], y_range=[-5, 5, 1], z_range=[0, 15, 2],
            x_length=6, y_length=6, z_length=5
        )
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.add(axes)

        # Équation du plan : z = 0.5*x + 0.5*y + 8
        def plan_func(x, y):
            return 0.5 * x + 0.5 * y + 8

        # 2. Génération des 100 points bruités autour du plan
        np.random.seed(42)
        x_vals = np.random.uniform(-3, 3, 100)
        y_vals = np.random.uniform(-3, 3, 100)
        # On ajoute un bruit normal sur l'axe Z
        z_vals = plan_func(x_vals, y_vals) + np.random.normal(0, 0.5, 100)

        points = VGroup(*[
            Dot3D(point=axes.c2p(x, y, z), color=BLUE, radius=0.05)
            for x, y, z in zip(x_vals, y_vals, z_vals)
        ])

        # --- ÉTAPE 1 : Mise en avant des points (2s) ---
        self.play(FadeIn(points, lag_ratio=0.05), run_time=2)
        self.wait(1)  # Attente pour atteindre les 3s du script

        # --- ÉTAPE 2 : Mise en évidence du plan incliné (3s) ---
        plan = Surface(
            lambda u, v: axes.c2p(u, v, plan_func(u, v)),
            u_range=[-3, 3],
            v_range=[-3, 3],
            checkerboard_colors=[RED_D, RED_E],
            fill_opacity=0.6
        )
        self.play(Create(plan), run_time=2)
        self.wait(1)

        # --- ÉTAPE 3 : Projection et réduction de dimension ---
        # Calcul des coordonnées projetées orthogonalement sur le plan
        # Vecteur normal au plan n = (0.5, 0.5, -1)
        n = np.array([0.5, 0.5, -1.0])
        n_norm = n / np.linalg.norm(n)
        
        projected_dots = VGroup()
        for x, y, z in zip(x_vals, y_vals, z_vals):
            p = np.array([x, y, z])
            # Point de référence sur le plan (0, 0, 8)
            p0 = np.array([0, 0, 8])
            # Projection orthogonale
            p_proj = p - np.dot(p - p0, n_norm) * n_norm
            projected_dots.add(Dot3D(point=axes.c2p(*p_proj), color=YELLOW, radius=0.05))

        # Animation de projection sur le plan existant
        self.play(
            Transform(points, projected_dots),
            run_time=2
        )
        self.wait(1)

        # Animation bonus : Rotation de la caméra pour voir l'effet 2D "plat"
        self.move_camera(phi=45 * DEGREES, theta=-30 * DEGREES, run_time=2)
        self.wait(1)