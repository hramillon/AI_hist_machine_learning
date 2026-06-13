from manim import *

class SceneGiniIndex(MovingCameraScene):
    def construct(self):

        def create_node(lines, width=3.6, height=1.9):
            rect = Rectangle(width=width, height=height, color=WHITE)
            content = VGroup(
                *[MathTex(l, font_size=22) for l in lines]
            ).arrange(DOWN, buff=0.12)
            content.move_to(rect.get_center())
            return VGroup(rect, content)

        # ── ARBRE INITIAL grand centré ──────────────────────────────────
        n0_big = create_node([
            "\\text{Petal Length} \\le 2.45",
            "i = 0",
            "\\text{value} = [40,\\ 40,\\ 40]",
            "\\text{Gini} = ?",
        ], width=4.0, height=2.0)
        n1_big = create_node([
            "i = 1",
            "\\text{value} = [40,\\ 0,\\ 0]",
            "\\text{Gini} = ?",
        ], width=3.0, height=1.6)
        n2_big = create_node([
            "\\text{Petal Length} \\le 4.75",
            "i = 2",
            "\\text{value} = [0,\\ 40,\\ 40]",
            "\\text{Gini} = ?",
        ], width=4.0, height=2.0)

        n0_big.move_to(UP * 2.2)
        n1_big.move_to(LEFT * 4.0 + DOWN * 0.6)
        n2_big.move_to(RIGHT * 4.0 + DOWN * 0.6)
        e1b = Line(n0_big[0].get_bottom(), n1_big[0].get_top())
        e2b = Line(n0_big[0].get_bottom(), n2_big[0].get_top())
        tree_big = VGroup(n0_big, n1_big, n2_big, e1b, e2b)

        self.play(FadeIn(tree_big))
        self.wait(0.5)

        # Zoom sur la racine
        self.play(
            self.camera.frame.animate
                .set_width(n0_big.get_width() * 1.8)
                .move_to(n0_big.get_center()),
            run_time=0.9
        )
        self.wait(0.6)

        # ── CONFIGURATION DE LA SCÈNE PRINCIPALE ───────────────────────
        # Caméra principale : 14 unités de large, centrée en (0,1)
        # Côté gauche [-7, -3] = zone nœud
        # Côté droit  [-1, +7] = zone calculs
        CAM_W = 14.0
        CAM_CENTER = [0.0, 1.0, 0]

        # Nœud unique affiché à gauche : centré en x=-5
        NODE_X = -5.0
        NODE_Y = 1.0

        # Zone calculs : commence à x = -1.5, bien à droite
        CALC_LEFT = -1.5

        # Les 3 nœuds sont placés au même endroit (on les swap)
        n0 = create_node([
            "\\text{Petal Length} \\le 2.45",
            "i = 0",
            "\\text{value} = [40,\\ 40,\\ 40]",
            "\\text{Gini} = ?",
        ], width=3.4, height=1.8).move_to([NODE_X, NODE_Y, 0])

        n1 = create_node([
            "i = 1",
            "\\text{value} = [40,\\ 0,\\ 0]",
            "\\text{Gini} = ?",
        ], width=3.0, height=1.6).move_to([NODE_X, NODE_Y, 0])

        n2 = create_node([
            "\\text{Petal Length} \\le 4.75",
            "i = 2",
            "\\text{value} = [0,\\ 40,\\ 40]",
            "\\text{Gini} = ?",
        ], width=3.4, height=1.8).move_to([NODE_X, NODE_Y, 0])

        # Transition : arbre disparaît, n0 apparaît seul à gauche
        self.play(
            ReplacementTransform(tree_big, n0),
            self.camera.frame.animate.set_width(CAM_W).move_to(CAM_CENTER),
            run_time=1.1
        )
        self.wait(0.4)
        self.play(n0[0].animate.set_color(YELLOW), run_time=0.3)

        # ── HELPER : position dans la zone calculs ──────────────────────
        def R(x_offset, y):
            """Ancre gauche dans la zone droite."""
            return [CALC_LEFT + x_offset, y, 0]

        # ── ÉTAPE 1 ─────────────────────────────────────────────────────
        titre = Text(
            "Étape 1 : probabilité d'erreur par classe :",
            font_size=17, color=YELLOW
        ).move_to(R(0, 2.8), aligned_edge=LEFT)
        self.play(Write(titre))

        p_setosa = MathTex(
            "P_{0,\\text{setosa}} = \\dfrac{40}{120} = \\dfrac{1}{3}",
            font_size=24
        ).move_to(R(0, 2.1), aligned_edge=LEFT)
        self.play(Write(p_setosa))
        self.wait(0.4)

        p_erreur = MathTex(
            "\\text{proba de mal classer :} \\quad 1 - P_{0,\\text{setosa}}",
            font_size=21
        ).move_to(R(0, 1.5), aligned_edge=LEFT)
        self.play(Write(p_erreur))
        self.wait(0.7)

        p_produit = MathTex(
            "P_{0,\\text{setosa}} \\times (1 - P_{0,\\text{setosa}})",
            font_size=24
        ).move_to(R(0, 2.1), aligned_edge=LEFT)
        self.play(FadeOut(p_setosa), FadeOut(p_erreur), FadeIn(p_produit))
        self.wait(0.7)

        # ── ÉTAPE 2 ─────────────────────────────────────────────────────
        titre2 = Text(
            "Étape 2 : somme sur toutes les classes",
            font_size=17, color=YELLOW
        ).move_to(titre, aligned_edge=LEFT)
        self.play(Transform(titre, titre2), FadeOut(p_produit))

        k_classes = MathTex(
            "K = \\{\\text{setosa},\\ \\text{versicolor},\\ \\text{virginica}\\}",
            font_size=22
        ).move_to(R(0, 2.1), aligned_edge=LEFT)
        self.play(Write(k_classes))

        formula_gini = MathTex(
            "G_0 = \\sum_{k \\in K} P_{0,k} \\times (1 - P_{0,k})",
            font_size=26
        ).move_to(R(0, 1.4), aligned_edge=LEFT)
        self.play(Write(formula_gini))
        self.wait(0.8)

        # ── ÉTAPE 3 ─────────────────────────────────────────────────────
        titre3 = Text(
            "Étape 3 : simplification",
            font_size=17, color=YELLOW
        ).move_to(titre, aligned_edge=LEFT)
        self.play(Transform(titre, titre3), FadeOut(k_classes))

        g_v1 = MathTex(
            "G_0 = \\sum_{k \\in K} \\left(P_{0,k} - P_{0,k}^2\\right)",
            font_size=26
        ).move_to(formula_gini, aligned_edge=LEFT)
        self.play(Transform(formula_gini, g_v1))
        self.wait(0.5)

        g_v2 = MathTex(
            "G_0 = \\sum_{k \\in K} P_{0,k} - \\sum_{k \\in K} P_{0,k}^2",
            font_size=26
        ).move_to(g_v1, aligned_edge=LEFT)
        self.play(Transform(formula_gini, g_v2))
        self.wait(0.5)

        g_v3 = MathTex(
            "G_0 = 1 - \\sum_{k \\in K} P_{0,k}^2",
            font_size=26, color=GREEN
        ).move_to(g_v2, aligned_edge=LEFT)
        self.play(Transform(formula_gini, g_v3))
        self.wait(0.7)

        # ── EXEMPLE NŒUD 0 ──────────────────────────────────────────────
        ex_titre = Text("Exemple nœud 0 :", font_size=17, color=BLUE
        ).move_to(R(0, 0.5), aligned_edge=LEFT)
        self.play(Write(ex_titre))

        calc_a = MathTex(
            "1 - \\left[\\left(\\tfrac{1}{3}\\right)^2", font_size=24
        ).move_to(R(0, -0.1), aligned_edge=LEFT)
        self.play(Write(calc_a)); self.wait(0.5)

        calc_b = MathTex(
            "1 - \\left[\\left(\\tfrac{1}{3}\\right)^2 + \\left(\\tfrac{1}{3}\\right)^2",
            font_size=24
        ).move_to(calc_a, aligned_edge=LEFT)
        self.play(Transform(calc_a, calc_b)); self.wait(0.5)

        calc_c = MathTex(
            "1 - \\left[\\left(\\tfrac{1}{3}\\right)^2 + \\left(\\tfrac{1}{3}\\right)^2"
            "+ \\left(\\tfrac{1}{3}\\right)^2\\right]",
            font_size=24
        ).move_to(calc_a, aligned_edge=LEFT)
        self.play(Transform(calc_a, calc_c)); self.wait(0.5)

        res_n0 = MathTex(
            "= 1 - \\dfrac{3}{9} = \\dfrac{2}{3} \\approx 0.667", font_size=24
        ).move_to(R(0, -0.75), aligned_edge=LEFT)
        self.play(Write(res_n0)); self.wait(0.6)

        new_gini_n0 = MathTex("\\text{Gini} = 0.667", font_size=22, color=GREEN
        ).move_to(n0[1][3])
        self.play(Transform(n0[1][3], new_gini_n0), n0[0].animate.set_color(GREEN))
        self.wait(0.8)

        # ── NŒUD i=1 ────────────────────────────────────────────────────
        self.play(
            FadeOut(titre), FadeOut(formula_gini),
            FadeOut(ex_titre), FadeOut(calc_a), FadeOut(res_n0),
        )
        self.play(ReplacementTransform(n0, n1))
        self.play(n1[0].animate.set_color(YELLOW), run_time=0.3)

        titre_n1 = Text("Exemple Parfait (i = 1)", font_size=18, color=YELLOW
        ).move_to(R(0, 2.8), aligned_edge=LEFT)
        self.play(Write(titre_n1))

        calcul_n1 = MathTex(
            "G_1 = 1 - 1^2 - 0^2 - 0^2 = 0", font_size=28
        ).move_to(R(0, 2.0), aligned_edge=LEFT)
        self.play(Write(calcul_n1)); self.wait(0.5)

        new_gini_n1 = MathTex("\\text{Gini} = 0", font_size=22, color=GOLD
        ).move_to(n1[1][2])
        self.play(Transform(n1[1][2], new_gini_n1), n1[0].animate.set_color(GOLD))
        self.wait(1.0)

        # ── NŒUD i=2 ────────────────────────────────────────────────────
        self.play(FadeOut(titre_n1), FadeOut(calcul_n1))
        self.play(ReplacementTransform(n1, n2))
        self.play(n2[0].animate.set_color(YELLOW), run_time=0.3)

        titre_n2 = Text("Cas le plus impur (i = 2)", font_size=18, color=RED
        ).move_to(R(0, 2.8), aligned_edge=LEFT)
        self.play(Write(titre_n2))

        calcul_n2 = MathTex(
            "G_2 = 1 - \\left(\\tfrac{1}{2}\\right)^2"
            "- \\left(\\tfrac{1}{2}\\right)^2 = \\dfrac{1}{2} = 0.5",
            font_size=28
        ).move_to(R(0, 2.0), aligned_edge=LEFT)
        self.play(Write(calcul_n2)); self.wait(0.5)

        new_gini_n2 = MathTex("\\text{Gini} = 0.5", font_size=22, color=RED
        ).move_to(n2[1][3])
        self.play(Transform(n2[1][3], new_gini_n2), n2[0].animate.set_color(RED))
        self.wait(1.0)

        # ── ARBRE FINAL avec toutes les valeurs Gini ─────────────────────
        self.play(FadeOut(titre_n2), FadeOut(calcul_n2))

        # Construire l'arbre final avec les bonnes valeurs Gini
        fn0 = create_node([
            "\\text{Petal Length} \\le 2.45",
            "i = 0",
            "\\text{value} = [40,\\ 40,\\ 40]",
            "\\text{Gini} = 0.667",
        ], width=3.8, height=1.9)
        fn0[1][3].set_color(GREEN)
        fn0[0].set_color(GREEN)

        fn1 = create_node([
            "i = 1",
            "\\text{value} = [40,\\ 0,\\ 0]",
            "\\text{Gini} = 0",
        ], width=3.0, height=1.6)
        fn1[1][2].set_color(GOLD)
        fn1[0].set_color(GOLD)

        fn2 = create_node([
            "\\text{Petal Length} \\le 4.75",
            "i = 2",
            "\\text{value} = [0,\\ 40,\\ 40]",
            "\\text{Gini} = 0.5",
        ], width=3.8, height=1.9)
        fn2[1][3].set_color(RED)
        fn2[0].set_color(RED)

        fn0.move_to([0.0,  2.2, 0])
        fn1.move_to([-3.5, 0.0, 0])
        fn2.move_to([ 3.5, 0.0, 0])

        fe1 = Line(fn0[0].get_bottom(), fn1[0].get_top())
        fe2 = Line(fn0[0].get_bottom(), fn2[0].get_top())
        tree_done = VGroup(fn0, fn1, fn2, fe1, fe2)

        self.play(
            ReplacementTransform(n2, fn2),
            self.camera.frame.animate
                .set_width(11.0)
                .move_to([0.0, 1.2, 0]),
            run_time=0.9
        )
        self.play(FadeIn(fn0), FadeIn(fn1), FadeIn(fe1), FadeIn(fe2))
        self.wait(2.0)