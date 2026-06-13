from manim import *
import numpy as np

class LLESwissRollZoom(ThreeDScene):
    def construct(self):
        np.random.seed(42)
        n = 300
        t = 1.5 * np.pi * (1 + 2 * np.random.rand(n))
        h = np.random.rand(n) * 2 - 1
        t_norm = (t - t.min()) / (t.max() - t.min())

        # Fonction de génération des points
        def make_pts(alpha_z=1.0, alpha_unroll=0.0):
            x = np.cos(t) * t * (1 - alpha_unroll) + t_norm * 5 * alpha_unroll
            y = h
            z = np.sin(t) * t * alpha_z * (1 - alpha_unroll)
            pts = np.stack([x, y, z], axis=1)
            pts[:, 0] = (pts[:, 0] - pts[:, 0].mean()) / pts[:, 0].std() * 2.0
            pts[:, 2] = (pts[:, 2] - pts[:, 2].mean()) / (pts[:, 2].std() + 1e-6) * 2.0 * alpha_z
            return pts

        colors = [interpolate_color(BLUE, RED, float(t_norm[i])) for i in range(n)]
        pts_start = make_pts(alpha_unroll=0.0)
        dots = VGroup(*[Dot3D(pts_start[i], radius=0.04, color=colors[i]) for i in range(n)])

        # 1. VUE INITIALE : Swiss Roll 3D
        self.set_camera_orientation(phi=65*DEGREES, theta=-60*DEGREES, zoom=1.0)
        self.add(dots)
        self.wait(1)

        # 2. ZOOM SUR UN POINT ET SES K-VOISINS
        # Choix du point central (index 150)
        center_idx = 150
        center_pt = pts_start[center_idx]
        
        # Recherche des 5 plus proches voisins (K=5)
        dists = np.linalg.norm(pts_start - center_pt, axis=1)
        k_indices = np.argsort(dists)[1:6] # Exclure le point lui-même
        
        # Mettre en valeur le point central et ses voisins
        dots[center_idx].set_color(YELLOW).set_scale(2.5)
        neighbor_lines = VGroup()
        for idx in k_indices:
            dots[idx].set_color(GREEN).set_scale(1.8)
            line = Line(center_pt, pts_start[idx], color=GREEN_A, stroke_width=2)
            neighbor_lines.add(line)

        # Zoom de la caméra sur le point central
        self.move_camera(
            phi=55*DEGREES, 
            theta=-45*DEGREES, 
            zoom=3.5, 
            focal_distance=10,
            frame_center=center_pt,
            run_time=2.5
        )
        self.play(Create(neighbor_lines), run_time=1)
        self.wait(1)

        # 3. AFFICHAGE DE L'ÉQUATION LLE
        self.camera.light_source.move_to(3 * IN)
        eq1 = MathTex(
            "W = \\arg\\min_W \\sum_{i=1}^m \\left\\| x_i - \\sum_{j=1}^m w_{i,j}x_j \\right\\|^2",
            font_size=18
        ).to_corner(UL).shift(DOWN * 0.2)
        
        eq2 = MathTex(
            "\\text{subject to } w_{i,j} = 0 \\text{ if } x_j \\notin \\text{k-NN}(x_i)",
            font_size=16
        ).next_to(eq1, DOWN, aligned_edge=LEFT)
        
        eq3 = MathTex(
            "\\sum_{j=1}^m w_{i,j} = 1 \\quad \\forall i",
            font_size=16
        ).next_to(eq2, DOWN, aligned_edge=LEFT)

        equations = VGroup(eq1, eq2, eq3)
        self.add_fixed_in_frame_mobjects(equations)
        self.play(FadeIn(equations), run_time=1.5)
        self.wait(3)

        # 4. DEZOOM
        self.play(FadeOut(equations), FadeOut(neighbor_lines))
        # Rétablir la taille/couleur d'origine pour le déroulement
        dots[center_idx].set_color(colors[center_idx]).set_scale(1/2.5)
        for idx in k_indices:
            dots[idx].set_color(colors[idx]).set_scale(1/1.8)

        self.move_camera(
            phi=75*DEGREES, 
            theta=-90*DEGREES, 
            zoom=1.0, 
            frame_center=[0, 0, 0],
            run_time=2
        )
        self.wait(0.5)

        # 5. DÉROULEMENT (Feuille 2D)
        pts_unrolled = make_pts(alpha_z=1.0, alpha_unroll=1.0)
        self.play(
            *[dots[i].animate.move_to(pts_unrolled[i]) for i in range(n)],
            self.camera.phi_tracker.animate.set_value(0*DEGREES), # Vue orthogonale de face
            self.camera.theta_tracker.animate.set_value(-90*DEGREES),
            run_time=4,
            rate_func=smooth
        )
        self.wait(1.5)