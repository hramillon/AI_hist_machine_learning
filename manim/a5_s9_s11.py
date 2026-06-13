from manim import *
import numpy as np

BG     = "#0F1117"
WHITE  = "#F0F4F8"
GREY   = "#8899AA"
PURPLE = "#A78BFA"
GOLD   = "#FFD54F"
GREEN  = "#A5D6A7"
RED    = "#EF9A9A"
BLUE   = "#4FC3F7"

# Fonction de coût convexe simple : J(θ) = θ² + 0.5
def J(t):
    return t**2 + 0.3

def dJ(t):
    return 2 * t


class Scene11Gradient(Scene):
    def construct(self):
        self.camera.background_color = BG
        self._convex_bowl()
        self._gradient_descent_steps()
        self._summary()

    # ── 1. Montrer la convexité ───────────────────────────────────────────────
    def _convex_bowl(self):
        ax = Axes(
            x_range=[-3.2, 3.2, 1], y_range=[-0.2, 5, 1],
            x_length=8, y_length=5,
            axis_config=dict(color=GREY, stroke_width=1,
                             include_ticks=False, include_tip=True,
                             tip_width=0.15, tip_height=0.15),
        ).shift(DOWN * 0.5)

        x_lbl = MathTex(r"\theta", font_size=26, color=GREY)\
                .next_to(ax.x_axis.get_end(), RIGHT, 0.1)
        y_lbl = MathTex(r"J(\theta)", font_size=26, color=GREY)\
                .next_to(ax.y_axis.get_end(), UP, 0.1)

        self.play(Create(ax), FadeIn(x_lbl), FadeIn(y_lbl), run_time=0.6)

        bowl = ax.plot(J, x_range=[-2.8, 2.8], color=PURPLE, stroke_width=3)
        self.play(Create(bowl), run_time=1.0)

        # Annotation "forme de bol = convexe"
        arrow_bowl = CurvedArrow(
            ax.c2p(2.0, 4.3), ax.c2p(1.3, 2.1),
            color=GOLD, angle=-TAU/6, stroke_width=2
        )
        lbl_bowl = Text("forme de bol\n→ convexe", font="Montserrat",
                        font_size=19, color=GOLD, line_spacing=1.2)\
                   .next_to(ax.c2p(2.0, 4.5), RIGHT, 0.1)
        self.play(Create(arrow_bowl), FadeIn(lbl_bowl), run_time=0.6)

        # Minimum global
        dot_min = Dot(ax.c2p(0, J(0)), radius=0.1, color=GREEN)
        lbl_min = Text("minimum global", font="Montserrat",
                       font_size=18, color=GREEN)\
                  .next_to(dot_min, DOWN, 0.2)
        self.play(FadeIn(dot_min), FadeIn(lbl_min))
        self.wait(0.8)

        # Deux points de départ différents → même minimum
        for x_start, side in [(-2.5, LEFT), (2.2, RIGHT)]:
            pt = Dot(ax.c2p(x_start, J(x_start)), radius=0.08, color=BLUE)
            lbl_start = Text("départ", font="Montserrat",
                             font_size=16, color=BLUE)\
                        .next_to(pt, side * 0.8 + UP * 0.3, buff=0.1)
            arr = Arrow(pt.get_center(), dot_min.get_center(),
                        buff=0.15, color=BLUE, stroke_width=1.5,
                        max_tip_length_to_length_ratio=0.12)
            self.play(FadeIn(pt), FadeIn(lbl_start), run_time=0.3)
            self.play(GrowArrow(arr), run_time=0.5)

        self.wait(0.8)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

        self._ax   = ax
        self._bowl = bowl
        self._x_lbl = x_lbl
        self._y_lbl = y_lbl

    # ── 2. Les 4 étapes de la descente de gradient ───────────────────────────
    def _gradient_descent_steps(self):
        ax = Axes(
            x_range=[-3.2, 3.2, 1], y_range=[-0.2, 5, 1],
            x_length=7.5, y_length=4.8,
            axis_config=dict(color=GREY, stroke_width=1,
                             include_ticks=False, include_tip=True,
                             tip_width=0.15, tip_height=0.15),
        ).shift(LEFT * 0.5 + DOWN * 0.6)

        x_lbl = MathTex(r"\theta", font_size=24, color=GREY)\
                .next_to(ax.x_axis.get_end(), RIGHT, 0.1)
        y_lbl = MathTex(r"J(\theta)", font_size=24, color=GREY)\
                .next_to(ax.y_axis.get_end(), UP, 0.08)
        bowl  = ax.plot(J, x_range=[-2.8, 2.8], color=PURPLE, stroke_width=2.8)

        self.play(Create(ax), FadeIn(x_lbl), FadeIn(y_lbl),
                  Create(bowl), run_time=0.7)

        # ── Étape 1 : Initialisation ──
        step_lbl = self._step_label("1. Initialisation", GOLD)
        self.play(FadeIn(step_lbl))

        theta = 2.5          # point de départ
        dot   = Dot(ax.c2p(theta, J(theta)), radius=0.12, color=GOLD)
        init_lbl = MathTex(r"\theta_0 = 2.5", font_size=22, color=GOLD)\
                   .next_to(dot, UP + RIGHT * 0.3, buff=0.12)
        self.play(FadeIn(dot), FadeIn(init_lbl))
        self.wait(0.7)

        # ── Étape 2 : Calcul du gradient (tangente) ──
        step_lbl2 = self._step_label("2. Calcul du gradient", BLUE)
        self.play(ReplacementTransform(step_lbl, step_lbl2), FadeOut(init_lbl))

        # Tangente au point courant
        slope = dJ(theta)
        tang  = self._tangent(ax, theta, slope, color=BLUE)
        slope_lbl = MathTex(
            r"\frac{\partial J}{\partial \theta} > 0",
            font_size=22, color=BLUE
        ).next_to(ax.c2p(theta, J(theta)), RIGHT, 0.5)
        self.play(Create(tang), FadeIn(slope_lbl))
        self.wait(0.7)

        # ── Étape 3 : Mise à jour ──
        step_lbl3 = self._step_label("3. Mise à jour  θ ← θ − α · ∇J(θ)", GREEN)
        self.play(ReplacementTransform(step_lbl2, step_lbl3),
                  FadeOut(tang), FadeOut(slope_lbl))

        # Descendre par itérations
        lr = 0.38
        n_steps = 7
        thetas = [theta]
        prev_dot = dot

        for i in range(n_steps):
            theta_new = theta - lr * dJ(theta)
            new_dot   = Dot(ax.c2p(theta_new, J(theta_new)),
                            radius=0.10, color=GREEN)
            # Flèche de mise à jour sur la courbe
            arr = Arrow(
                ax.c2p(theta, J(theta)),
                ax.c2p(theta_new, J(theta_new)),
                buff=0.05, color=GREEN,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.15
            )
            # Tangente du gradient
            tang_i = self._tangent(ax, theta, dJ(theta),
                                   color=BLUE, width=1.2, opacity=0.5)

            self.play(Create(tang_i), run_time=0.18)
            self.play(GrowArrow(arr), FadeIn(new_dot), run_time=0.32)
            self.play(FadeOut(tang_i), FadeOut(arr),
                      prev_dot.animate.scale(0.7).set_opacity(0.4),
                      run_time=0.18)

            theta    = theta_new
            prev_dot = new_dot
            thetas.append(theta)

        # Highlight minimum atteint
        dot_min = Dot(ax.c2p(theta, J(theta)), radius=0.14, color=GREEN)
        ring = Circle(radius=0.28, color=GREEN, stroke_width=2)\
               .move_to(ax.c2p(theta, J(theta)))
        min_lbl = Text("minimum !", font="Montserrat",
                       font_size=19, color=GREEN)\
                  .next_to(ring, DOWN, 0.15)

        self.play(Transform(new_dot, dot_min), Create(ring), run_time=0.4)
        self.play(FadeIn(min_lbl))
        self.wait(0.8)

        # ── Étape 4 : Répétition ──
        step_lbl4 = self._step_label("4. Répéter jusqu'à convergence", GREY)
        self.play(ReplacementTransform(step_lbl3, step_lbl4))
        self.wait(1.0)

        self._ax2 = ax

    # ── 3. Récap learning rate ────────────────────────────────────────────────
    def _summary(self):
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

        title = Text("Le taux d'apprentissage α", font="Montserrat",
                     font_size=26, color=WHITE).to_edge(UP, buff=0.4)
        self.play(FadeIn(title))

        # Trois mini-bols côte à côte
        configs = [
            {"lr": 0.05, "label": "α trop petit\n(lent)",    "col": RED,    "x": -4.5},
            {"lr": 0.38, "label": "α optimal\n(convergence)", "col": GREEN, "x":  0.0},
            {"lr": 1.10, "label": "α trop grand\n(diverge)",  "col": RED,    "x":  4.5},
        ]

        for cfg in configs:
            ax_m = Axes(
                x_range=[-3, 3, 1], y_range=[-0.2, 5, 1],
                x_length=3.2, y_length=2.6,
                axis_config=dict(color=GREY, stroke_width=0.7,
                                 include_ticks=False, include_tip=False),
            ).shift(RIGHT * cfg["x"] + DOWN * 0.5)
            b = ax_m.plot(J, x_range=[-2.8, 2.8],
                          color=PURPLE, stroke_width=2)
            self.play(Create(ax_m), Create(b), run_time=0.35)

            theta = 2.3
            prev  = Dot(ax_m.c2p(theta, J(theta)), radius=0.08, color=cfg["col"])
            self.play(FadeIn(prev), run_time=0.2)

            for _ in range(6):
                g = dJ(theta)
                theta_new = theta - cfg["lr"] * g
                theta_new = np.clip(theta_new, -2.8, 2.8)
                nd = Dot(ax_m.c2p(theta_new, J(theta_new)),
                         radius=0.07, color=cfg["col"])
                arr = Arrow(ax_m.c2p(theta, J(theta)),
                            ax_m.c2p(theta_new, J(theta_new)),
                            buff=0.04, color=cfg["col"],
                            stroke_width=1.5,
                            max_tip_length_to_length_ratio=0.2)
                self.play(GrowArrow(arr), FadeIn(nd), run_time=0.2)
                self.play(prev.animate.set_opacity(0.3), FadeOut(arr), run_time=0.1)
                prev  = nd
                theta = theta_new

            lbl_m = Text(cfg["label"], font="Montserrat",
                         font_size=15, color=cfg["col"],
                         line_spacing=1.2)\
                    .next_to(ax_m, DOWN, 0.15)
            self.play(FadeIn(lbl_m))

        self.wait(1.8)

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _step_label(self, text, color):
        return Text(text, font="Montserrat", font_size=20, color=color)\
               .to_corner(UL).shift(RIGHT * 0.3)

    def _tangent(self, ax, theta, slope, color, width=2, opacity=1.0):
        dt = 0.8
        x0, x1 = theta - dt, theta + dt
        y0 = J(theta) + slope * (-dt)
        y1 = J(theta) + slope * ( dt)
        # Clamp dans la vue
        x0 = max(x0, -2.8);  x1 = min(x1, 2.8)
        y0 = max(y0, -0.1);  y1 = min(y1,  4.9)
        return Line(ax.c2p(x0, y0), ax.c2p(x1, y1),
                    color=color, stroke_width=width).set_opacity(opacity)