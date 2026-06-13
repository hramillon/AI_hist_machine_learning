from manim import *
import numpy as np

class Distances(Scene):
    def construct(self):

        # projection axonométrique partagée
        def proj(x, y, z):
            return np.array([x + 0.6*z - 1.5, y + 0.35*z - 0.9, 0]) * 1.8

        edges = [(0,0,0,1,0,0),(0,0,0,0,1,0),(0,0,0,0,0,1),
                 (1,0,0,1,1,0),(1,0,0,1,0,1),(0,1,0,1,1,0),
                 (0,1,0,0,1,1),(0,0,1,1,0,1),(0,0,1,0,1,1),
                 (1,1,0,1,1,1),(1,0,1,1,1,1),(0,1,1,1,1,1)]

        # ── 1. CARRÉ 2D (7s) ────────────────────────────────────────────────
        title = Text("Carré unitaire 2D", font_size=36).to_edge(UP)
        sq = Square(side_length=4).set_stroke(BLUE, 3).set_fill(BLUE, 0.1)

        p1 = np.array([np.random.uniform(-2, 2), np.random.uniform(-2, 2), 0])
        p2 = np.array([np.random.uniform(-2, 2), np.random.uniform(-2, 2), 0])
        d1, d2 = Dot(p1, color=RED), Dot(p2, color=RED)
        seg = Line(p1, p2, color=YELLOW)
        avg = Text("Moyenne : 0.52", font_size=30, color=YELLOW).to_edge(DOWN)

        self.play(Write(title), Create(sq), run_time=2)
        self.play(FadeIn(d1), FadeIn(d2), Create(seg), Write(avg), run_time=2)
        self.wait(3)
        self.play(*[FadeOut(m) for m in [title, sq, d1, d2, seg, avg]])

        # ── 2. CUBE 3D (5s) ─────────────────────────────────────────────────
        title = Text("Cube unitaire 3D", font_size=36).to_edge(UP)
        avg2 = Text("Moyenne : 0.62", font_size=30, color=YELLOW).to_edge(DOWN)

        cube_lines = VGroup(*[
            Line(proj(*e[:3]), proj(*e[3:]), color=BLUE, stroke_width=2)
            for e in edges])

        # points aléatoires dans [0,1]³ projetés
        r1 = np.random.uniform(0, 1, 3)
        r2 = np.random.uniform(0, 1, 3)
        q1, q2 = proj(*r1), proj(*r2)
        e1, e2 = Dot(q1, color=RED), Dot(q2, color=RED)
        s = Line(q1, q2, color=YELLOW)

        self.play(Write(title), Create(cube_lines), run_time=2)
        self.play(FadeIn(e1), FadeIn(e2), Create(s), Write(avg2), run_time=1.5)
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in [title, cube_lines, e1, e2, s, avg2]])

        # ── 3. HYPERCUBE 1 000 000 D (7s) ───────────────────────────────────
        title = Text("Hypercube 1 000 000 de dimensions", font_size=28).to_edge(UP)
        avg3 = Text("Moyenne : 408.25", font_size=30, color=YELLOW).to_edge(DOWN)

        def shifted_cube(dx, dy, col, alpha=1.0):
            sh = np.array([dx, dy, 0])
            lines = VGroup(*[
                Line(proj(*e[:3])+sh, proj(*e[3:])+sh,
                     stroke_color=col, stroke_opacity=alpha, stroke_width=1.5)
                for e in edges])
            return lines, sh

        params = [(-1.2,-0.6,BLUE_D,1.0),(-.3,0,TEAL_B,.7),(.6,.6,PURPLE_B,.45)]
        layers, shifts = [], []
        for dx,dy,c,a in params:
            l, sh = shifted_cube(dx, dy, c, a)
            layers.append(l); shifts.append(sh)

        connectors = VGroup()
        for k in range(len(layers)-1):
            for vx,vy,vz in [(x,y,z) for x in[0,1] for y in[0,1] for z in[0,1]]:
                connectors.add(Line(
                    proj(vx,vy,vz)+shifts[k],
                    proj(vx,vy,vz)+shifts[k+1],
                    stroke_color=GREY, stroke_opacity=.3, stroke_width=1))

        hyper = VGroup(*layers, connectors)

        # points dans [0,1]³ projetés + décalés dans le layer central
        h1_3d = np.random.uniform(0, 1, 3)
        h2_3d = np.random.uniform(0, 1, 3)
        hq1 = proj(*h1_3d) + shifts[1]
        hq2 = proj(*h2_3d) + shifts[1]
        h1, h2 = Dot(hq1, color=RED), Dot(hq2, color=RED)
        hs = Line(hq1, hq2, color=YELLOW)

        self.play(Write(title), Create(hyper), run_time=3)
        self.play(FadeIn(h1), FadeIn(h2), Create(hs), Write(avg3), run_time=2)
        self.wait(2)