from manim import *

# ─── COULEURS SOBRES SUR FOND NOIR ───
SETOSA_COLOR     = WHITE
VERSICOLOR_COLOR = WHITE
VIRGINICA_COLOR  = WHITE

NODE_FILL        = "#1a1a1a"   # quasi-noir, discret
NODE_STROKE      = "#888888"
SETOSA_STROKE    = "#cccccc"
VERSICOLOR_STROKE= "#cccccc"
VIRGINICA_STROKE = "#cccccc"
AGENT_COLOR      = YELLOW
EDGE_COLOR       = "#666666"


def make_node(lines, width=3.0, height=1.05, fill="#1a1a1a", stroke="#888888", fsize=15):
    box = RoundedRectangle(corner_radius=0.12, width=width, height=height,
                           fill_color=fill, fill_opacity=1,
                           stroke_color=stroke, stroke_width=1.5)
    label = Text(lines, font_size=fsize, color=WHITE).move_to(box)
    return VGroup(box, label)


def edge(a, b):
    return Arrow(a.get_bottom(), b.get_top(),
                 buff=0.07, stroke_width=1.8,
                 color=EDGE_COLOR, tip_length=0.15)


def make_agent():
    return Circle(radius=0.15, fill_color=YELLOW, fill_opacity=1,
                  stroke_color=WHITE, stroke_width=1.5)


