from manim import *
import numpy as np

class Projection3D(ThreeDScene):
    def construct(self):
        self.camera.focal_distance = 15
        
        # Axes recentrés
        axes = ThreeDAxes(
            x_range=[-6, 6, 1], y_range=[-6, 6, 1], z_range=[-5, 5, 1],
            x_length=8, y_length=8, z_length=5
        )
        # On force les axes à être parfaitement au centre de l'écran
        axes.move_to(ORIGIN)
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.add(axes)

        # Équation descendue à +0 pour être centrée sur l'origine
        def plan_func(x, y):
            return 0.5 * x + 0.5 * y + 0

        # 1. ÉTAPE 1 : 100 POINTS EN 3D
        np.random.seed(42)
        x_vals = np.random.uniform(-3, 3, 100)
        y_vals = np.random.uniform(-3, 3, 100)
        z_vals = plan_func(x_vals, y_vals) + np.random.normal(0, 0.5, 100)

        points = VGroup(*[
            Dot3D(point=axes.c2p(x, y, z), color=BLUE, radius=0.06)
            for x, y, z in zip(x_vals, y_vals, z_vals)
        ])

        self.play(FadeIn(points, lag_ratio=0.015), run_time=2)
        self.wait(1)

        # 2. ÉTAPE 2 : APPARITION DU PLAN INCLINÉ RECENTRÉ
        plan = Surface(
            lambda u, v: axes.c2p(u, v, plan_func(u, v)),
            u_range=[-3, 3],
            v_range=[-3, 3],
            checkerboard_colors=[RED_D, RED_E],
            fill_opacity=0.6,
            resolution=(10, 10) 
        )
        self.play(FadeIn(plan), run_time=2)
        self.wait(1)

        # 3. ÉTAPE 3 : PROJECTION ET RÉDUCTION EN 2D
        n = np.array([0.5, 0.5, -1.0])
        n_norm = n / np.linalg.norm(n)
        plane_center = np.array([0, 0, 0])
        
        projected_dots_3d = VGroup()
        for x, y, z in zip(x_vals, y_vals, z_vals):
            p = np.array([x, y, z])
            p_proj = p - np.dot(p - plane_center, n_norm) * n_norm
            projected_dots_3d.add(Dot3D(point=axes.c2p(*p_proj), color=YELLOW, radius=0.06))

        self.play(Transform(points, projected_dots_3d), run_time=1.5)
        self.wait(0.5)

        # Carré 2D final parfaitement centré
        proj_plane = Square(side_length=5, fill_color=RED_E, fill_opacity=0.6).move_to(ORIGIN)
        
        points_2d_on_plane = VGroup()
        for x, y in zip(x_vals, y_vals):
            pt_2d = Dot(point=proj_plane.get_center() + np.array([x * 0.6, y * 0.6, 0]), color=YELLOW, radius=0.07)
            points_2d_on_plane.add(pt_2d)

        # Transition finale sans bouger la hauteur
        self.move_camera(
            phi=0, 
            theta=-90 * DEGREES, 
            added_anims=[
                FadeOut(axes),
                Transform(plan, proj_plane),
                Transform(points, points_2d_on_plane)
            ],
            run_time=3
        )
        self.wait(2)