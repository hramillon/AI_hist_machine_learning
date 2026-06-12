from manim import *

class InfiniteDimensions(ThreeDScene):
    def construct(self):
        # Caméra par défaut en 2D pour une lisibilité parfaite des textes
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)

        # 1. Échelle abaissée avec flèche au bout
        echelle_axe = Arrow(
            start=LEFT * 4.5, 
            end=RIGHT * 5, 
            buff=0, 
            stroke_width=4, 
            color=WHITE
        ).shift(UP * 2) # Abaissé par rapport au bord de l'écran

        # Chiffres de 0 à 10 placés sous la ligne de l'échelle
        chiffres = VGroup(*[
            Text(str(i), font_size=20).next_to(echelle_axe.point_from_proportion(i/10), DOWN, buff=0.2)
            for i in range(11)
        ])

        # Animation de l'échelle : La flèche d'abord, puis les chiffres de gauche à droite (2s)
        self.play(Create(echelle_axe), run_time=1)
        self.play(LaggedStart(*[Write(c) for c in chiffres], lag_ratio=0.1), run_time=2)
        self.wait(1)

        # 2. Évolution du vecteur au centre (Reste toujours centré)
        # t=0: (1)
        v_text = MathTex("(1)", font_size=42).move_to(ORIGIN)
        self.play(Write(v_text))
        self.wait(0.7)

        # t=1: (1, 8)
        v_text_2d = MathTex("(1, 8)", font_size=42).move_to(ORIGIN)
        self.play(Transform(v_text, v_text_2d))
        self.wait(0.7)

        # t=2: (1, 8, 3) - RESTE AU CENTRE
        v_text_3d = MathTex("(1, 8, 3)", font_size=42).move_to(ORIGIN)
        self.play(Transform(v_text, v_text_3d))
        self.wait(0.7)

        # 3. Apparition du Cube à droite (sans bouger le vecteur) pendant 2s
        # On passe temporairement l'affichage du cube en fausse 3D (isométrique) pour qu'il soit visible sans tourner la caméra
        cube = Cube(side_length=1.5, fill_opacity=0.4, fill_color=BLUE, stroke_color=BLUE_A).move_to(RIGHT * 4)
        cube.rotate(30 * DEGREES, axis=OUT)
        cube.rotate(60 * DEGREES, axis=RIGHT)
        
        self.play(Create(cube), run_time=0.5)
        self.play(Rotate(cube, angle=PI/2, axis=UP), run_time=1)
        self.wait(0.5)

        # 4. Passage à l'infini : Le cube disparaît, le vecteur s'allonge au centre
        self.play(FadeOut(cube), run_time=1)

        v_text_infini = MathTex("(1, 8, 3, \\dots, 5, 2)", font_size=42).move_to(ORIGIN)
        self.play(Transform(v_text, v_text_infini), run_time=1.5)
        self.play(v_text.animate.set_color(YELLOW), run_time=0.5)
        self.wait(2)