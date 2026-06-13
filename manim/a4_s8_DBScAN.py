from manim import *
import numpy as np

# ── Dataset moons ────────────────────────────────────────────────
np.random.seed(42)

def make_moons(n=120, noise=0.07):
    n_half = n // 2
    t0 = np.linspace(0, np.pi, n_half)
    x0 = np.cos(t0) + np.random.normal(0, noise, n_half)
    y0 = np.sin(t0) + np.random.normal(0, noise, n_half)
    t1 = np.linspace(0, np.pi, n_half)
    x1 =  1 - np.cos(t1) + np.random.normal(0, noise, n_half)
    y1 = -np.sin(t1) + 0.4 + np.random.normal(0, noise, n_half)
    X = np.vstack([np.column_stack([x0, y0]), np.column_stack([x1, y1])])
    return X

DATA = make_moons(n=120, noise=0.07)

# ── Mapping données → écran ──────────────────────────────────────
X_MIN, X_MAX = -1.6,  2.6
Y_MIN, Y_MAX = -1.1,  1.6
AX_X0, AX_X1 = -5.2,  4.8
AX_Y0, AX_Y1 = -2.6,  2.6

def to_screen(px, py):
    sx = AX_X0 + (px - X_MIN) / (X_MAX - X_MIN) * (AX_X1 - AX_X0)
    sy = AX_Y0 + (py - Y_MIN) / (Y_MAX - Y_MIN) * (AX_Y1 - AX_Y0)
    return np.array([sx, sy, 0.0])

def eps_to_screen_r(eps):
    """Convertit un epsilon (espace données) en rayon écran."""
    return eps / (X_MAX - X_MIN) * (AX_X1 - AX_X0)

# ── DBSCAN maison ────────────────────────────────────────────────
def dbscan(data, eps, min_pts=5):
    n = len(data)
    labels = np.full(n, -2)
    cluster_id = 0

    def neighbors(i):
        return [j for j in range(n)
                if j != i and np.linalg.norm(data[i] - data[j]) <= eps]

    for i in range(n):
        if labels[i] != -2:
            continue
        nb = neighbors(i)
        if len(nb) < min_pts:
            labels[i] = -1
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

# Palette de clusters (max 4 clusters possibles avec grand epsilon)
CLUSTER_PALETTE = ["#E8C84A", "#4AC8E8", "#E87A4A", "#A44AE8"]
NOISE_COLOR     = "#666666"
MIN_PTS         = 5


