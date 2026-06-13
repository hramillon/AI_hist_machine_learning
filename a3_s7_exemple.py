from manim import *

class IrisDecisionTreeAndBoundaries(Scene):
    def construct(self):
        # --- 1. Configuration ---
        c_blanc = WHITE
        
        # Données réelles extraites (PetalLengthCm, PetalWidthCm, Species)
        iris_data = [
            (1.4, 0.2, "setosa"), (1.4, 0.2, "setosa"), (1.3, 0.2, "setosa"),
            (1.5, 0.2, "setosa"), (1.4, 0.2, "setosa"), (1.7, 0.4, "setosa"),
            (1.5, 0.2, "setosa"), (1.4, 0.2, "setosa"), (1.5, 0.1, "setosa"),
            (4.7, 1.4, "versicolor"), (4.5, 1.5, "versicolor"), (4.9, 1.5, "versicolor"),
            (4.0, 1.3, "versicolor"), (4.6, 1.5, "versicolor"), (4.5, 1.3, "versicolor"),
            (4.7, 1.6, "versicolor"), (3.3, 1.0, "versicolor"), (4.6, 1.3, "versicolor"),
            (6.0, 2.5, "virginica"), (5.1, 1.9, "virginica"), (5.9, 2.1, "virginica"),
            (5.6, 1.8, "virginica"), (5.8, 2.2, "virginica"), (6.6, 2.1, "virginica"),
            (4.5, 1.7, "virginica"), (6.3, 1.8, "virginica"), (5.8, 1.8, "virginica")
        ]

        # --- 2. Partie Gauche : L'Arbre de Décision (Écartement maximalisé) ---
        pos_tree = {
            "N0": LEFT * 4.6 + UP * 2.3,
            
            "N1_G": LEFT * 6.3 + UP * 0.9,
            "N1_D": LEFT * 2.9 + UP * 0.9,
            
            "N2_G": LEFT * 4.1 + DOWN * 0.5,
            "N2_D": LEFT * 1.7 + DOWN * 0.5,
            
            "N3_GG": LEFT * 5.0 + DOWN * 1.9,
            "N3_GD": LEFT * 3.2 + DOWN * 1.9,
            "N3_DG": LEFT * 2.3 + DOWN * 1.9,
            "N3_DD": LEFT * 0.5 + DOWN * 1.9
        }

        # Fonction de création d'un nœud avec texte centré de manière robuste
        def creer_noeud(position, lignes_texte, largeur=1.3, hauteur=0.8, t_size=8):
            boite_noeud = Rectangle(width=largeur, height=hauteur, color=c_blanc)
            boite_noeud.move_to(position)
            
            bloc_texte = VGroup(*[
                Text(ligne, font_size=t_size, color=WHITE) for ligne in lignes_texte
            ]).arrange(DOWN, buff=0.05)
            
            bloc_texte.move_to(boite_noeud.get_center())
            return VGroup(boite_noeud, bloc_texte)

        # Génération des nœuds (Feuilles réduites à 0.9 de largeur pour garantir l'espace)
        n0 = creer_noeud(pos_tree["N0"], ["PetalLength", "<=", "2.45cm"], largeur=1.4)
        n1_g = creer_noeud(pos_tree["N1_G"], ["Iris", "setosa"], largeur=1.0, hauteur=0.6)
        n1_d = creer_noeud(pos_tree["N1_D"], ["PetalLength", "<=", "4.75cm"], largeur=1.4)
        
        n2_g = creer_noeud(pos_tree["N2_G"], ["PetalWidth", "<=", "1.65cm"], largeur=1.3)
        n2_d = creer_noeud(pos_tree["N2_D"], ["PetalWidth", "<=", "1.75cm"], largeur=1.3)

        n3_gg = creer_noeud(pos_tree["N3_GG"], ["Iris", "versicolor"], largeur=0.8, hauteur=0.6, t_size=7)
        n3_gd = creer_noeud(pos_tree["N3_GD"], ["Iris", "virginica"], largeur=0.8, hauteur=0.6, t_size=7)
        n3_dg = creer_noeud(pos_tree["N3_DG"], ["Iris", "versicolor"], largeur=0.8, hauteur=0.6, t_size=7)
        n3_dd = creer_noeud(pos_tree["N3_DD"], ["Iris", "virginica"], largeur=0.8, hauteur=0.6, t_size=7)

        # Liens de l'arbre
        liens_tree = VGroup(
            Line(n0[0].get_bottom(), n1_g[0].get_top(), color=c_blanc),
            Line(n0[0].get_bottom(), n1_d[0].get_top(), color=c_blanc),
            
            Line(n1_d[0].get_bottom(), n2_g[0].get_top(), color=c_blanc),
            Line(n1_d[0].get_bottom(), n2_d[0].get_top(), color=c_blanc),
            
            Line(n2_g[0].get_bottom(), n3_gg[0].get_top(), color=c_blanc),
            Line(n2_g[0].get_bottom(), n3_gd[0].get_top(), color=c_blanc),
            Line(n2_d[0].get_bottom(), n3_dg[0].get_top(), color=c_blanc),
            Line(n2_d[0].get_bottom(), n3_dd[0].get_top(), color=c_blanc)
        )

        # --- 3. Partie Droite : Espace de Décision 2D ---
        boite = Rectangle(width=4.8, height=4.5, stroke_width=2, color=c_blanc)
        boite.move_to(RIGHT * 3.8 + DOWN * 0.3)

        def point_to_coords(x, y):
            x_min, x_max = 0.5, 7.5
            y_min, y_max = -0.2, 3.0
            pct_x = (x - x_min) / (x_max - x_min)
            pct_y = (y - y_min) / (y_max - y_min)
            real_x = boite.get_left()[0] + pct_x * (boite.get_right()[0] - boite.get_left()[0])
            real_y = boite.get_bottom()[1] + pct_y * (boite.get_top()[1] - boite.get_bottom()[1])
            return np.array([real_x, real_y, 0])

        l1 = Line(point_to_coords(2.45, -0.2), point_to_coords(2.45, 3.0), color=c_blanc, stroke_width=2)
        l2 = Line(point_to_coords(2.45, 1.75), point_to_coords(7.5, 1.75), color=c_blanc, stroke_width=2)
        l3 = Line(point_to_coords(4.95, -0.2), point_to_coords(4.95, 1.75), color=c_blanc, stroke_width=2)

        lbl_x = Text("Petal Length (cm)", font_size=11).next_to(boite, DOWN, buff=0.2)
        lbl_y = Text("Petal Width (cm)", font_size=11).next_to(boite, RIGHT, buff=0.2).rotate(90 * DEGREES)

        # Points
        points_mobjects = VGroup()
        for x, y, species in iris_data:
            pos_pt = point_to_coords(x, y)
            if species == "setosa":
                pt = Circle(radius=0.06, color=c_blanc, fill_opacity=1, fill_color=WHITE).move_to(pos_pt)
            elif species == "versicolor":
                pt = Square(side_length=0.11, color=c_blanc, fill_opacity=1, fill_color=WHITE).move_to(pos_pt)
            else:
                pt = Triangle(color=c_blanc, fill_opacity=1, fill_color=WHITE).scale(0.06).move_to(pos_pt)
            points_mobjects.add(pt)

        # --- 4. Animation ---
        self.play(
            FadeIn(n0), 
            Create(boite), FadeIn(lbl_x), FadeIn(lbl_y),
            run_time=0.4
        )
        self.play(FadeIn(points_mobjects, lag_ratio=0.01), run_time=0.4)
        self.wait(0.2)

        self.play(
            Create(l1),
            Create(liens_tree[0]), Create(liens_tree[1]),
            FadeIn(n1_g), FadeIn(n1_d),
            run_time=0.4
        )
        self.wait(0.2)

        self.play(
            Create(l2), Create(l3),
            Create(liens_tree[2]), Create(liens_tree[3]),
            FadeIn(n2_g), FadeIn(n2_d),
            run_time=0.4
        )
        self.wait(0.2)

        self.play(
            Create(liens_tree[4]), Create(liens_tree[5]),
            Create(liens_tree[6]), Create(liens_tree[7]),
            FadeIn(n3_gg), FadeIn(n3_gd), FadeIn(n3_dg), FadeIn(n3_dd),
            run_time=0.4
        )
        self.wait(1.5)