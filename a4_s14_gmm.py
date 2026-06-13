from manim import *
import numpy as np
from scipy.stats import multivariate_normal

BG    = "#0F1117"
C1    = "#4FC3F7"
C2    = "#EF9A9A"
C3    = "#A5D6A7"
GOLD  = "#FFD54F"
WHITE = "#F0F4F8"
GREY  = "#8899AA"
COLORS = [C1, C2, C3]
K = 3

np.random.seed(42)

# ── Clusters très proches + variances larges => vrai chevauchement ──────────
MU_TRUE  = [np.array([ 0.0,  1.2]),
            np.array([ 1.0, -0.5]),
            np.array([-1.2, -0.3])]
SIG_TRUE = [np.eye(2)*1.4, np.eye(2)*1.4, np.eye(2)*1.4]
PI_TRUE  = [1/3, 1/3, 1/3]
N_PTS    = 80

def _gen():
    pts = []
    for mu, sig, pi in zip(MU_TRUE, SIG_TRUE, PI_TRUE):
        pts.append(np.random.multivariate_normal(mu, sig, int(N_PTS*pi)))
    return np.vstack(pts)

DATA = _gen()

def gauss_pdf(x, mu, sig):
    return multivariate_normal(mean=mu, cov=sig).pdf(x)

def e_step(data, mus, sigs, pis):
    r = np.column_stack([pis[k]*gauss_pdf(data, mus[k], sigs[k]) for k in range(K)])
    return r / r.sum(1, keepdims=True)

def m_step(data, r):
    mus, sigs, pis = [], [], []
    N = len(data)
    for k in range(K):
        Nk  = r[:,k].sum()
        mu  = (r[:,k,None]*data).sum(0)/Nk
        d   = data - mu
        sig = (r[:,k,None,None]*(d[:,:,None]*d[:,None,:])).sum(0)/Nk
        mus.append(mu); sigs.append(sig); pis.append(Nk/N)
    return mus, sigs, pis


