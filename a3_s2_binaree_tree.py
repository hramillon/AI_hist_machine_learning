from manim import *

class SceneGrandArbreBinaire(MovingCameraScene):
    def construct(self):
        # --- 1. Génération des positions d'un grand arbre (4 niveaux) ---
        positions = {}
        # Niveau 0
        positions["0_0"] = UP * 3
        # Niveau 1
        positions["1_0"] = LEFT * 3.5 + UP * 1
        positions["1_1"] = RIGHT * 3.5 + UP * 1
        # Niveau 2
        positions["2_0"] = LEFT * 5 + DOWN * 1
        positions["2_1"] = LEFT * 2 + DOWN * 1
        positions["2_2"] = RIGHT * 2 + DOWN * 1
        positions["2_3"] = RIGHT * 5 + DOWN * 1
        # Niveau 3 (Feuilles)
        positions["3_0"] = LEFT * 5.8 + DOWN * 3
        positions["3_1"] = LEFT * 4.2 + DOWN * 3
        positions["3_2"] = LEFT * 2.8 + DOWN * 3
        positions["3_3"] = LEFT * 1.2 + DOWN * 3

        # Styles
        c_noeud, c_highlight, c_enfant, c_feuille = WHITE, GOLD, BLUE, GREEN

        # Création des nœuds
        noeuds = {}
        for cle, pos in positions.items():
            noeuds[cle] = Circle(radius=0.3, color=c_noeud, fill_opacity=1, fill_color=BLACK).move_to(pos)

        # Création des liens
        liens = VGroup(
            Line(noeuds["0_0"].get_bottom(), noeuds["1_0"].get_top()),
            Line(noeuds["0_0"].get_bottom(), noeuds["1_1"].get_top()),
            Line(noeuds["1_0"].get_bottom(), noeuds["2_0"].get_top()),
            Line(noeuds["1_0"].get_bottom(), noeuds["2_1"].get_top()),
            Line(noeuds["1_1"].get_bottom(), noeuds["2_2"].get_top()),
            Line(noeuds["1_1"].get_bottom(), noeuds["2_3"].get_top()),
            Line(noeuds["2_0"].get_bottom(), noeuds["3_0"].get_top()),
            Line(noeuds["2_0"].get_bottom(), noeuds["3_1"].get_top()),
            Line(noeuds["2_1"].get_bottom(), noeuds["3_2"].get_top()),
            Line(noeuds["2_1"].get_bottom(), noeuds["3_3"].get_top()),
        )

        titre = Text("Arbre Binaire", font_size=45).to_edge(UP)
        
        # Groupement global pour rapetissir et descendre l'arbre par rapport au titre
        arbre_complet = VGroup(*noeuds.values(), liens)
        arbre_complet.scale(0.8).shift(DOWN * 0.5)

        # --- 2. Animations ---
        # Affichage initial global
        self.play(FadeIn(titre), Create(arbre_complet))
        self.wait(1)

        # Zoom sur la racine + Changement de couleur + Texte
        txt_noeud = Text("Nœud (Racine)", font_size=18, color=c_highlight).next_to(noeuds["0_0"], UP * 0.4)
        self.play(
            self.camera.frame.animate.move_to(noeuds["0_0"]).set(width=3.5),
            noeuds["0_0"].animate.set_color(c_highlight),
            FadeIn(txt_noeud),
            run_time=2
        )
        self.wait(1)

        # Dézoom et focus sur les deux enfants directs de la racine
        pos_enfants_milieu = (noeuds["1_0"].get_center() + noeuds["1_1"].get_center()) / 2
        txt_enfants = Text("Enfants", font_size=22, color=c_enfant).move_to(pos_enfants_milieu + UP * 0.6)
        self.play(
            self.camera.frame.animate.move_to(pos_enfants_milieu + UP * 0.2).set(width=8.5),
            noeuds["1_0"].animate.set_color(c_enfant),
            noeuds["1_1"].animate.set_color(c_enfant),
            FadeIn(txt_enfants),
            run_time=2
        )
        self.wait(1)

        # Descente rapide tout en bas et fixation sur une feuille profonde
        txt_feuille = Text("Feuille (Aucun enfant)", font_size=16, color=c_feuille).next_to(noeuds["3_0"], DOWN * 0.4)
        self.play(
            self.camera.frame.animate.move_to(noeuds["3_0"]).set(width=3),
            noeuds["3_0"].animate.set_color(c_feuille),
            FadeIn(txt_feuille),
            run_time=2.5
        )
        self.wait(2)