from manim import *
import numpy as np

BG     = "#0F1117"
WHITE  = "#F0F4F8"
GREY   = "#8899AA"
PURPLE = "#A78BFA"
GOLD   = "#FFD54F"
BLUE   = "#4FC3F7"
RED    = "#EF9A9A"

np.random.seed(7)

def make_circles():
    # Cercle intérieur (rouge)
    n = 60
    r_in  = np.random.uniform(0.4, 1.1, n)
    a_in  = np.random.uniform(0, 2*np.pi, n)
    X_in  = np.column_stack([r_in*np.cos(a_in), r_in*np.sin(a_in)])

    # Cercle extérieur (bleu)
    r_out = np.random.uniform(1.8, 2.6, n)
    a_out = np.random.uniform(0, 2*np.pi, n)
    X_out = np.column_stack([r_out*np.cos(a_out), r_out*np.sin(a_out)])

    return X_in, X_out


class Scene14Limits(Scene):
    def construct(self):
        self.camera.background_color = BG
        self._show_circles()
        self._try_lines()
        self._conclusion()

    # ── 1. Afficher les deux cercles de points ────────────────────────────────
    def _show_circles(self):
        ax = Axes(
            x_range=[-3.5, 3.5, 1], y_range=[-3.5, 3.5, 1],
            x_length=6.5, y_length=6.5,
            axis_config=dict(color=GREY, stroke_width=0.7,
                             include_ticks=False, include_tip=False),
        ).shift(LEFT * 0.8)
        self.play(Create(ax), run_time=0.4)

        X_in, X_out = make_circles()
        self._X_in  = X_in
        self._X_out = X_out
        self._ax    = ax

        dots_in = VGroup(*[
            Dot(ax.c2p(*p), radius=0.07, color=RED, fill_opacity=0.85)
            for p in X_in
        ])
        dots_out = VGroup(*[
            Dot(ax.c2p(*p), radius=0.07, color=BLUE, fill_opacity=0.85)
            for p in X_out
        ])

        lbl_in  = Text("Classe 1 (intérieur)", font="Montserrat",
                       font_size=20, color=RED)\
                  .to_corner(UR).shift(LEFT*0.3 + DOWN*0.5)
        lbl_out = Text("Classe 0 (extérieur)", font="Montserrat",
                       font_size=20, color=BLUE)\
                  .next_to(lbl_in, DOWN, 0.2)

        self.play(
            LaggedStart(*[FadeIn(d) for d in dots_in],  lag_ratio=0.025, run_time=0.9),
        )
        self.play(
            LaggedStart(*[FadeIn(d) for d in dots_out], lag_ratio=0.025, run_time=0.9),
        )
        self.play(FadeIn(lbl_in), FadeIn(lbl_out))
        self.wait(0.6)

        self._dots_in  = dots_in
        self._dots_out = dots_out
        self._lbl_in   = lbl_in
        self._lbl_out  = lbl_out

    # ── 2. Essayer des lignes droites — aucune ne marche ─────────────────────
    def _try_lines(self):
        ax = self._ax

        question = Text("Peut-on les séparer\navec une ligne droite ?",
                        font="Montserrat", font_size=22, color=GOLD,
                        line_spacing=1.3)\
                   .to_corner(UR).shift(LEFT*0.3 + DOWN*1.4)
        self.play(FadeOut(self._lbl_in), FadeOut(self._lbl_out))
        self.play(FadeIn(question))
        self.wait(0.4)

        # Tentatives de lignes droites
        attempts = [
            # (slope, intercept) en unités données
            ( 0.0,  0.0),   # horizontale au centre
            ( 1.2, -0.5),   # diagonale
            (-0.9,  0.3),   # autre diagonale
            ( 0.0,  1.5),   # horizontale haute
        ]

        fail_lbl = Text("✗", font="Montserrat",
                        font_size=36, color=RED)

        for slope, intercept in attempts:
            # Ligne en unités données → points écran
            x_vals = np.array([-3.4, 3.4])
            y_vals = slope * x_vals + intercept
            line = Line(
                ax.c2p(x_vals[0], y_vals[0]),
                ax.c2p(x_vals[1], y_vals[1]),
                color=GOLD, stroke_width=2.5
            )
            self.play(Create(line), run_time=0.45)
            self.wait(0.25)

            # Flash rouge pour montrer l'échec
            cross = Text("✗", font_size=38, color=RED)\
                    .move_to(ax.c2p(0, intercept + slope*0.3))
            self.play(FadeIn(cross, scale=1.4), run_time=0.2)
            self.wait(0.35)
            self.play(FadeOut(line), FadeOut(cross), run_time=0.3)

        self.wait(0.3)
        self._question = question

    # ── 3. Conclusion : frontière circulaire impossible en log-reg ────────────
    def _conclusion(self):
        ax = self._ax
        self.play(FadeOut(self._question))

        # Montrer ce que la log-reg produit réellement :
        # une droite (la meilleure possible) qui coupe mal
        best_line = Line(
            ax.c2p(-3.4, -3.4), ax.c2p(3.4, 3.4),
            color=PURPLE, stroke_width=2.5,
        )
        log_reg_lbl = Text("Meilleure frontière\nde la régression logistique",
                           font="Montserrat", font_size=18, color=PURPLE,
                           line_spacing=1.2)\
                     .to_corner(UR).shift(LEFT*0.3 + DOWN*0.5)
        self.play(Create(best_line), FadeIn(log_reg_lbl), run_time=0.6)
        self.wait(0.5)

        # Colorier les points mal classifiés
        errors_in  = VGroup()
        errors_out = VGroup()
        for p, d in zip(self._X_in, self._dots_in):
            # Côté de la ligne y = x  → p[1] - p[0]
            if p[1] - p[0] < 0:   # classé comme extérieur à tort
                errors_in.add(
                    Circle(radius=0.13, color=GOLD, stroke_width=2)
                    .move_to(d.get_center())
                )
        for p, d in zip(self._X_out, self._dots_out):
            if p[1] - p[0] > 0:
                errors_out.add(
                    Circle(radius=0.13, color=GOLD, stroke_width=2)
                    .move_to(d.get_center())
                )

        err_lbl = Text("Points mal classifiés",
                       font="Montserrat", font_size=17, color=GOLD)\
                  .to_corner(UR).shift(LEFT*0.3 + DOWN*1.6)
        self.play(
            LaggedStart(*[Create(e) for e in errors_in + errors_out],
                        lag_ratio=0.03, run_time=0.8),
            FadeIn(err_lbl),
        )
        self.wait(0.7)

        # Effacer la droite, montrer la vraie frontière circulaire idéale
        self.play(FadeOut(best_line), FadeOut(log_reg_lbl),
                  FadeOut(err_lbl),
                  *[FadeOut(e) for e in errors_in + errors_out],
                  run_time=0.4)

        ideal_circle = DashedVMobject(
            Circle(
                radius=ax.c2p(1.45, 0)[0] - ax.c2p(0, 0)[0],
                color=GREEN, stroke_width=2.5,
            ).move_to(ax.c2p(0, 0)),
            num_dashes=40, dashed_ratio=0.6,
        )
        ideal_lbl = Text("Frontière idéale\n(circulaire)",
                         font="Montserrat", font_size=18, color=GREEN,
                         line_spacing=1.2)\
                    .to_corner(UR).shift(LEFT*0.3 + DOWN*0.5)

        self.play(Create(ideal_circle), FadeIn(ideal_lbl), run_time=0.8)
        self.wait(0.6)

        # Message final
        msg = Text(
            "La régression logistique ne peut tracer\n"
            "que des frontières linéaires (droites).\n"
            "Ces données exigent une frontière non-linéaire.",
            font="Montserrat", font_size=20, color=WHITE,
            line_spacing=1.35,
        ).to_corner(UR).shift(LEFT*0.3 + DOWN*0.4)

        self.play(ReplacementTransform(ideal_lbl, msg), run_time=0.5)
        self.wait(2.0)