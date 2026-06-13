from manim import *
import numpy as np

# ── Dataset Iris : PetalLengthCm, PetalWidthCm ──────────────────
RAW = [
    (1.4,0.2),(1.4,0.2),(1.3,0.2),(1.5,0.2),(1.4,0.2),(1.7,0.4),(1.4,0.3),(1.5,0.2),
    (1.4,0.2),(1.5,0.1),(1.5,0.2),(1.6,0.2),(1.4,0.1),(1.1,0.1),(1.2,0.2),(1.5,0.4),
    (1.3,0.4),(1.4,0.3),(1.7,0.3),(1.5,0.3),(1.7,0.2),(1.5,0.4),(1.0,0.2),(1.7,0.5),
    (1.9,0.2),(1.6,0.2),(1.6,0.4),(1.5,0.2),(1.4,0.2),(1.6,0.2),(1.6,0.2),(1.5,0.4),
    (1.5,0.1),(1.4,0.2),(1.5,0.1),(1.2,0.2),(1.3,0.2),(1.5,0.1),(1.3,0.2),(1.5,0.2),
    (1.3,0.3),(1.3,0.3),(1.3,0.2),(1.6,0.6),(1.9,0.4),(1.4,0.3),(1.6,0.2),(1.4,0.2),
    (1.5,0.2),(1.4,0.2),
    (4.7,1.4),(4.5,1.5),(4.9,1.5),(4.0,1.3),(4.6,1.5),(4.5,1.3),(4.7,1.6),(3.3,1.0),
    (4.6,1.3),(3.9,1.4),(3.5,1.0),(4.2,1.5),(4.0,1.0),(4.7,1.4),(3.6,1.3),(4.4,1.4),
    (4.5,1.5),(4.1,1.0),(4.5,1.5),(3.9,1.1),(4.8,1.8),(4.0,1.3),(4.9,1.5),(4.7,1.2),
    (4.3,1.3),(4.4,1.4),(4.8,1.4),(5.0,1.7),(4.5,1.5),(3.5,1.0),(3.8,1.1),(3.7,1.0),
    (3.9,1.2),(5.1,1.6),(4.5,1.5),(4.5,1.6),(4.7,1.5),(4.4,1.3),(4.1,1.3),(4.0,1.3),
    (4.4,1.2),(4.6,1.4),(4.0,1.2),(3.3,1.0),(4.2,1.3),(4.2,1.2),(4.2,1.3),(4.3,1.3),
    (3.0,1.1),(4.1,1.3),
    (6.0,2.5),(5.1,1.9),(5.9,2.1),(5.6,1.8),(5.8,2.2),(6.6,2.1),(4.5,1.7),(6.3,1.8),
    (5.8,1.8),(6.1,2.5),(5.1,2.0),(5.3,1.9),(5.5,2.1),(5.0,2.0),(5.1,2.4),(5.3,2.3),
    (5.5,1.8),(6.7,2.2),(6.9,2.3),(5.0,1.5),(5.7,2.3),(4.9,2.0),(6.7,2.0),(4.9,1.8),
    (5.7,2.1),(6.0,1.8),(4.8,1.8),(4.9,1.8),(5.6,2.1),(5.8,1.6),(6.1,1.9),(6.4,2.0),
    (5.6,2.2),(5.1,1.5),(5.6,1.4),(6.1,2.3),(5.6,2.4),(5.5,1.8),(4.8,1.8),(5.4,2.1),
    (5.6,2.4),(5.1,2.3),(5.1,1.9),(5.9,2.3),(5.7,2.5),(5.2,2.3),(5.0,1.9),(5.2,2.0),
    (5.4,2.3),(5.1,1.8),
]

DATA = np.array(RAW, dtype=float)
K = 3

# ── Centroïdes initiaux : volontairement décalés pour forcer des réaffectations ──
# C0 dans les versicolor, C1 bas-droite (zone vide), C2 dans les setosa
# → à l'itération 2 plusieurs points changent de cluster
INIT_CENTROIDS = np.array([
    [3.5, 1.5],
    [5.0, 0.8],
    [1.5, 0.3],
], dtype=float)

