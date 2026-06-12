from manim import *
import random
import numpy as np


class HypercubeAnimation(Scene):
    def construct(self):

        # ─── SCÈNE 1 : carré unitaire 2D (4 secondes) ───────────────────────

        # Axes avec flèches
        axes = Axes(
            x_range=[0, 1.5, 0.5],
            y_range=[0, 1.5, 0.5],
            x_length=4,
            y_length=4,
            axis_config={"include_tip": True, "color": WHITE},
            tips=True,
        ).shift(LEFT * 0.5 + DOWN * 0.5)

        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")

        # Carré unitaire
        square = Square(side_length=axes.x_length * (1 / 1.5))
        square.set_stroke(BLUE, 3)
        square.set_fill(BLUE, opacity=0.15)

        # Aligner le carré sur l'origine des axes
        origin = axes.c2p(0, 0)
        corner = axes.c2p(1, 1)
        side = corner[0] - origin[0]
        square = Square(side_length=side)
        square.set_stroke(BLUE, 3)
        square.set_fill(BLUE, opacity=0.15)
        square.move_to(origin + np.array([side / 2, side / 2, 0]))

        # Point aléatoire dans [0,1]²
        rx, ry = random.uniform(0.1, 0.9), random.uniform(0.1, 0.9)
        dot = Dot(axes.c2p(rx, ry), color=RED, radius=0.08)
        dot_label = MathTex(
            f"({rx:.2f},\\,{ry:.2f})", font_size=24, color=RED
        ).next_to(dot, UR, buff=0.1)

        # Apparition progressive sur 4 secondes
        self.play(
            Create(axes),
            Write(x_label),
            Write(y_label),
            run_time=1.5
        )
        self.play(Create(square), run_time=1.5)
        self.play(FadeIn(dot), Write(dot_label), run_time=1.0)

        # ─── SCÈNE 1b : texte 0.4 % (5 secondes) ───────────────────────────

        percent_2d = Text("0.4 %", font_size=72, color=YELLOW, weight=BOLD)
        percent_2d.to_edge(RIGHT, buff=1)

        self.play(Write(percent_2d), run_time=1.0)
        self.wait(4.0)

        # ─── Disparition carré + texte ──────────────────────────────────────

        self.play(
            FadeOut(axes), FadeOut(x_label), FadeOut(y_label),
            FadeOut(square), FadeOut(dot), FadeOut(dot_label),
            FadeOut(percent_2d),
            run_time=1.0
        )

        # ─── SCÈNE 2 : hypercube 7D (représentation, 4+5 secondes) ──────────

        hypercube = self._build_hypercube_7d()
        hypercube.scale(0.9).shift(RIGHT * 1)

        self.play(Create(hypercube), run_time=3.2)   # 4 s au total

        # ─── SCÈNE 2b : texte 99,999999 % (5 secondes) ──────────────────────

        percent_7d = Text("99,999999 %", font_size=60, color=GREEN, weight=BOLD)
        percent_7d.to_edge(LEFT, buff=0.8)
        percent_7d.shift(DOWN * 0.3)

        self.play(Write(percent_7d), run_time=1.0)
        self.wait(4.0)

        self.play(
            FadeOut(hypercube),
            FadeOut(percent_7d),
            run_time=1.0,
        )

    # ────────────────────────────────────────────────────────────────────────
    def _build_hypercube_7d(self):
        """
        Représentation projective d'un 7-cube :
        on empile plusieurs projections de (hyper)cubes avec décalage
        pour évoquer la structure en couches des 128 sommets.
        """
        group = VGroup()

        # Sommets du cube 3D de base
        verts3 = np.array([
            [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
            [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1],
        ], dtype=float) - 0.5

        edges3 = [
            (0,1),(1,2),(2,3),(3,0),
            (4,5),(5,6),(6,7),(7,4),
            (0,4),(1,5),(2,6),(3,7),
        ]

        # Directions de projection pour les 4 dimensions supplémentaires
        offsets = [
            np.array([0.0,   0.0,  0]),
            np.array([0.55,  0.3,  0]),
            np.array([0.0,   0.6,  0]),
            np.array([0.55,  0.9,  0]),
        ]

        colors = [BLUE_D, BLUE_B, TEAL_D, TEAL_B]
        alphas = [1.0, 0.75, 0.55, 0.4]

        layers = []
        for k, (off, col, alp) in enumerate(zip(offsets, colors, alphas)):
            pts = verts3[:, :2] + off[:2]  # projection 2D
            layer_grp = VGroup()
            for i, j in edges3:
                line = Line(
                    np.append(pts[i], 0),
                    np.append(pts[j], 0),
                    stroke_color=col,
                    stroke_opacity=alp,
                    stroke_width=2,
                )
                layer_grp.add(line)
            layers.append(layer_grp)
            group.add(layer_grp)

        # Relier les couches entre elles (arêtes inter-couches)
        for k in range(len(layers) - 1):
            pts_a = verts3[:, :2] + offsets[k][:2]
            pts_b = verts3[:, :2] + offsets[k + 1][:2]
            for v in range(8):
                line = Line(
                    np.append(pts_a[v], 0),
                    np.append(pts_b[v], 0),
                    stroke_color=GREY,
                    stroke_opacity=0.35,
                    stroke_width=1,
                )
                group.add(line)

        # 3 couches supplémentaires décalées vers le bas → 7 dimensions évoquées
        extra_offsets = [
            np.array([0.28,  -0.5,  0]),
            np.array([0.83,  -0.2,  0]),
            np.array([0.28,   0.1,  0]),
        ]
        extra_colors = [PURPLE_B, PURPLE_D, MAROON_B]
        extra_alphas = [0.6, 0.45, 0.3]

        prev_pts = verts3[:, :2] + offsets[-1][:2]
        for off, col, alp in zip(extra_offsets, extra_colors, extra_alphas):
            pts = verts3[:, :2] + off[:2]
            layer_grp = VGroup()
            for i, j in edges3:
                line = Line(
                    np.append(pts[i], 0),
                    np.append(pts[j], 0),
                    stroke_color=col,
                    stroke_opacity=alp,
                    stroke_width=1.5,
                )
                layer_grp.add(line)
            group.add(layer_grp)
            for v in range(8):
                line = Line(
                    np.append(prev_pts[v], 0),
                    np.append(pts[v], 0),
                    stroke_color=GREY,
                    stroke_opacity=0.25,
                    stroke_width=1,
                )
                group.add(line)
            prev_pts = pts

        return group