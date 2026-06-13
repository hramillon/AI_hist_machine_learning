from manim import *
import random

class SceneEspaceDecision2D(Scene):
    def construct(self):
        # Configuration des couleurs
        c_dem = BLUE
        c_rep = RED
        c_coupure = GOLD

        # Titre de la scène
        titre = Text("Espace de Décision (2D)", font_size=36).to_edge(UP)
        self.play(FadeIn(titre))
        self.wait(0.5)

        # --- 1. Création de la Boîte (Espace 2D) ---
        boite = Rectangle(width=7, height=5, color=WHITE, stroke_width=3)
        boite.set_fill(BLACK, opacity=1)
        boite.shift(DOWN * 0.5)

        # Labels des axes
        label_x = Text("Score Contenu Droite", font_size=16).next_to(boite, DOWN, buff=0.2)
        label_y = Text("Temps de visionnage", font_size=16).next_to(boite, LEFT, buff=0.2).rotate(90 * DEGREES)

        # Conteneur global du visuel initial
        visual_group = VGroup(boite, label_x, label_y)
        
        # Position de départ hors écran à droite, puis animation vers le centre
        visual_group.shift(RIGHT * 10)
        self.play(visual_group.animate.shift(LEFT * 10), run_time=1.5)
        self.wait(0.5)

        # --- 2. Génération des Points (Démocrates vs Républicains) ---
        # Points Gauche (Démocrates)
        points_dem = VGroup(*[
            Dot(point=[random.uniform(-3.1, -0.7), random.uniform(-2.1, 2.1), 0], color=c_dem, radius=0.08)
            for _ in range(20)
        ])
        
        # Points Droite (Républicains)
        points_rep = VGroup(*[
            Dot(point=[random.uniform(-0.3, 3.1), random.uniform(-2.1, 2.1), 0], color=c_rep, radius=0.08)
            for _ in range(20)
        ])

        # Alignement sur le centre actuel de la boîte
        points_dem.shift(boite.get_center())
        points_rep.shift(boite.get_center())

        # Apparition des données utilisateur
        self.play(FadeIn(points_dem), FadeIn(points_rep), run_time=1)
        self.wait(1)

        # --- 3. Tracé de la Coupure Perpendiculaire ---
        x_coupure = boite.get_center()[0] - 0.5
        y_haut = boite.get_top()[1]
        y_bas = boite.get_bottom()[1]

        ligne_coupure = Line(
            start=[x_coupure, y_haut, 0],
            end=[x_coupure, y_bas, 0],
            color=c_coupure,
            stroke_width=5
        )

        # Texte explicatif à droite
        txt_coupure = Text("Seuil de décision\n(Coupure orthogonale)", font_size=14, color=c_coupure).next_to(boite, RIGHT, buff=0.4)

        # Animation de la coupure qui sépare les deux groupes
        self.play(Create(ligne_coupure), Write(txt_coupure), run_time=1.5)
        self.wait(1)

        # Écartement des groupes pour marquer la frontière
        self.play(
            points_dem.animate.shift(LEFT * 0.2),
            points_rep.animate.shift(RIGHT * 0.2),
            run_time=1
        )
        self.wait(2)