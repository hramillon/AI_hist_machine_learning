from manim import *
import numpy as np

from manim import *
import numpy as np

class PCAProjection3D(ThreeDScene):
    def construct(self):
        # --- INITIALISATION ÉCRAN SÉPARÉ ---
        title_pca = Text("PCA (Variance & Projection)", font_size=20).to_edge(UP).shift(LEFT * 3.5)
        title_lle = Text("LLE (Unrolling)", font_size=20).to_edge(UP).shift(RIGHT * 3.5)
        line = Line(UP * 4, DOWN * 4, color=GRAY)
        self.add(title_pca, title_lle, line)

        # GAUCHE : PCA (Initiale)
        np.random.seed(42)
        raw_pts = np.random.normal(size=(40, 3))
        raw_pts = raw_pts * np.array([1.5, 0.4, 0.1])
        theta = np.radians(30)
        c, s = np.cos(theta), np.sin(theta)
        R = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
        pca_pts_data = raw_pts @ R.T + np.array([-3.5, 0, 0])
        pca_dots = VGroup(*[Dot3D(point=pt, radius=0.05, color=BLUE) for pt in pca_pts_data])
        
        axis_1 = Line([-3.5, 0, 0], [-3.5 + 2*c, 2*s, 0], color=RED, stroke_width=4)
        axis_2 = Line([-3.5, 0, 0], [-3.5 - s, c, 0], color=GREEN, stroke_width=4)
        pca_axes = VGroup(axis_1, axis_2)

        # DROITE : LLE
        t = np.linspace(-1.5 * np.pi, 1.5 * np.pi, 40)
        lle_start_pts = np.c_[np.sin(t) * 1.2 + 3.5, t * 0.5, np.zeros_like(t)]
        lle_end_pts = np.c_[t * 0.5 + 3.5, np.zeros_like(t), np.zeros_like(t)]
        lle_dots = VGroup(*[Dot3D(point=pt, radius=0.06, color=PURPLE) for pt in lle_start_pts])
        
        lines = VGroup()
        for i in range(len(lle_start_pts) - 1):
            l = Line(lle_dots[i].get_center(), lle_dots[i+1].get_center(), color=GRAY_A, stroke_width=1.5)
            l.add_updater(lambda mob, idx=i: mob.put_start_and_end_on(lle_dots[idx].get_center(), lle_dots[idx+1].get_center()))
            lines.add(l)

        # --- PHASE 1 : ANIMATION SIMULTANÉE ---
        self.add(pca_axes)
        self.play(FadeIn(pca_dots), FadeIn(lle_dots), FadeIn(lines))
        self.wait(0.5)

        self.play(
            Rotate(pca_axes, angle=np.radians(15), about_point=np.array([-3.5, 0, 0])),
            *(lle_dots[i].animate.move_to(lle_end_pts[i]) for i in range(len(lle_dots))),
            run_time=3
        )
        self.wait(1)

        # --- PHASE 2 : NETTOYAGE & TRANSITION 3D ---
        self.play(FadeOut(title_lle), FadeOut(line), FadeOut(lle_dots), FadeOut(lines), FadeOut(title_pca))
        
        # Centrage et création du gros nuage "Cigare" 3D
        pts_3d_data = np.random.normal(size=(150, 3))
        pts_3d_data[:, 0] *= 2.5
        pts_3d_data[:, 1] *= 0.7
        pts_3d_data[:, 2] *= 0.4
        
        main_dots = VGroup(*[Dot3D(point=p, color=BLUE, radius=0.04) for p in pts_3d_data])
        pc1 = Line3D(start=[-3.5, 0, 0], end=[3.5, 0, 0], color=RED)
        pc2 = Line3D(start=[0, -1.5, 0], end=[0, 1.5, 0], color=GREEN)
        plane = Rectangle(width=7, height=3, fill_opacity=0.15, fill_color=WHITE).set_stroke(WHITE, 1)

        self.play(ReplacementTransform(pca_dots, main_dots), ReplacementTransform(pca_axes, VGroup(pc1, pc2)))
        self.wait(0.5)

        # Passage en vue 3D
        self.move_camera(phi=70 * DEGREES, theta=-45 * DEGREES, run_time=2)
        self.play(Create(plane))
        self.wait(1)

        # --- PHASE 3 : PROJECTION ET RETOUR FACE 2D ---
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, run_time=2.5)
        self.play(
            *[d.animate.move_to([d.get_center()[0], d.get_center()[1], 0]) for d in main_dots],
            run_time=2
        )
        self.wait(2)