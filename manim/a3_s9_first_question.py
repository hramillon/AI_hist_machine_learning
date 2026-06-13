from manim import *
import random

class Scene9CART(Scene):
    def construct(self):
        random.seed(42)

        # --- 1. Initialisation ---
        boite = Rectangle(width=6.5, height=4.5, color=WHITE, stroke_width=3)
        boite.set_fill(BLACK, opacity=1)
        boite.shift(UP * 0.5)

        pts_dem = VGroup(*[
            Dot(point=[random.uniform(-2.8, -0.3), random.uniform(-1.8, 1.8), 0], color=BLUE, radius=0.07)
            for _ in range(15)
        ]).shift(boite.get_center())

        pts_rep = VGroup(*[
            Dot(point=[random.uniform(0.3, 2.8), random.uniform(-1.8, 1.8), 0], color=RED, radius=0.07)
            for _ in range(15)
        ]).shift(boite.get_center())

        tous_les_points = VGroup(pts_dem, pts_rep)

        self.add(boite, tous_les_points)
        self.wait(0.5)

        # --- 2. Mauvaise Coupure ---
        ligne_mauvaise = Line(
            start=[boite.get_left()[0], boite.get_center()[1], 0],
            end=[boite.get_right()[0], boite.get_center()[1], 0],
            color=WHITE,
            stroke_width=5
        )

        self.play(Create(ligne_mauvaise), run_time=0.4)
        self.wait(0.5)

        txt_impure = Text("50% Démocrates / 50% Républicains", font_size=16, color=WHITE).move_to(boite.get_center() + UP * 0.3)
        
        self.play(
            ligne_mauvaise.animate.set_color(RED),
            FadeIn(txt_impure),
            run_time=0.3
        )
        self.wait(0.8)
        self.play(FadeOut(ligne_mauvaise), FadeOut(txt_impure), run_time=0.2)

        # --- 3. Bonne Coupure ---
        ligne_bonne = Line(
            start=[boite.get_center()[0], boite.get_top()[1], 0],
            end=[boite.get_center()[0], boite.get_bottom()[1], 0],
            color=WHITE,
            stroke_width=5
        )

        self.play(Create(ligne_bonne), run_time=0.4)
        self.wait(0.5)

        txt_pur_gauche = VGroup(
            Text("100% Dém", font_size=12, color=WHITE),
            Text("0% Rep", font_size=12, color=WHITE)
        ).arrange(DOWN, buff=0.05).move_to(boite.get_center() + LEFT * 1.6)

        txt_pur_droite = VGroup(
            Text("0% Dém", font_size=12, color=WHITE),
            Text("100% Rep", font_size=12, color=WHITE)
        ).arrange(DOWN, buff=0.05).move_to(boite.get_center() + RIGHT * 1.6)
        
        labels_purete = VGroup(txt_pur_gauche, txt_pur_droite)

        self.play(
            ligne_bonne.animate.set_color(GREEN),
            FadeIn(labels_purete),
            run_time=0.3
        )
        self.wait(0.5)

        # --- 4. Déplacement et Titre ---
        visuel_gauche = VGroup(boite, tous_les_points, ligne_bonne, labels_purete)
        target_pos = LEFT * 3.5 + UP * 0.5
        titre_cart = Text("CART", font_size=42, weight=BOLD).move_to(RIGHT * 3.5 + UP * 2.8)

        self.play(
            visuel_gauche.animate.scale(0.65).move_to(target_pos),
            Write(titre_cart),
            run_time=0.8
        )
        self.wait(0.4)

        # --- 5. Apparition Séquentielle Épurée ---
        ligne_k = Text("k :  largeur de la pétale  /  longueur de la pétale", font_size=13, color=WHITE)
        ligne_tk = Text("t_k :  1.5cm  /  2.45cm  /  3.8cm", font_size=13, color=WHITE)
        ligne_couple = Text("Couple final : (k, t_k)", font_size=14, color=WHITE)

        bloc_math = VGroup(ligne_k, ligne_tk, ligne_couple).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        bloc_math.next_to(titre_cart, DOWN, buff=0.4).shift(RIGHT * 0.2)

        self.play(Write(ligne_k), run_time=0.4)
        self.play(Write(ligne_tk), run_time=0.4)
        self.play(FadeIn(ligne_couple, shift=UP * 0.1), run_time=0.3)
        self.wait(0.4)

        # --- 6. Formule de Coût J et Définitions ---
        txt_minimisons = Text("On cherche à minimiser :", font_size=14, color=WHITE)
        
        formule_j = MathTex(
            "J(k, t_k) = \\frac{m_{\\text{gauche}}}{m} G_{\\text{gauche}} + \\frac{m_{\\text{droite}}}{m} G_{\\text{droite}}",
            font_size=24, color=WHITE
        )
        
        def_m = Text("m : nombre total d'instances (150)", font_size=12, color=WHITE)
        def_mg = Text("m_gauche : instances partant à gauche", font_size=12, color=WHITE)
        def_md = Text("m_droite : instances partant à droite", font_size=12, color=WHITE)
        def_g = Text("G : impureté du sous-groupe", font_size=12, color=WHITE)

        bloc_formule = VGroup(txt_minimisons, formule_j, def_m, def_mg, def_md, def_g).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        bloc_formule.next_to(bloc_math, DOWN, buff=0.5).shift(RIGHT * 0.1)

        self.play(Write(txt_minimisons), run_time=0.3)
        self.play(Write(formule_j), run_time=0.5)
        self.play(
            FadeIn(VGroup(def_m, def_mg, def_md, def_g), lag_ratio=0.2),
            run_time=0.6
        )
        self.wait(2.0)