from manim import *
import numpy as np

class PCAvsLLE(Scene):
    def construct(self):
        # Titres et Séparation
        title_pca = Text("PCA (Variance & Rotation)", font_size=24).to_edge(UP).shift(LEFT * 3.5)
        title_lle = Text("LLE (Unrolling Manifold)", font_size=24).to_edge(UP).shift(RIGHT * 3.5)
        line = Line(UP * 4, DOWN * 4, color=GRAY)
        self.add(title_pca, title_lle, line)

        # --- GAUCHE : PCA ---
        # Génération de points étirés
        np.random.seed(42)
        raw_pts = np.random.normal(size=(40, 3))
        # Correction ici : application de l'étirement directement
        raw_pts = raw_pts * np.array([1.5, 0.4, 0.0]) 
        
        # Rotation initiale pour l'effet oblique
        theta = np.radians(30)
        c, s = np.cos(theta), np.sin(theta)
        R = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
        pca_pts_data = raw_pts @ R.T + np.array([-3.5, 0, 0])

        pca_dots = VGroup(*[Dot(point=pt, radius=0.05, color=BLUE) for pt in pca_pts_data])
        
        # Axes PCA
        axis_1 = Line(start=[-3.5, 0, 0], end=[-3.5 + 2*c, 2*s, 0], color=RED, stroke_width=4)
        axis_2 = Line(start=[-3.5, 0, 0], end=[-3.5 - s, c, 0], color=GREEN, stroke_width=4)
        pca_axes = VGroup(axis_1, axis_2)

        # --- DROITE : LLE ---
        # Création d'un S-curve (manifold)
        t = np.linspace(-1.5 * np.pi, 1.5 * np.pi, 40)
        lle_start_pts = np.c_[np.sin(t) * 1.2 + 3.5, t * 0.5, np.zeros_like(t)]
        lle_end_pts = np.c_[t * 0.5 + 3.5, np.zeros_like(t), np.zeros_like(t)]

        lle_dots = VGroup(*[Dot(point=pt, radius=0.06, color=PURPLE) for pt in lle_start_pts])
        
        # Liens entre voisins (Réseau)
        lines = VGroup()
        for i in range(len(lle_start_pts) - 1):
            l = Line(lle_dots[i].get_center(), lle_dots[i+1].get_center(), color=GRAY_A, stroke_width=1.5)
            # Mise à jour automatique des lignes quand les points bougent
            l.add_updater(lambda mob, idx=i: mob.put_start_and_end_on(lle_dots[idx].get_center(), lle_dots[idx+1].get_center()))
            lines.add(l)

        # --- ANIMATION ---
        # Affichage initial
        self.add(pca_axes) # On affiche les axes au départ
        self.play(FadeIn(pca_dots), FadeIn(lle_dots), FadeIn(lines))
        self.wait(0.5)

        # 1. PCA : Rotation des axes pour s'aligner sur la variance
        self.play(
            Rotate(pca_axes, angle=np.radians(15), about_point=np.array([-3.5, 0, 0])),
            run_time=2,
            rate_func=linear
        )
        self.wait(0.5)

        # 2. LLE : Déroulement du manifold
        self.play(
            *(lle_dots[i].animate.move_to(lle_end_pts[i]) for i in range(len(lle_dots))),
            run_time=3,
            rate_func=smooth
        )
        self.wait(1.5)