# ════════════════════════════════════════════════════════════════
class DBSCANMoons(Scene):

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

    def show_step(self, old, text, color=WHITE, size=17):
        new = Text(text, font_size=size, color=color)
        new.to_edge(DOWN, buff=0.22)
        anims = ([FadeOut(old)] if old is not None else []) + [FadeIn(new)]
        self.play(*anims, run_time=0.25)
        return new

    # ── Run DBSCAN pour un epsilon et colorie les dots ───────────
    def run_dbscan_episode(self, dots, eps, step_lbl, eps_label_obj, legend_obj):
        """Retourne (step_lbl, eps_label_obj, legend_obj) mis à jour."""

        # Label epsilon en haut à droite
        new_eps_lbl = Text(f"ε = {eps}   MinPts = {MIN_PTS}",
                           font_size=19, color=YELLOW)
        new_eps_lbl.to_corner(UR, buff=0.35)

        anims_in = [FadeIn(new_eps_lbl)]
        if eps_label_obj is not None:
            anims_in.append(FadeOut(eps_label_obj))
        self.play(*anims_in, run_time=0.3)

        # Cercle ε illustratif sur un point représentatif
        sample_idx = 20
        sample_pos = to_screen(*DATA[sample_idx])
        r_screen   = eps_to_screen_r(eps)
        eps_circle = Circle(radius=r_screen, color=YELLOW,
                            stroke_width=1.5, fill_opacity=0.07,
                            fill_color=YELLOW)
        eps_circle.move_to(sample_pos)
        eps_circle_lbl = Text(f"ε", font_size=13, color=YELLOW)
        eps_circle_lbl.next_to(eps_circle, RIGHT, buff=0.08)

        step_lbl = self.show_step(step_lbl,
                                  f"ε = {eps} : chaque point cherche ses voisins dans ce rayon")
        self.play(Create(eps_circle), FadeIn(eps_circle_lbl), run_time=0.6)
        self.wait(1.0)
        self.play(FadeOut(eps_circle), FadeOut(eps_circle_lbl), run_time=0.3)

        # Calcul DBSCAN
        step_lbl = self.show_step(step_lbl, f"Propagation des clusters  (ε = {eps})…")
        db_labels = dbscan(DATA, eps=eps, min_pts=MIN_PTS)

        unique_clusters = sorted(set(db_labels) - {-1})
        n_clusters = len(unique_clusters)
        n_noise    = int(np.sum(db_labels == -1))

        # Coloriage
        color_anims = []
        for i, lbl in enumerate(db_labels):
            if lbl == -1:
                c = NOISE_COLOR
            else:
                c = CLUSTER_PALETTE[unique_clusters.index(lbl) % len(CLUSTER_PALETTE)]
            color_anims.append(
                dots[i].animate.set_fill(c).set_stroke(c)
            )
        self.play(*color_anims, run_time=0.9)
        self.wait(0.3)

        # Résultat
        step_lbl = self.show_step(
            step_lbl,
            f"ε = {eps}  →  {n_clusters} cluster(s)  |  {n_noise} point(s) de bruit",
            color=YELLOW
        )

        # Légende
        new_legend = VGroup()
        for k in unique_clusters:
            row = VGroup(
                Dot(radius=0.09, color=CLUSTER_PALETTE[unique_clusters.index(k) % len(CLUSTER_PALETTE)]),
                Text(f"Cluster {k+1}", font_size=13, color=WHITE)
            ).arrange(RIGHT, buff=0.1)
            new_legend.add(row)
        if n_noise > 0:
            new_legend.add(
                VGroup(Dot(radius=0.09, color=NOISE_COLOR),
                       Text("Bruit", font_size=13, color=WHITE)).arrange(RIGHT, buff=0.1)
            )
        new_legend.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        new_legend.to_corner(DR, buff=0.35)

        anims_leg = [FadeIn(new_legend)]
        if legend_obj is not None:
            anims_leg.append(FadeOut(legend_obj))
        self.play(*anims_leg, run_time=0.4)

        self.wait(2.0)

        # Remettre les points en blanc pour la prochaine passe
        self.play(*[d.animate.set_fill(WHITE).set_stroke(WHITE) for d in dots],
                  run_time=0.5)

        return step_lbl, new_eps_lbl, new_legend

    # ════════════════════════════════════════════════════════════
    def construct(self):

        # Axes + titre
        axes = self.make_axes()
        self.play(Create(axes), run_time=0.8)

        title = Text("DBSCAN – Dataset Moons", font_size=22, color=WHITE)
        title.to_edge(UP, buff=0.15)
        self.play(Write(title), run_time=0.6)

        # Points initiaux blancs
        dots = [Dot(to_screen(*p), radius=0.06, color=WHITE, fill_opacity=0.9)
                for p in DATA]
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.01), run_time=0.9)
        self.wait(0.3)

        step_lbl    = None
        eps_lbl_obj = None
        legend_obj  = None

        # ── Épisode 1 : ε trop petit → trop de bruit ────────────
        step_lbl = self.show_step(step_lbl,
                                  "Essayons avec un ε très petit…", color=WHITE)
        self.wait(0.5)
        step_lbl, eps_lbl_obj, legend_obj = self.run_dbscan_episode(
            dots, eps=0.08, step_lbl=step_lbl,
            eps_label_obj=eps_lbl_obj, legend_obj=legend_obj
        )

        # Commentaire
        step_lbl = self.show_step(step_lbl,
                                  "ε trop petit : les points ne se connectent pas → beaucoup de bruit",
                                  color="#FF6B6B", size=16)
        self.wait(1.8)

        # ── Épisode 2 : ε = 0.2 → bon ───────────────────────────
        step_lbl = self.show_step(step_lbl,
                                  "Augmentons ε…", color=WHITE)
        self.wait(0.4)
        step_lbl, eps_lbl_obj, legend_obj = self.run_dbscan_episode(
            dots, eps=0.2, step_lbl=step_lbl,
            eps_label_obj=eps_lbl_obj, legend_obj=legend_obj
        )

        step_lbl = self.show_step(step_lbl,
                                  "ε = 0.2 : les deux lunes sont bien séparées",
                                  color="#4AC8E8", size=16)
        self.wait(1.8)

        # ── Épisode 3 : ε = 0.5 → trop grand, fusionne tout ─────
        step_lbl = self.show_step(step_lbl,
                                  "Et si ε est trop grand ?", color=WHITE)
        self.wait(0.4)
        step_lbl, eps_lbl_obj, legend_obj = self.run_dbscan_episode(
            dots, eps=0.5, step_lbl=step_lbl,
            eps_label_obj=eps_lbl_obj, legend_obj=legend_obj
        )

        step_lbl = self.show_step(step_lbl,
                                  "ε trop grand : les deux lunes fusionnent en un seul cluster",
                                  color="#FF6B6B", size=16)
        self.wait(1.8)

        # ── Conclusion ───────────────────────────────────────────
        step_lbl = self.show_step(step_lbl,
                                  "Le choix de ε est crucial  →  ε = 0.2 donne le meilleur résultat ici",
                                  color=YELLOW, size=16)
        self.wait(2.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)


# ── COMMANDE ─────────────────────────────────────────────────────
# manim -pql dbscan_moons.py DBSCANMoons
# manim -pqh dbscan_moons.py DBSCANMoons