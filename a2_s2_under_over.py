from manim import *
import numpy as np

class AnalyseRegression(Scene):
    def construct(self):
        # 1. Configuration des axes (plus centrés)
        axes = Axes(
            x_range=[-3, 3, 1], 
            y_range=[-1, 8, 1], 
            x_length=7, 
            y_length=5,
            axis_config={"include_tip": True}
        ).shift(RIGHT * 0.5) 

        # 2. Données (Parabole bruitée)
        np.random.seed(42)
        x_data = np.array([-2.2, -1.5, -0.8, -0.2, 0.4, 1.1, 1.8, 2.3])
        y_data = x_data**2 + 1 + np.random.normal(0, 0.4, len(x_data))
        dots = VGroup(*[Dot(axes.c2p(x, y), color=BLUE, radius=0.08) for x, y in zip(x_data, y_data)])

        # 3. Étiquettes (Plus petites, positionnées en liste fixe à gauche)
        label_style = {"font_size": 24}
        
        # Position de départ pour le premier label
        label_bon = Text("Bon modèle", color=GREEN, **label_style).to_edge(LEFT, buff=1).shift(UP * 1)
        # Les suivants se placent en dessous du précédent
        label_over = Text("Overfitting", color=RED, **label_style).next_to(label_bon, DOWN, aligned_edge=LEFT, buff=0.4)
        label_under = Text("Underfitting", color=ORANGE, **label_style).next_to(label_over, DOWN, aligned_edge=LEFT, buff=0.4)

        # 4. Courbes
        bon_modele = axes.plot(lambda x: x**2 + 1, color=GREEN, x_range=[-2.4, 2.5])
        
        poly_overfit = np.polyfit(x_data, y_data, len(x_data) - 1)
        overfit_modele = axes.plot(lambda x: np.polyval(poly_overfit, x), color=RED, x_range=[-2.3, 2.4])
        
        underfit_modele = axes.plot(lambda x: -(1/2)*x + 1.25, color=ORANGE, x_range=[-2.5, 2.5])

        # --- SÉQUENCE D'ANIMATION ---

        # Phase 1 : Arrivée des points (4s)
        self.add(axes)
        self.play(FadeIn(dots, shift=RIGHT), run_time=2)
        self.wait(1)

        # Phase 2 : Bon Modèle (Affiche et reste)
        self.play(Create(bon_modele), Write(label_bon), run_time=1)
        self.wait(1)

        # Phase 3 : Overfitting (S'ajoute sans effacer le reste)
        self.play(Create(overfit_modele), Write(label_over), run_time=1)
        self.wait(14)

        # Phase 4 : Underfitting (S'ajoute également)
        self.play(Create(underfit_modele), Write(label_under), run_time=1)
        self.wait(8)