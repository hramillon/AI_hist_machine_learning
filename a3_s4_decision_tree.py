from manim import *

class SceneDecisionTreeFinal(MovingCameraScene):
    def construct(self):
        # --- 1. Configuration des Styles ---
        c_noeud = WHITE
        c_texte = WHITE
        c_oui = GREEN
        c_non = RED
        c_user = GOLD
        c_rep = RED_E       # Rouge pour Républicain
        c_dem = BLUE_E      # Bleu pour Démocrate
        
        # --- 2. Définition des Positions (Arbre étendu à 3 niveaux) ---
        pos = {
            "R": UP * 2,                 # Racine
            "G": LEFT * 3.5 + UP * 0,    # Enfant Gauche (Non)
            "D": RIGHT * 3.5 + UP * 0,   # Enfant Droite (Oui)
            "GG": LEFT * 5.2 + DOWN * 2, # Feuilles côté Gauche
            "GD": LEFT * 1.8 + DOWN * 2,
            "DG": RIGHT * 1.8 + DOWN * 2,# Feuilles côté Droite
            "DD": RIGHT * 5.2 + DOWN * 2
        }

        # --- 3. Création des Nœuds et Textes ---
        titre = Text("Arbre de Décision", font_size=40).to_edge(UP)

        # Niveau 0 : Racine
        racine_box = Rectangle(width=4.5, height=1.0, color=c_noeud, fill_opacity=1, fill_color=BLACK).move_to(pos["R"])
        q_racine = Text("Like du contenu\npolitique de droite ?", font_size=15, color=c_texte).move_to(pos["R"])
        
        # Niveau 1 : Sous-questions
        gauche_box = Rectangle(width=3.5, height=1.0, color=c_noeud, fill_opacity=1, fill_color=BLACK).move_to(pos["G"])
        q_gauche = Text("Regarde des vidéos\nécologistes ?", font_size=14, color=c_texte).move_to(pos["G"])
        
        droite_box = Rectangle(width=3.5, height=1.0, color=c_noeud, fill_opacity=1, fill_color=BLACK).move_to(pos["D"])
        q_droite = Text("Plus de 15 min/jour\nsur ces vidéos ?", font_size=14, color=c_texte).move_to(pos["D"])

        # Niveau 2 : Feuilles (Ellipsoïdes / Elipses)
        f_gg = Ellipse(width=3.0, height=0.8, color=c_dem, fill_opacity=0.6, fill_color=BLACK).move_to(pos["GG"])
        t_gg = Text("Démocrate\nConfirmé", font_size=12, color=WHITE).move_to(pos["GG"])

        f_gd = Ellipse(width=3.0, height=0.8, color=WHITE, fill_opacity=0.4, fill_color=BLACK).move_to(pos["GD"])
        t_gd = Text("Indécis / Neutre", font_size=12, color=WHITE).move_to(pos["GD"])

        f_dg = Ellipse(width=3.0, height=0.8, color=WHITE, fill_opacity=0.4, fill_color=BLACK).move_to(pos["DG"])
        t_dg = Text("Républicain\nIndécis", font_size=12, color=WHITE).move_to(pos["DG"])

        f_dd = Ellipse(width=3.0, height=0.8, color=c_rep, fill_opacity=0.6, fill_color=BLACK).move_to(pos["DD"])
        t_dd = Text("Républicain\nConfirmé", font_size=12, color=WHITE).move_to(pos["DD"])

        # --- 4. Création des Liens (Arêtes) ---
        l_gauche = Line(racine_box.get_bottom(), gauche_box.get_top(), stroke_width=4)
        l_droite = Line(racine_box.get_bottom(), droite_box.get_top(), stroke_width=4)
        
        l_gg = Line(gauche_box.get_bottom(), f_gg.get_top(), stroke_width=3)
        l_gd = Line(gauche_box.get_bottom(), f_gd.get_top(), stroke_width=3)
        l_dg = Line(droite_box.get_bottom(), f_dg.get_top(), stroke_width=3)
        l_dd = Line(droite_box.get_bottom(), f_dd.get_top(), stroke_width=3)

        liens_secondaires = VGroup(l_gg, l_gd, l_dg, l_dd)
        feuilles = VGroup(f_gg, t_gg, f_gd, t_gd, f_dg, t_dg, f_dd, t_dd)

        # Étiquettes Oui / Non (Niveau 1)
        txt_non_r = Text("Non", font_size=16, color=c_non).next_to(l_gauche.get_center(), LEFT * 0.4 + UP * 0.2)
        txt_oui_r = Text("Oui", font_size=16, color=c_oui).next_to(l_droite.get_center(), RIGHT * 0.4 + UP * 0.2)

        # Étiquettes Oui / Non (Niveau 2, sous le nœud de droite)
        txt_non_d = Text("Non", font_size=14, color=c_non).next_to(l_dg.get_center(), LEFT * 0.3 + UP * 0.1)
        txt_oui_d = Text("Oui", font_size=14, color=c_oui).next_to(l_dd.get_center(), RIGHT * 0.3 + UP * 0.1)

        # Point Utilisateur
        user_dot = Dot(point=pos["R"] + UP * 1.2, radius=0.14, color=c_user)

        # Groupe global pour l'arbre et les textes pour le fade out final
        tout_le_visuel = VGroup(
            titre, racine_box, q_racine, gauche_box, q_gauche, droite_box, q_droite,
            l_gauche, l_droite, liens_secondaires, feuilles,
            txt_non_r, txt_oui_r, txt_non_d, txt_oui_d, user_dot
        )

        # --- 5. Déroulement de l'Animation ---
        
        # Initialisation de la vue globale
        self.camera.frame.set(width=15).move_to(DOWN * 0.5)
        
        # Affichage de l'arbre entier
        self.play(FadeIn(titre))
        self.play(
            Create(racine_box), Write(q_racine),
            Create(l_gauche), Create(l_droite), Write(txt_non_r), Write(txt_oui_r),
            Create(gauche_box), Write(q_gauche),
            Create(droite_box), Write(q_droite),
            Create(liens_secondaires), Create(feuilles),
            Write(txt_non_d), Write(txt_oui_d),
            run_time=2
        )
        self.wait(0.5)

        # Positionnement de l'utilisateur sur la racine
        self.play(FadeIn(user_dot))
        self.play(user_dot.animate.move_to(racine_box.get_top()), run_time=0.8)
        self.wait(0.5)

        # --- PREMIER CHOIX (Racine) ---
        self.play(self.camera.frame.animate.move_to(pos["R"] + DOWN * 0.6).set(width=7.5), run_time=1.5)

        # Allumage gauche (Non) puis retour normal
        self.play(l_gauche.animate.set_color(c_non).set_stroke(width=7), run_time=0.6)
        self.wait(0.3)
        self.play(l_gauche.animate.set_color(WHITE).set_stroke(width=4), run_time=0.4)
        
        # Allumage droite (Oui)
        self.play(l_droite.animate.set_color(c_oui).set_stroke(width=7), run_time=0.6)
        self.wait(0.3)

        # Descente vers le nœud de droite
        self.play(
            user_dot.animate.move_to(droite_box.get_top()),
            self.camera.frame.animate.move_to(pos["D"] + DOWN * 0.5).set(width=6.5),
            run_time=1.8
        )
        self.wait(1)

        # --- DEUXIÈME CHOIX (Nœud 15 min) ---
        # Allumage gauche (Non) puis retour normal
        self.play(l_dg.animate.set_color(c_non).set_stroke(width=6), run_time=0.6)
        self.wait(0.3)
        self.play(l_dg.animate.set_color(WHITE).set_stroke(width=3), run_time=0.4)

        # Allumage droite (Oui) puis retour normal
        self.play(l_dd.animate.set_color(c_oui).set_stroke(width=6), run_time=0.6)
        self.wait(0.3)
        self.play(l_dd.animate.set_color(WHITE).set_stroke(width=3), run_time=0.4)
        
        # Validation du choix gauche (Non)
        self.play(l_dg.animate.set_color(c_non).set_stroke(width=6), run_time=0.4)

        # Descente vers l'ellipsoïde "Républicain Indécis"
        self.play(
            user_dot.animate.move_to(f_dg.get_top()),
            self.camera.frame.animate.move_to(pos["DG"]).set(width=4.5),
            run_time=1.8
        )
        self.wait(1)

        # --- TRANSITION PLAN NOIR TOTAL ---
        self.play(FadeOut(tout_le_visuel), run_time=1.5)
        self.wait(2)