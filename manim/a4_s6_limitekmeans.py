from manim import *
import numpy as np

# ── Génération du dataset moons ──────────────────────────────────
np.random.seed(42)

def make_moons(n=120, noise=0.07):
    n_half = n // 2
    # Demi-cercle supérieur (label 0)
    t0 = np.linspace(0, np.pi, n_half)
    x0 = np.cos(t0) + np.random.normal(0, noise, n_half)
    y0 = np.sin(t0) + np.random.normal(0, noise, n_half)

    # Demi-cercle inférieur (label 1), décalé pour se rapprocher sans se toucher
    t1 = np.linspace(0, np.pi, n_half)
    x1 =  1 - np.cos(t1) + np.random.normal(0, noise, n_half)
    y1 = -np.sin(t1) + 0.4 + np.random.normal(0, noise, n_half)

    X = np.vstack([np.column_stack([x0, y0]),
                   np.column_stack([x1, y1])])
    y = np.array([0]*n_half + [1]*n_half)
    return X, y

DATA, TRUE_LABELS = make_moons(n=120, noise=0.07)

K = 2
COLORS_K    = [RED, BLUE]
COLORS_TRUE = ["#E8C84A", "#4AC8E8"]   # jaune chaud / cyan pour DBSCAN
NOISE_COLOR = "#888888"

# ── Mapping données → écran ──────────────────────────────────────
X_MIN, X_MAX = -1.6,  2.6
Y_MIN, Y_MAX = -1.1,  1.6

AX_X0, AX_X1 = -5.2,  4.8
AX_Y0, AX_Y1 = -2.6,  2.6

def to_screen(px, py):
    sx = AX_X0 + (px - X_MIN) / (X_MAX - X_MIN) * (AX_X1 - AX_X0)
    sy = AX_Y0 + (py - Y_MIN) / (Y_MAX - Y_MIN) * (AX_Y1 - AX_Y0)
    return np.array([sx, sy, 0.0])

# ── K-Means helpers ──────────────────────────────────────────────
def km_assign(data, centroids):
    dists = np.array([[np.linalg.norm(p - c) for c in centroids] for p in data])
    return np.argmin(dists, axis=1)

def km_update(data, labels):
    return np.array([data[labels == k].mean(axis=0) for k in range(K)])

# ── DBSCAN maison ────────────────────────────────────────────────
def dbscan(data, eps=0.18, min_pts=5):
    n = len(data)
    labels = np.full(n, -2)   # -2 = non visité
    cluster_id = 0

    def neighbors(i):
        return [j for j in range(n)
                if j != i and np.linalg.norm(data[i] - data[j]) <= eps]

    for i in range(n):
        if labels[i] != -2:
            continue
        nb = neighbors(i)
        if len(nb) < min_pts:
            labels[i] = -1   # bruit
            continue
        labels[i] = cluster_id
        seeds = list(nb)
        while seeds:
            s = seeds.pop()
            if labels[s] == -1:
                labels[s] = cluster_id
            if labels[s] != -2:
                continue
            labels[s] = cluster_id
            snb = neighbors(s)
            if len(snb) >= min_pts:
                seeds.extend(snb)
        cluster_id += 1

    return labels


