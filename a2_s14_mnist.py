from manim import *
from sklearn.datasets import fetch_openml
import numpy as np

class MnistZoom(Scene):
    def construct(self):
        # 1. Récupération des vraies données MNIST
        mnist = fetch_openml('mnist_784', version=1, as_frame=False, parser='liac-arff')
        mnist_data = mnist.data[42].reshape(28, 28).astype(int)[::-1]
        zoom_data = mnist_data[12:16, 12:16]

        # 2. Création de la grille de pixels initiale
        pixel_size = 0.12
        pixels = VGroup(*[
            Square(side_length=pixel_size, stroke_width=0.5, stroke_color=GRAY)
            .set_fill(interpolate_color(BLACK, WHITE, mnist_data[r, c]/255), opacity=1)
            .move_to([c * pixel_size, r * pixel_size, 0])
            for r in range(28) for c in range(28)
        ]).center()

        # --- ANIMATION 1 : Affichage fixe au milieu (13 secondes) ---
        self.add(pixels)
        self.wait(13s)

        # --- ANIMATION 2 : Étalement en vecteur, Zoom et Reformation (15 secondes) ---
        grille_positions = [p.get_center() for p in pixels]
        
        # Taille grandie des pixels lors du zoom sur le vecteur pour bien les voir
        vecteur_pixel_size_zoom = 0.4 
        
        # Aller : Étalement en un vecteur ultra large qui dépasse de l'écran (6.5s)
        self.play(
            *[pixels[i].animate.move_to([(i - 392) * vecteur_pixel_size_zoom, 0, 0])
                               .set_width(vecteur_pixel_size_zoom)
                               .set_height(vecteur_pixel_size_zoom)
                               .set_stroke(width=1, color=GRAY)
              for i in range(len(pixels))],
            run_time=6.5
        )
        
        # Pause : Défilement/Zoom sur le vecteur pour observer les valeurs/pixels (2s)
        self.play(pixels.animate.shift(LEFT * 3), run_time=2)
        
        # Retour : Contraction et reformation de l'image initiale (6.5s)
        self.play(
            *[pixels[i].animate.move_to(grille_positions[i])
                               .set_width(pixel_size)
                               .set_height(pixel_size)
                               .set_stroke(width=0.5, color=GRAY)
              for i in range(len(pixels))],
            run_time=6.5
        )

        # --- ANIMATION 3 : Zoom final avec valeurs numériques (8 secondes) ---
        cadre_zoom = Rectangle(
            width=4 * pixel_size, 
            height=4 * pixel_size, 
            color=RED, 
            stroke_width=2
        ).move_to(pixels[12*28 + 12].get_center() + RIGHT * pixel_size * 1.5 + UP * pixel_size * 1.5)

        case_size = 1.2
        grille_zoomee = VGroup()
        valeurs_textes = VGroup()

        for r in range(4):
            for c in range(4):
                val = zoom_data[r, c]
                pos = [c * case_size + 1, (3 - r) * case_size - 1.8, 0]
                
                case = Square(side_length=case_size, stroke_width=2, stroke_color=RED).move_to(pos)
                case.set_fill(interpolate_color(BLACK, WHITE, val / 255), opacity=1)
                grille_zoomee.add(case)
                
                txt = Text(str(val), font_size=20, color=BLACK if val > 128 else WHITE).move_to(pos)
                valeurs_textes.add(txt)

        self.play(Create(cadre_zoom), run_time=1)
        self.play(
            pixels.animate.scale(0.6).to_edge(LEFT, buff=1),
            cadre_zoom.animate.scale(0.6).move_to(pixels[12*28 + 12].get_center() + (RIGHT * pixel_size * 1.5 + UP * pixel_size * 1.5) * 0.6),
            run_time=2
        )
        self.play(Create(grille_zoomee), run_time=1.5)
        self.play(LaggedStart(*[Write(t) for t in valeurs_textes], lag_ratio=0.05), run_time=2)
        self.wait(1.5)