# ──────────────────────────────────────────────────────────────
class RandomForestExplained(Scene):

    # ── Construit l'arbre COMPLET (7 nœuds) ──────────────────
    def build_full_tree(self, s=1.0, origin=ORIGIN):
        """Retourne dict de nœuds + VGroup des flèches + VGroup total"""
        o = origin

        root  = make_node("PetalLengthCm <= 2.45\ngini=0.667  n=120", 3.0*s, 1.05*s, fsize=int(14*s))
        root.move_to(o + UP*3.0*s)

        setosa = make_node("Iris-setosa\ngini=0  n=40", 2.4*s, 0.95*s, stroke="#aaaaaa", fsize=int(13*s))
        setosa.move_to(o + UP*1.4*s + LEFT*3.8*s)

        n2 = make_node("PetalLengthCm <= 4.75\ngini=0.5  n=80", 3.0*s, 1.05*s, fsize=int(14*s))
        n2.move_to(o + UP*1.4*s + RIGHT*1.0*s)

        n3 = make_node("PetalWidthCm <= 1.65\ngini=0.053  n=37", 2.9*s, 1.0*s, fsize=int(13*s))
        n3.move_to(o + DOWN*0.4*s + LEFT*1.5*s)

        n4 = make_node("PetalWidthCm <= 1.75\ngini=0.206  n=43", 2.9*s, 1.0*s, fsize=int(13*s))
        n4.move_to(o + DOWN*0.4*s + RIGHT*3.8*s)

        lv = make_node("Iris-versicolor\ngini=0  n=36", 2.4*s, 0.95*s, stroke="#aaaaaa", fsize=int(13*s))
        lv.move_to(o + DOWN*1.8*s + LEFT*2.9*s)

        lv1= make_node("Iris-virginica\ngini=0  n=1", 2.4*s, 0.95*s, stroke="#aaaaaa", fsize=int(13*s))
        lv1.move_to(o + DOWN*1.8*s + LEFT*0.1*s)

        lv2= make_node("Iris-versicolor\ngini=0.5  n=8", 2.4*s, 0.95*s, stroke="#aaaaaa", fsize=int(13*s))
        lv2.move_to(o + DOWN*1.8*s + RIGHT*2.5*s)

        lv3= make_node("Iris-virginica\ngini=0.056  n=35", 2.4*s, 0.95*s, stroke="#aaaaaa", fsize=int(13*s))
        lv3.move_to(o + DOWN*1.8*s + RIGHT*5.2*s)

        nodes = dict(root=root, setosa=setosa, n2=n2, n3=n3, n4=n4,
                     lv=lv, lv1=lv1, lv2=lv2, lv3=lv3)

        edges = VGroup(
            edge(root, setosa), edge(root, n2),
            edge(n2, n3), edge(n2, n4),
            edge(n3, lv), edge(n3, lv1),
            edge(n4, lv2), edge(n4, lv3),
        )

        full = VGroup(VGroup(*nodes.values()), edges)
        return nodes, edges, full

    # ── Construit l'arbre SIMPLIFIÉ (n4 retiré, feuille à la place) ──
    def build_simple_tree(self, s=1.0, origin=ORIGIN):
        o = origin

        root  = make_node("PetalLengthCm <= 2.45\ngini=0.667  n=120", 3.0*s, 1.05*s, fsize=int(14*s))
        root.move_to(o + UP*3.0*s)

        setosa = make_node("Iris-setosa\ngini=0  n=40", 2.4*s, 0.95*s, stroke="#aaaaaa", fsize=int(13*s))
        setosa.move_to(o + UP*1.4*s + LEFT*3.8*s)

        n2 = make_node("PetalLengthCm <= 4.75\ngini=0.5  n=80", 3.0*s, 1.05*s, fsize=int(14*s))
        n2.move_to(o + UP*1.4*s + RIGHT*1.0*s)

        n3 = make_node("PetalWidthCm <= 1.65\ngini=0.053  n=37", 2.9*s, 1.0*s, fsize=int(13*s))
        n3.move_to(o + DOWN*0.4*s + LEFT*1.5*s)

        # n4 remplacé par une feuille directe
        leaf_vir = make_node("Iris-virginica\ngini=0.206  n=43", 2.4*s, 0.95*s, stroke="#aaaaaa", fsize=int(13*s))
        leaf_vir.move_to(o + DOWN*0.4*s + RIGHT*3.8*s)

        lv = make_node("Iris-versicolor\ngini=0  n=36", 2.4*s, 0.95*s, stroke="#aaaaaa", fsize=int(13*s))
        lv.move_to(o + DOWN*1.8*s + LEFT*2.9*s)

        lv1= make_node("Iris-virginica\ngini=0  n=1", 2.4*s, 0.95*s, stroke="#aaaaaa", fsize=int(13*s))
        lv1.move_to(o + DOWN*1.8*s + LEFT*0.1*s)

        nodes = dict(root=root, setosa=setosa, n2=n2, n3=n3,
                     leaf_vir=leaf_vir, lv=lv, lv1=lv1)

        edges = VGroup(
            edge(root, setosa), edge(root, n2),
            edge(n2, n3), edge(n2, leaf_vir),   # flèche directe vers la feuille
            edge(n3, lv), edge(n3, lv1),
        )

        full = VGroup(VGroup(*nodes.values()), edges)
        return nodes, edges, full

    # ── Agent traverse un chemin, résultat EN DESSOUS de l'arbre ──
    def animate_agent(self, nodes, path_keys, result_str, tree_bottom_y, run_time=0.45):
        agent = make_agent()
        agent.move_to(nodes[path_keys[0]].get_top() + UP*0.3)
        self.play(FadeIn(agent), run_time=0.3)

        for key in path_keys:
            self.play(agent.animate.move_to(nodes[key].get_center()), run_time=run_time)
            self.wait(0.1)

        res = Text(result_str, font_size=22, color=WHITE)
        res.move_to(DOWN * (abs(tree_bottom_y) + 0.55))
        self.play(FadeIn(res, shift=DOWN*0.15), run_time=0.3)
        self.wait(0.6)
        self.play(FadeOut(agent), FadeOut(res), run_time=0.5)

    # ════════════════════════════════════════════════════════════
    def construct(self):

        # ── 1. Afficher l'arbre ──────────────────────────────
        title = Text("Arbre de décision – Dataset Iris", font_size=26, color=WHITE)
        title.to_edge(UP, buff=0.25)
        self.play(Write(title), run_time=0.8)

        nodes, edges, full_tree = self.build_full_tree(s=0.78, origin=UP*0.1)

        self.play(LaggedStart(*[FadeIn(n, shift=DOWN*0.1) for n in nodes.values()],
                              lag_ratio=0.1), run_time=1.6)
        self.play(LaggedStart(*[Create(e) for e in edges], lag_ratio=0.07), run_time=1.0)
        self.wait(0.4)

        # ── 2. Agents traversent l'arbre (résultats sous l'arbre) ─
        tree_bottom = min(n.get_bottom()[1] for n in nodes.values())

        paths = [
            (["root", "setosa"],         "→ Iris-setosa"),
            (["root", "n2", "n3", "lv"], "→ Iris-versicolor"),
            (["root", "n2", "n4", "lv3"],"→ Iris-virginica"),
        ]
        for path_keys, label in paths:
            self.animate_agent(nodes, path_keys, label, tree_bottom)

        # ── 3. Modifier l'arbre : swap instantané vers l'arbre simplifié ──
        s_nodes, s_edges, s_full = self.build_simple_tree(s=0.78, origin=UP*0.1)

        self.play(
            FadeOut(VGroup(*nodes.values()), edges),
            FadeIn(s_full),
            run_time=0.35,
        )
        self.wait(0.3)

        # ── 4. Dézoom → forêt de 10 arbres ─────────────────────
        forest_title = Text("Random Forest : une forêt d'arbres", font_size=26, color=WHITE)
        forest_title.to_edge(UP, buff=0.25)

        # Regrouper tout ce qui est à l'écran dans un seul VGroup
        current_tree_vgroup = s_full

        self.play(
            FadeOut(title),
            current_tree_vgroup.animate.scale(0.17).move_to(LEFT*5.5 + DOWN*1.2),
            run_time=1.1,
        )
        self.play(Write(forest_title), run_time=0.6)

        # 9 arbres supplémentaires (simplifiés, mini)
        positions = [
            LEFT*5.5 + DOWN*1.2,
            LEFT*3.6 + DOWN*1.2,
            LEFT*1.7 + DOWN*1.2,
            RIGHT*0.2 + DOWN*1.2,
            RIGHT*2.1 + DOWN*1.2,
            RIGHT*4.0 + DOWN*1.2,
            RIGHT*5.9 + DOWN*1.2,
            LEFT*4.5 + UP*1.5,
            LEFT*0.3 + UP*1.5,
            RIGHT*3.9 + UP*1.5,
        ]

        mini_trees = [current_tree_vgroup]
        anims = []
        for i in range(1, 10):
            _, _, ft = self.build_simple_tree(s=0.78, origin=ORIGIN)
            ft.scale(0.17).move_to(positions[i])
            mini_trees.append(ft)
            anims.append(FadeIn(ft, shift=UP*0.05))

        self.play(LaggedStart(*anims, lag_ratio=0.08), run_time=1.8)
        self.wait(0.3)

        # ── 5. Chaque agent traverse SON arbre ──────────────────
        vote_title = Text("Chaque arbre vote…", font_size=20, color=WHITE)
        vote_title.next_to(forest_title, DOWN, buff=0.1)
        self.play(FadeIn(vote_title))

        # votes : 3 setosa, 4 versicolor, 3 virginica
        vote_labels = ["Setosa"]*3 + ["Versicolor"]*4 + ["Virginica"]*3

        agent_anims = []
        agents_list = []
        for tree in mini_trees:
            ag = make_agent()
            ag.scale(0.6)
            ag.move_to(tree.get_top() + UP*0.08)
            agents_list.append(ag)
            agent_anims.append(FadeIn(ag))

        self.play(LaggedStart(*agent_anims, lag_ratio=0.06), run_time=1.2)

        # agents descendent vers le bas de leur arbre
        move_anims = []
        for ag, tree in zip(agents_list, mini_trees):
            move_anims.append(ag.animate.move_to(tree.get_bottom() + DOWN*0.12))
        self.play(*move_anims, run_time=1.0)
        self.wait(0.3)

        # affichage des votes
        vote_text_objs = []
        for i, (ag, label) in enumerate(zip(agents_list, vote_labels)):
            vt = Text(label, font_size=9, color=WHITE)
            vt.next_to(ag, DOWN, buff=0.04)
            vote_text_objs.append(vt)

        self.play(LaggedStart(*[FadeIn(v) for v in vote_text_objs], lag_ratio=0.05), run_time=1.0)
        self.wait(0.5)

        self.play(FadeOut(vote_title))

        # ── 6. Résultat final en blanc, en bas ──────────────────
        tally = Text("Setosa ×3     Versicolor ×4     Virginica ×3", font_size=20, color=WHITE)
        tally.to_edge(DOWN, buff=0.75)
        self.play(Write(tally), run_time=0.8)
        self.wait(0.4)

        result = Text("La forêt choisit : Iris-versicolor", font_size=26, color=WHITE, weight=BOLD)
        result.to_edge(DOWN, buff=0.3)
        self.play(Write(result), run_time=0.9)
        self.wait(2.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)


# ── COMMANDE ──────────────────────────────────────────────────
# manim -pql random_forest_animation.py RandomForestExplained
# manim -pqh random_forest_animation.py RandomForestExplained