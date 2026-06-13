from manim import *
import numpy as np

np.random.seed(42)

# ── Palette sobre ────────────────────────────────────────────────
CURVE_COLOR   = WHITE
NOISE_COLOR   = "#888888"
SIGNAL_COLOR  = "#4AC8E8"
GAUSS_COLOR   = "#E8C84A"
ZERO_COLOR    = "#888888"


# ════════════════════════════════════════════════════════════════
class GaussianNoise(Scene):

    # ════════════════════════════════════════════════════════════
    def construct(self):

        # ════════════════════════════════════════════════════════
        # ACTE 1 — Le monde réel : signal parfait vs mesuré
        # ════════════════════════════════════════════════════════
        title = Text("Bruit gaussien", font_size=24, color=WHITE)
        title.to_edge(UP, buff=0.2)
        self.play(Write(title), run_time=0.7)

        # Axes signal
        ax = Axes(
            x_range=[0, 10, 1], y_range=[-2.5, 2.5, 1],
            x_length=9, y_length=4.5,
            axis_config={"color": GRAY, "stroke_width": 1.5,
                         "include_tip": True, "tip_length": 0.18},
        ).shift(UP * 0.2)

        xl = Text("temps", font_size=14, color=GRAY).next_to(ax.x_axis, DOWN, buff=0.45)
        yl = Text("signal", font_size=14, color=GRAY).rotate(PI/2).next_to(ax.y_axis, LEFT, buff=0.55)

        self.play(Create(ax), Write(xl), Write(yl), run_time=0.8)

        # Signal vrai (sinusoïde lisse)
        true_signal = ax.plot(lambda x: np.sin(x), color=SIGNAL_COLOR,
                              stroke_width=2.5, x_range=[0, 10])
        lbl_true = Text("signal vrai", font_size=14, color=SIGNAL_COLOR)
        lbl_true.next_to(ax.c2p(8, 1.15), UP, buff=0.08)

        self.wait(0.5)
        self.play(Create(true_signal), FadeIn(lbl_true), run_time=1.2)
        self.wait(1.0)

        # Signal bruité (points)
        t_vals = np.linspace(0, 10, 80)
        noise  = np.random.normal(0, 0.35, len(t_vals))
        noisy  = np.sin(t_vals) + noise

        noisy_dots = VGroup(*[
            Dot(ax.c2p(t, y), radius=0.045, color=NOISE_COLOR, fill_opacity=0.8)
            for t, y in zip(t_vals, noisy)
        ])

        self.wait(0.5)
        self.play(LaggedStart(*[FadeIn(d) for d in noisy_dots], lag_ratio=0.01),
                  run_time=1.2)
        self.wait(1.2)

        # Flèche + label « bruit »
        sample_t, sample_y_true = 4.0, np.sin(4.0)
        sample_y_noisy = sample_y_true + 0.6
        arr = Arrow(ax.c2p(4.0, sample_y_true), ax.c2p(4.0, sample_y_noisy),
                    buff=0, stroke_width=1.8, color=GAUSS_COLOR, tip_length=0.15)
        arr_lbl = Text("erreur", font_size=13, color=GAUSS_COLOR).next_to(arr, RIGHT, buff=0.08)
        self.play(Create(arr), FadeIn(arr_lbl), run_time=0.5)
        self.wait(1.0)
        self.play(FadeOut(arr), FadeOut(arr_lbl), run_time=0.3)

        # ════════════════════════════════════════════════════════
        # ACTE 2 — Additionner des micro-erreurs → TCL
        # ════════════════════════════════════════════════════════
        self.wait(0.5)
        self.wait(1.0)

        # Montrer 5 petites erreurs uniformes qui s'empilent
        bar_group = VGroup()
        bar_colors = [RED, BLUE, GREEN, ORANGE, PURPLE]
        sources = ["réseau", "capteur", "lumière", "temp.", "bruit élec."]
        for i in range(5):
            val = np.random.uniform(-0.3, 0.3)
            bar = Rectangle(width=abs(val)*2.5, height=0.28,
                            fill_color=bar_colors[i], fill_opacity=0.85,
                            stroke_width=0)
            bar.move_to(LEFT*3.5 + DOWN*(i*0.42 - 0.6))
            if val < 0:
                bar.shift(LEFT * abs(val)*1.25)
            lbl_s = Text(sources[i], font_size=12, color=bar_colors[i])
            lbl_s.next_to(bar, RIGHT, buff=0.1)
            bar_group.add(VGroup(bar, lbl_s))

        self.play(FadeOut(true_signal), FadeOut(lbl_true), FadeOut(noisy_dots),
                  FadeOut(ax), FadeOut(xl), FadeOut(yl), run_time=0.4)

        self.play(LaggedStart(*[FadeIn(b) for b in bar_group], lag_ratio=0.15),
                  run_time=1.0)
        self.wait(0.8)

        self.wait(0.5)
        self.wait(1.2)

        self.play(FadeOut(bar_group), run_time=0.4)

        # ════════════════════════════════════════════════════════
        # ACTE 3 — La courbe en cloche (gaussienne)
        # ════════════════════════════════════════════════════════
        ax2 = Axes(
            x_range=[-3.5, 3.5, 1], y_range=[0, 0.5, 0.1],
            x_length=9, y_length=4.2,
            axis_config={"color": GRAY, "stroke_width": 1.5,
                         "include_tip": True, "tip_length": 0.18},
        ).shift(UP * 0.25)

        xl2 = Text("erreur", font_size=14, color=GRAY).next_to(ax2.x_axis, DOWN, buff=0.45)
        yl2 = Text("probabilité", font_size=14, color=GRAY).rotate(PI/2).next_to(ax2.y_axis, LEFT, buff=0.55)

        self.play(Create(ax2), Write(xl2), Write(yl2), run_time=0.7)

        def gauss(x, mu=0, sigma=1):
            return np.exp(-0.5*((x-mu)/sigma)**2) / (sigma*np.sqrt(2*np.pi))

        bell = ax2.plot(lambda x: gauss(x), color=GAUSS_COLOR,
                        stroke_width=3, x_range=[-3.5, 3.5])

        self.wait(0.5)
        self.play(Create(bell), run_time=1.2)
        self.wait(0.6)

        # Zone remplie sous la courbe
        area = ax2.get_area(bell, x_range=[-3.5, 3.5],
                            color=GAUSS_COLOR, opacity=0.15)
        self.play(FadeIn(area), run_time=0.5)

        # Ligne μ = 0
        zero_line = ax2.get_vertical_line(ax2.c2p(0, gauss(0)),
                                          color=WHITE, stroke_width=1.5,
                                          line_func=DashedLine)
        mu_lbl = Text("μ = 0", font_size=15, color=WHITE).next_to(ax2.c2p(0, 0.43), UP, buff=0.05)
        self.play(Create(zero_line), FadeIn(mu_lbl), run_time=0.5)
        self.wait(0.5)

        # Accolade σ
        sigma_line = DoubleArrow(ax2.c2p(0, 0.18), ax2.c2p(1, 0.18),
                                 buff=0, stroke_width=1.5, color=SIGNAL_COLOR,
                                 tip_length=0.14)
        sigma_lbl  = Text("σ (écart-type)", font_size=13, color=SIGNAL_COLOR)
        sigma_lbl.next_to(sigma_line, UP, buff=0.08)
        self.play(Create(sigma_line), FadeIn(sigma_lbl), run_time=0.5)

        self.wait(0.5)
        self.wait(1.5)

        # ── Comparer deux σ ──────────────────────────────────────
        bell_narrow = ax2.plot(lambda x: gauss(x, sigma=0.5),
                               color=SIGNAL_COLOR, stroke_width=2,
                               x_range=[-3.5, 3.5])
        bell_wide   = ax2.plot(lambda x: gauss(x, sigma=1.8),
                               color=RED, stroke_width=2,
                               x_range=[-3.5, 3.5])

        lbl_narrow = Text("σ petit = peu de bruit", font_size=13, color=SIGNAL_COLOR)
        lbl_narrow.to_corner(UR, buff=0.35).shift(DOWN*0.2)
        lbl_wide   = Text("σ grand = beaucoup de bruit", font_size=13, color=RED)
        lbl_wide.next_to(lbl_narrow, DOWN, buff=0.18, aligned_edge=LEFT)

        self.wait(0.5)
        self.play(
            Create(bell_narrow), Create(bell_wide),
            FadeIn(lbl_narrow), FadeIn(lbl_wide),
            FadeOut(sigma_line), FadeOut(sigma_lbl),
            run_time=1.0
        )
        self.wait(1.8)

        # ════════════════════════════════════════════════════════
        # ACTE 4 — Bruit centré sur 0 : pas de biais
        # ════════════════════════════════════════════════════════
        self.play(
            FadeOut(bell_narrow), FadeOut(bell_wide),
            FadeOut(lbl_narrow), FadeOut(lbl_wide),
            FadeOut(area), FadeOut(zero_line), FadeOut(mu_lbl),
            FadeOut(bell),
            run_time=0.4
        )

        # Remonter signal + bruit sur les axes ax2 réutilisés comme axe temporel
        self.play(FadeOut(ax2), FadeOut(xl2), FadeOut(yl2), run_time=0.3)

        ax3 = Axes(
            x_range=[0, 10, 1], y_range=[-2, 2, 1],
            x_length=9, y_length=4.0,
            axis_config={"color": GRAY, "stroke_width": 1.5,
                         "include_tip": True, "tip_length": 0.18},
        ).shift(UP * 0.3)
        xl3 = Text("temps", font_size=14, color=GRAY).next_to(ax3.x_axis, DOWN, buff=0.45)
        yl3 = Text("erreur", font_size=14, color=GRAY).rotate(PI/2).next_to(ax3.y_axis, LEFT, buff=0.55)
        self.play(Create(ax3), Write(xl3), Write(yl3), run_time=0.6)

        # Trace du bruit seul (centrée sur 0)
        t2   = np.linspace(0, 10, 200)
        err  = np.random.normal(0, 0.4, 200)
        noise_path = VMobject(stroke_color=NOISE_COLOR, stroke_width=1.5)
        noise_path.set_points_smoothly([ax3.c2p(t, e) for t, e in zip(t2, err)])

        zero_h = DashedLine(ax3.c2p(0, 0), ax3.c2p(10, 0),
                            stroke_width=1.2, color=WHITE)
        zero_lbl = Text("moyenne = 0", font_size=13, color=WHITE)
        zero_lbl.next_to(ax3.c2p(8, 0), UP, buff=0.08)

        self.wait(0.5)
        self.play(Create(noise_path), Create(zero_h), FadeIn(zero_lbl), run_time=1.2)
        self.wait(1.8)

        # ════════════════════════════════════════════════════════
        # CONCLUSION
        # ════════════════════════════════════════════════════════
        self.wait(0.5)
        self.wait(2.8)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)


# ── COMMANDE ─────────────────────────────────────────────────────
# manim -pql gaussian_noise.py GaussianNoise
# manim -pqh gaussian_noise.py GaussianNoise