# ════════════════════════════════════════════════════════════════
class KMeansDBSCAN(Scene):

    def make_axes(self):
        ax_x = Arrow([AX_X0-0.2, AX_Y0, 0], [AX_X1+0.2, AX_Y0, 0],
                     buff=0, stroke_width=1.5, color=WHITE, tip_length=0.18)
        ax_y = Arrow([AX_X0, AX_Y0-0.2, 0], [AX_X0, AX_Y1+0.2, 0],
                     buff=0, stroke_width=1.5, color=WHITE, tip_length=0.18)

        ticks_x = VGroup()
        for v in [-1, 0, 1, 2]:
            sp = to_screen(v, Y_MIN)
            ticks_x.add(
                Line([sp[0], AX_Y0-0.08, 0], [sp[0], AX_Y0+0.08, 0],
                     stroke_width=1, color=GRAY),
                Text(str(v), font_size=11, color=GRAY).move_to([sp[0], AX_Y0-0.26, 0])
            )

        ticks_y = VGroup()
        for v in [-1.0, -0.5, 0.0, 0.5, 1.0, 1.5]:
            sp = to_screen(X_MIN, v)
            ticks_y.add(
                Line([AX_X0-0.08, sp[1], 0], [AX_X0+0.08, sp[1], 0],
                     stroke_width=1, color=GRAY),
                Text(f"{v:.1f}", font_size=11, color=GRAY).move_to([AX_X0-0.42, sp[1], 0])
            )

        xlabel = Text("x", font_size=16, color=WHITE).next_to(ax_x, DOWN, buff=0.55)
        ylabel = Text("y", font_size=16, color=WHITE).rotate(PI/2).next_to(ax_y, LEFT, buff=0.65)

        return VGroup(ax_x, ax_y, ticks_x, ticks_y, xlabel, ylabel)

    # ── label d'étape centré en bas ──────────────────────────────
    def show_step(self, old_lbl, text, color=WHITE, size=18):
        new_lbl = Text(text, font_size=size, color=color)
        new_lbl.to_edge(DOWN, buff=0.22)
        if old_lbl is not None:
            self.play(FadeOut(old_lbl), run_time=0.18)
        self.play(FadeIn(new_lbl), run_time=0.28)
        return new_lbl

    # ════════════════════════════════════════════════════════════
    def construct(self):

        # ── Axes + titre ─────────────────────────────────────────
        axes = self.make_axes()
        self.play(Create(axes), run_time=0.8)

        title = Text("K-Means  (k=2)  –  Dataset Moons",
                     font_size=20, color=WHITE).to_edge(UP, buff=0.15)
        self.play(Write(title), run_time=0.6)

        # ── Points (blancs) ──────────────────────────────────────
        dots = [Dot(to_screen(*p), radius=0.06, color=WHITE, fill_opacity=0.9)
                for p in DATA]
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.012), run_time=1.0)
        self.wait(0.3)

        # ── Centroïdes initiaux ──────────────────────────────────
        # Placés à gauche/droite pour qu'ils coupent les lunes verticalement
        # → K-Means va échouer à séparer les deux croissants
        centroids = np.array([[-0.3, 0.2], [1.3, 0.2]], dtype=float)

        cent_stars = []
        for c in centroids:
            s = Star(n=5, outer_radius=0.22, inner_radius=0.10,
                     fill_color=YELLOW, fill_opacity=1,
                     stroke_color=WHITE, stroke_width=1.2)
            s.move_to(to_screen(*c))
            cent_stars.append(s)

        step_lbl = self.show_step(None, "Initialisation des centroïdes", color=YELLOW)
        self.play(LaggedStart(*[FadeIn(s, scale=1.4) for s in cent_stars], lag_ratio=0.2),
                  run_time=0.6)
        self.wait(0.9)

        labels = np.full(len(DATA), -1)

        # ════ BOUCLE K-MEANS ════════════════════════════════════
        for iteration in range(6):

            # Affectation
            step_lbl = self.show_step(step_lbl,
                                      f"Itération {iteration+1}  –  Affectation")
            new_labels = km_assign(DATA, centroids)

            self.play(*[dots[i].animate.set_fill(COLORS_K[new_labels[i]])
                                        .set_stroke(COLORS_K[new_labels[i]])
                        for i in range(len(dots))],
                      run_time=0.8)
            self.wait(1.1)

            # Mise à jour
            step_lbl = self.show_step(step_lbl,
                                      f"Itération {iteration+1}  –  Mise à jour des centroïdes")
            new_centroids = km_update(DATA, new_labels)

            self.play(*[cent_stars[i].animate.move_to(to_screen(*new_centroids[i]))
                        for i in range(K)],
                      run_time=0.7)
            self.wait(1.1)

            if np.allclose(centroids, new_centroids, atol=1e-6) and np.array_equal(labels, new_labels):
                step_lbl = self.show_step(step_lbl, "Convergence atteinte ✓", color=YELLOW, size=20)
                self.wait(1.2)
                break

            centroids = new_centroids
            labels    = new_labels

        # ── Constat d'échec ──────────────────────────────────────
        step_lbl = self.show_step(step_lbl,
                                  "K-Means échoue : il ne peut séparer que des clusters convexes",
                                  color="#FF6B6B", size=17)
        self.wait(2.2)

        # ════════════════════════════════════════════════════════
        # TRANSITION → DBSCAN
        # ════════════════════════════════════════════════════════
        new_title = Text("DBSCAN  –  Density-Based Spatial Clustering",
                         font_size=20, color=WHITE).to_edge(UP, buff=0.15)

        self.play(
            FadeOut(step_lbl),
            FadeOut(VGroup(*cent_stars)),
            Transform(title, new_title),
            *[d.animate.set_fill(WHITE).set_stroke(WHITE) for d in dots],
            run_time=0.8,
        )
        self.wait(0.4)

        # ── Explication epsilon ──────────────────────────────────
        step_lbl = self.show_step(None,
                                  "DBSCAN : on cherche des zones denses (ε-voisinage + MinPts)",
                                  color=YELLOW, size=17)
        self.wait(1.5)

        # Cercle ε illustratif sur un point central
        sample_pt = DATA[30]
        eps_val   = 0.18
        eps_screen_r = eps_val / (X_MAX - X_MIN) * (AX_X1 - AX_X0)
        eps_circle = Circle(radius=eps_screen_r, color=YELLOW,
                            stroke_width=1.5, fill_opacity=0.0)
        eps_circle.move_to(to_screen(*sample_pt))
        eps_label  = Text(f"ε = {eps_val}", font_size=14, color=YELLOW)
        eps_label.next_to(eps_circle, RIGHT, buff=0.1)

        self.play(Create(eps_circle), Write(eps_label), run_time=0.7)
        self.wait(1.2)
        self.play(FadeOut(eps_circle), FadeOut(eps_label), run_time=0.4)

        # ── Calcul DBSCAN et coloriage ───────────────────────────
        step_lbl = self.show_step(step_lbl,
                                  "DBSCAN identifie les clusters par densité…", size=18)

        db_labels = dbscan(DATA, eps=eps_val, min_pts=5)
        n_clusters = len(set(db_labels) - {-1})
        dbscan_colors = [COLORS_TRUE[0], COLORS_TRUE[1]]   # 2 clusters attendus

        color_anims = []
        for i, lbl in enumerate(db_labels):
            if lbl == -1:
                color_anims.append(dots[i].animate.set_fill(NOISE_COLOR).set_stroke(NOISE_COLOR))
            else:
                c = dbscan_colors[lbl % len(dbscan_colors)]
                color_anims.append(dots[i].animate.set_fill(c).set_stroke(c))

        self.play(*color_anims, run_time=1.0)
        self.wait(1.3)

        # ── Résultat ─────────────────────────────────────────────
        n_noise = int(np.sum(db_labels == -1))
        step_lbl = self.show_step(step_lbl,
                                  f"DBSCAN trouve {n_clusters} clusters  |  {n_noise} point(s) de bruit (gris)",
                                  color=YELLOW, size=18)

        # Légende
        legend = VGroup(
            VGroup(Dot(radius=0.1, color=COLORS_TRUE[0]),
                   Text("Cluster 1", font_size=14, color=WHITE)).arrange(RIGHT, buff=0.12),
            VGroup(Dot(radius=0.1, color=COLORS_TRUE[1]),
                   Text("Cluster 2", font_size=14, color=WHITE)).arrange(RIGHT, buff=0.12),
            VGroup(Dot(radius=0.1, color=NOISE_COLOR),
                   Text("Bruit", font_size=14, color=WHITE)).arrange(RIGHT, buff=0.12),
        )
        legend.arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        legend.to_corner(UR, buff=0.4)
        self.play(FadeIn(legend), run_time=0.5)
        self.wait(2.8)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)


# ── COMMANDE ──────────────────────────────────────────────────────
# manim -pql kmeans_dbscan_moons.py KMeansDBSCAN
# manim -pqh kmeans_dbscan_moons.py KMeansDBSCAN