class GMMem(Scene):
    def construct(self):
        self.camera.background_color = BG
        self._setup()
        self._e_step_anim()
        self._m_step_anim()
        self._run_iterations()
        self._soft_zoom()

    # ── 1. Données + init ───────────────────────────────────────────────────
    def _setup(self):
        ax = Axes(
            x_range=[-4, 4, 1], y_range=[-4, 4, 1],
            x_length=6.8, y_length=6.2,
            axis_config=dict(color=GREY, stroke_width=1, include_ticks=False,
                             include_tip=False),
        ).shift(LEFT*1.2)
        self.play(Create(ax), run_time=0.5)

        dots = VGroup(*[Dot(ax.c2p(*p), radius=0.06, color=GREY) for p in DATA])
        self.play(LaggedStart(*[FadeIn(d) for d in dots],
                              lag_ratio=0.012, run_time=1.2))

        # Init EM
        self._mus  = [np.array([ 0.8, 1.8]),
                      np.array([ 1.8,-1.2]),
                      np.array([-1.8, 0.4])]
        self._sigs = [np.eye(2)]*3
        self._pis  = [1/3]*3

        ellipses = self._make_ellipses(ax, self._mus, self._sigs)
        self.play(LaggedStart(*[Create(e) for e in ellipses],
                              lag_ratio=0.3, run_time=0.9))

        lbl = Text("Initialisation aléatoire", font="Montserrat",
                   font_size=21, color=GOLD).to_corner(UL).shift(RIGHT*0.2)
        self.play(FadeIn(lbl))
        self.wait(0.6)

        self._ax       = ax
        self._dots     = dots
        self._ellipses = ellipses
        self._lbl      = lbl

    # ── 2. Étape E ──────────────────────────────────────────────────────────
    def _e_step_anim(self):
        lbl = Text("Étape E  —  Expectation", font="Montserrat",
                   font_size=21, color=C1).to_corner(UL).shift(RIGHT*0.2)
        self.play(ReplacementTransform(self._lbl, lbl))

        desc = Text("Probabilité d'appartenance de chaque point\nà chaque gaussienne",
                    font="Montserrat", font_size=18, color=WHITE, line_spacing=1.35)\
               .to_edge(RIGHT).shift(LEFT*0.25+UP*0.6)
        self.play(FadeIn(desc))
        self.wait(0.3)

        r = e_step(DATA, self._mus, self._sigs, self._pis)

        # Couleur = mélange RVB pondéré par r (visualise l'appartenance douce)
        def blend(ri):
            cols = [color_to_rgb(c) for c in COLORS]
            rgb  = sum(ri[k]*np.array(cols[k]) for k in range(K))
            return rgb_to_color(np.clip(rgb,0,1))

        new_dots = VGroup(*[
            Dot(self._ax.c2p(*p), radius=0.06, color=blend(r[i]))
            for i,p in enumerate(DATA)
        ])
        self.play(Transform(self._dots, new_dots), run_time=1.0)
        self.wait(0.5)

        # Annoter 3 points frontière avec leur vecteur
        second = np.sort(r,axis=1)[:,1]
        for rank, idx in enumerate(np.argsort(-second)[:3]):
            pos   = self._ax.c2p(*DATA[idx])
            probs = r[idx]
            circ  = Circle(radius=0.22, color=GOLD, stroke_width=2)\
                    .move_to(pos)
            txt   = Text(f"[{probs[0]:.2f}, {probs[1]:.2f}, {probs[2]:.2f}]",
                         font="Courier New", font_size=17, color=GOLD)\
                    .next_to(circ, UP if rank<2 else DOWN, 0.1)
            self.play(Create(circ), FadeIn(txt), run_time=0.4)
            self.wait(0.5)
            self.play(FadeOut(circ), FadeOut(txt), run_time=0.3)

        self.play(FadeOut(desc))
        self._r   = r
        self._lbl = lbl

    # ── 3. Étape M ──────────────────────────────────────────────────────────
    def _m_step_anim(self):
        lbl = Text("Étape M  —  Maximization", font="Montserrat",
                   font_size=21, color=C2).to_corner(UL).shift(RIGHT*0.2)
        self.play(ReplacementTransform(self._lbl, lbl))

        desc = Text("Recalculer μ, Σ, π pour maximiser\nla vraisemblance des données",
                    font="Montserrat", font_size=18, color=WHITE, line_spacing=1.35)\
               .to_edge(RIGHT).shift(LEFT*0.25+UP*0.6)
        self.play(FadeIn(desc))
        self.wait(0.3)

        new_mus, new_sigs, new_pis = m_step(DATA, self._r)
        new_ell = self._make_ellipses(self._ax, new_mus, new_sigs)
        self.play(*[Transform(self._ellipses[k], new_ell[k]) for k in range(K)],
                  run_time=0.9)
        self.wait(0.6)

        self._mus, self._sigs, self._pis = new_mus, new_sigs, new_pis
        self.play(FadeOut(desc))
        self._lbl = lbl

    # ── 4. Itérations ───────────────────────────────────────────────────────
    def _run_iterations(self):
        lbl = Text("Convergence itérative", font="Montserrat",
                   font_size=21, color=GOLD).to_corner(UL).shift(RIGHT*0.2)
        self.play(ReplacementTransform(self._lbl, lbl))

        def blend(ri):
            cols = [color_to_rgb(c) for c in COLORS]
            rgb  = sum(ri[k]*np.array(cols[k]) for k in range(K))
            return rgb_to_color(np.clip(rgb,0,1))

        for _ in range(6):
            r = e_step(DATA, self._mus, self._sigs, self._pis)
            new_dots = VGroup(*[
                Dot(self._ax.c2p(*p), radius=0.06, color=blend(r[i]))
                for i,p in enumerate(DATA)
            ])
            self.play(Transform(self._dots, new_dots), run_time=0.28)

            new_mus, new_sigs, new_pis = m_step(DATA, r)
            new_ell = self._make_ellipses(self._ax, new_mus, new_sigs)
            self.play(*[Transform(self._ellipses[k], new_ell[k]) for k in range(K)],
                      run_time=0.28)
            self._mus, self._sigs, self._pis = new_mus, new_sigs, new_pis
            self._r = r

        self.wait(0.8)
        self._lbl = lbl

    # ── 5. Zoom sur l'appartenance douce ────────────────────────────────────
    def _soft_zoom(self):
        lbl = Text("Appartenance douce — soft assignment", font="Montserrat",
                   font_size=21, color=C3).to_corner(UL).shift(RIGHT*0.2)
        self.play(ReplacementTransform(self._lbl, lbl))

        r = self._r
        second = np.sort(r,axis=1)[:,1]
        # Les 3 points les plus ambigus
        targets = np.argsort(-second)[:3]

        for idx in targets:
            pos   = self._ax.c2p(*DATA[idx])
            probs = r[idx]
            col   = COLORS[np.argmax(probs)]

            circ = Circle(radius=0.25, color=col, stroke_width=2.5).move_to(pos)
            pvec = Text(f"[{probs[0]:.2f}, {probs[1]:.2f}, {probs[2]:.2f}]",
                        font="Courier New", font_size=19, color=col)\
                  .next_to(circ, UP, 0.12)

            self.play(Create(circ), FadeIn(pvec), run_time=0.4)

            # Barres de proba à droite
            bars_g, labs_g = VGroup(), VGroup()
            BW, BH = 0.7, 1.8
            x0, y0 = 4.8, -0.5
            for j, (p, c, name) in enumerate(zip(probs, COLORS, ["G₁","G₂","G₃"])):
                h   = BH * p
                bar = Rectangle(width=BW, height=h, color=c,
                                fill_color=c, fill_opacity=0.75, stroke_width=1)\
                      .move_to([x0 + j*1.05, y0 + h/2, 0])
                lab = Text(f"{name}\n{p:.2f}", font="Montserrat",
                           font_size=15, color=c).next_to(bar, DOWN, 0.1)
                bars_g.add(bar); labs_g.add(lab)

            self.play(LaggedStart(*[GrowFromEdge(b,DOWN) for b in bars_g],
                                  lag_ratio=0.2, run_time=0.6))
            self.play(LaggedStart(*[FadeIn(l) for l in labs_g],
                                  lag_ratio=0.15, run_time=0.4))
            self.wait(1.0)
            self.play(FadeOut(circ), FadeOut(pvec), FadeOut(bars_g), FadeOut(labs_g),
                      run_time=0.3)

        self.wait(0.5)

    # ── Helper ellipses ─────────────────────────────────────────────────────
    def _make_ellipses(self, ax, mus, sigs):
        ellipses = VGroup()
        for mu, sig, col in zip(mus, sigs, COLORS):
            vals, vecs = np.linalg.eigh(sig)
            angle = np.arctan2(vecs[1,1], vecs[0,1])
            w = 2*np.sqrt(vals[1])*2
            h = 2*np.sqrt(vals[0])*2
            p0 = ax.c2p(*mu)
            sw = abs(ax.c2p(mu[0]+w/2, mu[1])[0] - p0[0])
            sh = abs(ax.c2p(mu[0], mu[1]+h/2)[1] - p0[1])
            ell = Ellipse(width=sw*2, height=sh*2, color=col,
                          stroke_width=2, fill_color=col, fill_opacity=0.07)\
                  .rotate(angle).move_to(p0)
            cross = VGroup(
                Line(LEFT*0.13, RIGHT*0.13, color=col, stroke_width=2.2),
                Line(DOWN*0.13, UP   *0.13, color=col, stroke_width=2.2),
            ).move_to(p0)
            ellipses.add(VGroup(ell, cross))
        return ellipses