COLORS = [RED, BLUE, GREEN]   # cluster 0, 1, 2
CENTROID_COLOR = YELLOW

# ── Mapping données → coordonnées écran ──────────────────────────
X_MIN, X_MAX = 0.5, 7.5
Y_MIN, Y_MAX = 0.0, 2.8

# Axes visuels : de (-5.5, -3.5) à (5.5, 3.5) en espace Manim
AX_X0, AX_X1 = -5.5, 5.0
AX_Y0, AX_Y1 = -2.6, 2.6

def to_screen(px, py):
    sx = AX_X0 + (px - X_MIN) / (X_MAX - X_MIN) * (AX_X1 - AX_X0)
    sy = AX_Y0 + (py - Y_MIN) / (Y_MAX - Y_MIN) * (AX_Y1 - AX_Y0)
    return np.array([sx, sy, 0.0])

def assign(data, centroids):
    dists = np.array([[np.linalg.norm(p - c) for c in centroids] for p in data])
    return np.argmin(dists, axis=1)

def update_centroids(data, labels):
    new_c = []
    for k in range(K):
        pts = data[labels == k]
        new_c.append(pts.mean(axis=0) if len(pts) > 0 else data[np.random.randint(len(data))])
    return np.array(new_c)


# ════════════════════════════════════════════════════════════════
class KMeansIris(Scene):

    def construct(self):

        # ── Axes ────────────────────────────────────────────────
        ax_x = Arrow(start=[AX_X0-0.2, AX_Y0, 0], end=[AX_X1+0.2, AX_Y0, 0],
                     buff=0, stroke_width=1.5, color=WHITE, tip_length=0.2)
        ax_y = Arrow(start=[AX_X0, AX_Y0-0.2, 0], end=[AX_X0, AX_Y1+0.2, 0],
                     buff=0, stroke_width=1.5, color=WHITE, tip_length=0.2)

        xlabel = Text("PetalLengthCm", font_size=16, color=WHITE).next_to(ax_x, DOWN, buff=0.55)
        ylabel = Text("PetalWidthCm",  font_size=16, color=WHITE).rotate(PI/2).next_to(ax_y, LEFT, buff=0.65)

        # ticks X
        ticks_x = VGroup()
        for v in [1,2,3,4,5,6,7]:
            sp = to_screen(v, Y_MIN)
            tick = Line([sp[0], AX_Y0-0.1, 0], [sp[0], AX_Y0+0.1, 0], stroke_width=1, color=GRAY)
            lbl  = Text(str(v), font_size=11, color=GRAY).move_to([sp[0], AX_Y0-0.28, 0])
            ticks_x.add(tick, lbl)

        # ticks Y
        ticks_y = VGroup()
        for v in [0.5,1.0,1.5,2.0,2.5]:
            sp = to_screen(X_MIN, v)
            tick = Line([AX_X0-0.1, sp[1], 0], [AX_X0+0.1, sp[1], 0], stroke_width=1, color=GRAY)
            lbl  = Text(f"{v:.1f}", font_size=11, color=GRAY).move_to([AX_X0-0.42, sp[1], 0])
            ticks_y.add(tick, lbl)

        axes = VGroup(ax_x, ax_y, xlabel, ylabel, ticks_x, ticks_y)
        self.play(Create(axes), run_time=0.9)

        title = Text("K-Means  (k=3)  –  Iris  PetalLength × PetalWidth",
                     font_size=20, color=WHITE).to_edge(UP, buff=0.15)
        self.play(Write(title), run_time=0.7)

        # ── Points initiaux (tous blancs) ───────────────────────
        dots = []
        for px, py in DATA:
            d = Dot(to_screen(px, py), radius=0.055, color=WHITE, fill_opacity=0.85)
            dots.append(d)
        dot_group = VGroup(*dots)
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.015), run_time=1.2)
        self.wait(0.4)

        # ── Centroïdes initiaux ──────────────────────────────────
        centroids = INIT_CENTROIDS.copy()
        cent_dots = []
        for i, c in enumerate(centroids):
            cd = Star(n=5, outer_radius=0.2, inner_radius=0.1,
                      fill_color=CENTROID_COLOR, fill_opacity=1,
                      stroke_color=WHITE, stroke_width=1.2)
            cd.move_to(to_screen(c[0], c[1]))
            cent_dots.append(cd)

        step_lbl = Text("Initialisation des centroïdes", font_size=18, color=YELLOW)
        step_lbl.to_edge(DOWN, buff=0.2)
        self.play(FadeIn(step_lbl))
        self.play(LaggedStart(*[FadeIn(cd, scale=1.4) for cd in cent_dots], lag_ratio=0.15), run_time=0.7)
        self.wait(1.0)

        labels = np.full(len(DATA), -1)

        # ════ BOUCLE K-MEANS ════════════════════════════════════
        for iteration in range(6):

            # ── ÉTAPE 1 : Affectation ────────────────────────────
            self.play(FadeOut(step_lbl), run_time=0.2)
            step_lbl = Text(f"Itération {iteration+1}  –  Affectation",
                            font_size=18, color=WHITE)
            step_lbl.to_edge(DOWN, buff=0.2)
            self.play(FadeIn(step_lbl), run_time=0.3)

            new_labels = assign(DATA, centroids)

            # Colorier les points selon leur cluster
            color_anims = []
            for i, (d, lbl) in enumerate(zip(dots, new_labels)):
                color_anims.append(d.animate.set_fill(COLORS[lbl]).set_stroke(COLORS[lbl]))

            self.play(*color_anims, run_time=0.9)
            self.wait(1.2)   # ← PAUSE affectation

            # ── ÉTAPE 2 : Mise à jour des centroïdes ────────────
            self.play(FadeOut(step_lbl), run_time=0.2)
            step_lbl = Text(f"Itération {iteration+1}  –  Mise à jour des centroïdes",
                            font_size=18, color=WHITE)
            step_lbl.to_edge(DOWN, buff=0.2)
            self.play(FadeIn(step_lbl), run_time=0.3)

            new_centroids = update_centroids(DATA, new_labels)

            move_anims = []
            for i, (cd, nc) in enumerate(zip(cent_dots, new_centroids)):
                move_anims.append(cd.animate.move_to(to_screen(nc[0], nc[1])))

            self.play(*move_anims, run_time=0.8)
            self.wait(1.2)   # ← PAUSE mise à jour

            # Convergence ?
            if np.allclose(centroids, new_centroids, atol=1e-6) and np.array_equal(labels, new_labels):
                self.play(FadeOut(step_lbl), run_time=0.2)
                step_lbl = Text("Convergence atteinte ✓", font_size=20, color=YELLOW, weight=BOLD)
                step_lbl.to_edge(DOWN, buff=0.2)
                self.play(FadeIn(step_lbl), run_time=0.4)
                self.wait(1.5)
                break

            centroids = new_centroids
            labels    = new_labels

        # ── Légende finale ───────────────────────────────────────
        legend_items = [
            (COLORS[0], "Cluster 1"),
            (COLORS[1], "Cluster 2"),
            (COLORS[2], "Cluster 3"),
        ]
        legend = VGroup()
        for color, txt in legend_items:
            dot  = Dot(radius=0.1, color=color)
            lab  = Text(txt, font_size=15, color=WHITE)
            row  = VGroup(dot, lab).arrange(RIGHT, buff=0.15)
            legend.add(row)
        legend.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        legend.to_corner(UL, buff=0.5)

        self.play(FadeIn(legend), run_time=0.6)
        self.wait(2.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# ── COMMANDE ──────────────────────────────────────────────────────
# manim -pql kmeans_animation.py KMeansIris
# manim -pqh kmeans_animation.py KMeansIris