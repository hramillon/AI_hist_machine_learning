from manim import *
import numpy as np

BG     = "#0F1117"
WHITE  = "#F0F4F8"
GREY   = "#8899AA"
PURPLE = "#A78BFA"
GOLD   = "#FFD54F"
GREEN  = "#A5D6A7"
RED    = "#EF9A9A"
DARK_GREEN = "#2E7D32"
DARK_RED   = "#B71C1C"


class Scene5Cost(Scene):
    def construct(self):
        self.camera.background_color = BG
        self._spam_good()
        self._spam_bad()
        self._formula()
        self._both_curves()

    # ── 1. Bon cas : spam prédit à 0.99 ──────────────────────────────────────
    def _spam_good(self):
        title = Text("Fonction de coût", font="Montserrat",
                     font_size=32, color=WHITE).to_edge(UP, buff=0.35)
        self.play(FadeIn(title))

        # Email visuel
        email = self._email_box().shift(LEFT * 3.5 + UP * 0.4)
        label_y = MathTex(r"y = 1 \text{ (spam)}", font_size=26, color=RED)\
                  .next_to(email, DOWN, 0.2)
        self.play(FadeIn(email), FadeIn(label_y), run_time=0.6)

        # Flèche → modèle → prédiction
        arrow1 = Arrow(email.get_right(), email.get_right() + RIGHT * 1.5,
                       buff=0, color=GREY, stroke_width=2)
        pred_good = MathTex(r"\hat{p} = 0.99", font_size=32, color=GREEN)\
                    .next_to(arrow1, RIGHT, 0.15)
        self.play(GrowArrow(arrow1), Write(pred_good), run_time=0.6)

        # Coût → faible
        arrow2 = Arrow(pred_good.get_right(), pred_good.get_right() + RIGHT * 1.4,
                       buff=0, color=GREY, stroke_width=2)
        cost_good = MathTex(r"c \approx 0.01", font_size=30, color=GREEN)\
                    .next_to(arrow2, RIGHT, 0.15)
        bar_good = self._cost_bar(height=0.15, color=GREEN)\
                   .next_to(cost_good, DOWN, 0.25)
        comment_good = Text("coût faible ✓", font="Montserrat",
                            font_size=19, color=GREEN)\
                       .next_to(bar_good, DOWN, 0.15)
        self.play(GrowArrow(arrow2), Write(cost_good), run_time=0.5)
        self.play(FadeIn(bar_good), FadeIn(comment_good))
        self.wait(1.2)

        self._good_group = VGroup(email, label_y, arrow1, pred_good,
                                  arrow2, cost_good, bar_good, comment_good)
        self._title = title

    # ── 2. Mauvais cas : spam prédit à 0.01 ──────────────────────────────────
    def _spam_bad(self):
        # Même email, déplacer le groupe précédent vers le haut
        self.play(self._good_group.animate.shift(UP * 1.4).scale(0.82),
                  run_time=0.5)

        email2 = self._email_box().shift(LEFT * 3.5 - UP * 1.6)
        label_y2 = MathTex(r"y = 1 \text{ (spam)}", font_size=26, color=RED)\
                   .next_to(email2, DOWN, 0.2)
        self.play(FadeIn(email2), FadeIn(label_y2), run_time=0.5)

        arrow1b = Arrow(email2.get_right(), email2.get_right() + RIGHT * 1.5,
                        buff=0, color=GREY, stroke_width=2)
        pred_bad = MathTex(r"\hat{p} = 0.01", font_size=32, color=RED)\
                   .next_to(arrow1b, RIGHT, 0.15)
        self.play(GrowArrow(arrow1b), Write(pred_bad), run_time=0.6)

        arrow2b = Arrow(pred_bad.get_right(), pred_bad.get_right() + RIGHT * 1.4,
                        buff=0, color=GREY, stroke_width=2)
        cost_bad = MathTex(r"c \approx 4.6", font_size=30, color=RED)\
                   .next_to(arrow2b, RIGHT, 0.15)
        bar_bad = self._cost_bar(height=1.4, color=RED)\
                  .next_to(cost_bad, DOWN, 0.25)
        comment_bad = Text("coût élevé ✗", font="Montserrat",
                           font_size=19, color=RED)\
                      .next_to(bar_bad, DOWN, 0.15)
        self.play(GrowArrow(arrow2b), Write(cost_bad), run_time=0.5)
        self.play(FadeIn(bar_bad), FadeIn(comment_bad))
        self.wait(1.4)

        self.play(FadeOut(self._good_group),
                  FadeOut(VGroup(email2, label_y2, arrow1b, pred_bad,
                                 arrow2b, cost_bad, bar_bad, comment_bad)),
                  FadeOut(self._title),
                  run_time=0.5)

    # ── 3. Formule mathématique ───────────────────────────────────────────────
    def _formula(self):
        formula = MathTex(
            r"c(\theta) = \begin{cases}"
            r"-\log(\hat{p}) & \text{si } y = 1 \\"
            r"-\log(1 - \hat{p}) & \text{si } y = 0"
            r"\end{cases}",
            font_size=38, color=WHITE
        ).shift(UP * 1.6)

        self.play(Write(formula), run_time=1.2)

        # Annoter chaque branche
        brace1 = Brace(formula[0][10:22], direction=DOWN, color=GREEN)
        ann1 = Text("pénalise si confiant\net dans le faux",
                    font="Montserrat", font_size=17, color=GREEN,
                    line_spacing=1.2).next_to(brace1, DOWN, 0.1)

        self.play(FadeIn(brace1), FadeIn(ann1), run_time=0.5)
        self.wait(0.7)
        self.play(FadeOut(brace1), FadeOut(ann1), run_time=0.3)

        # Montrer que −log(0.99) ≈ 0.01  et  −log(0.01) ≈ 4.6
        val1 = MathTex(r"-\log(0.99) \approx 0.01", font_size=28, color=GREEN)\
               .shift(DOWN * 0.3 + LEFT * 2.8)
        val2 = MathTex(r"-\log(0.01) \approx 4.61", font_size=28, color=RED)\
               .shift(DOWN * 0.3 + RIGHT * 2.8)
        sep = Line(UP * 0.3, DOWN * 0.9, color=GREY, stroke_width=0.8)\
              .shift(DOWN * 0.3)
        self.play(FadeIn(val1), FadeIn(sep), FadeIn(val2), run_time=0.6)
        self.wait(1.2)
        self.play(FadeOut(val1), FadeOut(val2), FadeOut(sep))

        self._formula_mob = formula

    # ── 4. Les deux courbes côte à côte ──────────────────────────────────────
    def _both_curves(self):
        self.play(self._formula_mob.animate.scale(0.62).to_edge(UP, buff=0.2),
                  run_time=0.5)

        # Axes gauche : −log(p̂), y=1
        ax_left = Axes(
            x_range=[0.01, 1, 0.25], y_range=[0, 5, 1],
            x_length=4.2, y_length=3.2,
            axis_config=dict(color=GREY, stroke_width=1,
                             include_ticks=True, include_tip=False),
            x_axis_config={"numbers_to_include": [0.25, 0.5, 0.75, 1.0],
                           "font_size": 18},
            y_axis_config={"numbers_to_include": [0, 1, 2, 3, 4],
                           "font_size": 18},
        ).shift(LEFT * 2.8 + DOWN * 0.85)

        ax_right = Axes(
            x_range=[0, 0.99, 0.25], y_range=[0, 5, 1],
            x_length=4.2, y_length=3.2,
            axis_config=dict(color=GREY, stroke_width=1,
                             include_ticks=True, include_tip=False),
            x_axis_config={"numbers_to_include": [0.0, 0.25, 0.5, 0.75],
                           "font_size": 18},
            y_axis_config={"numbers_to_include": [0, 1, 2, 3, 4],
                           "font_size": 18},
        ).shift(RIGHT * 2.8 + DOWN * 0.85)

        # Labels
        lbl_left  = MathTex(r"-\log(\hat{p})", font_size=22, color=GREEN)\
                    .next_to(ax_left,  UP, 0.12)
        lbl_left2 = Text("y = 1", font="Montserrat", font_size=18, color=GREEN)\
                    .next_to(lbl_left, DOWN, 0.08)
        lbl_right  = MathTex(r"-\log(1 - \hat{p})", font_size=22, color=PURPLE)\
                     .next_to(ax_right, UP, 0.12)
        lbl_right2 = Text("y = 0", font="Montserrat", font_size=18, color=PURPLE)\
                     .next_to(lbl_right, DOWN, 0.08)

        self.play(Create(ax_left), Create(ax_right),
                  FadeIn(lbl_left), FadeIn(lbl_left2),
                  FadeIn(lbl_right), FadeIn(lbl_right2),
                  run_time=0.7)

        # Courbe gauche : −log(p̂)  pour p̂ ∈ (0,1]
        curve_left = ax_left.plot(
            lambda p: -np.log(p),
            x_range=[0.02, 0.99],
            color=GREEN, stroke_width=2.8
        )
        # Courbe droite : −log(1−p̂) pour p̂ ∈ [0,1)
        curve_right = ax_right.plot(
            lambda p: -np.log(1 - p),
            x_range=[0.01, 0.97],
            color=PURPLE, stroke_width=2.8
        )

        self.play(Create(curve_left), Create(curve_right), run_time=1.1)

        # Points clés sur courbe gauche
        for p_val, label_str, side in [(0.99, r"\hat{p}=0.99 \Rightarrow c\approx0.01", RIGHT),
                                        (0.01, r"\hat{p}=0.01 \Rightarrow c\approx4.6",  RIGHT)]:
            c_val = min(-np.log(p_val), 4.9)
            dot  = Dot(ax_left.c2p(p_val, c_val), radius=0.09, color=GOLD)
            ann  = MathTex(label_str, font_size=17, color=GOLD)\
                   .next_to(dot, side * 0.5 + UP * 0.3, buff=0.1)
            self.play(FadeIn(dot), FadeIn(ann), run_time=0.45)
            self.wait(0.7)

        # Annotation symétrie courbe droite
        insight = Text("Symétrique : pénalise\nsi le modèle dit ŷ=1\nalors que y=0",
                       font="Montserrat", font_size=17, color=PURPLE,
                       line_spacing=1.25)\
                  .next_to(ax_right, DOWN, 0.2)
        self.play(FadeIn(insight))
        self.wait(1.5)

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _email_box(self):
        box  = RoundedRectangle(width=2.2, height=1.3,
                                corner_radius=0.15,
                                color=GREY, stroke_width=1.5,
                                fill_color="#1C2333", fill_opacity=1)
        line1 = Line(LEFT*0.7, RIGHT*0.7, color=GREY, stroke_width=1)\
                .shift(UP*0.25)
        line2 = Line(LEFT*0.7, RIGHT*0.3, color=GREY, stroke_width=1)
        line3 = Line(LEFT*0.7, RIGHT*0.5, color=GREY, stroke_width=1)\
                .shift(DOWN*0.25)
        icon = Text("✉", font_size=22, color=GREY).shift(LEFT*0.55 + UP*0.25)
        return VGroup(box, line1, line2, line3, icon)

    def _cost_bar(self, height, color):
        bar = Rectangle(width=0.5, height=height,
                        color=color, fill_color=color, fill_opacity=0.8,
                        stroke_width=1)
        return bar