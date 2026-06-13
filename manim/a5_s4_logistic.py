from manim import *
import numpy as np

BG    = "#0F1117"
WHITE = "#F0F4F8"
GREY  = "#8899AA"
PURPLE = "#A78BFA"
GOLD   = "#FFD54F"
BLUE   = "#4FC3F7"
GREEN  = "#A5D6A7"
RED    = "#EF9A9A"

def sigmoid(t):
    return 1 / (1 + np.exp(-t))


class Scene4Sigmoid(Scene):
    def construct(self):
        self.camera.background_color = BG
        self._linear_problem()
        self._introduce_sigmoid()
        self._draw_curve()
        self._threshold()
        self._two_examples()

    # ── 1. Montrer que la régression linéaire sort n'importe quoi ────────────
    def _linear_problem(self):
        # Axe numérique simple
        line = NumberLine(
            x_range=[-4, 4, 1], length=9,
            color=GREY, include_numbers=True,
            font_size=22,
        ).shift(UP * 0.3)
        label_axis = Text("θᵀx  (valeur brute)", font="Montserrat",
                          font_size=20, color=GREY).next_to(line, DOWN, 0.35)

        self.play(Create(line), FadeIn(label_axis), run_time=0.7)

        # flèche qui balaye de -inf à +inf
        arrow_sweep = Arrow(line.n2p(-3.5), line.n2p(3.5),
                            buff=0, color=BLUE, stroke_width=3)
        inf_txt = Text("−∞  →  +∞", font="Montserrat",
                       font_size=22, color=BLUE).next_to(line, UP, 0.3)
        self.play(GrowArrow(arrow_sweep), FadeIn(inf_txt), run_time=0.9)
        self.wait(0.5)

        problem = Text("On veut une probabilité ∈ [0, 1]…",
                       font="Montserrat", font_size=22, color=GOLD)\
                  .to_edge(DOWN).shift(UP * 0.2)
        self.play(FadeIn(problem, shift=UP * 0.1))
        self.wait(1.0)
        self.play(FadeOut(line), FadeOut(label_axis),
                  FadeOut(arrow_sweep), FadeOut(inf_txt), FadeOut(problem))

    # ── 2. Présenter la formule σ ─────────────────────────────────────────────
    def _introduce_sigmoid(self):
        formula_p = MathTex(
            r"\hat{p} = \sigma(\theta^T x)",
            font_size=44, color=WHITE
        ).shift(UP * 1.2)

        formula_sig = MathTex(
            r"\sigma(t) = \frac{1}{1 + e^{-t}}",
            font_size=44, color=PURPLE
        ).next_to(formula_p, DOWN, 0.55)

        brace_p   = Brace(formula_p,   direction=RIGHT, color=GREY)
        brace_sig = Brace(formula_sig, direction=RIGHT, color=GREY)
        txt_p   = Text("probabilité prédite", font="Montserrat",
                       font_size=18, color=GREY).next_to(brace_p, RIGHT, 0.15)
        txt_sig = Text("écrase ℝ dans [0, 1]", font="Montserrat",
                       font_size=18, color=GREY).next_to(brace_sig, RIGHT, 0.15)

        self.play(Write(formula_p), run_time=0.8)
        self.play(FadeIn(brace_p), FadeIn(txt_p))
        self.wait(0.5)
        self.play(Write(formula_sig), run_time=0.9)
        self.play(FadeIn(brace_sig), FadeIn(txt_sig))
        self.wait(1.2)
        self.play(FadeOut(brace_p), FadeOut(txt_p),
                  FadeOut(brace_sig), FadeOut(txt_sig))

        # Conserver les formules en haut, réduites
        self.play(
            formula_p.animate.scale(0.7).to_corner(UL).shift(RIGHT*0.3+DOWN*0.1),
            formula_sig.animate.scale(0.7).to_corner(UR).shift(LEFT*0.3+DOWN*0.1),
            run_time=0.7
        )
        self._f_p   = formula_p
        self._f_sig = formula_sig

    # ── 3. Tracer la courbe sigmoïde ─────────────────────────────────────────
    def _draw_curve(self):
        ax = Axes(
            x_range=[-6, 6, 1], y_range=[-0.1, 1.1, 0.5],
            x_length=9, y_length=4.5,
            axis_config=dict(color=GREY, stroke_width=1,
                             include_ticks=True, include_tip=True,
                             tip_width=0.15, tip_height=0.15),
            x_axis_config={"numbers_to_include": [-4, -2, 0, 2, 4],
                           "font_size": 20},
            y_axis_config={"numbers_to_include": [0, 0.5, 1],
                           "font_size": 20},
        ).shift(DOWN * 0.6)

        x_lbl = MathTex(r"t = \theta^T x", font_size=24, color=GREY)\
                .next_to(ax.x_axis.get_end(), RIGHT, 0.15)
        y_lbl = MathTex(r"\sigma(t)", font_size=24, color=GREY)\
                .next_to(ax.y_axis.get_end(), UP, 0.1)

        self.play(Create(ax), FadeIn(x_lbl), FadeIn(y_lbl), run_time=0.7)

        curve = ax.plot(sigmoid, x_range=[-6, 6], color=PURPLE, stroke_width=3)
        self.play(Create(curve), run_time=1.2)

        # Asymptotes pointillées
        dash_0 = DashedLine(ax.c2p(-6, 0), ax.c2p(6, 0),
                            dash_length=0.12, color=GREY, stroke_width=1)
        dash_1 = DashedLine(ax.c2p(-6, 1), ax.c2p(6, 1),
                            dash_length=0.12, color=GREY, stroke_width=1)
        lbl_0 = Text("0", font_size=18, color=GREY).next_to(ax.c2p(-6.2, 0), LEFT, 0.05)
        lbl_1 = Text("1", font_size=18, color=GREY).next_to(ax.c2p(-6.2, 1), LEFT, 0.05)
        self.play(Create(dash_0), Create(dash_1),
                  FadeIn(lbl_0), FadeIn(lbl_1), run_time=0.5)
        self.wait(0.5)

        self._ax    = ax
        self._curve = curve
        self._x_lbl = x_lbl
        self._y_lbl = y_lbl
        self._dashes = VGroup(dash_0, dash_1, lbl_0, lbl_1)

    # ── 4. Ligne de seuil 0.5 ────────────────────────────────────────────────
    def _threshold(self):
        ax = self._ax
        # ligne horizontale seuil
        thresh_line = DashedLine(
            ax.c2p(-6, 0.5), ax.c2p(6, 0.5),
            dash_length=0.15, color=GOLD, stroke_width=2
        )
        thresh_lbl = Text("seuil 0.5", font="Montserrat",
                          font_size=19, color=GOLD)\
                     .next_to(ax.c2p(4.5, 0.5), UP, 0.1)

        self.play(Create(thresh_line), FadeIn(thresh_lbl), run_time=0.6)

        # Zone ŷ=0 (gauche / bas)
        zone0 = ax.get_area(self._curve,
                             x_range=[-6, 0],
                             bounded_graph=ax.plot(lambda t: 0.5, x_range=[-6, 0]),
                             color=BLUE, opacity=0.12)
        lbl_z0 = Text("ŷ = 0", font="Montserrat",
                       font_size=22, color=BLUE).move_to(ax.c2p(-3.5, 0.22))

        # Zone ŷ=1 (droite / haut)
        zone1 = ax.get_area(self._curve,
                             x_range=[0, 6],
                             bounded_graph=ax.plot(lambda t: 0.5, x_range=[0, 6]),
                             color=GREEN, opacity=0.12)
        lbl_z1 = Text("ŷ = 1", font="Montserrat",
                       font_size=22, color=GREEN).move_to(ax.c2p(3.5, 0.78))

        self.play(FadeIn(zone0), FadeIn(lbl_z0),
                  FadeIn(zone1), FadeIn(lbl_z1), run_time=0.7)
        self.wait(0.8)

        self._thresh_line = thresh_line
        self._thresh_lbl  = thresh_lbl
        self._zones = VGroup(zone0, lbl_z0, zone1, lbl_z1)

    # ── 5. Deux exemples concrets ─────────────────────────────────────────────
    def _two_examples(self):
        ax = self._ax

        examples = [
            {"t":  2.5, "color": GREEN, "label": "p̂ ≈ 0.92  →  ŷ = 1", "side": UP},
            {"t": -1.8, "color": BLUE,  "label": "p̂ ≈ 0.14  →  ŷ = 0", "side": DOWN},
        ]

        for ex in examples:
            t_val = ex["t"]
            p_val = sigmoid(t_val)
            col   = ex["color"]

            # Point sur la courbe
            pt_screen = ax.c2p(t_val, p_val)
            dot = Dot(pt_screen, radius=0.1, color=col)

            # Lignes verticale + horizontale (projection)
            v_line = DashedLine(ax.c2p(t_val, 0), pt_screen,
                                dash_length=0.1, color=col, stroke_width=1.5)
            h_line = DashedLine(ax.c2p(-6, p_val), pt_screen,
                                dash_length=0.1, color=col, stroke_width=1.5)

            # Annotation
            ann = Text(ex["label"], font="Montserrat",
                       font_size=19, color=col)\
                  .next_to(dot, ex["side"] * 0.8 + RIGHT * 0.3, buff=0.2)

            self.play(Create(v_line), Create(h_line), run_time=0.4)
            self.play(FadeIn(dot), FadeIn(ann), run_time=0.4)
            self.wait(0.9)

        self.wait(1.0)